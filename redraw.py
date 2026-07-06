"""
Temporary utility: redraw block_diagram.png from the already-saved
grok_connections.json without calling Grok again. Use this while
iterating on layout/drawing code (colors, routing, spacing, etc.) so
you don't burn tokens re-inferring connections that haven't changed.

Only rerun the real pipeline (generate_diagram.py) once you've actually
changed which blocks/manuals/user_prompt.txt are involved - this script
just re-renders the picture from what's already in grok_connections.json.
"""

import json

from generate_diagram import CONNECTIONS_PATH, IMAGE_PATH, discover_blocks, draw_diagram


def main() -> None:
    blocks = discover_blocks()

    with open(CONNECTIONS_PATH, "r", encoding="utf-8") as f:
        connections = json.load(f)["connections"]

    draw_diagram([info["block"] for info in blocks.values()], connections)
    print(f"Redrew {IMAGE_PATH} from {CONNECTIONS_PATH} ({len(connections)} connection(s)) - no Grok calls made.")


if __name__ == "__main__":
    main()
