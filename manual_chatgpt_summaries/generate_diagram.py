"""
Generalized, multi-block pipeline (no longer hardcoded to C_GROUP + C_DRV_1D):

1. Discover every block by scanning io_jsons/*.json - each file holds the
   DEFAULT, standard input/output ports for one Siemens CEMAT block
   (ground truth for the generic case, not something an LLM has to
   guess). This default selection is only a subset of every port the
   real block actually supports - the rest are documented in the
   block's summary markdown but omitted from the JSON because most
   projects don't need them.
1a. If a summary_markdowns/*.md file has no matching io_jsons/*.json at
    all, one is bootstrapped automatically: Grok reads that summary and
    synthesizes a standard default ports JSON for it (grounded so it can
    only use ports the summary documents), saved to io_jsons/ so it
    behaves like any other pre-existing default file from then on.
1b. PORT_SELECTION_MODE decides whether to stop at that default subset
    or go further:
      - "default": use the io_jsons ports exactly as-is (original
        behaviour, no extra Grok calls).
      - "intelligence": also read the block's summary markdown (which
        documents the FULL port list, not just the default selection)
        and ask Grok whether this project's connection rules call for
        adding ports beyond the default set, or dropping default ports
        that don't apply - producing an adjusted port list that then
        feeds into every step below exactly like the default one would.
2. Pair each block with its connection-rule summary: the file in
   summary_markdowns/ that has the SAME filename stem (e.g.
   io_jsons/C_GROUP_009.json <-> summary_markdowns/C_GROUP_009.md). Add a
   new block by dropping a matching pair of files into those two folders.
3. Only ask Grok about pairs of blocks whose rule summaries actually
   mention each other (a cheap text pre-filter) - with 10+ blocks this
   keeps the number of API calls close to the number of REAL
   relationships instead of blowing up as every-block-vs-every-block.
4. For each relevant pair, ask Grok to infer connections using both
   blocks' (possibly intelligence-adjusted) ports + their rules,
   validate the result against those ports (drop anything hallucinated),
   and combine everything into one connections list.
5. Deterministically draw every block in a row (pins straight from the
   resolved port lists) and wire up every inferred connection, each with
   its own color, then save block_diagram.png.

Step 5 is plain, fixed matplotlib code (not LLM-generated) - an earlier
attempt at having the model invent both the port layout AND the drawing
code produced overlapping, unreadable output once blocks had more than a
handful of pins. Grok's job is limited to the part it's actually good at:
reading the rules and figuring out which ports connect (and, in
"intelligence" mode, which ports should even be on the diagram).
"""

import glob
import itertools
import json
import os
import re
import time

from dotenv import load_dotenv
from openai import OpenAI, RateLimitError
import matplotlib.pyplot as plt
import matplotlib.patches as patches

load_dotenv()  # loads GROK_API_KEY from a .env file in this folder, if present

MODEL_NAME = "llama-3.3-70b-versatile"  # change here if the model name is wrong

IO_JSONS_DIR = "io_jsons"
SUMMARY_MD_DIR = "summary_markdowns"
CONNECTIONS_PATH = "grok_connections.json"
IMAGE_PATH = "block_diagram.png"

# Pacing between Grok calls so many small pairwise requests don't blow
# past Groq's per-minute token cap. Bump this up if you add blocks with
# much larger summaries and start seeing rate-limit retries.
SECONDS_BETWEEN_CALLS = 20

# Port selection mode - change this one flag to switch behaviour for
# every discovered block:
#   "default"      - use exactly the ports listed in each io_jsons/*.json
#                    file. No extra Grok calls, identical to the
#                    original behaviour.
#   "intelligence" - additionally consult each block's summary markdown
#                    (which documents every port the real block
#                    supports, not just the default selection) and ask
#                    Grok to add or remove ports so the default set
#                    better matches what this project's own connection
#                    rules call for.
PORT_SELECTION_MODE = "default" 

client = OpenAI(
    api_key=os.environ["GROK_API_KEY"],
    base_url="https://api.groq.com/openai/v1",
)


# Beyond this many seconds, a rate-limit error is treated as a big quota
# (e.g. Groq's daily "tokens per day" cap) rather than the usual
# per-minute one - blindly sleeping through a 20+ minute wait would just
# hang the script, so we fail fast with a clear message instead.
RATE_LIMIT_MAX_AUTO_WAIT = 120


def _parse_retry_seconds(message: str):
    """Pull the "Please try again in Xm Ys" / "in Xs" suggestion out of a
    Groq rate-limit error message, so we wait exactly as long as Groq
    says instead of guessing with a fixed backoff."""
    match = re.search(r"try again in (?:(\d+)m)?(\d+(?:\.\d+)?)s", message)
    if not match:
        return None
    minutes = float(match.group(1)) if match.group(1) else 0.0
    return minutes * 60 + float(match.group(2))


