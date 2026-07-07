"""
Generalized, multi-block pipeline (no longer hardcoded to C_GROUP + C_DRV_1D):

0. The real input is the full raw manual in detailed_markdowns/*.md. For
   any manual with no matching summary_markdowns/*.md yet, ask Grok to
   read it and write that structured connection-rule summary (see
   summarize_detailed_manual) - this only runs once per manual; delete a
   summary file if you want it regenerated from its source manual.
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

Optional: if a user_prompt.txt file exists next to this script, its text
is read once and appended to every Grok prompt (port refinement AND
connection inference) as extra, project-specific guidance - e.g. "this
project always wires the quick-stop feedback" or any other context the
manuals don't capture. It never overrides the hallucination-guard rules;
it's purely extra context to help judgment calls. Leave it missing or
empty to get the original behaviour.
"""

import glob
import itertools
import json
import os
import re
import time

from dotenv import load_dotenv
from openai import OpenAI, RateLimitError, APIStatusError
import matplotlib.pyplot as plt
import matplotlib.patches as patches

load_dotenv()  # loads GROK_API_KEY from a .env file in this folder, if present

MODEL_NAME = "llama-3.3-70b-versatile"  # change here if the model name is wrong

DETAILED_MD_DIR = "detailed_markdowns"
IO_JSONS_DIR = "io_jsons"
SUMMARY_MD_DIR = "summary_markdowns"
CONNECTIONS_PATH = "grok_connections.json"
IMAGE_PATH = "block_diagram.png"
LAYOUT_PATH = "layout.json"

# Optional free-text file where the person running this pipeline can
# describe their specific application/project in their own words - e.g.
# which signals matter most, or context the manuals don't capture - to
# help Grok make better judgment calls on port selection and connections.
# Safe to leave missing or empty; everything works exactly as before.
USER_PROMPT_PATH = "user_prompt.txt"

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
    """Pull the "Please try again in Xh Ym Zs" / "Xm Ys" / "Xs" suggestion
    out of a Groq rate-limit error message, so we wait exactly as long as
    Groq says instead of guessing with a fixed backoff."""
    match = re.search(r"try again in (?:(\d+)h)?(?:(\d+)m)?(\d+(?:\.\d+)?)s", message)
    if not match:
        return None
    hours = float(match.group(1)) if match.group(1) else 0.0
    minutes = float(match.group(2)) if match.group(2) else 0.0
    return hours * 3600 + minutes * 60 + float(match.group(3))


def _call_model(system_prompt: str, user_prompt: str, json_mode: bool):
    """Call Groq once, retrying on rate limits that clear quickly (e.g.
    per-minute token caps). Rate limits that need a long wait (e.g. a
    daily token cap) fail fast with a clear message instead of blocking
    the script for tens of minutes. Returns parsed JSON when json_mode is
    True, otherwise the raw text response (used for the free-form
    Markdown summarization step)."""
    kwargs = {"response_format": {"type": "json_object"}} if json_mode else {}
    for attempt in range(3):
        try:
            response = client.chat.completions.create(
                model=MODEL_NAME,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=0,
                **kwargs,
            )
            content = response.choices[0].message.content
            return json.loads(content) if json_mode else content
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
        except APIStatusError as e:
            if e.status_code == 413:
                raise RuntimeError(
                    "Groq rejected this request as too large for its per-minute token "
                    "limit (a single prompt used more tokens than the whole per-minute "
                    "cap allows) - retrying won't help since the request itself needs to "
                    "be smaller. This usually means one of the blocks involved has an "
                    "unusually large summary/port list; consider trimming its manual, or "
                    "upgrading the Groq tier for a higher per-request limit."
                ) from e
            raise
    raise RuntimeError("Gave up after repeated rate limit errors.")


def call_model_json(system_prompt: str, user_prompt: str) -> dict:
    return _call_model(system_prompt, user_prompt, json_mode=True)


def call_model_text(system_prompt: str, user_prompt: str) -> str:
    return _call_model(system_prompt, user_prompt, json_mode=False)


# ---------------------------------------------------------------------
# Summarization: the real input is the full raw manual in
# detailed_markdowns/*.md - turn each one with no matching summary yet
# into the structured connection-rule summary the rest of the pipeline
# (and, ultimately, another AI reading only that summary) needs.
# ---------------------------------------------------------------------

SUMMARY_SYSTEM_PROMPT = (
    "You are a careful industrial automation engineering assistant who writes "
    "precise, well-structured Markdown documentation."
)

SUMMARY_PROMPT_TEMPLATE = """
You are helping build an automated pipeline that turns Siemens CEMAT function
block manuals into Python code that draws a block diagram (boxes with labeled
input/output pins) and infers the wiring between blocks. Another AI model will
read your summary later to (1) figure out which pins connect between two
blocks, and (2) generate the diagram code. It will NOT have access to the
original manual - only to what you write here. So your summary must be
complete enough to fully replace the manual for that purpose, but should not
include legal text, revision history, tables of contents, or anything not
needed to understand the block's interface and behavior.

I will give you the full Markdown manual for one CEMAT function block. Read
it carefully and produce a single Markdown summary with EXACTLY this
structure:

# <BLOCK_NAME> Summary

## Purpose
2-4 sentences: what this block does and where it's used in a cement plant
application.

## Inputs
One bullet per input pin, in this exact format:
- `PortName` (format/datatype): what it does, what triggers/sets it, and
  where its signal typically comes from (e.g. "from the group block's
  start command" or "from an OS operator button") if the manual says so.

## Outputs
One bullet per output pin, same format:
- `PortName` (format/datatype): what it does and where its signal typically
  goes to (e.g. "feeds a group block's run feedback input"), if the manual
  says so.

## Group/Object Links
Any pins used to link this block to other blocks (e.g. group links, MUX
links). Same bullet format as above. If none, write "None".

## Key Connection Notes
A short bullet list of any explicit statements in the manual about how this
block's pins connect to another block's pins (e.g. "GR_LINK1 must be
connected to the group's G_LINK output", "StartAut receives the automatic
start command from the controlling group"). Quote the manual briefly where
useful. This section is the most important one for inferring wiring later,
so don't skip real connection statements even if the rest of the summary
stays brief.

## Uncertain / Ambiguous Points
Anything about the interface or wiring that the manual doesn't state clearly.
Be honest here rather than guessing.

RULES:
- Use only port/pin names that literally appear in the manual. Do not
  invent, rename, or guess a name.
- Do not include legal notices, table of contents, page numbers, feature-bit
  reference tables, or OS-permission tables unless a specific bit/permission
  directly changes how a pin connects to another block.
- Keep the whole summary focused and readable - long enough to be complete
  on inputs/outputs/connections, short enough that it's not just the manual
  copy-pasted.
- Output only the Markdown summary, nothing else (no preamble, no "Here is...").

Block name for this manual: {block_name}

Manual content follows below (or attached):

{manual}
""".strip()


