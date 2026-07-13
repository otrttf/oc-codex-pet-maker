from __future__ import annotations

import argparse
import json
from pathlib import Path

from PIL import Image


DEFAULT_STATES = [
    "idle",
    "running-right",
    "running-left",
    "waving",
    "jumping",
    "failed",
    "waiting",
    "running",
    "review",
]


def load_manifest(path: Path) -> list[tuple[str, Path]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    rows = data.get("rows")
    if not isinstance(rows, list) or not rows:
        raise ValueError("Manifest must contain a non-empty `rows` array.")
    result = []
    for row in rows:
        state = row["state"]
        strip = (path.parent / row["strip"]).resolve()
        result.append((state, strip))
    return result


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Compose transparent Codex pet row strips into one spritesheet."
    )
    parser.add_argument("--manifest", type=Path, help="JSON file with rows: [{state, strip}].")
    parser.add_argument("--row", action="append", help="state=/absolute/or/relative/strip.png")
    parser.add_argument("--out", required=True, type=Path)
    parser.add_argument("--webp-out", type=Path)
    parser.add_argument("--cell-width", type=int, default=192)
    parser.add_argument("--cell-height", type=int, default=208)
    parser.add_argument("--frames", type=int, default=8)
    args = parser.parse_args()

    if args.manifest:
        rows = load_manifest(args.manifest.resolve())
    elif args.row:
        rows = []
        for item in args.row:
            if "=" not in item:
                raise ValueError(f"Expected --row state=path, got {item!r}")
            state, raw_path = item.split("=", 1)
            rows.append((state, Path(raw_path).expanduser().resolve()))
    else:
        raise ValueError("Provide either --manifest or one or more --row values.")

    expected_states = DEFAULT_STATES[: len(rows)]
    actual_states = [state for state, _ in rows]
    if actual_states != expected_states:
        raise ValueError(f"Unexpected row order: {actual_states}. Expected: {expected_states}.")

    row_size = (args.cell_width * args.frames, args.cell_height)
    atlas = Image.new("RGBA", (row_size[0], args.cell_height * len(rows)), (0, 0, 0, 0))
    for row_index, (state, strip_path) in enumerate(rows):
        if not strip_path.exists():
            raise FileNotFoundError(strip_path)
        strip = Image.open(strip_path).convert("RGBA")
        if strip.size != row_size:
            raise ValueError(f"{state} row has size {strip.size}; expected {row_size}: {strip_path}")
        atlas.alpha_composite(strip, (0, row_index * args.cell_height))

    args.out.parent.mkdir(parents=True, exist_ok=True)
    atlas.save(args.out)
    print(args.out)
    if args.webp_out:
        args.webp_out.parent.mkdir(parents=True, exist_ok=True)
        atlas.save(args.webp_out, lossless=True, method=6)
        print(args.webp_out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