def call_model_json(system_prompt: str, user_prompt: str) -> dict:
    """Call Groq once and return the parsed JSON response, retrying on
    rate limits that clear quickly (e.g. per-minute token caps). Rate
    limits that need a long wait (e.g. a daily token cap) fail fast with
    a clear message instead of blocking the script for tens of minutes."""
    for attempt in range(3):
        try:
            response = client.chat.completions.create(
                model=MODEL_NAME,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=0,
                response_format={"type": "json_object"},
            )
            return json.loads(response.choices[0].message.content)
        except RateLimitError as e:
            suggested_wait = _parse_retry_seconds(str(e))
            if suggested_wait is not None and suggested_wait > RATE_LIMIT_MAX_AUTO_WAIT:
                raise RuntimeError(
                    f"Groq's rate limit says to wait {suggested_wait / 60:.1f} minute(s) "
                    "before retrying - that's a large/daily quota limit, not a quick "
                    "per-minute one, so this run is stopping instead of blocking. Wait "
                    "for that reset and rerun the script, process fewer blocks per day, "
                    "or upgrade the Groq tier."
                ) from e
            wait = (suggested_wait + 2) if suggested_wait is not None else 30 * (attempt + 1)
            print(f"  Rate limited, waiting {wait:.0f}s and retrying (attempt {attempt + 1}/3)...")
            time.sleep(wait)
    raise RuntimeError("Gave up after repeated rate limit errors.")


# ---------------------------------------------------------------------
# Discovery: load every block's JSON + its matching rules summary
# ---------------------------------------------------------------------

def normalize(s: str) -> str:
    return re.sub(r"[^a-z0-9]", "", s.lower())


def extract_section(markdown: str, header: str) -> str:
    """Return the body text of one '## <header>' section of a summary
    markdown file, up to the next '## ' heading (or end of file).
    Empty string if that header isn't present."""
    match = re.search(rf"##\s+{re.escape(header)}\s*\n(.*?)(?=\n##\s|\Z)", markdown, re.DOTALL)
    return match.group(1) if match else ""


def extract_backticked_names(text: str) -> set:
    """Every `PortName`-style identifier mentioned in a chunk of summary
    text - used as the "this name is actually documented somewhere, it's
    not a hallucination" allow-list for both intelligence mode and the
    bootstrap-a-missing-json step below."""
    return set(re.findall(r"`([A-Za-z_][A-Za-z0-9_]*)`", text))


