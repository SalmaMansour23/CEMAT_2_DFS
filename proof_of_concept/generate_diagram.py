"""
Simple 4-step pipeline:

1. Summarize: turn each raw manual in detailed_markdowns/*.md with no
   matching summary_markdowns/*.md yet into a structured connection-rule
   summary (see summarize_detailed_manual). Runs once per manual; delete
   a summary file to regenerate it. Several instances of the exact same
   underlying block (e.g. one digital input channel reused as a start
   button, a stop button, and a sensor) share one generic manual, so
   their summaries end up with identical bodies - only the title/name is
   instance-specific, derived from the filename, never from the manual.

2. Select ports: for each block with no matching io_jsons/*.json yet,
   read its summary AND the user's own user_prompt.txt description of
   their application, and ask Grok to cherry-pick the smallest set of
   real ports this specific project actually needs - each with a short
   reason (see select_ports_for_block). This is the ONLY port-selection
   step; there is no separate "default vs intelligence" mode anymore.
   Runs once per block; delete an io_jsons/*.json file to force
   re-selection (e.g. after changing user_prompt.txt).

3. Infer connections: for every pair of blocks whose summaries mention
   each other (or every pair, if user_prompt.txt has content), ask Grok
   to infer the wiring between their selected ports, with a reason per
   connection (see infer_connections_for_pair). Simple field input
   devices (pushbuttons, sensors, digital/analog input channels) are
   handled deterministically, not by prompt rules: they never wire to
   each other, and only their main output ("Q") ever matters (see
   is_input_device_block / force_input_device_ports / validate_connections).
   Whenever a destination gets separate start and stop commands from two
   different sources, a small AND gate (start AND NOT stop) is always
   spliced in automatically (see insert_start_stop_interlocks) - this is
   a fixed rule, not something the model has to remember.

4. Draw: place blocks left-to-right by actual data flow, automatically
   stacking blocks of the same type that land at the same point in the
   flow into one column (see compute_layers / automatic_columns) - e.g.
   several digital input channels used as different buttons/sensors
   stack together, while a differently-typed block at the same point
   still gets its own column. An optional layout.json can pin an exact
   arrangement instead. This step is plain, fixed matplotlib code (not
   LLM-generated) - Grok's job is limited to reading manuals and
   figuring out ports/wiring, not inventing the drawing itself.

Optional: if user_prompt.txt exists next to this script, its text is
read once and used in step 2 (port selection) and step 3 (connection
inference) as the description of what this specific project needs.
Leave it missing or empty to get a minimal default selection instead.
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

# Optional free-text file where the person running this pipeline
# describes their specific application in their own words - used to
# pick the minimal ports each block needs (step 2) and to help infer
# connections (step 3). Safe to leave missing or empty.
USER_PROMPT_PATH = "user_prompt.txt"

# Pacing between Grok calls so many small pairwise requests don't blow
# past Groq's per-minute token cap. Bump this up if you add blocks with
# much larger summaries and start seeing rate-limit retries.
SECONDS_BETWEEN_CALLS = 20

client = OpenAI(
    api_key=os.environ["GROK_API_KEY"],
    base_url="https://api.groq.com/openai/v1",
    # Without this, the SDK silently retries a 429 itself (its own sleep,
    # not ours) before _call_model's rate-limit handling below ever sees
    # it - so a long wait looks like the script just hanging instead of
    # printing the clear fail-fast message.
    max_retries=0,
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
# Step 1 - Summarization: turn each raw manual into a structured
# connection-rule summary the rest of the pipeline needs.
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

## Similar Signal Disambiguation
CEMAT blocks often have several pins that sound similar at a glance but
serve genuinely different situations - e.g. a "remote"-only interlock vs. a
general-purpose one, or a single-drive start command vs. a group/route-level
one. For every group of two or more inputs (or two or more outputs) whose
names or one-line descriptions could be confused for each other, write one
bullet per signal in that group explaining specifically what distinguishes
it from the others (remote vs. local, general vs. mode-specific,
single-device vs. group/route-level, automatic vs. manual, etc.) and one
concrete example scenario where THIS signal - and not the similar-sounding
ones - is the correct one to use. Base every distinction ONLY on what the
manual actually documents about each pin - do not invent a difference it
doesn't support. If the manual has no groups of similar/overlapping pins,
write "None".

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

Note: the manual below may refer to itself throughout by a generic
catalog name (e.g. "CH_DI") - that's expected when the same reusable
block is instantiated multiple times for different physical devices
(e.g. one instance wired to a start button, another to a stop button,
another to a sensor). Always title your summary "# {block_name} Summary"
using the exact name given above, not whatever generic name the manual
uses internally - but keep the rest of the summary (Purpose, Inputs,
Outputs, etc.) describing the block's actual generic function, since
that part is genuinely the same across every instance of this block.

Manual content follows below (or attached):

{manual}
""".strip()


