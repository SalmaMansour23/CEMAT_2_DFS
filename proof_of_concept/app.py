"""
Chat-style frontend for generate_diagram.py (ChatGPT/Claude-style): type
your application description and attach manual(s) in one combined input
box, send, and watch the reply stream in - first the same progress
messages the command-line pipeline already prints, then the finished
block diagram - both appearing as the assistant's reply to your message.

This is a thin wrapper: it reuses generate_diagram.py's existing logic
completely unchanged (summarization, port selection, connection
inference, deterministic gate insertion, drawing) - it doesn't
reimplement any of it. Uploaded manuals are copied into
detailed_markdowns/ under their ORIGINAL filenames, so the pipeline's
existing "skip if a summary with the same name already exists" logic
(ensure_all_summaries_exist) applies exactly as it does from the
command line - no manual is re-summarized just because it came through
the chat instead of already being on disk. Manuals you attach in one
turn stay on disk for every later turn too, so you can build a project
up across several messages.

Note: progress streaming works by temporarily redirecting sys.stdout
(process-wide) while the pipeline runs in a background thread, since
the pipeline already reports progress via plain print() calls and this
avoids threading a logger callback through dozens of call sites. That's
fine for one person generating one diagram at a time (the normal use of
this tool) - sending a second message before the first reply finishes
would interleave their progress logs, so wait for each reply to finish.
"""

import os
import queue
import shutil
import sys
import threading

# Make relative paths (detailed_markdowns/, user_prompt.txt, .env, etc.)
# resolve against this script's own folder regardless of what working
# directory the process was launched from.
os.chdir(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import gradio as gr

import generate_diagram as pipeline


class _QueueWriter:
    """A minimal stdout-like object: buffers partial writes and pushes
    each COMPLETE line into a queue as soon as it's written, so the
    chat reply below can poll the queue and stream progress into the
    assistant's message bubble as it happens."""

    def __init__(self, q: "queue.Queue"):
        self.q = q
        self.buffer = ""

    def write(self, text: str) -> None:
        self.buffer += text
        while "\n" in self.buffer:
            line, self.buffer = self.buffer.split("\n", 1)
            self.q.put(line)

    def flush(self) -> None:
        pass


def _save_uploaded_manuals(files) -> list:
    """Copy uploaded manual files into detailed_markdowns/ under their
    ORIGINAL filenames, so the existing same-filename-stem-skips-
    resummarization logic applies unchanged."""
    os.makedirs(pipeline.DETAILED_MD_DIR, exist_ok=True)
    saved = []
    for f in files or []:
        src_path = f if isinstance(f, str) else f.name
        dest_name = os.path.basename(src_path)
        dest_path = os.path.join(pipeline.DETAILED_MD_DIR, dest_name)
        shutil.copyfile(src_path, dest_path)
        saved.append(dest_name)
    return saved


def _run_pipeline_in_background(q: "queue.Queue", result: dict) -> None:
    """Runs the exact same steps as `python generate_diagram.py`, with
    stdout captured line-by-line into `q` for the chat reply to stream."""
    old_stdout = sys.stdout
    sys.stdout = _QueueWriter(q)
    try:
        pipeline.main()
        result["ok"] = True
    except Exception as e:
        result["ok"] = False
        result["error"] = str(e)
        q.put(f"ERROR: {e}")
    finally:
        sys.stdout = old_stdout
        q.put(None)  # sentinel: pipeline finished


def respond(message: dict, history: list):
    """Handles one chat turn: adds the user's text + attachments to the
    conversation, then streams the assistant's reply - progress lines
    as they arrive, followed by the finished diagram image."""
    text = (message.get("text") or "").strip()
    files = message.get("files") or []

    history = history + [{"role": "user", "content": text or "(no description given)"}]
    for f in files:
        history.append({"role": "user", "content": gr.File(f)})
    yield history, gr.MultimodalTextbox(value=None, interactive=False)

    if files:
        saved = _save_uploaded_manuals(files)
        history.append({
            "role": "assistant",
            "content": f"Saved {len(saved)} manual(s) to {pipeline.DETAILED_MD_DIR}/: {', '.join(saved)}",
        })

    with open(pipeline.USER_PROMPT_PATH, "w", encoding="utf-8") as f:
        f.write(text)

    history.append({"role": "assistant", "content": "Starting..."})
    yield history, gr.MultimodalTextbox(value=None, interactive=False)

    q: "queue.Queue" = queue.Queue()
    result: dict = {}
    thread = threading.Thread(target=_run_pipeline_in_background, args=(q, result), daemon=True)
    thread.start()

    log_lines = []
    while True:
        line = q.get()
        if line is None:
            break
        log_lines.append(line)
        history[-1]["content"] = "\n".join(log_lines)
        yield history, gr.MultimodalTextbox(value=None, interactive=False)

    if result.get("ok") and os.path.exists(pipeline.IMAGE_PATH):
        history.append({"role": "assistant", "content": gr.Image(pipeline.IMAGE_PATH)})
    else:
        history.append({"role": "assistant", "content": "Failed - see the log above for the error."})

    yield history, gr.MultimodalTextbox(value=None, interactive=True)


with gr.Blocks(title="CEMAT Block Diagram Generator") as demo:
    gr.Markdown(
        "# CEMAT Block Diagram Generator\n"
        "Describe your application and attach the raw CEMAT manual(s) in markdown for the blocks in your project"
    )
    chatbot = gr.Chatbot(height=600, label="Diagram Assistant")
    msg_box = gr.MultimodalTextbox(
        file_types=[".md"],
        file_count="multiple",  # default is "single" - blocks ctrl/shift multi-select and re-attaching after the first file
        placeholder="Describe your application, attach manual(s), and press enter...",
        show_label=False,
    )

    msg_box.submit(respond, inputs=[msg_box, chatbot], outputs=[chatbot, msg_box])


if __name__ == "__main__":
    demo.queue().launch()