def bootstrap_default_json(md_path: str) -> dict:
    """A summary markdown was found with no matching io_jsons/*.json file
    at all - there is no default port selection for this block yet. Ask
    Grok to read the summary and synthesize one: the small, standard
    subset of ports a normal/simple integration would wire up (the same
    kind of curated default the other io_jsons files hold), grounded so
    it can only use ports the summary actually documents. The result is
    saved to io_jsons/ so every later run treats it like any other
    pre-existing default file (this only runs once per new block)."""
    stem = os.path.splitext(os.path.basename(md_path))[0]
    json_path = os.path.join(IO_JSONS_DIR, stem + ".json")

    with open(md_path, "r", encoding="utf-8") as f:
        rules = f.read()

    print(f"No io_jsons file found for summary '{stem}' - asking Grok to bootstrap a default "
          f"ports JSON for it from the summary (one-time; will be saved to {json_path}).")

    name_match = re.search(r"#\s+(\S+)\s+Summary", rules)
    fallback_name = name_match.group(1) if name_match else stem

    # Ground against every backticked name in the WHOLE document, not just
    # specific "## Inputs"/"## Outputs" sections - different summary files
    # (hand-written by different ChatGPT sessions) don't always use the
    # exact same section headings, and if none of them match, section-only
    # extraction returns an empty allow-list and silently drops every
    # single proposed port. Matching against the full text is more robust
    # and still blocks outright invented names.
    allowed_names = extract_backticked_names(rules)

    system_prompt = (
        "You are a careful industrial automation engineering assistant. "
        "Output only valid JSON."
    )

    user_prompt = f"""
There is no curated default input/output ports JSON for this Siemens
CEMAT block yet - only its connection-rule summary markdown exists,
shown in full below. That summary typically documents 40-50+ ports
total (every port the real block supports), but a normal default
selection is NOT that whole list - it is a short, logical, general-
purpose subset, typically only around 8-15 inputs and 8-15 outputs,
covering the ports a simple, everyday integration would actually wire
up. Read the summary and produce ONLY that short default subset.

Guidance for picking the default subset:
- Include the ports the "Purpose" and "Key Connection Notes" sections
  describe as core to starting, stopping, interlocking, and reporting
  run/fault/warning status for this block, plus any group/object link
  ports needed to attach it to other blocks.
- Exclude ports the summary itself calls out as internal-only, test-only,
  OS/diagnostic/visualization-only, or "not intended for application use"
  (see its "Uncertain / Ambiguous Points" section if present).
- Exclude rarely-used configuration/feature/status bit fields, OS/HMI
  interfaces, and low-level status/diagnostic buffers unless the Key
  Connection Notes describe them as part of normal wiring.
- Do NOT just copy every port from the summary's "Inputs"/"Outputs"
  sections into your answer - that defeats the purpose. Be selective:
  pick the handful that a normal engineer would actually connect.

STRICT RULES:
- Every port name you output MUST literally appear (the summary wraps
  port names in backticks like `ExamplePort`, but the JSON "name" value
  you output must be the bare name with NO backticks around it, e.g.
  "ExamplePort" not "`ExamplePort`") somewhere in the summary text below.
  Never invent, rename, or guess a name.
- Output a real "block_type" and one-sentence "description" based on the
  summary's "Purpose" section.

Output only valid JSON in exactly this shape:
{{
  "block_name": "...",
  "block_type": "...",
  "description": "...",
  "inputs": [{{"name": "...", "datatype": "...", "description": "..."}}],
  "outputs": [{{"name": "...", "datatype": "...", "description": "..."}}]
}}

=== Summary markdown ({stem}) ===
{rules}
""".strip()

    result = call_model_json(system_prompt, user_prompt)

    def sanitize(ports: list) -> list:
        kept = []
        for p in ports:
            # Strip stray backticks/whitespace the model sometimes copies
            # in from the summary's `Markdown` styling - without this, a
            # single formatting slip makes every name fail the allow-list
            # check and silently empties the whole port list.
            name = (p.get("name") or "").strip().strip("`").strip()
            if name in allowed_names:
                kept.append({
                    "name": name,
                    "datatype": p.get("datatype", "?"),
                    "description": p.get("description", ""),
                })
            else:
                print(f"  Dropping bootstrapped port '{name}' for {stem} - not documented "
                      f"anywhere in its summary.")
        return kept

    block = {
        "block_name": result.get("block_name") or fallback_name,
        "block_type": result.get("block_type", "Unknown"),
        "description": result.get("description", ""),
        "inputs": sanitize(result.get("inputs", [])),
        "outputs": sanitize(result.get("outputs", [])),
    }

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(block, f, indent=2, ensure_ascii=False)
    print(f"  Saved bootstrapped default ports JSON to {json_path}")

    return block


def discover_blocks() -> dict:
    """Load every *.json in io_jsons/, and pair each with the summary .md
    in summary_markdowns/ that best matches its filename: prefer an exact
    same-stem match (C_GROUP_009.json <-> C_GROUP_009.md); fall back to
    the block's "block_name" field appearing in the summary's filename.

    Any summary .md left over with no matching json at all gets a
    default ports JSON bootstrapped for it (see bootstrap_default_json)
    so it can be discovered and connected just like every other block."""
    md_paths = glob.glob(os.path.join(SUMMARY_MD_DIR, "*.md"))
    blocks = {}
    claimed_md_paths = set()

    for json_path in sorted(glob.glob(os.path.join(IO_JSONS_DIR, "*.json"))):
        with open(json_path, "r", encoding="utf-8") as f:
            block = json.load(f)
        name = block["block_name"]
        stem = os.path.splitext(os.path.basename(json_path))[0]

        match = next((p for p in md_paths if os.path.splitext(os.path.basename(p))[0] == stem), None)
        if match is None:
            match = next((p for p in md_paths if normalize(name) in normalize(os.path.basename(p))), None)

        rules = ""
        if match:
            claimed_md_paths.add(match)
            with open(match, "r", encoding="utf-8") as f:
                rules = f.read()
        else:
            print(f"Warning: no summary .md found for block '{name}' - it will only be drawn, "
                  f"not connected (add a same-named file to {SUMMARY_MD_DIR}/).")

        if name in blocks:
            print(f"Warning: duplicate block_name '{name}' (from {json_path}) - keeping the first one found.")
            continue

        blocks[name] = {"block": block, "rules": rules, "json_path": json_path, "summary_path": match}

    for md_path in sorted(md_paths):
        if md_path in claimed_md_paths:
            continue
        block = bootstrap_default_json(md_path)
        name = block["block_name"]
        if name in blocks:
            print(f"Warning: bootstrapped block_name '{name}' (from {md_path}) already discovered - skipping.")
            continue
        json_path = os.path.join(IO_JSONS_DIR, os.path.splitext(os.path.basename(md_path))[0] + ".json")
        with open(md_path, "r", encoding="utf-8") as f:
            rules = f.read()
        blocks[name] = {"block": block, "rules": rules, "json_path": json_path, "summary_path": md_path}

    print(f"Discovered {len(blocks)} block(s): {', '.join(blocks)}")
    return blocks


