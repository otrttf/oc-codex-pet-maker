# Showcase GIF Shadow Notes

These notes document the visual shadow style used by Lanxi's GitHub Pages showcase GIFs.

## Scope

This is only for public showcase GIFs under `docs/assets/`.

Do not add these shadows to the actual Codex pet package. The real `spritesheet.webp` should stay clean and transparent.

## What We Observed

Most early showcase GIFs, such as `lanxi-idle.gif` and `lanxi-waving.gif`, already contain a soft sticker-like shadow baked into the rendered frame. The effect is not produced by page CSS.

The later `lanxi-running-right.gif` and `lanxi-running-left.gif` were regenerated from the transparent `spritesheet.webp`, so they initially looked flatter:

- no baked contact shadow
- no dense shadow core near the character edge
- weaker outer gradient
- smaller source size before display scaling

The older showcase GIFs are `384 x 416`, while the first regenerated running GIFs were `192 x 208`. For page display, running previews should also be exported as `384 x 416`.

## Visual Target

The preferred Lanxi showcase shadow has:

- a light page background close to `#F6F9FE`
- a darker core very close to the character and feet
- a broader soft blur that fades outward
- slight down-right offset
- no hard floor oval
- no detached effect marks
- no shadow in the actual transparent pet spritesheet

The shadow should read like a soft sticker/illustration depth cue, not like a realistic cast shadow.

## Reproduction Recipe

When regenerating page showcase animations from transparent pet frames:

1. Load each transparent `192 x 208` frame from `spritesheet.webp`.
2. Scale to `384 x 416` with high-quality resampling.
3. Composite onto a solid `#F6F9FE` background.
4. Build the shadow from the alpha mask using multiple layers:

   - **Near-edge core:** alpha blur radius `2-4`, dark blue/black, opacity around `35-45%`, offset roughly `(3, 5)`.
   - **Outer haze:** alpha blur radius `8-14`, dark blue/black, opacity around `14-24%`, offset roughly `(6, 8)`.
   - **Optional contact emphasis:** stronger local shadow near the lowest contact area if the pet looks detached.

5. Composite shadow layers before the character frame.
6. Save as animated GIF with the same timing as the source preview.

Avoid using only one low-opacity blur layer. It tends to look too flat compared with the older Lanxi showcase assets.

For the running previews, the page now prefers transparent animated WebP plus CSS
`drop-shadow()` over baking the shadow into GIF pixels. This avoids GIF palette
banding and the visible "jelly edge" between shadow and background.

The current repository includes a helper script for the page-only running previews:

```bash
python3 scripts/render_showcase_gifs.py \
  --spritesheet 40-draft-package/spritesheet.webp \
  --output-dir docs/assets
```

This script intentionally writes only:

- `docs/assets/lanxi-running-right.gif`
- `docs/assets/lanxi-running-left.gif`
- `docs/assets/lanxi-running-right.webp`
- `docs/assets/lanxi-running-left.webp`

## Current Caveat

The regenerated `running-right` and `running-left` showcase GIFs use the scripted multi-layer shadow above for fallback. The GitHub Pages showcase uses the transparent WebP versions with CSS `drop-shadow()` for smoother blending. If visual consistency needs more tuning, adjust the script or CSS rather than editing the actual pet package.