def block_name_from_stem(stem: str) -> str:
    """Strip a trailing Siemens revision suffix like '_009' off a
    filename stem (C_RelMod_009 -> "C_RelMod") to get the plain block
    name for this specific instance."""
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

    # Force the title to the filename-derived block_name no matter what
    # Grok actually wrote - the raw manual for a generic, reusable block
    # refers to itself by its own generic catalog name throughout, and
    # Grok sometimes echoes that instead of the specific instance name
    # it was given, even when told not to. The body text underneath is
    # expected to stay generic/shared across identical instances - only
    # the title needs to be instance-specific, since that's what
    # discover_blocks()/select_ports_for_block rely on.
    title_line = f"# {block_name} Summary"
    if re.match(r"^#\s+.+$", summary):
        summary = re.sub(r"^#\s+.+$", title_line, summary, count=1)
    else:
        summary = f"{title_line}\n\n{summary}"

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
# Shared helpers
# ---------------------------------------------------------------------

def normalize(s: str) -> str:
    return re.sub(r"[^a-z0-9]", "", s.lower())


def load_user_guidance() -> str:
    """Read USER_PROMPT_PATH if it exists, so the person running this
    pipeline can describe their specific application in their own
    words. Returns "" if the file is missing or empty - callers just
    fall back to a minimal default selection in that case."""
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

USER'S APPLICATION DESCRIPTION (use it to decide what's needed, but
never invent a port/connection it doesn't actually support):
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
    "Outputs" sections and "Uncertain / Ambiguous Points", since the same
    port names/types/descriptions are already sent verbatim in the JSON
    port lists alongside this text. Falls back to the full text
    untouched if none of those headers are present."""
    if not rules:
        return rules
    keep_headers = ["Purpose", "Group/Object Links", "Key Connection Notes", "Similar Signal Disambiguation"]
    sections = [(h, extract_section(rules, h)) for h in keep_headers]
    excerpt = "\n\n".join(f"## {h}\n{body.strip()}" for h, body in sections if body.strip())
    return excerpt or rules


def extract_backticked_names(text: str) -> set:
    """Every `PortName`-style identifier mentioned in a chunk of summary
    text - the "this name is actually documented somewhere, it's not a
    hallucination" allow-list used when selecting ports."""
    return set(re.findall(r"`([A-Za-z_][A-Za-z0-9_]*)`", text))


def is_input_device_block(block: dict) -> bool:
    """True for a simple field input device (pushbutton, sensor, digital/
    analog input channel module) - the kind of block whose only relevant
    signal in a basic application is a single output.

    This is Grok's own explicit judgment call, asked directly as a plain
    yes/no question with full context (the block's summary and the
    user's application description) in the SAME call that selects its
    ports - see select_ports_for_block. There is no keyword list or
    fallback here: guessing this from block_type/description text after
    the fact proved unreliable (the same underlying block, used for two
    different instances, got worded differently enough by Grok that a
    keyword search caught one and missed the other), whereas Grok
    already knows the answer at selection time - it just needs to be
    asked to state it, not have it reverse-engineered from prose later."""
    return bool(block.get("is_input_device"))