# ---------------------------------------------------------------------
# Port selection mode: "default" keeps the io_jsons ports untouched;
# "intelligence" asks Grok to widen/narrow that default set using each
# block's own summary markdown, which documents the full port list.
# ---------------------------------------------------------------------

def refine_ports_intelligently(block: dict, rules: str) -> dict:
    """"intelligence" mode only: the io_jsons file is just Siemens'
    DEFAULT port selection, not the full set the real block supports.
    The summary markdown documents the full set. Ask Grok, using that
    summary's own Purpose/Key Connection Notes as the specification of
    what a real integration needs, whether any ports should be added on
    top of the default set or removed from it. Returns a new block dict
    with adjusted "inputs"/"outputs"; falls back to the default block
    untouched if there is no summary to reason from."""
    if not rules.strip():
        return block

    allowed_names = (
        extract_backticked_names(extract_section(rules, "Inputs"))
        | extract_backticked_names(extract_section(rules, "Outputs"))
        | extract_backticked_names(extract_section(rules, "Group/Object Links"))
    )

    system_prompt = (
        "You are a careful industrial automation engineering assistant. "
        "Output only valid JSON."
    )

    user_prompt = f"""
The JSON below is the DEFAULT selection of input/output ports for the
Siemens CEMAT block {block['block_name']} - the generic subset most
projects use. It is not the full list of ports this block actually
supports; it is a starting point.

The markdown after it is that block's connection-rule summary, which
documents the FULL port list this block supports (see its own "Inputs"
and "Outputs" sections) as well as its "Purpose" and "Key Connection
Notes" - treat those two sections as the specification of what a real
integration of this block actually needs.

Your task: decide whether the DEFAULT port list should be adjusted for
this project:
- ADD a port that is documented in the summary's "Inputs"/"Outputs"/
  "Group/Object Links" sections but missing from the default list, ONLY
  if the "Purpose" or "Key Connection Notes" text gives a concrete
  reason a real integration would need to wire it (e.g. it names that
  port directly as part of how this block connects to others).
- REMOVE a default port only if the summary text makes clear it is not
  applicable to a normal/simple integration (this should be rare).
- Otherwise, leave the port exactly as in the default list.

STRICT RULES:
- Every port name you output MUST literally appear (the summary wraps
  port names in backticks like `ExamplePort`, but the JSON "name" value
  you output must be the bare name with NO backticks around it, e.g.
  "ExamplePort" not "`ExamplePort`") in the summary text below. Never
  invent, rename, or guess a name.
- Do not add a port "just because it's documented" - only add it if the
  Purpose/Key Connection Notes text gives a real, concrete reason.
- When in doubt, prefer the default list unchanged - being conservative
  here is better than guessing.
- Keep every port's "datatype" and a short "description" (reuse the
  summary's wording where possible).

Output only valid JSON in exactly this shape (the full, final port
lists - not just the changes):
{{
  "inputs": [{{"name": "...", "datatype": "...", "description": "..."}}],
  "outputs": [{{"name": "...", "datatype": "...", "description": "..."}}]
}}

=== {block['block_name']} DEFAULT ports (JSON) ===
{json.dumps({"inputs": block["inputs"], "outputs": block["outputs"]}, indent=2)}

=== {block['block_name']} connection rules (full summary) ===
{rules}
""".strip()

    result = call_model_json(system_prompt, user_prompt)

    def sanitize(proposed: list, default_ports: list) -> list:
        default_names = {p["name"] for p in default_ports}
        kept = []
        for p in proposed:
            name = (p.get("name") or "").strip().strip("`").strip()
            if name in default_names or name in allowed_names:
                kept.append({
                    "name": name,
                    "datatype": p.get("datatype", "?"),
                    "description": p.get("description", ""),
                })
            else:
                print(f"  Intelligence mode: dropping proposed port '{name}' for "
                      f"{block['block_name']} - not documented anywhere in its summary.")
        return kept

    new_inputs = sanitize(result.get("inputs", block["inputs"]), block["inputs"])
    new_outputs = sanitize(result.get("outputs", block["outputs"]), block["outputs"])

    added_in = {p["name"] for p in new_inputs} - {p["name"] for p in block["inputs"]}
    removed_in = {p["name"] for p in block["inputs"]} - {p["name"] for p in new_inputs}
    added_out = {p["name"] for p in new_outputs} - {p["name"] for p in block["outputs"]}
    removed_out = {p["name"] for p in block["outputs"]} - {p["name"] for p in new_outputs}
    if added_in or removed_in or added_out or removed_out:
        print(f"  Intelligence mode adjusted {block['block_name']}: "
              f"+in{sorted(added_in)} -in{sorted(removed_in)} "
              f"+out{sorted(added_out)} -out{sorted(removed_out)}")
    else:
        print(f"  Intelligence mode: default ports already sufficient for {block['block_name']}.")

    adjusted = dict(block)
    adjusted["inputs"] = new_inputs or block["inputs"]
    adjusted["outputs"] = new_outputs or block["outputs"]
    return adjusted


