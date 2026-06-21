from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image, ImageChops, ImageFilter


DEFAULT_STATES = {
    "running-right": 1,
    "running-left": 2,
}


def lower_contact_mask(alpha: Image.Image) -> Image.Image:
    width, height = alpha.size
    mask = Image.new("L", alpha.size, 0)
    crop_y = int(height * 0.58)
    bottom = alpha.crop((0, crop_y, width, height)).filter(ImageFilter.GaussianBlur(5))
    mask.paste(bottom, (0, crop_y))
    return mask


def offset_mask(mask: Image.Image, offset: tuple[int, int]) -> Image.Image:
    result = Image.new("L", mask.size, 0)
    result.paste(mask, offset)
    return result


def weighted_mask(mask: Image.Image, weight: float) -> Image.Image:
    return mask.point(lambda value: min(255, int(value * weight)))


def add_shadow_mask(
    combined: Image.Image,
    alpha: Image.Image,
    *,
    blur: float,
    weight: float,
    offset: tuple[int, int],
) -> Image.Image:
    layer = alpha.filter(ImageFilter.GaussianBlur(blur))
    layer = offset_mask(layer, offset)
    layer = weighted_mask(layer, weight)
    return ImageChops.add(combined, layer, scale=1.0, offset=0)


def build_shadow_mask(alpha: Image.Image) -> Image.Image:
    """Build a page-only shadow mask.

    The older Lanxi showcase GIFs look like the shadow is baked into the
    illustration. Darkening the background with a continuous mask avoids the
    hard "jelly edge" that GIFs can get from compositing colored blur layers.
    """

    shadow = Image.new("L", alpha.size, 0)
    contact = lower_contact_mask(alpha)
    for source, blur, weight, offset in (
        (alpha, 24, 0.10, (18, 20)),
        (alpha, 14, 0.16, (13, 16)),
        (alpha, 8, 0.16, (9, 11)),
        (contact, 20, 0.24, (9, 18)),
        (contact, 11, 0.38, (6, 13)),
        (contact, 5, 0.42, (4, 9)),
    ):
        shadow = add_shadow_mask(shadow, source, blur=blur, weight=weight, offset=offset)
    return shadow.filter(ImageFilter.GaussianBlur(0.6))


def darken_background(
    background: tuple[int, int, int, int],
    shadow_mask: Image.Image,
    size: tuple[int, int],
) -> Image.Image:
    bg = Image.new("RGBA", size, background)
    strength = shadow_mask.point(lambda value: min(130, int(value * 0.82)))
    dark = Image.new("RGBA", size, (31, 34, 45, 255))
    bg = Image.composite(dark, bg, strength)
    return bg


def render_state(
    sheet: Image.Image,
    *,
    row: int,
    cell_width: int,
    cell_height: int,
    frames: int,
    scale: int,
    background: tuple[int, int, int, int],
    duration_ms: int,
    output: Path,
) -> None:
    output_frames = []
    out_size = (cell_width * scale, cell_height * scale)

    for index in range(frames):
        frame = sheet.crop(
            (
                index * cell_width,
                row * cell_height,
                (index + 1) * cell_width,
                (row + 1) * cell_height,
            )
        ).convert("RGBA")
        frame = frame.resize(out_size, Image.Resampling.LANCZOS)
        alpha = frame.getchannel("A")

        canvas = darken_background(background, build_shadow_mask(alpha), out_size)
        canvas.alpha_composite(frame)
        output_frames.append(
            canvas.convert(
                "P",
                palette=Image.Palette.ADAPTIVE,
                dither=Image.Dither.FLOYDSTEINBERG,
            )
        )

    output.parent.mkdir(parents=True, exist_ok=True)
    output_frames[0].save(
        output,
        save_all=True,
        append_images=output_frames[1:],
        duration=duration_ms,
        loop=0,
        disposal=2,
    )


def render_transparent_webp_state(
    sheet: Image.Image,
    *,
    row: int,
    cell_width: int,
    cell_height: int,
    frames: int,
    scale: int,
    duration_ms: int,
    output: Path,
) -> None:
    output_frames = []
    out_size = (cell_width * scale, cell_height * scale)

    for index in range(frames):
        frame = sheet.crop(
            (
                index * cell_width,
                row * cell_height,
                (index + 1) * cell_width,
                (row + 1) * cell_height,
            )
        ).convert("RGBA")
        output_frames.append(frame.resize(out_size, Image.Resampling.LANCZOS))

    output.parent.mkdir(parents=True, exist_ok=True)
    output_frames[0].save(
        output,
        save_all=True,
        append_images=output_frames[1:],
        duration=duration_ms,
        loop=0,
        lossless=True,
        method=6,
    )


def parse_background(value: str) -> tuple[int, int, int, int]:
    raw = value.strip().lstrip("#")
    if len(raw) != 6:
        raise ValueError("--background must be a 6-digit hex color")
    return (int(raw[0:2], 16), int(raw[2:4], 16), int(raw[4:6], 16), 255)


def main() -> int:
    parser = argparse.ArgumentParser(description="Render page-only Lanxi showcase GIFs.")
    parser.add_argument("--spritesheet", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    parser.add_argument("--cell-width", type=int, default=192)
    parser.add_argument("--cell-height", type=int, default=208)
    parser.add_argument("--frames", type=int, default=8)
    parser.add_argument("--scale", type=int, default=2)
    parser.add_argument("--duration-ms", type=int, default=120)
    parser.add_argument("--background", default="#F6F9FE")
    args = parser.parse_args()

    sheet = Image.open(args.spritesheet).convert("RGBA")
    background = parse_background(args.background)

    for state, row in DEFAULT_STATES.items():
        render_state(
            sheet,
            row=row,
            cell_width=args.cell_width,
            cell_height=args.cell_height,
            frames=args.frames,
            scale=args.scale,
            background=background,
            duration_ms=args.duration_ms,
            output=args.output_dir / f"lanxi-{state}.gif",
        )
        render_transparent_webp_state(
            sheet,
            row=row,
            cell_width=args.cell_width,
            cell_height=args.cell_height,
            frames=args.frames,
            scale=args.scale,
            duration_ms=args.duration_ms,
            output=args.output_dir / f"lanxi-{state}.webp",
        )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
