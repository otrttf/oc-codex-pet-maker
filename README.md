# OC Codex Pet Maker Skill

Create a custom Codex desktop pet from your own OC/avatar concept, with a repeatable workflow for state planning, sprite generation, cleanup, QA, and packaging.

This repository contains:

- a Codex Skill entrypoint: [`skill/SKILL.md`](skill/SKILL.md)
- reusable Python tools for cutting and packaging sprites
- bilingual production guides
- a complete Lanxi example pet package

中文制作指南：[docs/CODEX_PET_CREATION_GUIDE.zh-CN.md](docs/CODEX_PET_CREATION_GUIDE.zh-CN.md)

## Quick Start

The Python scripts require Pillow:

```bash
python3 -m pip install Pillow
```

### 1. Install The Skill

Copy the skill folder into your Codex skills directory:

```bash
mkdir -p ~/.codex/skills/oc-codex-pet-maker
cp -R skill/* ~/.codex/skills/oc-codex-pet-maker/
```

Then start a new Codex conversation and say something like:

```text
Use the OC Codex Pet Maker skill to help me create a Codex pet for my OC.
```

The Skill should first explain the 9 Codex pet states and help you create a state action plan before generating images.

### 2. Create A State Action Plan

Codex pets use 9 animation states:

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

Use the planning template:

[`templates/state-action-plan.template.md`](templates/state-action-plan.template.md)

### 3. Generate And Cut Sprite Rows

After each horizontal sprite strip is generated, cut it into transparent `192x208` cells:

```bash
python3 scripts/cut_strip_to_cells.py \
  --src path/to/source-strip.png \
  --prefix output-prefix \
  --frames 8 \
  --mode smart-components \
  --key-color ff00ff \
  --key-tolerance 120 \
  --component-padding 22
```

Review the generated:

```text
<prefix>-cell-preview.png
<prefix>-preview.gif
<prefix>-metrics.json
```

### 4. Compose A Spritesheet

Create a manifest for the 9 approved rows, then compose the final atlas:

```bash
python3 scripts/compose_spritesheet.py \
  --manifest examples/lanxi/rows-manifest.json \
  --out 40-draft-package/spritesheet.png \
  --webp-out 40-draft-package/spritesheet.webp
```

Validate the package:

```bash
python3 scripts/validate_pet_package.py --package-dir 40-draft-package
```

## Why This Exists

Making a polished Codex pet is more fragile than making a nice illustration. The final pet needs to survive:

- small `192x208` cells
- 9 distinct app states
- transparent background cleanup
- long hair and wide motion
- row-by-row animation consistency
- `spritesheet.webp` packaging

One of the biggest lessons from Lanxi was that generated horizontal strips often place frames too close together. This project includes spacing rules and a `smart-components` cutter that detects real character boundaries, warns about tight gutters, and avoids cutting neighboring hair or props into the wrong frame.

## Guides

- English guide: [`docs/CODEX_PET_CREATION_GUIDE.md`](docs/CODEX_PET_CREATION_GUIDE.md)
- 中文指南：[`docs/CODEX_PET_CREATION_GUIDE.zh-CN.md`](docs/CODEX_PET_CREATION_GUIDE.zh-CN.md)
- Sprite strip spacing rules: [`docs/SPRITE_STRIP_SPACING_RULES.md`](docs/SPRITE_STRIP_SPACING_RULES.md)
- Roadmap: [`docs/ROADMAP.md`](docs/ROADMAP.md)

## Repository Structure

```text
oc-codex-pet-maker/
  skill/
    SKILL.md
  scripts/
    cut_strip_to_cells.py
    compose_spritesheet.py
    validate_pet_package.py
  templates/
    state-action-plan.template.md
  docs/
    CODEX_PET_CREATION_GUIDE.md
    CODEX_PET_CREATION_GUIDE.zh-CN.md
    SPRITE_STRIP_SPACING_RULES.md
    ROADMAP.md
  examples/
    lanxi/
      rows-manifest.json
      rows/
  10-references/
  20-states/
  40-draft-package/
```

## Lanxi Example

Lanxi is the example pet used to develop this workflow. She is a cute-cool chibi virtual avatar with long aqua hair, school-uniform street-dance styling, and a small laptop/standing-desk workflow for `waiting` and `running` states.

The example includes:

- canonical character references in [`10-references/`](10-references/)
- state references in [`20-states/`](20-states/)
- approved row strips in [`examples/lanxi/rows/`](examples/lanxi/rows/)
- a ready draft package in [`40-draft-package/`](40-draft-package/)

You can validate the Lanxi package with:

```bash
python3 scripts/validate_pet_package.py --package-dir 40-draft-package
```

## Current Limitations

- Slight magenta edge contamination can still appear after chroma removal. It is much better than the early versions, but further edge cleanup is a future improvement.
- The current Skill is a draft entrypoint. It documents the workflow and calls the local scripts, but it is not yet packaged as a one-command installer.
- Generated assets can make the repository large. Legacy experiments and debug files are intentionally ignored.