def apply_port_selection_mode(blocks: dict) -> None:
    """Mutates each discovered block's port list in place according to
    PORT_SELECTION_MODE. No-op (and no extra Grok calls) in "default"
    mode, which keeps the original, pre-existing behaviour."""
    if PORT_SELECTION_MODE != "intelligence":
        return

    names = list(blocks)
    for i, name in enumerate(names, start=1):
        info = blocks[name]
        if not info["rules"].strip():
            continue
        print(f"[{i}/{len(names)}] Intelligence mode: reviewing default ports for {name}...")
        info["block"] = refine_ports_intelligently(info["block"], info["rules"])
        if i < len(names):
            time.sleep(SECONDS_BETWEEN_CALLS)


# ---------------------------------------------------------------------
# Candidate pairs: only ask Grok about pairs whose rules actually
# mention each other, so N blocks doesn't mean N^2 API calls in practice
# ---------------------------------------------------------------------

def candidate_pairs(blocks: dict) -> list:
    names = list(blocks)
    pairs = []
    for a, b in itertools.combinations(names, 2):
        a_mentions_b = normalize(b) in normalize(blocks[a]["rules"])
        b_mentions_a = normalize(a) in normalize(blocks[b]["rules"])
        if a_mentions_b or b_mentions_a:
            pairs.append((a, b))
    return pairs


# ---------------------------------------------------------------------
# Connection inference (same approach as the original 2-block version,
# now parameterized so it works for any pair of discovered blocks)
# ---------------------------------------------------------------------

def infer_connections_for_pair(block_a: dict, rules_a: str, block_b: dict, rules_b: str) -> dict:
    name_a, name_b = block_a["block_name"], block_b["block_name"]

    system_prompt = (
        "You are a careful industrial automation engineering assistant. "
        "Output only valid JSON."
    )

    user_prompt = f"""
Below are the REAL, standard input/output ports for two Siemens CEMAT
blocks, {name_a} and {name_b}, as JSON, followed by their connection-rule
summaries (one may be empty if no summary file was found for that block).

Your task: infer the connections between {name_a} and {name_b} - in
EITHER direction (an output of either block can feed an input of the
other).

STRICT RULES:
- Only use port names that literally appear in the JSON port lists
  below. Do not invent, rename, or guess a port name.
- Every connection's "from_port" must be a port listed in from_block's
  "outputs", and "to_port" must be a port listed in to_block's "inputs".
- Only include a connection in "connections" if the rule summaries
  clearly support it. If you think a connection likely exists but the
  text doesn't clearly support both ends, put it under
  "uncertain_connections" instead, with a short note on what's missing.
- Do not invent a connection just to look complete.
- Go through EVERY bullet point in the "Key Connection Notes" section of
  BOTH summaries one by one and check it against the port lists - do not
  stop after finding the first few obvious matches. Missing a documented
  rule is as bad as inventing a fake one.

GROUP/ROUTE-LINK CONNECTIONS ARE MANDATORY, NOT UNCERTAIN:
- A "*_LINK"-style output connecting to the other block's primary
  "*_LINK1"/"*_LINK" input is how one block is attached to another in
  CEMAT (e.g. a group's link output to a drive's primary link input).
  For a simple, single-instance setup this is always wired, not
  optional. If a summary says something like "the main group should be
  connected to GR_LINK1" or "connect this output to the GR_LINK
  interface", treat that as confident, documented support and put the
  connection in "connections" with high confidence - do NOT push it into
  "uncertain_connections" just because the manual also mentions other
  configurations (multiple groups/routes, multiplexers) that don't apply
  to this simple case.

WATCH FOR INVERTED / SPLIT SIGNALS:
- Sometimes one output feeds two different input ports on the other
  block - one directly, and one logically inverted (NOT'd). Look for
  language like "negated", "inverted", or a description of one port as
  the logical opposite of another (e.g. a running signal commonly feeds
  both a "running" feedback directly AND a "stopped"/"off" feedback as
  its negation). When you find this pattern, output BOTH connections
  separately, each with its own "inverted" field:
  - the direct connection: "inverted": false
  - the negated connection: "inverted": true
  The same "from_port" CAN appear in more than one connection (fan-out)
  when the manual supports it.

Output only valid JSON in exactly this shape:
{{
  "connections": [
    {{
      "from_block": "{name_a}",
      "from_port": "...",
      "to_block": "{name_b}",
      "to_port": "...",
      "reason": "short reason citing the rule",
      "confidence": 0.0,
      "inverted": false
    }}
  ],
  "uncertain_connections": []
}}

=== {name_a} ports (JSON) ===
{json.dumps(block_a, indent=2)}

=== {name_b} ports (JSON) ===
{json.dumps(block_b, indent=2)}

=== {name_a} connection rules ===
{rules_a or "(no summary found for this block)"}

=== {name_b} connection rules ===
{rules_b or "(no summary found for this block)"}
""".strip()

    return call_model_json(system_prompt, user_prompt)