def block_name_from_stem(stem: str) -> str:
    """Strip a trailing Siemens revision suffix like '_009' off a
    filename stem (C_RelMod_009 -> "C_RelMod") to get the plain block
    name to hand to Grok."""
    return re.sub(r"_\d+$", "", stem)


def summarize_detailed_manual(md_path: str) -> None:
    """Ask Grok to turn one full raw CEMAT manual into the structured
    connection-rule summary the rest of the pipeline needs, saved to
    summary_markdowns/ under the SAME filename stem as the manual."""
    stem = os.path.splitext(os.path.basename(md_path))[0]
    out_path = os.path.join(SUMMARY_MD_DIR, stem + ".md")
    block_name = block_name_from_stem(stem)

    with open(md_path, "r", encoding="utf-8") as f:
        manual = f.read()

    user_prompt = SUMMARY_PROMPT_TEMPLATE.format(block_name=block_name, manual=manual)
    summary = call_model_text(SUMMARY_SYSTEM_PROMPT, user_prompt).strip()

    os.makedirs(SUMMARY_MD_DIR, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(summary + "\n")
    print(f"  Saved summary to {out_path}")


def ensure_all_summaries_exist() -> None:
    """For every detailed_markdowns/*.md manual with no matching
    summary_markdowns/*.md yet (same filename stem), generate one via
    Grok. Existing summaries are left untouched - delete a summary file
    if you want it regenerated from its source manual."""
    detailed_paths = sorted(glob.glob(os.path.join(DETAILED_MD_DIR, "*.md")))
    existing_stems = {
        os.path.splitext(os.path.basename(p))[0]
        for p in glob.glob(os.path.join(SUMMARY_MD_DIR, "*.md"))
    }

    missing = [p for p in detailed_paths
               if os.path.splitext(os.path.basename(p))[0] not in existing_stems]

    for i, md_path in enumerate(missing, start=1):
        print(f"[{i}/{len(missing)}] No summary found for '{os.path.basename(md_path)}' - "
              f"asking Grok to summarize it...")
        summarize_detailed_manual(md_path)
        if i < len(missing):
            time.sleep(SECONDS_BETWEEN_CALLS)


# ---------------------------------------------------------------------
# Discovery: load every block's JSON + its matching rules summary
# ---------------------------------------------------------------------

def normalize(s: str) -> str:
    return re.sub(r"[^a-z0-9]", "", s.lower())


def load_user_guidance() -> str:
    """Read USER_PROMPT_PATH if it exists, so the person running this
    pipeline can add their own free-text notes about this specific
    application to help guide port selection and connection inference.
    Returns "" if the file is missing or empty - callers just skip
    injecting anything in that case, so this is fully optional."""
    if not os.path.exists(USER_PROMPT_PATH):
        return ""
    with open(USER_PROMPT_PATH, "r", encoding="utf-8") as f:
        return f.read().strip()


def user_guidance_block(user_guidance: str) -> str:
    """Render the optional user-guidance section for a prompt. Empty
    string (nothing added to the prompt) if there is no guidance."""
    if not user_guidance:
        return ""
    return f"""

USER-SUPPLIED GUIDANCE FOR THIS SPECIFIC APPLICATION (from the person
running this pipeline - use it to help judgment calls, but it does NOT
override the STRICT RULES above: still only use real, literal port names
from the JSON lists, and only include what those lists actually support):
\"\"\"
{user_guidance}
\"\"\""""


def extract_section(markdown: str, header: str) -> str:
    """Return the body text of one '## <header>' section of a summary
    markdown file, up to the next '## ' heading (or end of file).
    Empty string if that header isn't present."""
    match = re.search(rf"##\s+{re.escape(header)}\s*\n(.*?)(?=\n##\s|\Z)", markdown, re.DOTALL)
    return match.group(1) if match else ""


def connection_rules_excerpt(rules: str) -> str:
    """Trim a full connection-rule summary down to just the sections that
    actually help infer connections between two blocks (Purpose,
    Group/Object Links, Key Connection Notes) - dropping its "Inputs"/
    "Outputs" sections and "Uncertain / Ambiguous Points". The Inputs/
    Outputs prose just restates the same port names/types/descriptions
    already sent verbatim in the JSON port lists alongside this text, so
    for a block with a large port list (40-90+ ports, now that bootstrap
    keeps the full list instead of a curated subset) repeating all of it
    a second time as prose can by itself be enough to blow past Groq's
    per-request token cap. Falls back to the full text untouched if none
    of those headers are present, since some hand-written summaries use
    different section names."""
    if not rules:
        return rules
    keep_headers = ["Purpose", "Group/Object Links", "Key Connection Notes"]
    sections = [(h, extract_section(rules, h)) for h in keep_headers]
    excerpt = "\n\n".join(f"## {h}\n{body.strip()}" for h, body in sections if body.strip())
    return excerpt or rules


def extract_backticked_names(text: str) -> set:
    """Every `PortName`-style identifier mentioned in a chunk of summary
    text - used as the "this name is actually documented somewhere, it's
    not a hallucination" allow-list for both intelligence mode and the
    bootstrap-a-missing-json step below."""
    return set(re.findall(r"`([A-Za-z_][A-Za-z0-9_]*)`", text))


def bootstrap_default_json(md_path: str) -> dict:
    """A summary markdown was found with no matching io_jsons/*.json file
    at all - there is no ports JSON for this block yet. Ask Grok to read
    the summary and extract the FULL, literal port list it documents
    (not a curated subset - see the note below on why), grounded so it
    can only use ports the summary actually documents. The result is
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
There is no ports JSON for this Siemens CEMAT block yet - only its
connection-rule summary markdown exists, shown in full below. Extract
EVERY port documented in the summary into a complete, literal port
list - every bullet in its "Inputs" and "Outputs" sections, plus any
port mentioned in a "Group/Object Links" section that isn't already
listed there. Do NOT curate, filter, or leave any of them out, even
ones that look like internal/OS/diagnostic-only ports - this JSON is
later used to check whether a proposed connection's port name is real,
so leaving a real, documented port out of this list would make a
genuine, correctly-documented connection get wrongly rejected later
just because it never made it into this file. Skip a port only if the
summary's own "Uncertain / Ambiguous Points" section says its exact
name is unclear or unconfirmed.

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
        # Always use the name parsed straight out of the summary's own
        # "# <Name> Summary" header rather than whatever Grok echoes back
        # for "block_name" - the prompt below embeds the file stem (which
        # includes the trailing "_009"-style version suffix) as a label,
        # and Grok sometimes copies that suffix into its own answer,
        # producing a block name like "C_MEAS_I_009" instead of the real
        # logical name "C_MEAS_I". That mismatch breaks every later
        # name-based lookup (candidate pairing, user-guidance matching).
        "block_name": fallback_name,
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

def refine_ports_intelligently(block: dict, rules: str, user_guidance: str = "") -> dict:
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
{user_guidance_block(user_guidance)}
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


def apply_port_selection_mode(blocks: dict, user_guidance: str = "") -> None:
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
        info["block"] = refine_ports_intelligently(info["block"], info["rules"], user_guidance)
        if i < len(names):
            time.sleep(SECONDS_BETWEEN_CALLS)


def assign_port_values(block: dict, user_guidance: str) -> dict:
    """If user_guidance specifies a literal configured value for any of
    this block's input ports (e.g. "HHA 90" for a high-high alarm limit
    input), ask Grok to map that onto the real port name so it can be
    shown next to its pin in the diagram - like a real engineering
    parameter sheet - instead of only being usable as prose context for
    connection inference. Returns {} (no extra Grok call, no values) if
    user_guidance is empty; never invents a value the user didn't
    actually specify."""
    if not user_guidance.strip():
        return {}

    input_names = [p["name"] for p in block["inputs"]]
    if not input_names:
        return {}

    system_prompt = (
        "You are a careful industrial automation engineering assistant. "
        "Output only valid JSON."
    )
    user_prompt = f"""
