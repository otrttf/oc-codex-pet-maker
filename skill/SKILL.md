---
name: oc-codex-pet-maker
description: Use this skill to create, repair, QA, or package a Codex desktop pet from an animal idea, mascot, brand or product cue, existing artwork, avatar, reference image, text concept, or existing sprite assets.
---

# OC Codex Pet Maker

Use this skill when the user wants to create, repair, QA, or package a custom Codex desktop pet.

This skill is self-contained when installed from this repository's `skill/` folder. Resolve referenced `templates/`, `docs/`, and `scripts/` paths relative to this `SKILL.md` first.

## Mandatory Beginner Guidance

Assume the user may know only that they want a Codex pet. Do not require them to discover the workflow, copy a long prompt, understand sprite terminology, or prepare a reference image before the conversation starts.

Every response during creation must:

1. Say what was just completed or decided.
2. Explain the immediate next step in plain language.
3. Ask a concrete question or request a concrete approval.
4. Label optional information as optional and offer a sensible default or `skip` choice.

Never end a phase with only a status report such as “installed,” “ready,” or “send a reference image.” Never assume that the user has a reference image. Never make the user infer the next prompt from external documentation or promotional images.

### First-Run Intake

When the user asks to make a pet but has not provided enough information, first explain the three supported starting routes:

1. **Text only:** turn an ordinary-language idea into a canonical reference.
2. **Reference image:** use uploaded artwork or a photo while preserving user-selected details.
3. **Existing sprite assets:** inspect, repair, cut, QA, or package existing files.

Then guide the user one step at a time. Do not ask for every field in one large questionnaire.

Required to begin:

- **Starting route:** text only, reference image, or existing sprite assets.
- **Pet concept:** what the pet is; a short phrase is enough.

Conditionally required:

- **Source files:** only when the user chooses the reference-image or existing-sprite route.
- **Approval:** before image generation, before replacing files, and before installing a finished pet package.

Optional, with defaults allowed:

- Pet name; use a temporary working name if skipped and ask again before packaging.
- Visual style or material; propose a suitable default if skipped.
- Signature traits or details that must not change; strongly recommend these for reference-image users.
- Color palette, personality, directional asymmetry, and forbidden details.
- Preferred actions; propose defaults when skipped.

Start with a message equivalent to this in the user's language:

```text
可以从 3 种方式开始：
1. 只有文字想法
2. 上传参考图
3. 已有 sprite，需要检查或修复

开始只需要告诉我两件事：你选哪一种，以及你想做一个什么样的宠物。
宠物名称、视觉风格和动作偏好都可以暂时不填，我会一步一步问你。
```

If the user already supplied some fields, preserve them and ask only for the next missing required item. If the user supplies a complete brief, summarize it and move directly to state planning.

### Optional Full-Brief Shortcut

Offer this only as a convenience, not as a prerequisite:

```text
请使用 OC Codex Pet Maker Skill 帮我制作一个 Codex 宠物。
宠物设定（必填）：……
素材来源（必填）：纯文字 / 我会上传参考图 / 我已有 sprite
宠物名称（选填）：……
视觉风格或材质（选填）：……
必须保留的特征（选填；有参考图时建议填写）：……
动作偏好（选填）：……
请一步一步引导我；先说明 9 个状态并给出动作方案，等我确认后再生图。
```

### Guided Phase Handoffs

After each phase, explicitly lead into the next one:

1. **Intake complete:** summarize the route, concept, confirmed traits, and defaults; say that the next step is the 9-state action plan.
2. **State plan approved:** say that the next step is creating or importing one canonical reference and explain what the user will review.
3. **Canonical reference approved:** say that the next step is creating state references; work one state or a small reviewable batch at a time.
4. **State references approved:** say that the next step is generating or importing animation strips and checking spacing before cutting.
5. **Each strip processed:** show or link the cell preview, GIF, and metrics; state pass/fail and ask whether to keep, revise, or regenerate that row.
6. **All rows approved:** say that the next step is composing and structurally validating the package.
7. **Package validated:** distinguish structural validation from visual QA and Codex Desktop activation; explain the current safe installation/activation check and ask for approval before copying files.

Do not silently jump across an approval gate. Do not merely list the whole workflow and wait; actively ask the next question.

## Required Pre-Generation Step: State Action Planning

After the first-run intake is complete, explain the Codex pet state contract and ask whether the user wants to keep or customize the actions. Do not make state planning the first unexplained question when the user has not yet chosen a starting route or described a pet concept.

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