def validate_connections(connections: list, blocks_by_name: dict) -> list:
    """Drop any connection that references a block/port not actually
    present in the JSON files (belt-and-suspenders check against
    hallucination)."""

    def has_output(block_name, port_name):
        if block_name not in blocks_by_name:
            return False
        return port_name in {p["name"] for p in blocks_by_name[block_name]["outputs"]}

    def has_input(block_name, port_name):
        if block_name not in blocks_by_name:
            return False
        return port_name in {p["name"] for p in blocks_by_name[block_name]["inputs"]}

    valid = []
    for c in connections:
        from_block, from_port = c.get("from_block"), c.get("from_port")
        to_block, to_port = c.get("to_block"), c.get("to_port")
        if not has_output(from_block, from_port):
            print(f"  Dropping connection - '{from_port}' is not an output of {from_block}: {c}")
            continue
        if not has_input(to_block, to_port):
            print(f"  Dropping connection - '{to_port}' is not an input of {to_block}: {c}")
            continue
        valid.append(c)
    return valid


# ---------------------------------------------------------------------
# Deterministic drawing (fixed layout code, not LLM-generated)
# ---------------------------------------------------------------------

ROW_HEIGHT = 1.0
TITLE_HEIGHT = 3
BOX_WIDTH = 6.0
GAP = 14.0  # horizontal gap between adjacent boxes, leaves room for labels + wires
VERTICAL_GAP = 3.0  # vertical space between stacked component boxes in hub-and-spoke mode
STUB = 0.6  # length of the little tick mark sticking out of each pin


def is_group_block(block: dict) -> bool:
    return "group" in block.get("block_type", "").strip().lower()


def block_height(block: dict) -> float:
    n_rows = max(len(block["inputs"]), len(block["outputs"]), 1)
    return (n_rows + 1) * ROW_HEIGHT + TITLE_HEIGHT


def box_layout(block: dict, box_left: float, box_bottom: float = 0.0) -> dict:
    """Compute the geometry for one block's box: its rectangle plus the
    y-position of every input and output pin."""
    box_top = box_bottom + block_height(block)

    def pin_ys(n):
        top_of_pins = box_top - TITLE_HEIGHT - ROW_HEIGHT * 0.5
        return [top_of_pins - i * ROW_HEIGHT for i in range(n)]

    return {
        "left": box_left,
        "right": box_left + BOX_WIDTH,
        "top": box_top,
        "bottom": box_bottom,
        "input_ys": pin_ys(len(block["inputs"])),
        "output_ys": pin_ys(len(block["outputs"])),
    }


def layout_all_blocks(blocks_in_order: list) -> dict:
    """Place every block left-to-right in a single row (in the given
    order) and return {block_name: layout}."""
    layouts = {}
    x = 0.0
    for block in blocks_in_order:
        layouts[block["block_name"]] = box_layout(block, box_left=x)
        x += BOX_WIDTH + GAP
    return layouts


def layout_hub_and_spokes(group_block: dict, component_blocks: list) -> dict:
    """Group module on the left; every one of its components stacked
    vertically, one after another, in a single column on the right -
    all top-aligned with the group so the whole thing reads as one
    hub-and-spoke unit instead of sprawling into a wide row."""
    layouts = {}
    stack_x = BOX_WIDTH + GAP

    heights = [block_height(b) for b in component_blocks]
    total_stack_height = sum(heights) + VERTICAL_GAP * max(len(component_blocks) - 1, 0)
    top = max(block_height(group_block), total_stack_height)

    layouts[group_block["block_name"]] = box_layout(
        group_block, box_left=0.0, box_bottom=top - block_height(group_block)
    )

    y = top
    for block, height in zip(component_blocks, heights):
        bottom = y - height
        layouts[block["block_name"]] = box_layout(block, box_left=stack_x, box_bottom=bottom)
        y = bottom - VERTICAL_GAP

    return layouts