def force_input_device_ports(block: dict) -> dict:
    """Enforce the one STRUCTURAL fact that's true by definition for a
    simple field input device, regardless of what it's called or which
    vendor/catalog it's from: it has no wired inputs. Which output(s) to
    keep is NOT hardcoded to a specific name (e.g. "Q") - that would only
    hold for one specific block family - so whatever Grok already
    selected as this block's outputs is trusted as-is."""
    adjusted = dict(block)
    adjusted["inputs"] = []
    return adjusted


# ---------------------------------------------------------------------
# Step 2 - Port selection: for each block, cherry-pick the smallest set
# of real ports THIS project actually needs, using the user's own
# description of their application.
# ---------------------------------------------------------------------

def select_ports_for_block(md_path: str, user_guidance: str) -> dict:
    """Read one block's summary and the user's application description,
    and ask Grok to pick the smallest set of real ports this specific
    project actually needs, each with a short reason. Saved to
    io_jsons/*.json so later runs reuse it without another Grok call -
    delete the file to force re-selection (e.g. after changing
    user_prompt.txt)."""
    stem = os.path.splitext(os.path.basename(md_path))[0]
    json_path = os.path.join(IO_JSONS_DIR, stem + ".json")
    block_name = block_name_from_stem(stem)

    with open(md_path, "r", encoding="utf-8") as f:
        rules = f.read()

    print(f"No io_jsons file found for '{stem}' - asking Grok to pick this project's ports for it...")

    allowed_names = extract_backticked_names(rules)

    system_prompt = "You are a careful industrial automation engineer. Output only valid JSON."
    user_prompt = f"""
Block: {block_name}

Below is this block's connection-rule summary, followed by the user's
own description of what they're building.

Pick the smallest set of real ports (inputs and outputs) this specific
project actually needs - as few as possible. For each port, give a
one-sentence reason tied to the user's description. If the user's
description gives a literal configured value for an input (a setpoint,
alarm limit, etc.), include it as "value".

Rules:
- Only use port names that appear in the summary below. Never invent one.
- If the user gave no relevant description for this block, pick the
  minimal set needed for basic start/stop/run operation only.

"block_type" should be the general CATEGORY of block (e.g. "Digital
Input Channel", "Analog Measurement", "Motor Drive"), not this
instance's name - two different instances of the same underlying block
should get the same block_type.

Also answer directly, as plain facts about this block (not a guess from
wording elsewhere):
- "is_input_device": true if this is a simple field input device (a
  pushbutton, sensor, or digital/analog input channel module) whose
  only relevant signal in a basic application is a single output value,
  with no inputs that would ever need to be wired to another block.
  false for anything else (a drive, a group/route, a measurement block
  with real configuration inputs, a logic block, etc.).
- "is_group": true if this is a supervisory group/route block that
  coordinates other objects (drives, valves, etc.) as members. false otherwise.

Output only this JSON shape:
{{
  "block_type": "...",
  "description": "...",
  "is_input_device": false,
  "is_group": false,
  "inputs": [{{"name": "...", "datatype": "...", "description": "...", "reason": "...", "value": "..."}}],
  "outputs": [{{"name": "...", "datatype": "...", "description": "...", "reason": "..."}}]
}}

=== {block_name} summary ===
{rules}

=== User's application description ===
{user_guidance or "(none given - pick the minimal standard set for basic operation)"}
""".strip()

    result = call_model_json(system_prompt, user_prompt)

    def sanitize(ports: list) -> list:
        kept = []
        for p in ports:
            name = (p.get("name") or "").strip().strip("`")
            if name in allowed_names:
                kept.append(p)
            else:
                print(f"  Dropping '{name}' for {block_name} - not a real port in its summary.")
        return kept

    inputs = sanitize(result.get("inputs", []))
    outputs = sanitize(result.get("outputs", []))

    block = {
        "block_name": block_name,
        "block_type": result.get("block_type", "Unknown"),
        "description": result.get("description", ""),
        "is_input_device": bool(result.get("is_input_device")),
        "is_group": bool(result.get("is_group")),
        "inputs": [{"name": p["name"], "datatype": p.get("datatype", "?"),
                    "description": p.get("description", ""), "reason": p.get("reason", "")}
                   for p in inputs],
        "outputs": [{"name": p["name"], "datatype": p.get("datatype", "?"),
                     "description": p.get("description", ""), "reason": p.get("reason", "")}
                    for p in outputs],
    }

    port_values = {p["name"]: str(p["value"]) for p in inputs if p.get("value")}
    if port_values:
        block["port_values"] = port_values

    if block["is_input_device"]:
        block = force_input_device_ports(block)
        print(f"  {block_name} is a simple input device (Grok's own call) - clearing its wired inputs.")

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(block, f, indent=2, ensure_ascii=False)
    print(f"  Saved {block_name}'s selected ports to {json_path}")

    return block


