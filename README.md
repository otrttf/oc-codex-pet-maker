# Codex Pet Maker Skill

[English](README.md) | [中文](README.zh-CN.md)

Create a Codex desktop pet from an animal idea, mascot, brand or product cue, existing artwork, avatar, reference image, or text-only concept. The workflow covers state planning, sprite generation or import, cleanup, QA, and packaging.

This repository contains:

- a Codex Skill entrypoint: [`skill/SKILL.md`](skill/SKILL.md)
- reusable Python tools for cutting and packaging sprites
- bilingual production guides
- a complete Lanxi example pet package

## Showcase

See the Lanxi demo page:

[https://otrttf.github.io/oc-codex-pet-maker/](https://otrttf.github.io/oc-codex-pet-maker/)

The source page lives at [`docs/index.html`](docs/index.html).

![Lanxi animated pet states](docs/assets/lanxi-state-overview.png)

## Quick Start

The Python scripts require Pillow:

```bash
python3 -m pip install Pillow
```

### 1. Install The Skill

Copy the self-contained `skill/` folder into your Codex skills directory:

```bash
mkdir -p ~/.codex/skills/oc-codex-pet-maker
cp -R skill/* ~/.codex/skills/oc-codex-pet-maker/
```

The installed skill includes the entrypoint, required templates, sprite-strip rules, and Python scripts. This means a new Codex conversation can resolve the paths referenced by the Skill without depending on the original repository checkout.

Then start a new Codex conversation and say something like:

```text
Use the Codex Pet Maker skill to help me create a Codex pet.
Pet idea or source: …
Visual style or material: …
Signature traits to preserve: …
```

The Skill should first explain the 9 Codex pet states and help you create a state action plan before generating images.

Expected first-run flow:

1. Read the Skill entrypoint.
2. Explain the 9 Codex pet states.
3. Fill or customize the state action plan.
4. Wait for your approval before image generation.
5. Generate state strips, cut them, QA previews, compose the spritesheet, and validate the package.

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

When the Skill is installed, the same template is also available inside the installed Skill directory.

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
  --manifest /absolute/path/to/your-pet/rows-manifest.json \
  --out /absolute/path/to/your-pet/package/spritesheet.png \
  --webp-out /absolute/path/to/your-pet/package/spritesheet.webp
```

Validate the package:

```bash
python3 scripts/validate_pet_package.py \
  --package-dir /absolute/path/to/your-pet/package
```

Use this template when creating your package metadata:

[`templates/pet-json.template.json`](templates/pet-json.template.json)

## Why This Exists

Making a polished Codex pet is more fragile than making a nice illustration. The final pet needs to survive:

- small `192x208` cells
- 9 distinct app states
- transparent background cleanup
- wide silhouettes, attached features, and props
- row-by-row animation consistency
- `spritesheet.webp` packaging

One of the biggest lessons from building a real pet was that generated horizontal strips often place frames too close together. This project includes spacing rules and a `smart-components` cutter that detects subject boundaries, warns about tight gutters, and avoids cutting neighboring features or props into the wrong frame.

## How This Relates To Hatch Pet

This project grew from practical experience using the Codex Hatch Pet Skill. Hatch Pet provides a streamlined, agent-orchestrated path from an idea or references to a packaged pet. Codex Pet Maker is a companion toolkit for users who want to inspect, customize, learn from, or repair the intermediate process.

It focuses on problems that can appear during a real Hatch Pet workflow:

- confusing the 9 app states, especially directional movement and task-processing `running`
- identity, proportion, palette, material, or prop drift between generated rows
- frames placed too close together, causing neighboring features to bleed into the wrong cell
- chroma-key residue, transparent-pixel contamination, and colored edge halos
- unsafe mirroring when markings, attached features, or props are asymmetric
- correct atlas dimensions but weak motion, size popping, wrong direction, or unclear state meaning
- needing to inspect and repair one failed row without regenerating the entire pet

The repository keeps the planning templates, intermediate-file conventions, spacing rules, deterministic scripts, and QA guidance visible. It does not replace Hatch Pet, and Hatch Pet's capabilities may evolve with Codex.

## Guides

- English guide: [`docs/CODEX_PET_CREATION_GUIDE.md`](docs/CODEX_PET_CREATION_GUIDE.md)
- 中文指南：[`docs/CODEX_PET_CREATION_GUIDE.zh-CN.md`](docs/CODEX_PET_CREATION_GUIDE.zh-CN.md)
- Sprite strip spacing rules: [`docs/SPRITE_STRIP_SPACING_RULES.md`](docs/SPRITE_STRIP_SPACING_RULES.md)
- Installation notes: [`docs/INSTALLATION.md`](docs/INSTALLATION.md)
- Showcase GIF shadow notes: [`docs/SHOWCASE_GIF_SHADOW_NOTES.md`](docs/SHOWCASE_GIF_SHADOW_NOTES.md)
- GitHub publishing notes: [`docs/GITHUB_PUBLISHING_NOTES.zh-CN.md`](docs/GITHUB_PUBLISHING_NOTES.zh-CN.md)
- Roadmap: [`docs/ROADMAP.md`](docs/ROADMAP.md)

## Repository Structure

```text
oc-codex-pet-maker/
  skill/
    SKILL.md
    docs/
      SPRITE_STRIP_SPACING_RULES.md
    scripts/
      cut_strip_to_cells.py
      compose_spritesheet.py
      validate_pet_package.py
    templates/
      state-action-plan.template.md
      state-reference-prompt.template.md
      sprite-strip-prompt.template.md
      rows-manifest.template.json
      pet-json.template.json
  scripts/
    cut_strip_to_cells.py
    compose_spritesheet.py
    validate_pet_package.py
  templates/
    state-action-plan.template.md
    state-reference-prompt.template.md
    sprite-strip-prompt.template.md
    rows-manifest.template.json
    pet-json.template.json
  docs/
    CODEX_PET_CREATION_GUIDE.md
    CODEX_PET_CREATION_GUIDE.zh-CN.md
    GITHUB_PUBLISHING_NOTES.zh-CN.md
    INSTALLATION.md
    SPRITE_STRIP_SPACING_RULES.md
    SHOWCASE_GIF_SHADOW_NOTES.md
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

Lanxi is the finished case study used to develop and test this workflow. The public showcase keeps the final pet images and animation results, while the reusable instructions intentionally omit the private creative brief and prompts behind the design.

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

## License

MIT. See [`LICENSE`](LICENSE).
