# Lanxi Codex Pet

Lanxi is a work-in-progress custom Codex desktop pet. The goal is to create a polished chibi anime avatar with stable Codex pet animations, clean transparent sprites, and a repeatable production workflow.

中文制作指南：[docs/CODEX_PET_CREATION_GUIDE.zh-CN.md](docs/CODEX_PET_CREATION_GUIDE.zh-CN.md)

This project is not fully finished yet. The current focus is validating the character design, state references, sprite row generation, chroma-key cleanup, and `192x208` frame safety before assembling the final Codex `spritesheet.webp`.

## Current Direction

Lanxi is a cute but cool Q-version virtual avatar:

- light aqua-blue long hair
- silver-gray eyes
- silver `J` hair clip
- silver `H` earring
- white school-uniform outfit
- white, black, and pale-pink sporty street-dance jacket
- white pleated skirt
- silver waist chain with a small `X` charm
- white over-the-knee socks
- black academy-style shoes
- white safety shorts / bloomers under the skirt for running and jumping states

The canonical character rules live in:

[10-references/lanxi-q-reference/LANXI_CHARACTER_SPEC.md](10-references/lanxi-q-reference/LANXI_CHARACTER_SPEC.md)

## Project Structure

```text
Lanxi/
  README.md
  docs/
    CODEX_PET_CREATION_GUIDE.md
    SPRITE_STRIP_SPACING_RULES.md
  templates/
    state-action-plan.template.md
  skill/
    SKILL.md
  scripts/
    cut_strip_to_cells.py
    compose_spritesheet.py
    validate_pet_package.py
  examples/
    lanxi/
  10-references/
    lanxi-q-reference/
    lanxi-approved/
  20-states/
    lanxi-q-states/
  30-sprite-tests/
    lanxi-q-sprite-tests/
  80-legacy/
  90-debug/
```

## Important Folders

- `10-references/lanxi-q-reference/`
  - Current Q-version canonical reference and character spec.
- `20-states/lanxi-q-states/`
  - Current state reference images, including idle, waiting, running, failed, review, waving, jumping, running-left, and running-right.
- `30-sprite-tests/lanxi-q-sprite-tests/`
  - Sprite row experiments and cleanup scripts.
  - Includes `cut_strip_to_cells.py`, a reusable helper for cutting chroma-key sprite strips into `192x208` transparent cells.
- `templates/`
  - Reusable planning templates for future Codex pet projects.
- `skill/`
  - Draft Codex skill entrypoint that tells Codex how to use this workflow.
- `scripts/`
  - Reusable Python tools for cutting strips, composing spritesheets, and validating pet packages.
- `examples/`
  - Example manifests and project inputs. `examples/lanxi/rows-manifest.json` points to the current Lanxi row candidates.
- `80-legacy/`
  - Older pet packages and earlier run artifacts.
- `90-debug/`
  - Debug crops and inspection outputs from previous hair-clipping and WebP issues.

## Current Best Running-Right Candidate

The current preferred right-running row is:

- Source strip: `30-sprite-tests/lanxi-q-sprite-tests/running-right-8frame-strip-v3-first-style-legfix-shorts.png`
- Clean `192x208` strip: `30-sprite-tests/lanxi-q-sprite-tests/running-right-8frame-192x208-transparent-v3-first-style-legfix-shorts-component-clean.png`
- Preview GIF: `30-sprite-tests/lanxi-q-sprite-tests/running-right-8frame-preview-v3-first-style-legfix-shorts-component-clean.gif`

This candidate keeps the more expressive first-style look while fixing leg artifacts, adding safety shorts, removing stray neighboring-frame fragments, and reducing magenta edge contamination.

## Workflow Summary

The repeatable workflow is documented here:

- English: [docs/CODEX_PET_CREATION_GUIDE.md](docs/CODEX_PET_CREATION_GUIDE.md)
- 中文：[docs/CODEX_PET_CREATION_GUIDE.zh-CN.md](docs/CODEX_PET_CREATION_GUIDE.zh-CN.md)

Sprite strip spacing rules live here:

[docs/SPRITE_STRIP_SPACING_RULES.md](docs/SPRITE_STRIP_SPACING_RULES.md)

State action planning template:

[templates/state-action-plan.template.md](templates/state-action-plan.template.md)

At a high level:

1. Explain the Codex pet state contract to the user.
2. Fill and approve a state action plan.
3. Design and approve one canonical character reference.
4. Simplify the character for `192x208` readability.
5. Generate state references first, then sprite strips.
6. Use chroma-key backgrounds and wide frame spacing.
7. Cut generated strips into transparent `192x208` cells.
8. Remove neighboring-frame fragments and magenta edge residue.
9. Build and QA the final `spritesheet.webp`.

## Reusable Scripts

Cut a generated horizontal strip into transparent `192x208` cells:

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

Compose approved row strips into a Codex spritesheet:

```bash
python3 scripts/compose_spritesheet.py \
  --manifest examples/lanxi/rows-manifest.json \
  --out 40-draft-package/spritesheet.png \
  --webp-out 40-draft-package/spritesheet.webp
```

Validate a pet package:

```bash
python3 scripts/validate_pet_package.py --package-dir 40-draft-package
```

The draft Skill entrypoint is:

[skill/SKILL.md](skill/SKILL.md)

## Current Status

- Canonical Q-version character: done.
- State reference images: mostly done.
- Running-right 8-frame row: candidate available.
- Running-left 8-frame row: generated and awaiting final visual review.
- Full Codex spritesheet: not yet finalized.
- Final package: not yet ready.

## Notes For GitHub

Generated image assets may be large. Before publishing, decide whether to keep all experiments or only keep:

- canonical references
- final state references
- final sprite rows
- cleanup scripts
- final package
- selected QA previews

Older experiments can be moved to releases, Git LFS, or left out of the repository if size becomes a problem.
