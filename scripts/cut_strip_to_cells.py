from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


def parse_hex_color(value: str) -> tuple[int, int, int]:
    raw = value.strip().lstrip("#")
    if len(raw) != 6:
        raise ValueError(f"Expected a 6-digit hex color, got {value!r}")
    return int(raw[0:2], 16), int(raw[2:4], 16), int(raw[4:6], 16)


def is_key_color(r: int, g: int, b: int, key: tuple[int, int, int], tolerance: int) -> bool:
    return abs(r - key[0]) + abs(g - key[1]) + abs(b - key[2]) <= tolerance


def decontaminate(r: int, g: int, b: int, key: tuple[int, int, int]) -> tuple[int, int, int]:
    kr, kg, kb = key
    # Pull antialiased edge pixels away from the chroma key color. This is intentionally
    # conservative: it reduces key spill without recoloring the pet's real palette.
    if kr >= kg and kr >= kb and r > 150 and b > 150 and g < 135:
        avg = int((r + b) / 2)
        if avg - g > 55:
            return max(0, int(r * 0.82)), min(180, max(g, int(avg * 0.72))), max(0, int(b * 0.90))
    if kg >= kr and kg >= kb and g > 150 and r < 150 and b < 170:
        return min(190, max(r, int(g * 0.42))), max(0, int(g * 0.70)), min(190, max(b, int(g * 0.42)))
    return r, g, b


def components(mask: Image.Image) -> list[dict]:
    w, h = mask.size
    pix = mask.load()
    seen = bytearray(w * h)
    comps: list[dict] = []
    for y in range(h):
        for x in range(w):
            idx = y * w + x
            if seen[idx] or pix[x, y] == 0:
                continue
            q = [(x, y)]
            seen[idx] = 1
            pts = []
            minx = maxx = x
            miny = maxy = y
            area = 0
            while q:
                cx, cy = q.pop()
                pts.append((cx, cy))
                area += 1
                minx = min(minx, cx)
                maxx = max(maxx, cx)
                miny = min(miny, cy)
                maxy = max(maxy, cy)
                for nx in (cx - 1, cx, cx + 1):
                    for ny in (cy - 1, cy, cy + 1):
                        if nx == cx and ny == cy:
                            continue
                        if 0 <= nx < w and 0 <= ny < h:
                            ni = ny * w + nx
                            if not seen[ni] and pix[nx, ny] != 0:
                                seen[ni] = 1
                                q.append((nx, ny))
            comps.append({"area": area, "bbox": (minx, miny, maxx + 1, maxy + 1), "pts": pts})
    return comps


def intersects(a: tuple[int, int, int, int], b: tuple[int, int, int, int]) -> bool:
    return not (a[2] <= b[0] or b[2] <= a[0] or a[3] <= b[1] or b[3] <= a[1])


def build_keyed_image_and_mask(
    image: Image.Image,
    key: tuple[int, int, int],
    tolerance: int,
) -> tuple[Image.Image, Image.Image]:
    keyed = image.convert("RGBA")
    pix = keyed.load()
    mask = Image.new("L", keyed.size, 0)
    mp = mask.load()
    for y in range(keyed.height):
        for x in range(keyed.width):
            r, g, b, a = pix[x, y]
            if a and not is_key_color(r, g, b, key, tolerance):
                nr, ng, nb = decontaminate(r, g, b, key)
                pix[x, y] = (nr, ng, nb, a)
                mp[x, y] = 255
            else:
                pix[x, y] = (0, 0, 0, 0)
    return keyed, mask