def discover_blocks(user_guidance: str = "") -> dict:
    """Load every *.json in io_jsons/, and pair each with the summary .md
    in summary_markdowns/ that best matches its filename: prefer an exact
    same-stem match (C_GROUP_009.json <-> C_GROUP_009.md); fall back to
    the block's "block_name" field appearing in the summary's filename.

    Any summary .md left over with no matching json at all gets its
    ports selected for this project (see select_ports_for_block) so it
    can be discovered and connected just like every other block."""
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
        block = select_ports_for_block(md_path, user_guidance)
        name = block["block_name"]
        if name in blocks:
            print(f"Warning: block_name '{name}' (from {md_path}) already discovered - skipping.")
            continue
        json_path = os.path.join(IO_JSONS_DIR, os.path.splitext(os.path.basename(md_path))[0] + ".json")
        with open(md_path, "r", encoding="utf-8") as f:
            rules = f.read()
        blocks[name] = {"block": block, "rules": rules, "json_path": json_path, "summary_path": md_path}

    print(f"Discovered {len(blocks)} block(s): {', '.join(blocks)}")
    return blocks


# ---------------------------------------------------------------------
# Step 3 - Connection inference: only ask Grok about pairs whose rules
# actually mention each other (or every pair, if user_prompt.txt has
# content), so N blocks doesn't mean N^2 API calls in practice.
# ---------------------------------------------------------------------

def candidate_pairs(blocks: dict, user_guidance: str = "") -> list:
    names = list(blocks)
    all_pairs = list(itertools.combinations(names, 2))

    # Two independent field input devices never wire directly to each
    # other - each is independent and feeds a downstream consumer, not
    # another input device. Hard, deterministic exclusion (also saves
    # tokens) rather than relying on the model to remember this.
    all_pairs = [
        (a, b) for a, b in all_pairs
        if not (is_input_device_block(blocks[a]["block"]) and is_input_device_block(blocks[b]["block"]))
    ]

    if user_guidance.strip():
        # The user has given freeform guidance about how they want things
        # connected. We can't reliably tell which specific block pair
        # loose, possibly-imperfect text is about, so when guidance is
        # present, check every remaining pair and let Grok weigh it.
        return all_pairs

    pairs = []
    for a, b in all_pairs:
        a_mentions_b = normalize(b) in normalize(blocks[a]["rules"])
        b_mentions_a = normalize(a) in normalize(blocks[b]["rules"])
        if a_mentions_b or b_mentions_a:
            pairs.append((a, b))
    return pairs