def draw_block(ax, block: dict, layout: dict, instance_no: int) -> None:
    left, right, top, bottom = layout["left"], layout["right"], layout["top"], layout["bottom"]

    ax.add_patch(patches.Rectangle((left, bottom), BOX_WIDTH, top - bottom,
                                    edgecolor="black", facecolor="white", linewidth=1.5, zorder=2))
    ax.add_patch(patches.Rectangle((left, top - TITLE_HEIGHT), BOX_WIDTH, TITLE_HEIGHT,
                                    edgecolor="black", facecolor="white", linewidth=1.5, zorder=2))
    tag_w, tag_h = BOX_WIDTH * 0.42, TITLE_HEIGHT * 0.45
    ax.add_patch(patches.Rectangle((right - tag_w - 0.15, top - tag_h - 0.15), tag_w, tag_h,
                                    edgecolor="black", facecolor="#bfe3e3", linewidth=1, zorder=3))

    block_type = block["block_type"]
    if len(block_type) > 14:
        block_type = block_type[:13] + "…"

    ax.text(left + 0.15, top - 0.5, str(instance_no), fontsize=7, va="top", ha="left", zorder=4)
    ax.text(left + 0.15, top - 1.3, block["block_name"], fontsize=8, fontweight="bold", va="top", ha="left", zorder=4)
    ax.text(left + 0.15, top - 2.25, block_type, fontsize=6, va="top", ha="left", zorder=4)

    for y, port in zip(layout["input_ys"], block["inputs"]):
        ax.plot([left - STUB, left], [y, y], color="black", linewidth=1, zorder=1)
        ax.text(left - STUB - 0.15, y, port["name"], fontsize=7, family="monospace",
                va="center", ha="right", zorder=4)

    for y, port in zip(layout["output_ys"], block["outputs"]):
        ax.plot([right, right + STUB], [y, y], color="black", linewidth=1, zorder=1)
        ax.text(right + STUB + 0.15, y, port["name"], fontsize=7, family="monospace",
                va="center", ha="left", zorder=4)


def pin_y(layout: dict, block: dict, port_name: str, side: str) -> float:
    names = [p["name"] for p in block[side]]
    idx = names.index(port_name)
    return layout["input_ys" if side == "inputs" else "output_ys"][idx]


def connection_colors(n: int) -> list:
    """Return n visually distinct colors, one per connection, so an
    engineer can tell adjacent wires apart even when they run close
    together. Cycles through a couple of qualitative palettes if there
    are more connections than one palette provides."""
    palette = list(plt.get_cmap("tab20").colors) + list(plt.get_cmap("tab20b").colors)
    return [palette[i % len(palette)] for i in range(n)]


def draw_connections(ax, connections: list, blocks_by_name: dict, layouts: dict, is_forward) -> None:
    """Route every connection. "Forward" connections (as decided by the
    is_forward callback) get a clean elbow straight through the open gap
    between the two boxes, since both pins face that gap - each forward
    wire gets its own vertical lane so several of them sharing a gap
    don't visually coincide. Everything else is routed through a shared
    "highway" lane below the whole drawing - every such wire gets its
    own lane so they never overlap - since those pins face away from
    each other and a straight line would have to cut through boxes in
    between."""
    lowest_bottom = min(l["bottom"] for l in layouts.values())
    wrap_offset = 1.5
    wrap_count = 0
    forward_lane = 0
    n_forward = sum(1 for c in connections if is_forward(c))
    colors = connection_colors(len(connections))

    for c, color in zip(connections, colors):
        from_name, from_port = c["from_block"], c["from_port"]
        to_name, to_port = c["to_block"], c["to_port"]
        from_layout, to_layout = layouts[from_name], layouts[to_name]
        y_from = pin_y(from_layout, blocks_by_name[from_name], from_port, "outputs")
        y_to = pin_y(to_layout, blocks_by_name[to_name], to_port, "inputs")

        if is_forward(c):
            x1 = from_layout["right"] + STUB
            x2 = to_layout["left"] - STUB
            forward_lane += 1
            x_mid = x1 + (x2 - x1) * (forward_lane / (n_forward + 1))
            xs = [x1, x_mid, x_mid, x2]
            ys = [y_from, y_from, y_to, y_to]
        else:
            x1 = from_layout["right"] + STUB
            x2 = to_layout["left"] - STUB
            wrap_y = lowest_bottom - (2 + wrap_count * wrap_offset)
            wrap_count += 1
            xs = [x1, x1, x2, x2]
            ys = [y_from, wrap_y, wrap_y, y_to]

        ax.plot(xs, ys, color=color, linewidth=1.4, zorder=1)
        ax.plot(xs[0], ys[0], marker="s", markersize=4, color=color, zorder=5)

        if c.get("inverted"):
            # small open circle = logical NOT, drawn where the wire meets the destination pin
            ax.add_patch(patches.Circle((xs[-1], ys[-1]), 0.18, edgecolor=color,
                                         facecolor="white", linewidth=1.4, zorder=6))
        else:
            ax.plot(xs[-1], ys[-1], marker="s", markersize=4, color=color, zorder=5)