def clean_segment(
    segment: Image.Image,
    key: tuple[int, int, int],
    tolerance: int,
) -> tuple[Image.Image, Image.Image, list[dict]]:
    keyed, mask = build_keyed_image_and_mask(segment, key, tolerance)
    pix = keyed.load()
    comps = components(mask)
    removed = []
    if comps:
        main_comp = max(comps, key=lambda c: c["area"])
        mx1, my1, mx2, my2 = main_comp["bbox"]
        expanded = (max(0, mx1 - 18), max(0, my1 - 18), min(segment.width, mx2 + 18), min(segment.height, my2 + 18))
        keep = Image.new("L", segment.size, 0)
        kp = keep.load()
        for comp in comps:
            if comp is main_comp or (comp["area"] >= 12 and intersects(comp["bbox"], expanded)):
                for x, y in comp["pts"]:
                    kp[x, y] = 255
            else:
                removed.append({"area": comp["area"], "bbox": list(comp["bbox"])})
        mask = keep
        mp = mask.load()
        for y in range(segment.height):
            for x in range(segment.width):
                if mp[x, y] == 0:
                    pix[x, y] = (0, 0, 0, 0)
    return keyed, mask, removed


def component_crop_boxes(
    image: Image.Image,
    frames: int,
    key: tuple[int, int, int],
    tolerance: int,
    padding: int,
    min_area: int,
    adaptive_padding: bool,
    padding_guard: int,
    min_gutter_warning_px: int,
    fail_min_gutter_px: int | None,
) -> tuple[list[tuple[int, int, int, int]], list[dict], dict]:
    _, mask = build_keyed_image_and_mask(image, key, tolerance)
    comps = [comp for comp in components(mask) if comp["area"] >= min_area]
    comps.sort(key=lambda comp: comp["area"], reverse=True)
    selected = comps[:frames]
    selected.sort(key=lambda comp: (comp["bbox"][0] + comp["bbox"][2]) / 2)
    if len(selected) != frames:
        raise RuntimeError(f"Expected {frames} large components, found {len(selected)}")

    gutters = []
    for idx in range(len(selected) - 1):
        left_bbox = selected[idx]["bbox"]
        right_bbox = selected[idx + 1]["bbox"]
        gutters.append(
            {
                "between_components": [idx + 1, idx + 2],
                "px": right_bbox[0] - left_bbox[2],
            }
        )

    min_gutter = min((gutter["px"] for gutter in gutters), default=None)
    tight_gutters = [
        gutter for gutter in gutters if gutter["px"] < min_gutter_warning_px
    ]
    if fail_min_gutter_px is not None:
        failing = [gutter for gutter in gutters if gutter["px"] < fail_min_gutter_px]
        if failing:
            details = ", ".join(
                f"{item['between_components'][0]}-{item['between_components'][1]}={item['px']}px"
                for item in failing
            )
            raise RuntimeError(
                f"Source strip frame gutters are too tight for reliable cutting: {details}. "
                "Regenerate with wider pure-chroma gutters or lower --fail-min-gutter-px."
            )

    boxes = []
    diagnostics = []
    for idx, comp in enumerate(selected):
        x1, y1, x2, y2 = comp["bbox"]
        left_gutter = x1 - selected[idx - 1]["bbox"][2] if idx > 0 else None
        right_gutter = selected[idx + 1]["bbox"][0] - x2 if idx < len(selected) - 1 else None
        left_padding = padding
        right_padding = padding
        if adaptive_padding:
            if left_gutter is not None:
                left_padding = min(left_padding, max(0, left_gutter - padding_guard))
            if right_gutter is not None:
                right_padding = min(right_padding, max(0, right_gutter - padding_guard))

        box = (
            max(0, x1 - left_padding),
            max(0, y1 - padding),
            min(image.width, x2 + right_padding),
            min(image.height, y2 + padding),
        )
        boxes.append(box)
        diagnostics.append(
            {
                "component": idx + 1,
                "area": comp["area"],
                "bbox": [x1, y1, x2, y2],
                "left_gutter_px": left_gutter,
                "right_gutter_px": right_gutter,
                "requested_padding_px": padding,
                "effective_padding_px": {
                    "left": left_padding,
                    "top": padding,
                    "right": right_padding,
                    "bottom": padding,
                },
                "padded_crop_box": list(box),
            }
        )
    spacing_summary = {
        "adaptive_padding": adaptive_padding,
        "padding_guard_px": padding_guard,
        "requested_component_padding_px": padding,
        "min_gutter_px": min_gutter,
        "min_gutter_warning_px": min_gutter_warning_px,
        "gutters": gutters,
        "warnings": [
            (
                f"components {item['between_components'][0]}-{item['between_components'][1]} "
                f"only have {item['px']}px gutter; use wider generated gutters or adaptive padding"
            )
            for item in tight_gutters
        ],
    }
    return boxes, diagnostics, spacing_summary


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--src", required=True, type=Path)
    parser.add_argument("--prefix", required=True)
    parser.add_argument("--frames", type=int, default=8)
    parser.add_argument("--mode", choices=["equal-slots", "smart-components"], default="equal-slots")
    parser.add_argument("--cell-width", type=int, default=192)
    parser.add_argument("--cell-height", type=int, default=208)
    parser.add_argument("--safe-pad-x", type=int, default=18)
    parser.add_argument("--safe-pad-y", type=int, default=14)
    parser.add_argument("--key-color", default="ff00ff", help="Chroma key color as hex, for example ff00ff or 00ff00.")
    parser.add_argument("--key-tolerance", type=int, default=95)
    parser.add_argument("--component-padding", type=int, default=16)
    parser.add_argument("--min-component-area", type=int, default=1000)
    parser.add_argument(
        "--fixed-component-padding",
        action="store_true",
        help="Disable automatic left/right padding shrinkage when neighboring frames are close.",
    )
    parser.add_argument(
        "--padding-guard",
        type=int,
        default=2,
        help="Minimum pure-chroma pixels to leave between an adaptive crop and the next component.",
    )
    parser.add_argument(
        "--min-gutter-warning-px",
        type=int,
        default=24,
        help="Write warnings when detected component gutters are below this width.",
    )
    parser.add_argument(
        "--fail-min-gutter-px",
        type=int,
        default=None,
        help="Fail if any detected component gutter is below this width.",
    )
    args = parser.parse_args()

    im = Image.open(args.src).convert("RGBA")
    outdir = args.src.parent
    cell_w, cell_h = args.cell_width, args.cell_height
    key = parse_hex_color(args.key_color)
    seg_w = im.width // args.frames
    frames = []
    metrics = []
    component_diagnostics = []
    spacing_summary = None

    if args.mode == "smart-components":
        crop_boxes, component_diagnostics, spacing_summary = component_crop_boxes(
            im,
            frames=args.frames,
            key=key,
            tolerance=args.key_tolerance,
            padding=args.component_padding,
            min_area=args.min_component_area,
            adaptive_padding=not args.fixed_component_padding,
            padding_guard=args.padding_guard,
            min_gutter_warning_px=args.min_gutter_warning_px,
            fail_min_gutter_px=args.fail_min_gutter_px,
        )
    else:
        crop_boxes = [
            (i * seg_w, 0, (i + 1) * seg_w if i < args.frames - 1 else im.width, im.height)
            for i in range(args.frames)
        ]

    for i, crop_box in enumerate(crop_boxes):
        seg = im.crop(crop_box).convert("RGBA")
        seg, mask, removed = clean_segment(seg, key, args.key_tolerance)

        bbox = mask.getbbox() or (0, 0, seg.width, seg.height)
        crop = seg.crop(bbox)
        max_w = cell_w - args.safe_pad_x * 2
        max_h = cell_h - args.safe_pad_y * 2
        scale = min(max_w / crop.width, max_h / crop.height)
        new_size = (max(1, round(crop.width * scale)), max(1, round(crop.height * scale)))
        resized = crop.resize(new_size, Image.Resampling.LANCZOS)
        rp = resized.load()
        for y in range(resized.height):
            for x in range(resized.width):
                r, g, b, a = rp[x, y]
                if a and is_key_color(r, g, b, key, args.key_tolerance):
                    rp[x, y] = (0, 0, 0, 0)
                elif a:
                    nr, ng, nb = decontaminate(r, g, b, key)
                    rp[x, y] = (nr, ng, nb, a)

        frame = Image.new("RGBA", (cell_w, cell_h), (0, 0, 0, 0))
        x = (cell_w - new_size[0]) // 2
        y = cell_h - new_size[1] - args.safe_pad_y
        frame.alpha_composite(resized, (x, y))
        frames.append(frame)
        metrics.append(
            {
                "frame": i + 1,
                "source_crop_box": list(crop_box),
                "bbox": list(bbox),
                "bbox_size": [bbox[2] - bbox[0], bbox[3] - bbox[1]],
                "fit_size": list(new_size),
                "scale": scale,
                "placed_xy": [x, y],
                "removed_components": removed,
            }
        )

    slot_w, slot_h = 220, 260
    cols = min(4, args.frames)
    rows = math.ceil(args.frames / cols)
    sheet = Image.new("RGB", (slot_w * cols, slot_h * rows), (246, 244, 250))
    draw = ImageDraw.Draw(sheet)
    try:
        font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 13)
    except Exception:
        font = ImageFont.load_default()

    for i, frame in enumerate(frames):
        col, row = i % cols, i // cols
        ox, oy = col * slot_w + 14, row * slot_h + 32
        draw.text((ox, oy - 24), f"frame {i + 1}", fill=(30, 30, 40), font=font)
        tile = 16
        for yy in range(oy, oy + cell_h, tile):
            for xx in range(ox, ox + cell_w, tile):
                color = (255, 255, 255) if ((xx // tile + yy // tile) % 2 == 0) else (232, 232, 238)
                draw.rectangle([xx, yy, min(xx + tile - 1, ox + cell_w - 1), min(yy + tile - 1, oy + cell_h - 1)], fill=color)
        draw.rectangle([ox, oy, ox + cell_w - 1, oy + cell_h - 1], outline=(80, 180, 120), width=2)
        draw.rectangle(
            [ox + args.safe_pad_x, oy + args.safe_pad_y, ox + cell_w - args.safe_pad_x - 1, oy + cell_h - args.safe_pad_y - 1],
            outline=(220, 190, 90),
            width=1,
        )
        sheet.paste(frame.convert("RGB"), (ox, oy), frame.getchannel("A"))
        draw.text((ox, oy + cell_h + 6), f"{metrics[i]['fit_size'][0]}x{metrics[i]['fit_size'][1]} s {metrics[i]['scale']:.3f}", fill=(80, 80, 95), font=font)

    strip = Image.new("RGBA", (cell_w * args.frames, cell_h), (0, 0, 0, 0))
    for i, frame in enumerate(frames):
        strip.alpha_composite(frame, (i * cell_w, 0))

    preview = outdir / f"{args.prefix}-cell-preview.png"
    outstrip = outdir / f"{args.prefix}-192x208-transparent.png"
    metrics_path = outdir / f"{args.prefix}-metrics.json"
    gif = outdir / f"{args.prefix}-preview.gif"
    sheet.save(preview)
    strip.save(outstrip)
    metrics_path.write_text(
        json.dumps(
            {
                "mode": args.mode,
                "source": str(args.src),
                "spacing_summary": spacing_summary,
                "component_diagnostics": component_diagnostics,
                "frames": metrics,
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    gif_frames = []
    for frame in frames:
        bg = Image.new("RGBA", (cell_w, cell_h), (246, 244, 250, 255))
        bg.alpha_composite(frame)
        gif_frames.append(bg.convert("P", palette=Image.Palette.ADAPTIVE))
    gif_frames[0].save(gif, save_all=True, append_images=gif_frames[1:], duration=100, loop=0, disposal=2)

    print(preview)
    print(outstrip)
    print(gif)
    print(metrics_path)
    if spacing_summary and spacing_summary["warnings"]:
        print("spacing warnings:")
        for warning in spacing_summary["warnings"]:
            print(f"- {warning}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