def infer_connections_for_pair(block_a: dict, rules_a: str, block_b: dict, rules_b: str, user_guidance: str = "") -> dict:
    name_a, name_b = block_a["block_name"], block_b["block_name"]
    rules_a = connection_rules_excerpt(rules_a)
    rules_b = connection_rules_excerpt(rules_b)

    system_prompt = "You are a careful industrial automation engineer. Output only valid JSON."

    user_prompt = f"""
Below are the real input/output ports for two Siemens CEMAT blocks,
{name_a} and {name_b}, as JSON, followed by their connection-rule
summaries.

Infer the connections between {name_a} and {name_b} - in either
direction (an output of either block can feed an input of the other).

STRICT RULES:
- Only use port names that literally appear in the JSON lists below. Never invent one.
- Only include a connection if the summaries or the user's own guidance clearly support it -
  if unsure, put it under "uncertain_connections" instead of guessing.
- Wire only what's needed for the application the user described - skip diagnostic,
  simulation, or status-only signals unless the user specifically needs them.
- GROUP <-> COMPONENT LINK: if one block is a supervisory group/route and the other is its
  member, they always share a dedicated link port pair (name varies: G_LINK, GR_LINK1,
  O_LINK, etc. - whatever the port lists actually call it). Find it and wire it in the
  correct direction: whichever block's OWN "outputs" list contains the link port is the source.
- GROUP <-> COMPONENT FEEDBACK: a group also usually needs run/stop feedback from its members
  (e.g. a drive's running output feeding the group's running-feedback input, and its negation
  feeding the stopped-feedback input) - wire it if matching ports exist.
- ALARM -> INTERLOCK: if one block has an alarm/limit output and the other has an
  interlock/protection input, and the guidance describes this kind of safety relationship,
  wire the alarm into the interlock.
- SIMILAR SIGNALS: if a summary's "Similar Signal Disambiguation" section lists several
  similar-purpose ports, pick the one matching what the user actually described, not the
  most generic-sounding one.
- Mark a connection "inverted": true if the signal must be logically negated before
  reaching its destination.
- Tag each connection's "role" with what it actually does: "start" (a start/run/ON
  command), "stop" (a stop/OFF command), or "other" (anything else - feedback,
  interlock, process value, link, etc.). Judge this the same way you judged the
  connection itself - by what the port and the application actually mean, not by
  whether the word "start"/"stop" literally appears anywhere.

Output only valid JSON in exactly this shape:
{{
  "connections": [
    {{
      "from_block": "{name_a}",
      "from_port": "...",
      "to_block": "{name_b}",
      "to_port": "...",
      "reason": "short reason",
      "confidence": 0.0,
      "inverted": false,
      "role": "start|stop|other"
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
    hallucination).

    This alone is enough to guarantee a simple input device never
    receives a wired input and never uses anything but its selected
    output(s): force_input_device_ports (see select_ports_for_block)
    already cleared its "inputs" to [] before connection inference ever
    ran, so has_input() below is always False for it, and Grok was never
    even shown a port that isn't one of its selected outputs in the
    first place - no separate special-case check needed."""

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
        # direction reversed. If flipping from/to makes both ends check
        # out against the real port lists, auto-correct instead of
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


