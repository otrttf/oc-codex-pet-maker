# Sprite Strip Spacing Rules

These rules are used when generating Lanxi animation strips before cutting them into Codex pet cells.

## Why This Exists

The final Codex spritesheet uses adjacent `192x208` cells with no visible gutter. That is fine for the final atlas.

The generated source strip is different: it is an intermediate image. It should contain large pure-chroma gutters between poses so the cutter can isolate each frame without pulling in hair, desk edges, laptop corners, or shoe fragments from the neighboring frame.

## Prompt Block

Use this block in every future sprite-strip generation prompt:

```text
Source strip spacing is mandatory:
- The 8 frames are intermediate source frames, not the final packed spritesheet.
- Leave at least 80px of pure #FF00FF empty background between every two neighboring poses.
- No hair, desk, laptop, shoes, skirt, jacket, hands, accessories, or effects may enter the gutter area.
- If the character or prop is too wide, shrink the character and prop uniformly; never reduce the gutter.
- Keep each frame as one isolated component on the chroma background, with no overlap between neighboring frames.
- The final Codex cells will be packed later by code; do not pack the source strip tightly.
```

For rows with large props, such as `waiting` and `running`, add:

```text
The character plus desk plus laptop must still fit inside one isolated frame component. Make the desk compact and centered with the character. Preserve the 80px pure-magenta gutter on both sides of each frame.
```

## Cutter Defaults

Use `smart-components` for generated strips:

```bash
python3 cut_strip_to_cells.py \
  --src <strip>.png \
  --prefix <prefix> \
  --frames 8 \
  --mode smart-components \
  --key-color ff00ff \
  --key-tolerance 120 \
  --component-padding 22
```

The cutter now detects the real gutter between neighboring components and shrinks left/right padding automatically when the source strip is too tight. Metrics are written to:

```text
<prefix>-metrics.json
```

Look for:

```text
spacing_summary.min_gutter_px
spacing_summary.warnings
component_diagnostics[].effective_padding_px
```

## Quality Gate

Recommended acceptance rule:

```text
min_gutter_px >= 24
```

If `min_gutter_px` is below `24`, the adaptive cutter may still rescue the row, but the source strip should be considered fragile. For important final rows, regenerate with wider gutters unless the cut preview is visually perfect.

To force the cutter to reject tight source strips:

```bash
python3 cut_strip_to_cells.py \
  --src <strip>.png \
  --prefix <prefix> \
  --frames 8 \
  --mode smart-components \
  --key-color ff00ff \
  --key-tolerance 120 \
  --component-padding 22 \
  --fail-min-gutter-px 24
```

Use this strict mode when deciding whether a source strip is production-ready. Use the default adaptive mode when rescuing an otherwise good row.
