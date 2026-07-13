from __future__ import annotations

import argparse
import json
from pathlib import Path

from PIL import Image


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a Codex pet package.")
    parser.add_argument("--package-dir", required=True, type=Path)
    parser.add_argument("--cell-width", type=int, default=192)
    parser.add_argument("--cell-height", type=int, default=208)
    parser.add_argument("--frames", type=int, default=8)
    parser.add_argument("--rows", type=int, default=9)
    args = parser.parse_args()

    package_dir = args.package_dir.expanduser().resolve()
    pet_json = package_dir / "pet.json"
    if not pet_json.exists():
        raise FileNotFoundError(f"Missing pet.json: {pet_json}")

    data = json.loads(pet_json.read_text(encoding="utf-8"))
    for key in ("id", "displayName", "description", "spritesheetPath"):
        if not data.get(key):
            raise ValueError(f"pet.json must contain non-empty `{key}`")

    spritesheet = package_dir / data["spritesheetPath"]
    if not spritesheet.exists():
        raise FileNotFoundError(f"Missing spritesheet: {spritesheet}")

    image = Image.open(spritesheet)
    expected_size = (args.cell_width * args.frames, args.cell_height * args.rows)
    if image.size != expected_size:
        raise ValueError(f"Spritesheet size {image.size} does not match {expected_size}")

    result = {
        "ok": True,
        "package_dir": str(package_dir),
        "pet_id": data["id"],
        "display_name": data["displayName"],
        "spritesheet": str(spritesheet),
        "size": list(image.size),
        "mode": image.mode,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