def insert_start_stop_interlocks(connections: list, blocks_by_name: dict) -> tuple:
    """Deterministic safety-wiring pattern - not left to the model to
    decide WHETHER to do, since it's a fixed engineering rule rather
    than a judgment call: if a destination block gets its start-type
    command from one source block and its stop-type command from a
    DIFFERENT source block - the classic separate start/stop pushbutton
    setup - splice in a small synthetic AND gate between them (start
    signal AND NOT stop signal), which becomes the ONLY path for the
    start command (so it's never live without the gate's protection).

    The stop command is different: it still ALSO feeds the gate
    (inverted, as the safety check against a simultaneous start), but
    its own DIRECT connection to the destination is left in place rather
    than being consumed by the gate - the stop signal doesn't need the
    gate's protection to reach its destination, only the start signal
    does.

    WHICH connection is start-type/stop-type is Grok's own explicit
    "role" tag on each connection (see infer_connections_for_pair) -
    not a regex guess over port names/descriptions. A port's literal
    name or static description often doesn't say "start"/"stop" at all
    (e.g. "Automatic ON command"), and a bare substring search is also
    fooled by unrelated mode qualifiers (e.g. "single-start mode" is
    describing an operating mode, not a start command) - Grok already
    knows which is which when it proposes the connection, so it's asked
    to say so directly instead of that being reverse-engineered from
    prose afterward.

    Returns (new_connections, new_gate_blocks) - gate blocks are
    synthetic (not loaded from any file) and only exist for this
    diagram; add them to the block list handed to draw_diagram."""
    by_destination: dict = {}
    for c in connections:
        by_destination.setdefault(c["to_block"], []).append(c)

    gate_blocks = []
    new_connections = list(connections)

    for to_block, dest_conns in by_destination.items():
        start_conn = next((c for c in dest_conns if c.get("role") == "start"), None)
        stop_conn = next((c for c in dest_conns if c.get("role") == "stop"), None)
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

        # Start is fully consumed by the gate - it should never reach the
        # destination except through it. Stop is NOT removed: it keeps
        # its own direct connection to the destination (already in
        # new_connections) in addition to also feeding the gate below.
        new_connections.remove(start_conn)
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


# ---------------------------------------------------------------------
# Step 4 - Deterministic drawing (fixed layout code, not LLM-generated)
# ---------------------------------------------------------------------

ROW_HEIGHT = 1.0
TITLE_HEIGHT = 3
ANNOTATION_LINE_HEIGHT = 0.75  # extra vertical space per annotation line beyond the first
BOX_WIDTH = 6.0
GAP = 14.0  # horizontal gap between adjacent columns, leaves room for labels + wires
VERTICAL_GAP = 3.0  # vertical space between stacked blocks in the same column
STUB = 0.6  # length of the little tick mark sticking out of each pin


def is_group_block(block: dict) -> bool:
    """Grok's own explicit judgment call (see select_ports_for_block),
    not a "group" keyword search - a block's block_type can legitimately
    describe something else entirely (e.g. "Motor Drive") while its
    Purpose text merely mentions groups it interfaces with, which a bare
    keyword search can't tell apart from actually being one."""
    return bool(block.get("is_group"))


def annotation_lines(block: dict) -> list:
    """Optional custom subtitle lines for one block (block["annotation"]
    in its io_jsons/*.json, a string that can contain "\\n" for multiple
    lines) shown under the block name instead of the default block_type
    text. Empty list if the block has no "annotation"."""
    text = (block.get("annotation") or "").strip()
    return text.split("\n") if text else []


def title_height(block: dict) -> float:
    """Title band height for one block: the default TITLE_HEIGHT, plus
    room for any annotation lines beyond the first."""
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


def compute_layers(blocks_in_order: list, connections: list) -> dict:
    """Assign each block a left-to-right layer number by actual data
    flow (Kahn's algorithm, processed one whole "ready" batch at a time):
    0 for a pure source, N+1 for anything fed only by layer-N-or-earlier
    blocks. Independent blocks with no path between them - e.g. two
    separate buttons feeding the same drive - land in the SAME layer,
    which is what lets automatic_columns group them into one column.
    Falls back gracefully on a cycle (e.g. a component that both takes
    commands from and sends feedback back to another block) by breaking
    the tie on whichever remaining block has the fewest unresolved
    incoming edges. Ties are otherwise broken by original discovery
    order, so the layout stays stable across runs."""
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
    layer_of = {}
    layer = 0
    while remaining:
        ready = sorted(
            (n for n in remaining if in_degree[n] == 0),
            key=lambda n: original_index[n],
        )
        if not ready:
            ready = [min(remaining, key=lambda n: (in_degree[n], original_index[n]))]
        for n in ready:
            layer_of[n] = layer
            remaining.discard(n)
            for m in out_edges[n]:
                if m in remaining:
                    in_degree[m] -= 1
        layer += 1
    return layer_of


