---
name: oc-codex-pet-maker
description: Use this skill to create, repair, QA, or package a Codex desktop pet from an animal idea, mascot, brand or product cue, existing artwork, avatar, reference image, text concept, or existing sprite assets.
---

# Codex Pet Maker

Use this skill when the user wants to create, repair, QA, or package a custom Codex desktop pet.

This skill is self-contained when installed from this repository's `skill/` folder. Resolve referenced `templates/`, `docs/`, and `scripts/` paths relative to this `SKILL.md` first.

## Required First Step: State Action Planning

Before generating state references or sprite strips, explain the Codex pet state contract to the user and ask whether they want to keep or customize the actions.

Use the project template:

```text
templates/state-action-plan.template.md
```

The states are:

| Row | State | Meaning |
| --- | --- | --- |
| 0 | `idle` | default calm state |
| 1 | `running-right` | dragged/moving right |
| 2 | `running-left` | dragged/moving left |
| 3 | `waving` | greeting |
| 4 | `jumping` | upbeat jump |
| 5 | `failed` | task failed or recoverable error |
| 6 | `waiting` | waiting for user input or approval |
| 7 | `running` | task is processing, not literal foot-running |
| 8 | `review` | reviewing/checking result |

Do not proceed to image generation until the user approves the default state action plan or a customized plan.

## Workflow

1. Identify the starting point: text concept, reference images, non-character subject, or existing sprite assets that need repair.
2. Explain and approve the state action plan.
3. Generate or import a canonical pet reference and confirm its silhouette, surface/material, palette, markings, attached features, and proportions.
4. Generate state references with the prompt template.
5. Generate chroma-key horizontal sprite strips with the prompt template and spacing rules.
6. Cut strips into `192x208` transparent cells with the bundled cutter.
7. QA cell previews, animated GIFs, spacing metrics, and edge cleanup.
8. Compose a `1536x1872` spritesheet for 8 columns x 9 rows.
9. Create `pet.json` from the template and install to the Codex pet directory only with user approval.

## Sprite Strip Rules

Read this reference before prompting for horizontal strips:

```text
docs/SPRITE_STRIP_SPACING_RULES.md
```

Key rule: source strips are intermediate images. They need wide pure-chroma gutters between frame components. The final packed spritesheet is created later by code.

Useful templates:

```text
templates/state-reference-prompt.template.md
templates/sprite-strip-prompt.template.md
```

## Cutter

Use:

```bash
python3 scripts/cut_strip_to_cells.py \
  --src <strip>.png \
  --prefix <prefix> \
  --frames 8 \
  --mode smart-components \
  --key-color ff00ff \
  --key-tolerance 120 \
  --component-padding 22
```

Review:

```text
<prefix>-cell-preview.png
<prefix>-preview.gif
<prefix>-metrics.json
```

If `spacing_summary.warnings` exists, inspect the preview carefully. Use strict QA with `--fail-min-gutter-px 24` when deciding whether a source strip is production-ready.

## Compose And Validate

After all 9 row strips are approved, create a manifest from:

```text
templates/rows-manifest.template.json
```

It should look like:

```json
{
  "rows": [
    {"state": "idle", "strip": "path/to/idle-192x208-transparent.png"},
    {"state": "running-right", "strip": "path/to/running-right-192x208-transparent.png"},
    {"state": "running-left", "strip": "path/to/running-left-192x208-transparent.png"},
    {"state": "waving", "strip": "path/to/waving-192x208-transparent.png"},
    {"state": "jumping", "strip": "path/to/jumping-192x208-transparent.png"},
    {"state": "failed", "strip": "path/to/failed-192x208-transparent.png"},
    {"state": "waiting", "strip": "path/to/waiting-192x208-transparent.png"},
    {"state": "running", "strip": "path/to/running-192x208-transparent.png"},
    {"state": "review", "strip": "path/to/review-192x208-transparent.png"}
  ]
}
```

Then run:

```bash
python3 scripts/compose_spritesheet.py \
  --manifest <rows-manifest.json> \
  --out <package-dir>/spritesheet.png \
  --webp-out <package-dir>/spritesheet.webp
```

Create `<package-dir>/pet.json` from:

```text
templates/pet-json.template.json
```

Keep `spritesheetPath` pointing to the generated `spritesheet.webp`, then validate:

```bash
python3 scripts/validate_pet_package.py --package-dir <package-dir>
```

For pet package installation guidance, read:

```text
docs/INSTALLATION.md
```

## Important Distinctions

- `running` means task processing, not literal movement.
- `running-right` and `running-left` are directional movement states. They do not have to be literal running; use any compact directional motion appropriate to the pet's anatomy or form.
- `waiting`, `running`, and `review` should have distinct actions.
- Avoid detached effects, shadows, glows, text, labels, UI, and symbols unless intentionally part of the pet and cleanly cuttable.
- Do not assume the pet is humanoid. Describe silhouette, material, markings, attached features, motion, and expression in ways that also work for animals, slimes, robots, plants, objects, and abstract icons.