The person running this pipeline wrote the following free-text guidance
about their specific project:
\"\"\"
{user_guidance}
\"\"\"

Below is the real input port list for one Siemens CEMAT block,
{block['block_name']}. Does the guidance above specify a literal
configured value (a setpoint, alarm limit, range boundary, etc.) for
any of these specific input ports? If so, map each one to that value as
a short display string (e.g. "90", "0.0", "100").

STRICT RULES:
- Only include a port if the guidance clearly gives a value for it -
  match by MEANING (e.g. "high-high alarm" -> whichever port here is
  documented/named as the high-high limit), not by requiring the user
  to type the exact port name.
- Do NOT invent or guess a value for any port the guidance doesn't
  actually specify - an empty mapping is the correct answer if the
  guidance doesn't cover this block at all.
- Only use port names that literally appear in the list below.

=== {block['block_name']} inputs ===
{json.dumps(input_names, indent=2)}

Output only valid JSON in exactly this shape:
{{"port_values": {{"PortName": "value"}}}}
""".strip()

    result = call_model_json(system_prompt, user_prompt)
    values = result.get("port_values", {}) or {}
    return {name: str(value) for name, value in values.items() if name in input_names}


def assign_all_port_values(blocks: dict, user_guidance: str) -> None:
    """Mutates each discovered block in place, adding a "port_values"
    dict for any input ports user_guidance specifies literal values for
    (see assign_port_values), and saves it back to that block's
    io_jsons/*.json so redraw.py (and any later run) sees it without
    another Grok call. No-op (and no extra Grok calls at all) if
    user_guidance is empty."""
    if not user_guidance.strip():
        return

    names = list(blocks)
    for i, name in enumerate(names, start=1):
        info = blocks[name]
        print(f"[{i}/{len(names)}] Checking user guidance for configured port values on {name}...")
        values = assign_port_values(info["block"], user_guidance)
        if values:
            info["block"]["port_values"] = values
            with open(info["json_path"], "w", encoding="utf-8") as f:
                json.dump(info["block"], f, indent=2, ensure_ascii=False)
            print(f"  Set port value(s) for {name}: {values} (saved to {info['json_path']})")
        if i < len(names):
            time.sleep(SECONDS_BETWEEN_CALLS)


# ---------------------------------------------------------------------
# Candidate pairs: only ask Grok about pairs whose rules actually
# mention each other, so N blocks doesn't mean N^2 API calls in practice
# ---------------------------------------------------------------------

def candidate_pairs(blocks: dict, user_guidance: str = "") -> list:
    names = list(blocks)
    all_pairs = list(itertools.combinations(names, 2))

    if user_guidance.strip():
        # The user has given freeform guidance about how they want things
        # connected. We can't reliably tell which specific block pair
        # loose, possibly-imperfect text is about - they may abbreviate,
        # paraphrase, or not name a block exactly as its file is named -
        # so trying to pattern-match guidance text against block names
        # would just recreate the same rigid-matching problem. Instead,
        # when guidance is present, check every pair and let Grok itself
        # weigh the guidance (it already sees the real port lists too,
        # so it won't invent a connection between unrelated blocks just
        # because guidance exists).
        return all_pairs

    pairs = []
    for a, b in all_pairs:
        a_mentions_b = normalize(b) in normalize(blocks[a]["rules"])
        b_mentions_a = normalize(a) in normalize(blocks[b]["rules"])
        if a_mentions_b or b_mentions_a:
            pairs.append((a, b))
    return pairs


# ---------------------------------------------------------------------
# Connection inference (same approach as the original 2-block version,
# now parameterized so it works for any pair of discovered blocks)
# ---------------------------------------------------------------------

def infer_connections_for_pair(block_a: dict, rules_a: str, block_b: dict, rules_b: str, user_guidance: str = "") -> dict:
    name_a, name_b = block_a["block_name"], block_b["block_name"]
    rules_a = connection_rules_excerpt(rules_a)
    rules_b = connection_rules_excerpt(rules_b)

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
  and/or the user-supplied guidance (see the "USER-SUPPLIED GUIDANCE"
  section near the end, if present) clearly support it. The user's own
  guidance is a legitimate, standalone basis for including a connection
  even if the official summaries don't spell it out - the user knows
  their own application and may describe a real relationship the
  summaries never document. If you think a connection likely exists but
  neither the summaries nor the user guidance clearly support both ends,
  put it under "uncertain_connections" instead, with a short note on
  what's missing.
- Do not invent a connection just to look complete.
- Go through EVERY bullet point in the "Key Connection Notes" section of
  BOTH summaries one by one and check it against the port lists - do not
  stop after finding the first few obvious matches. Missing a documented
  rule is as bad as inventing a fake one.

MINIMAL, ESSENTIAL WIRING ONLY:
- Only wire the small set of signals genuinely needed for the described
  application to work correctly - e.g. start/stop commands, run
  feedback, the core process value, and safety interlocks. Do NOT wire
  diagnostic, simulation, mode-selection (e.g. a digital input module's
  MODE port), OS/HMI, maintenance, or status-only signals just because
  matching ports happen to exist on both sides - a real, working
  default engineering setup does not connect everything it technically
  could.
- Before including a connection, ask: would the system fail to perform
  its basic described function without this wire? If not, leave it out
  even if it's technically a valid, documented connection somewhere.
  Prefer a small, clean set of connections over an exhaustive one.
- PUSHBUTTON / DIGITAL INPUT MODULES: for a simple pushbutton or digital
  input module (block_type/description says "digital input" or
  "pushbutton"), the ONLY port that ever matters for wiring is its main
  boolean output (typically named "Q"). Never wire its MODE, VALUE,
  QBAD, QLAST, QMOD_ERR, SIM_*, SUBS_*, LAST_ON, QUALITY, or any other
  port to anything - these are internal/diagnostic, not part of a basic
  application, no matter how plausible a reason sounds.
- INDEPENDENT INPUT DEVICES NEVER WIRE TO EACH OTHER: two different
  input-type blocks (pushbuttons, sensors, digital/analog input
  modules) are never connected directly to one another - each is
  independent and feeds the same downstream consumer (e.g. a drive),
  not each other. If both name_a and name_b are input-type devices with
  no other block between them in this pair, do not invent a connection
  between them; this holds even if a summary or guidance text seems to
  loosely suggest a relationship - a real one always exists.

GROUP <-> COMPONENT LINK CONNECTION IS MANDATORY - NEVER SKIP, NEVER UNCERTAIN:
- FIRST check the precondition: this rule only applies when one of these
  two blocks is actually a supervisory "group"/"route" block (its own
  block_type, description, or Purpose section identifies it as a group,
  route, or master coordinating other objects) and the other is a
  member/component of that specific group/route. If neither block is a
  group/route supervisor - e.g. both are peer field-device blocks such
  as a drive and a measurement/annunciation/process-feedback block -
  this rule does NOT apply, even if both port lists happen to contain
  "LINK" in some port name. Sharing the substring "LINK" is not, by
  itself, evidence of a group/component relationship: most CEMAT blocks
  have some kind of *LINK* port for unrelated purposes (e.g. joining a
  totally different group, or being a slave object of a third block), so
  do not force a connection here without first confirming one side is
  genuinely the group/route being joined.
- Once (and only once) that precondition is confirmed: CEMAT ALWAYS
  physically wires the group to that component through a dedicated link
  interface - the exact name varies per block (G_LINK, GR_LINK1,
  GR_LINK2, O_LINK, O_LINKQ, MUX_LINK, R_LINK, ...) so use whatever the
  port lists actually call it, do not assume it must be named exactly
  "G_LINK"/"GR_LINK1".
- Concretely, once the precondition holds: scan both port lists for any
  output whose name contains "LINK" and any input whose name contains
  "LINK". If you find a plausible pair (one block's "*LINK*" output and
  the other's "*LINK*" input), you MUST output that connection in
  "connections" with confidence >= 0.95, even if the summary's prose
  doesn't spell it out in so many words - the port names themselves are
  the evidence. This is true for a normal, single-instance setup even
  when the manual also discusses other configurations (multiple
  groups/routes, multiplexers) that don't apply here.
- CRITICAL - GETTING THE DIRECTION RIGHT: the "*LINK*" port name that
  contains "LINK" can legitimately appear on EITHER side as an input
  in one block and as an output in the other - do not assume which
  block is the source just because it "feels" like the group should
  send it or a component should send it. You must check literally:
  1. Look at BlockA's "outputs" list and BlockB's "outputs" list - find
     which one of the two actually contains a "*LINK*" entry in its
     OWN "outputs" array (not inputs).
  2. Look at the OTHER block's "inputs" list - confirm it contains a
     matching "*LINK*" entry in its OWN "inputs" array (not outputs).
  3. The block whose "outputs" array literally contains the "*LINK*"
     port is "from_block"/"from_port". The block whose "inputs" array
     literally contains the matching "*LINK*" port is "to_block"/
     "to_port". Never reverse this - a port that is listed under a
     block's "inputs" can NEVER be that block's "from_port", and a
     port listed under a block's "outputs" can NEVER be that block's
     "to_port".
  4. Before finalizing this connection, re-check both port lists one
     more time to confirm from_port truly sits in from_block's
     "outputs" and to_port truly sits in to_block's "inputs" - if it
     is reversed, swap from_block/from_port with to_block/to_port.
- Do NOT push this into "uncertain_connections" and do NOT leave it out
  entirely. A missing group/component link is one of the most serious
  errors possible here, since it is what physically attaches the
  component to its group - treat finding it as mandatory, not a bonus.

GROUP <-> COMPONENT RUN/STOP FEEDBACK IS EXPECTED, NOT OPTIONAL:
- A supervisory group almost always needs to know when its member
  objects are actually running/stopped. If the group side has
  feedback-style inputs for this (commonly named like FbObjOn/FbObjOff,
  or described as "feedback that objects are running/stopped") AND the
  component side has a running/stopped-style output (commonly named
  like RunSig/OffSig, or similarly described), connect them:
  - the component's "running" output -> the group's "on/running"
    feedback input, direct ("inverted": false).
  - the same output, negated, -> the group's "off/stopped" feedback
    input ("inverted": true) - UNLESS the component separately exposes
    its own explicit "stopped" output, in which case connect that
    directly instead.
  Only skip this pair if the relevant ports genuinely don't exist in
  either block's port list - do not skip it just because the summary
  text is thin on the subject; the existence of matching port names on
  both sides is itself strong evidence this connection is real.

SAFETY INTERLOCK FROM ALARM / LIMIT-EXCEEDED OUTPUTS:
- If one block exposes an alarm/limit-exceeded-style output (e.g. a
  high-high, high, low, or low-low limit output, or any output whose
  name or description signals an abnormal condition) and the other
  block has an interlock/protection/stop-style input (e.g. IntStop,
  IntProtG, IntProtA, or similarly described), and the summaries or the
  user's guidance describe this kind of protective relationship between
  them, connect the alarm output to that interlock/stop input so the
  abnormal condition actually stops or blocks the second block. This is
  a real safety-wiring pattern (e.g. an over-temperature reading
  tripping a motor), not just a nice-to-have - include it under the same
  "essential wiring" standard as start/stop/run feedback above.

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
{user_guidance_block(user_guidance)}
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

        if has_output(from_block, from_port) and has_input(to_block, to_port):
            valid.append(c)
            continue

        # The model occasionally reports a real connection with the
        # direction reversed (e.g. swaps a group's LINK output with a
        # component's LINK input). If flipping from/to makes both ends
        # check out against the real port lists, auto-correct instead of
        # silently dropping a connection that actually exists.
        if has_output(to_block, to_port) and has_input(from_block, from_port):
            swapped = dict(c)
            swapped["from_block"], swapped["from_port"] = to_block, to_port
            swapped["to_block"], swapped["to_port"] = from_block, from_port
            print(f"  Auto-correcting reversed connection direction: {c}")
            valid.append(swapped)
            continue

        if not has_output(from_block, from_port):
            print(f"  Dropping connection - '{from_port}' is not an output of {from_block}: {c}")
        elif not has_input(to_block, to_port):
            print(f"  Dropping connection - '{to_port}' is not an input of {to_block}: {c}")
        else:
            print(f"  Dropping connection - direction/ports could not be validated: {c}")
    return valid


START_PORT_RE = re.compile(r"start", re.IGNORECASE)
STOP_PORT_RE = re.compile(r"stop|quickstp", re.IGNORECASE)


def insert_start_stop_interlocks(connections: list, blocks_by_name: dict) -> tuple:
    """Deterministic safety-wiring pattern - not left to the model, since
    it's a fixed rule rather than a judgment call: if a destination
    block gets its start-type command from one source block and its
    stop-type command from a DIFFERENT source block - the classic
    separate start/stop pushbutton setup - splice in a small synthetic
    AND gate between them (start signal AND NOT stop signal) instead of
    wiring both buttons straight into the destination. This stops the
    destination from ever seeing a contradictory "start AND stop both
    pressed" state as a bare start command.

    A destination port counts as "start-type"/"stop-type" if either its
    bare name (e.g. StartLoc/StopLoc) OR its documented description
    (e.g. an abbreviated port like "ESR" described as "Local start
    pushbutton") matches START_PORT_RE/STOP_PORT_RE - matching on name
    alone isn't enough, since different Siemens manuals abbreviate these
    ports very differently and the description is often the only place
    the actual meaning ("start"/"stop") is spelled out in English.

    Returns (new_connections, new_gate_blocks) - gate blocks are
    synthetic (not loaded from any file) and only exist for this
    diagram; add them to the block list handed to draw_diagram."""

    def port_search_text(block_name, port_name):
        block = blocks_by_name.get(block_name, {})
        match = next((p for p in block.get("inputs", []) if p["name"] == port_name), None)
        return f"{port_name} {(match or {}).get('description', '')}"

    by_destination: dict = {}
    for c in connections:
        by_destination.setdefault(c["to_block"], []).append(c)

    gate_blocks = []
    new_connections = list(connections)

    for to_block, dest_conns in by_destination.items():
        start_conn = next(
            (c for c in dest_conns if START_PORT_RE.search(port_search_text(to_block, c["to_port"]))), None
        )
        stop_conn = next(
            (c for c in dest_conns if STOP_PORT_RE.search(port_search_text(to_block, c["to_port"]))), None
        )
        if not start_conn or not stop_conn or start_conn["from_block"] == stop_conn["from_block"]:
            continue  # no separate start/stop sources feeding this block - nothing to protect

        gate_name = f"AND_{to_block}"
        gate_blocks.append({
            "block_name": gate_name,
            "block_type": "AND",
            "description": f"Prevents a simultaneous start+stop command from reaching "
                            f"{to_block}'s {start_conn['to_port']} input.",
            "inputs": [
                {"name": "IN1", "datatype": "BOOL", "description": "Start command"},
                {"name": "IN2", "datatype": "BOOL", "description": "Stop command (inverted)"},
            ],
            "outputs": [{"name": "OUT", "datatype": "BOOL", "description": "Gated start command"}],
        })

        new_connections.remove(start_conn)
        new_connections.remove(stop_conn)
        new_connections.append({
            "from_block": start_conn["from_block"], "from_port": start_conn["from_port"],
            "to_block": gate_name, "to_port": "IN1",
            "reason": "Start command into the start/stop safety AND gate",
            "confidence": 0.99, "inverted": False,
        })
        new_connections.append({
            "from_block": stop_conn["from_block"], "from_port": stop_conn["from_port"],
            "to_block": gate_name, "to_port": "IN2",
            "reason": "Stop command (inverted) into the start/stop safety AND gate",
            "confidence": 0.99, "inverted": True,
        })
        new_connections.append({
            "from_block": gate_name, "from_port": "OUT",
            "to_block": to_block, "to_port": start_conn["to_port"],
            "reason": "Gated start command to the destination block",
            "confidence": 0.99, "inverted": False,
        })

    return new_connections, gate_blocks


def infer_logic_gates(blocks_by_name: dict, connections: list, user_guidance: str) -> tuple:
    """General-purpose logic-gate synthesis - unlike the deterministic
    start/stop AND gate above (a fixed rule that always fires), this is
    exploratory: given the full picture (every block's real ports, every
    already-inferred connection, and the user's own free-text guidance),
    ask Grok whether any other 2-input logic gate (AND/OR/NOR) should be
    inserted to embed control logic the user actually described that a
    plain block-to-block wire can't express - e.g. "trip if either of
    two alarms fires" needs an OR gate. Only runs (and only costs tokens)
    when user_guidance is non-empty, since without it there's no
    reliable signal for what extra logic - if any - the user wants
    beyond what plain per-pair connection inference already covers.

    Every gate has exactly 2 inputs (IN1, IN2) and 1 output (OUT) - a
    single-signal inversion (NOT) doesn't need its own gate, it's just
    an "inverted": true connection, same as everywhere else in this
    pipeline. Every proposed connection is validated against the real
    (or newly-proposed-gate) port lists before being accepted, same as
    validate_connections does for normal connections.

    Returns (new_connections, new_gate_blocks); (connections, [])
    unchanged if user_guidance is empty or Grok proposes nothing."""
    if not user_guidance.strip():
        return connections, []

    system_prompt = (
        "You are a careful industrial automation engineering assistant. "
        "Output only valid JSON."
    )

    blocks_summary = {
        name: {"inputs": [p["name"] for p in b["inputs"]], "outputs": [p["name"] for p in b["outputs"]]}
        for name, b in blocks_by_name.items()
    }

    user_prompt = f"""
Below is the full picture of one control diagram: every block's real
port names, every connection already inferred between them, and the
user's own free-text guidance about their application.

Your task: decide whether any 2-input logic gate (AND, OR, or NOR)
should be inserted to correctly embed control logic the user described
that a plain block-to-block wire can't express by itself - e.g. "trip
if either alarm fires" needs an OR gate; "run only if both permissives
are true" needs an AND gate. Do NOT propose a gate unless the user's
guidance (or an unambiguous combination of documented signals) clearly
calls for combining two specific signals before they reach a specific
destination port - a plausible-sounding guess is worse than no gate at
all here. The classic separate start/stop pushbutton safety interlock
is already handled elsewhere automatically - do not propose it again;
only propose genuinely NEW logic beyond that.

STRICT RULES:
- Only reference block/port names that literally appear below.
- Each gate has exactly 2 inputs (IN1, IN2) and 1 output (OUT) - for a
  single-signal inversion (NOT), just mark the relevant connection's
  "inverted" as true instead of inventing a gate for it.
- For every gate you propose, you MUST also say which existing
  connection(s) it replaces (in "remove_connections") and which new
  connections route through it instead (in "add_connections") - a gate
  that doesn't actually connect into the diagram is useless.
- If nothing clearly calls for a new gate, return empty lists - this is
  the common, correct answer when the guidance doesn't describe this
  kind of combinational logic.

=== Blocks (name -> real ports) ===
{json.dumps(blocks_summary, indent=2)}

=== Already-inferred connections ===
{json.dumps(connections, indent=2)}

=== User guidance ===
\"\"\"
{user_guidance}
\"\"\"

Output only valid JSON in exactly this shape:
{{
  "gate_blocks": [
    {{"block_name": "...", "gate_type": "AND|OR|NOR", "description": "..."}}
  ],
  "remove_connections": [
    {{"from_block": "...", "from_port": "...", "to_block": "...", "to_port": "..."}}
  ],
  "add_connections": [
    {{"from_block": "...", "from_port": "...", "to_block": "...", "to_port": "...", "inverted": false, "reason": "..."}}
  ]
}}
""".strip()

    result = call_model_json(system_prompt, user_prompt)

    proposed_gates = result.get("gate_blocks", []) or []
    gate_blocks = []
    for g in proposed_gates:
        gate_type = (g.get("gate_type") or "").upper()
        name = g.get("block_name")
        if gate_type not in ("AND", "OR", "NOR") or not name:
            print(f"  Skipping proposed gate {g!r} - missing a name or an unknown gate_type.")
            continue
        gate_blocks.append({
            "block_name": name,
            "block_type": gate_type,
            "description": g.get("description", ""),
            "inputs": [
                {"name": "IN1", "datatype": "BOOL", "description": "Gate input 1"},
                {"name": "IN2", "datatype": "BOOL", "description": "Gate input 2"},
            ],
            "outputs": [{"name": "OUT", "datatype": "BOOL", "description": "Gate output"}],
        })

    if not gate_blocks:
        return connections, []

    all_names = set(blocks_by_name) | {g["block_name"] for g in gate_blocks}
    port_lookup = {**blocks_by_name, **{g["block_name"]: g for g in gate_blocks}}
    new_connections = list(connections)

    def matches(c, spec):
        return (c.get("from_block") == spec.get("from_block") and c.get("from_port") == spec.get("from_port")
                and c.get("to_block") == spec.get("to_block") and c.get("to_port") == spec.get("to_port"))

    for spec in result.get("remove_connections", []) or []:
        match = next((c for c in new_connections if matches(c, spec)), None)
        if match:
            new_connections.remove(match)
        else:
            print(f"  Warning: gate step asked to remove a connection that doesn't exist: {spec}")

    def has_output(block_name, port_name):
        block = port_lookup.get(block_name)
        return bool(block) and port_name in {p["name"] for p in block["outputs"]}

    def has_input(block_name, port_name):
        block = port_lookup.get(block_name)
        return bool(block) and port_name in {p["name"] for p in block["inputs"]}

    for spec in result.get("add_connections", []) or []:
        from_block, from_port = spec.get("from_block"), spec.get("from_port")
        to_block, to_port = spec.get("to_block"), spec.get("to_port")
        if from_block not in all_names or to_block not in all_names:
            print(f"  Dropping gate-step connection - unknown block: {spec}")
        elif not has_output(from_block, from_port):
            print(f"  Dropping gate-step connection - '{from_port}' is not an output of {from_block}: {spec}")
        elif not has_input(to_block, to_port):
            print(f"  Dropping gate-step connection - '{to_port}' is not an input of {to_block}: {spec}")
        else:
            new_connections.append({
                "from_block": from_block, "from_port": from_port,
                "to_block": to_block, "to_port": to_port,
                "reason": spec.get("reason", "Logic gate wiring"),
                "confidence": spec.get("confidence", 0.85),
                "inverted": bool(spec.get("inverted", False)),
            })

    print(f"  Inferred {len(gate_blocks)} additional logic gate(s): {[g['block_name'] for g in gate_blocks]}")
    return new_connections, gate_blocks


# ---------------------------------------------------------------------
# Deterministic drawing (fixed layout code, not LLM-generated)
# ---------------------------------------------------------------------

ROW_HEIGHT = 1.0
TITLE_HEIGHT = 3
ANNOTATION_LINE_HEIGHT = 0.75  # extra vertical space per annotation line beyond the first
BOX_WIDTH = 6.0
GAP = 14.0  # horizontal gap between adjacent boxes, leaves room for labels + wires
VERTICAL_GAP = 3.0  # vertical space between stacked component boxes in hub-and-spoke mode
STUB = 0.6  # length of the little tick mark sticking out of each pin


def is_group_block(block: dict) -> bool:
    return "group" in block.get("block_type", "").strip().lower()


def annotation_lines(block: dict) -> list:
    """Optional custom subtitle lines for one block (block["annotation"]
    in its io_jsons/*.json, a string that can contain "\\n" for multiple
    lines) shown under the block name instead of the default block_type
    text - e.g. to surface fixed engineering setpoints (alarm limits,
    scale range, etc.) for this specific project without hardcoding them
    into the drawing code. Empty list if the block has no "annotation"."""
    text = (block.get("annotation") or "").strip()
    return text.split("\n") if text else []


def title_height(block: dict) -> float:
    """Title band height for one block: the default TITLE_HEIGHT, plus
    room for any annotation lines beyond the first (which already fits
    in the same space the single-line block_type subtitle used)."""
    extra_lines = max(len(annotation_lines(block)) - 1, 0)
    return TITLE_HEIGHT + extra_lines * ANNOTATION_LINE_HEIGHT


def block_height(block: dict) -> float:
    n_rows = max(len(block["inputs"]), len(block["outputs"]), 1)
    return (n_rows + 1) * ROW_HEIGHT + title_height(block)


def box_layout(block: dict, box_left: float, box_bottom: float = 0.0) -> dict:
    """Compute the geometry for one block's box: its rectangle plus the
    y-position of every input and output pin."""
    box_top = box_bottom + block_height(block)

    def pin_ys(n):
        top_of_pins = box_top - title_height(block) - ROW_HEIGHT * 0.5
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


def topological_order(blocks_in_order: list, connections: list) -> list:
    """Order blocks left-to-right by actual data flow (Kahn's algorithm):
    if one block's output feeds another's input, the source ends up to
    the left of the destination, instead of whatever order the blocks
    happened to be discovered in. Falls back gracefully when the
    connection graph has a cycle - e.g. a component that both takes
    commands from and sends feedback back to another block, which is
    common and expected - by breaking the tie on whichever remaining
    block has the fewest unresolved incoming edges, rather than giving
    up on ordering the rest of the diagram. Ties are otherwise broken by
    original discovery order, so the layout stays stable across runs."""
    names = [b["block_name"] for b in blocks_in_order]
    original_index = {name: i for i, name in enumerate(names)}

    out_edges = {name: set() for name in names}
    in_degree = {name: 0 for name in names}
    for c in connections:
        a, b = c.get("from_block"), c.get("to_block")
        if a not in out_edges or b not in out_edges or a == b or b in out_edges[a]:
            continue
        out_edges[a].add(b)
        in_degree[b] += 1

    remaining = set(names)
    ordered_names = []
    while remaining:
        ready = sorted(
            (n for n in remaining if in_degree[n] == 0),
            key=lambda n: original_index[n],
        )
        if not ready:
            # A cycle is blocking further progress - break it by picking
            # the remaining block with the fewest unresolved incoming
            # edges instead of stalling.
            ready = [min(remaining, key=lambda n: (in_degree[n], original_index[n]))]
        for n in ready:
            ordered_names.append(n)
            remaining.discard(n)
            for m in out_edges[n]:
                if m in remaining:
                    in_degree[m] -= 1

    name_to_block = {b["block_name"]: b for b in blocks_in_order}
    return [name_to_block[n] for n in ordered_names]


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


def load_manual_layout(blocks_by_name: dict, connections: list) -> list:
    """Optional manual override for block placement (layout.json next to
    this script): a JSON object like {"columns": [["A"], ["B", "C"],
    ["D"]]} - each inner list is one column, stacked vertically,
    left-to-right in the order given. Lets you pin an exact arrangement
    that pure data-flow ordering can't express on its own - e.g. two
    sibling blocks with no connection between them (so nothing in the
    connection graph says which should be left/right of the other, or
    that they belong in the same column) still need a specific spot.

    A block layout.json doesn't mention yet (most commonly a synthetic
    logic-gate block, whose name is only decided at run time) doesn't
    invalidate the whole thing - it's inserted automatically right after
    the rightmost column any of its source blocks appears in, so e.g. a
    gate fed by two buttons in column 1 lands in a new column 2, ahead
    of whatever was already there (like the motor at column 2), instead
    of being silently ignored or dumped somewhere nonsensical.

    Returns None (falls back to the automatic topological layout) only
    if the file is missing, or if it names a block that doesn't actually
    exist."""
    if not os.path.exists(LAYOUT_PATH):
        return None

    with open(LAYOUT_PATH, "r", encoding="utf-8") as f:
        spec = json.load(f)

    columns_of_names = [list(column) for column in spec.get("columns", [])]
    named = [name for column in columns_of_names for name in column]
    unknown = [name for name in named if name not in blocks_by_name]
    if unknown:
        print(f"Warning: {LAYOUT_PATH} lists unknown block(s) {unknown} - ignoring it and "
              f"falling back to automatic left-to-right ordering.")
        return None

    missing = [name for name in blocks_by_name if name not in named]
    if missing:
        col_index = {name: i for i, column in enumerate(columns_of_names) for name in column}
        sources_of = {}
        for c in connections:
            if c["to_block"] in missing:
                sources_of.setdefault(c["to_block"], []).append(c["from_block"])

        for name in missing:
            known_source_cols = [col_index[s] for s in sources_of.get(name, []) if s in col_index]
            insert_at = min((max(known_source_cols) + 1) if known_source_cols else len(columns_of_names),
                             len(columns_of_names))
            columns_of_names.insert(insert_at, [name])
            col_index = {n: i for i, column in enumerate(columns_of_names) for n in column}

        print(f"Note: {LAYOUT_PATH} doesn't mention {missing} - auto-placed based on their "
              f"source blocks' columns. Add them to {LAYOUT_PATH} yourself to pin their exact position.")

    return [[blocks_by_name[name] for name in column] for column in columns_of_names]


def layout_columns(columns: list) -> dict:
    """Place blocks in explicit left-to-right columns (each column a
    list of blocks stacked vertically, top-aligned to the tallest
    column) per an optional manual layout.json override - the general
    form of layout_hub_and_spokes's single-group-plus-stack layout, for
    an arbitrary number of columns."""
    layouts = {}
    stack_heights = [
        sum(block_height(b) for b in column) + VERTICAL_GAP * max(len(column) - 1, 0)
        for column in columns
    ]
    top = max(stack_heights)

    x = 0.0
    for column in columns:
        y = top
        for block in column:
            height = block_height(block)
            bottom = y - height
            layouts[block["block_name"]] = box_layout(block, box_left=x, box_bottom=bottom)
            y = bottom - VERTICAL_GAP
        x += BOX_WIDTH + GAP

    return layouts


def draw_block(ax, block: dict, layout: dict, instance_no: int) -> None:
    left, right, top, bottom = layout["left"], layout["right"], layout["top"], layout["bottom"]
    t_height = title_height(block)

    ax.add_patch(patches.Rectangle((left, bottom), BOX_WIDTH, top - bottom,
                                    edgecolor="black", facecolor="white", linewidth=1.5, zorder=2))
    ax.add_patch(patches.Rectangle((left, top - t_height), BOX_WIDTH, t_height,
                                    edgecolor="black", facecolor="white", linewidth=1.5, zorder=2))
    tag_w, tag_h = BOX_WIDTH * 0.42, TITLE_HEIGHT * 0.45
    ax.add_patch(patches.Rectangle((right - tag_w - 0.15, top - tag_h - 0.15), tag_w, tag_h,
                                    edgecolor="black", facecolor="#bfe3e3", linewidth=1, zorder=3))

    ax.text(left + 0.15, top - 0.5, str(instance_no), fontsize=7, va="top", ha="left", zorder=4)
    ax.text(left + 0.15, top - 1.3, block["block_name"], fontsize=8, fontweight="bold", va="top", ha="left", zorder=4)

    lines = annotation_lines(block)
    if lines:
        for i, line in enumerate(lines):
            ax.text(left + 0.15, top - 2.25 - i * ANNOTATION_LINE_HEIGHT, line,
                    fontsize=6, va="top", ha="left", zorder=4)
    else:
        block_type = block["block_type"]
        if len(block_type) > 14:
            block_type = block_type[:13] + "…"
        ax.text(left + 0.15, top - 2.25, block_type, fontsize=6, va="top", ha="left", zorder=4)

    port_values = block.get("port_values", {})
    for y, port in zip(layout["input_ys"], block["inputs"]):
        ax.plot([left - STUB, left], [y, y], color="black", linewidth=1, zorder=1)
        value = port_values.get(port["name"])
        label = f"{value}-{port['name']}" if value is not None else port["name"]
        ax.text(left - STUB - 0.15, y, label, fontsize=7, family="monospace",
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


CHAR_WIDTH_ESTIMATE = 0.42  # rough monospace glyph width (data units) at the pin-label fontsize


def pin_label_text(block: dict, port: dict, side: str) -> str:
    """The exact text draw_block renders for one pin's label - kept in
    sync with draw_block so routing can measure it accurately (an input
    with a configured port_values entry is longer than its bare name,
    e.g. "90.0-VAL_HH" instead of just "VAL_HH")."""
    if side == "inputs":
        value = block.get("port_values", {}).get(port["name"])
        return f"{value}-{port['name']}" if value is not None else port["name"]
    return port["name"]


def label_clearance(block: dict, side: str) -> float:
    """How far a wire needs to travel out from this block before it's
    clear of every pin label on the given side, so a highway wire's
    vertical run doesn't cut straight through unrelated pins' label
    text on its way to the shared basement lane."""
    ports = block.get(side, [])
    widest = max((len(pin_label_text(block, p, side)) for p in ports), default=0)
    return STUB + widest * CHAR_WIDTH_ESTIMATE


def draw_connections(ax, connections: list, blocks_by_name: dict, layouts: dict, is_forward) -> None:
    """Route every connection. "Forward" connections (as decided by the
    is_forward callback) get a clean elbow straight through the open gap
    between the two boxes, since both pins face that gap - each forward
    wire gets its own vertical lane so several of them sharing a gap
    don't visually coincide. Everything else is routed through a shared
    "highway" lane below the whole drawing - every such wire gets its
    own lane so they never overlap - since those pins face away from
    each other and a straight line would have to cut through boxes in
    between.

    Highway wires additionally stagger their vertical drop near the
    source and their vertical rise near the destination (side_lane
    below) - without this, every highway wire leaving the same source
    block (or entering the same destination block) would drop/rise
    along the exact same x position regardless of which port it's
    actually on, making them visually indistinguishable from each other
    even though their horizontal "basement" row is already unique."""
    lowest_bottom = min(l["bottom"] for l in layouts.values())
    wrap_offset = 1.5
    side_stagger = 0.35
    wrap_count = 0
    from_lane_count: dict = {}
    to_lane_count: dict = {}
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
            from_lane_count[from_name] = from_lane_count.get(from_name, 0) + 1
            to_lane_count[to_name] = to_lane_count.get(to_name, 0) + 1
            x1 = (from_layout["right"] + label_clearance(blocks_by_name[from_name], "outputs")
                  + (from_lane_count[from_name] - 1) * side_stagger)
            x2 = (to_layout["left"] - label_clearance(blocks_by_name[to_name], "inputs")
                  - (to_lane_count[to_name] - 1) * side_stagger)
            wrap_y = lowest_bottom - (2 + wrap_count * wrap_offset)
            wrap_count += 1
            # Explicitly draw the horizontal run from the pin itself out
            # to x1/x2 (not just the vertical drop) - without this, the
            # line only started AT x1/x2, leaving a visible gap between
            # the pin and where the wire actually begins whenever the
            # label-clearance offset is bigger than the tiny pin stub.
            xs = [from_layout["right"], x1, x1, x2, x2, to_layout["left"]]
            ys = [y_from, y_from, wrap_y, wrap_y, y_to, y_to]

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
        manual_columns = load_manual_layout(blocks_by_name, connections)
        if manual_columns:
            # A layout.json override is present and names every block
            # exactly once - use its explicit column groupings instead of
            # the automatic topological ordering below.
            layouts = layout_columns(manual_columns)
            col_of = {b["block_name"]: i for i, column in enumerate(manual_columns) for b in column}
            is_forward = lambda c: col_of[c["to_block"]] == col_of[c["from_block"]] + 1  # noqa: E731
            ordered_for_numbering = [b for column in manual_columns for b in column]
        else:
            # Fallback: no single group detected (zero, or more than one),
            # and no manual layout.json override - order blocks
            # left-to-right by actual data flow (whichever block feeds
            # another's input goes to the left of it) instead of whatever
            # order they happened to be discovered in.
            blocks_in_order = topological_order(blocks_in_order, connections)
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
    user_guidance = load_user_guidance()
    if user_guidance:
        print(f"Loaded user guidance from {USER_PROMPT_PATH} ({len(user_guidance)} chars).")

    ensure_all_summaries_exist()
    blocks = discover_blocks()
    apply_port_selection_mode(blocks, user_guidance)
    assign_all_port_values(blocks, user_guidance)
    pairs = candidate_pairs(blocks, user_guidance)
    print(f"Found {len(pairs)} candidate pair(s) whose rules reference each other: {pairs}")

    all_connections, all_uncertain = [], []
    for i, (name_a, name_b) in enumerate(pairs, start=1):
        info_a, info_b = blocks[name_a], blocks[name_b]
        print(f"[{i}/{len(pairs)}] Asking Grok to infer connections between {name_a} and {name_b}...")
        result = infer_connections_for_pair(info_a["block"], info_a["rules"], info_b["block"], info_b["rules"], user_guidance)
        all_connections.extend(result.get("connections", []))
        all_uncertain.extend(result.get("uncertain_connections", []))
        if i < len(pairs):
            time.sleep(SECONDS_BETWEEN_CALLS)

    blocks_by_name = {name: info["block"] for name, info in blocks.items()}
    connections = validate_connections(all_connections, blocks_by_name)

    # Deterministic safety gate first (always fires when the pattern
    # exists, free), then the general Grok-driven gate step sees the
    # already-gated picture (so it won't try to re-propose the same
    # start/stop gate) and can add any other logic the user described.
    connections, safety_gates = insert_start_stop_interlocks(connections, blocks_by_name)
    if safety_gates:
        print(f"Inserted {len(safety_gates)} safety AND gate(s): {[g['block_name'] for g in safety_gates]}")

    blocks_by_name_with_gates = {**blocks_by_name, **{g["block_name"]: g for g in safety_gates}}
    connections, extra_gates = infer_logic_gates(blocks_by_name_with_gates, connections, user_guidance)
    gate_blocks = safety_gates + extra_gates

    # The final, post-gate state is what gets saved - redraw.py just
    # loads this directly, no need to recompute any gate logic.
    with open(CONNECTIONS_PATH, "w", encoding="utf-8") as f:
        json.dump({"connections": connections, "uncertain_connections": all_uncertain, "gate_blocks": gate_blocks},
                   f, indent=2, ensure_ascii=False)
    print(f"Saved {len(connections)} connections ({len(gate_blocks)} gate block(s)) to {CONNECTIONS_PATH}")

    draw_diagram([info["block"] for info in blocks.values()] + gate_blocks, connections)


if __name__ == "__main__":
    main()