def automatic_columns(blocks_in_order: list, connections: list) -> list:
    """Default automatic layout: place blocks left-to-right by data-flow
    layer (see compute_layers), and within the same layer, stack blocks
    of the same kind into one column - e.g. several digital input
    channels used as different buttons/sensors read as one family and
    stack together, while a differently-typed block at the same layer
    (like an analog measurement block) still gets its own column.

    Simple field input devices are grouped by is_input_device_block()
    (a stable, deterministic classification - see that function) rather
    than by the raw block_type string, since Grok's freely-written
    block_type for a specific instance is not reliably identical even
    across instances of the exact same underlying block - grouping by
    the raw string would silently split them into separate columns
    whenever the wording happened to differ. Every other block still
    groups by its own block_type, since those aren't repeated generic
    instances the same way."""
    layer_of = compute_layers(blocks_in_order, connections)
    original_index = {b["block_name"]: i for i, b in enumerate(blocks_in_order)}

    groups: dict = {}
    for b in blocks_in_order:
        type_key = "INPUT_DEVICE" if is_input_device_block(b) else b.get("block_type", "")
        key = (layer_of[b["block_name"]], type_key)
        groups.setdefault(key, []).append(b)

    ordered_keys = sorted(
        groups,
        key=lambda key: (key[0], original_index[groups[key][0]["block_name"]]),
    )
    return [groups[key] for key in ordered_keys]


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
    instead of the automatic one.

    A block layout.json doesn't mention yet (most commonly a synthetic
    logic-gate block, whose name is only decided at run time) doesn't
    invalidate the whole thing - it's inserted automatically right after
    the rightmost column any of its source blocks appears in.

    Returns None (falls back to automatic_columns) only if the file is
    missing, or if it names a block that doesn't actually exist."""
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
    column) - the general form of layout_hub_and_spokes's
    single-group-plus-stack layout, for an arbitrary number of columns."""
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
    sync with draw_block so routing can measure it accurately."""
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
    source and their vertical rise near the destination - without this,
    every highway wire leaving the same source block (or entering the
    same destination block) would drop/rise along the exact same x
    position regardless of which port it's actually on."""
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
            # to x1/x2 (not just the vertical drop) so the wire never
            # visibly floats disconnected from its pin.
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
        # layout.json can pin an exact arrangement; otherwise place
        # blocks automatically by data-flow layer, stacking same-type
        # blocks at the same layer into one column.
        columns = load_manual_layout(blocks_by_name, connections) or automatic_columns(blocks_in_order, connections)
        layouts = layout_columns(columns)
        col_of = {b["block_name"]: i for i, column in enumerate(columns) for b in column}
        is_forward = lambda c: col_of[c["to_block"]] == col_of[c["from_block"]] + 1  # noqa: E731
        ordered_for_numbering = [b for column in columns for b in column]

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
    blocks = discover_blocks(user_guidance)
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

    # Deterministic safety gate: always fires when a destination gets
    # separate start/stop commands from two different sources, for free.
    connections, gate_blocks = insert_start_stop_interlocks(connections, blocks_by_name)
    if gate_blocks:
        print(f"Inserted {len(gate_blocks)} safety AND gate(s): {[g['block_name'] for g in gate_blocks]}")

    with open(CONNECTIONS_PATH, "w", encoding="utf-8") as f:
        json.dump({"connections": connections, "uncertain_connections": all_uncertain, "gate_blocks": gate_blocks},
                   f, indent=2, ensure_ascii=False)
    print(f"Saved {len(connections)} connections ({len(gate_blocks)} gate block(s)) to {CONNECTIONS_PATH}")

    draw_diagram([info["block"] for info in blocks.values()] + gate_blocks, connections)


if __name__ == "__main__":
    main()