def draw_diagram(blocks_in_order: list, connections: list) -> None:
    blocks_by_name = {b["block_name"]: b for b in blocks_in_order}
    group_blocks = [b for b in blocks_in_order if is_group_block(b)]

    if len(group_blocks) == 1 and len(blocks_in_order) > 1:
        # Hub-and-spoke: the group module on the left, every other
        # discovered block ("its components") stacked vertically in a
        # column on the right, all wired back to the single group.
        group_block = group_blocks[0]
        component_blocks = [b for b in blocks_in_order if b is not group_block]
        layouts = layout_hub_and_spokes(group_block, component_blocks)
        group_name = group_block["block_name"]
        is_forward = lambda c: c["from_block"] == group_name  # noqa: E731
        ordered_for_numbering = [group_block] + component_blocks
    else:
        # Fallback: no single group detected (zero, or more than one) -
        # lay every block out left-to-right in a row instead.
        layouts = layout_all_blocks(blocks_in_order)
        order = [b["block_name"] for b in blocks_in_order]
        index_of = {name: i for i, name in enumerate(order)}
        is_forward = lambda c: index_of[c["to_block"]] == index_of[c["from_block"]] + 1  # noqa: E731
        ordered_for_numbering = blocks_in_order

    n_highway = sum(1 for c in connections if not is_forward(c))
    overall_height = max(l["top"] for l in layouts.values())
    lowest_bottom = min(l["bottom"] for l in layouts.values())
    bottom_margin = 2 + n_highway * 1.5 + 1
    overall_width = max(l["right"] for l in layouts.values()) + 4

    fig_height_in = min(max((overall_height - lowest_bottom) * 0.22, 6), 60)
    fig_width_in = min(max(overall_width * 0.22, 12), 60)

    fig, ax = plt.subplots(figsize=(fig_width_in, fig_height_in))

    for i, block in enumerate(ordered_for_numbering, start=1):
        draw_block(ax, block, layouts[block["block_name"]], instance_no=i)

    draw_connections(ax, connections, blocks_by_name, layouts, is_forward)

    ax.set_xlim(-4, overall_width)
    ax.set_ylim(lowest_bottom - bottom_margin, overall_height + 1)
    ax.set_aspect("auto")
    ax.axis("off")

    plt.savefig(IMAGE_PATH, dpi=150, bbox_inches="tight")
    print(f"Saved diagram to {IMAGE_PATH}")


def main() -> None:
    blocks = discover_blocks()
    apply_port_selection_mode(blocks)
    pairs = candidate_pairs(blocks)
    print(f"Found {len(pairs)} candidate pair(s) whose rules reference each other: {pairs}")

    all_connections, all_uncertain = [], []
    for i, (name_a, name_b) in enumerate(pairs, start=1):
        info_a, info_b = blocks[name_a], blocks[name_b]
        print(f"[{i}/{len(pairs)}] Asking Grok to infer connections between {name_a} and {name_b}...")
        result = infer_connections_for_pair(info_a["block"], info_a["rules"], info_b["block"], info_b["rules"])
        all_connections.extend(result.get("connections", []))
        all_uncertain.extend(result.get("uncertain_connections", []))
        if i < len(pairs):
            time.sleep(SECONDS_BETWEEN_CALLS)

    blocks_by_name = {name: info["block"] for name, info in blocks.items()}
    connections = validate_connections(all_connections, blocks_by_name)

    with open(CONNECTIONS_PATH, "w", encoding="utf-8") as f:
        json.dump({"connections": connections, "uncertain_connections": all_uncertain},
                   f, indent=2, ensure_ascii=False)
    print(f"Saved {len(connections)} validated connections to {CONNECTIONS_PATH}")

    draw_diagram([info["block"] for info in blocks.values()], connections)


if __name__ == "__main__":
    main()
