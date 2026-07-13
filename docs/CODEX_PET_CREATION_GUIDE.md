# How To Make A Polished Codex Pet

This guide turns lessons from a real Codex pet production run into a reusable checklist. Private creative prompts and identifying design details from the finished case study are intentionally omitted.

## 1. Understand The Codex Pet Format

A Codex pet is not simply a GIF. It is usually packaged as:

- `pet.json`
- `spritesheet.webp`

The spritesheet is an atlas made of fixed-size animation cells. In our workflow, each cell is:

```text
192 x 208 px
```

The common full atlas layout has 9 rows of states:

```text
0 idle
1 running-right
2 running-left
3 waving
4 jumping
5 failed
6 waiting
7 running
8 review
```

Each row contains multiple frames for that state. The app reads the row and plays the frames as an animation.

## 2. Explain The State Contract Early

Most users do not know that a Codex pet has separate animation states. Do not hide this until the end.

Before generating state references or animation strips, show the user the state contract:

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

Then ask whether the user wants to keep default actions or customize specific states.

Use this template:

```text
templates/state-action-plan.template.md
```

Do not generate state images until the user has approved either the default state action plan or a customized one.

## 3. Start With The Pet, Not The Spritesheet

Do not begin by asking for a full spritesheet. First create or import and approve one canonical pet reference.

Choose the appropriate starting path:

1. **Text-only concept:** generate a base pet image before making state rows.
2. **Existing reference images:** select or combine them into one approved visual source of truth.
3. **Animal, object, plant, robot, mascot, or abstract subject:** describe silhouette, material, markings, attached features, palette, and motion without forcing humanoid anatomy.
4. **Existing strips or spritesheet:** preserve the accepted identity and repair only the failing rows or packaging steps.

Save the approved source as `canonical-reference.png`. Record:

- pet type or subject
- silhouette and proportions
- surface or material
- markings and attached features
- palette
- personality or overall feeling
- forbidden changes
- directional asymmetry and motion-specific rules

Approve the canonical reference only when it remains readable at `192x208`, shows the complete pet form, has no unintended text or effects, and contains every feature that must remain consistent.

The artwork can come from Codex image generation, another image tool, or user-supplied files. The Python scripts in this repository do not invent visual artwork; they process supplied strips deterministically. Save imported state references under a project-owned folder such as `20-states/`, and save source strips with the state name, for example `idle-source.png`.

If an image model cannot produce the exact number of separated poses, do not duplicate frames silently. Retry with a simpler motion, smaller pet scale, and wider gutters; test 4 or 6 frames to validate the idea, then generate a fresh 8-frame production row because the final atlas uses 8 columns.

## 4. Make The Character Sprite-Friendly

Pretty illustration detail does not automatically survive `192x208`.

Pet-safe means:

- large readable silhouette
- simple readable masses
- clear expression or focal feature
- limited tiny attached details
- no thin loose decorations
- no floating effects
- no shadows or soft glows
- complete pet form visible with padding

Wide silhouettes, trailing features, leaves, tails, antennae, cables, or props must remain compact enough to fit inside each frame.

Good rule:

```text
The character should occupy about 75-85% of the final cell height.
```

For motion-heavy rows, use smaller and more compact poses.

## 5. Define The Pet States Before Generating Rows

Do not let every state become a random cute pose. Define each state clearly.

Fill in the action plan with the user's own choices:

| State | Meaning | User action |
| --- | --- | --- |
| `idle` | default calm state | … |
| `running-right` | dragged/moving right | … |
| `running-left` | dragged/moving left | … |
| `waving` | greeting | … |
| `jumping` | upbeat response | … |
| `failed` | task failed | … |
| `waiting` | waiting for user | … |
| `running` | task processing | … |
| `review` | reviewing result | … |

Avoid semantic confusion:

- `running` is not literal foot-running. It means task processing.
- `running-right` and `running-left` are directional movement states. They can use any compact travel motion appropriate to the pet's form.
- `waiting` should not duplicate `running`; make their intentions visibly distinct.

## 6. Generate State References Before Animation Rows

State references are single images showing each pose concept. They help stabilize the design before generating multi-frame strips.

Recommended order:

1. `idle`
2. `running-right`
3. `running-left`
4. `waving`
5. `jumping`
6. `failed`
7. `waiting`
8. `running`
9. `review`

For each state reference, check:

- Does it still look like the same pet?
- Are signature markings and attached features preserved?
- Is the complete form readable at small size?
- Does the pose match the state?
- Does anything stick too far left or right?
- Are there extra props that will make the final sprite too wide?

## 7. Use Chroma Backgrounds For Sprite Rows

For generated row strips, use a solid chroma background. We used:

```text
#FF00FF
```

Prompt rules:

- one horizontal strip
- exact frame count
- wide empty chroma gutters between frames
- no labels
- no borders
- no guide marks
- no shadows
- no motion effects
- no floating symbols
- complete pet form visible in every frame

Why this matters:

The final pet needs transparent frames. A clean chroma background makes it possible to remove the background deterministically.

## 8. Keep Frames Far Apart

One major failure mode was frame bleed:

```text
The trailing feature from one frame appeared in the neighboring frame.
```

This happened because the generated strip placed poses too close together. When the strip was split into equal cells, part of one character entered the neighboring frame.

Avoid it by prompting for:

- very wide empty gutters
- smaller character scale
- compact silhouette and attached features
- no wide trailing details
- no pet parts or props near frame edges

Also verify with actual cutting, not only with the original image.

For future prompts, use the stricter reusable spacing rules in:

docs/SPRITE_STRIP_SPACING_RULES.md
```

Important generation rule:

```text
Leave at least 80px of pure #FF00FF empty background between every two neighboring poses.
If the character or prop is too wide, shrink the character and prop uniformly; never reduce the gutter.
```

## 9. Always Cut And Preview At 192x208

Do not approve a row by looking only at the generated strip. Always cut it into final cells and preview those cells.

Use:

```bash
python3 scripts/cut_strip_to_cells.py \
  --src <strip>.png \
  --prefix <output-prefix> \
  --frames 8 \
  --mode smart-components
```

This produces:

- `<prefix>-cell-preview.png`
- `<prefix>-192x208-transparent.png`
- `<prefix>-preview.gif`
- `<prefix>-metrics.json`

Review all of them.

For AI-generated horizontal strips, prefer:

```text
--mode smart-components
```

This mode detects each pet component's real bounding box across the full strip before cropping. It prevents equal-width cut lines from slicing off attached features when generated frames are not perfectly aligned.

Use `--mode equal-slots` only when the source strip was created from a strict grid and every frame is already guaranteed to stay inside its slot.

The current cutter also detects real spacing between neighboring components. If the source strip is too tight, it writes warnings into `<prefix>-metrics.json`:

```text
spacing_summary.min_gutter_px
spacing_summary.warnings
component_diagnostics[].effective_padding_px
```

By default, `smart-components` uses adaptive left/right padding. This means a requested `--component-padding 22` will automatically shrink near a tight neighboring frame instead of cutting in pet or prop fragments from the next frame.

For strict QA, add:

```text
--fail-min-gutter-px 24
```

This rejects fragile source strips whose detected frame gutters are below `24px`.

## 10. Remove Detached Neighbor Fragments

Even with good prompting, equal-width slicing can capture a small detached part from the neighboring frame.

The fix is not always to regenerate. If the stray piece is disconnected from the main character, remove it during post-processing.

The `cut_strip_to_cells.py` script does this:

1. Remove magenta background.
2. Detect connected components.
3. Keep the main pet component.
4. Keep small nearby components that belong to the pet.
5. Remove far-away detached fragments.

This prevents an attached or trailing feature from one frame appearing in the next frame.

## 11. Clean Magenta Edge Contamination

Another failure mode was magenta halo:

```text
The pet looked like it had a pink glow after chroma removal.
```

This happens because anti-aliased edge pixels blend the character with the magenta background.

Mitigation:

- use a hard, flat chroma background
- prompt for crisp edges and no glow
- remove pixels close to magenta
- decontaminate edge colors after resizing
- inspect on a checkerboard background

Do not approve a row only on a pink background. A halo can hide there.

## 12. Watch For Generated Structure Artifacts

AI-generated animation rows often create small but distracting structural errors: duplicated parts, merged shapes, detached fragments, changing markings, or props crossing through the pet. Describe the actual failure in a short repair prompt:

```text
Keep the approved silhouette and attached features unchanged.
Remove the detached or duplicated fragment at: …
Keep these shapes visually separate: …
Do not move this marking or prop: …
```

Repair prompts should identify only the visible defect and the approved feature that must remain stable; do not expose or copy another pet's private design specification.

## 13. Decide When To Use 4 Frames Vs 8 Frames

More frames are not always better.

4 frames:

- easier to generate cleanly
- easier to keep separated
- fewer anatomy errors
- often enough for a small desktop pet

8 frames:

- smoother motion
- more expressive
- higher risk of frame bleed
- more chances for anatomy drift

Recommended strategy:

1. Generate a 4-frame or 6-frame test.
2. Validate style, pose, anatomy, and cleanup.
3. Only then expand to 8 frames.
4. If an action keeps failing, simplify or change the motion instead of forcing it. Preserve the pet identity and state meaning.

## 14. Mirror Only When It Is Semantically Safe

Mirroring one directional row to make the other sounds tempting, but it can break identity.

Mirroring can flip markings, symbols, attached features, prop placement, or asymmetric silhouettes. If side-specific identity matters, generate both directions separately. If the pet is symmetric enough at pet size, mirroring may be acceptable only after visual inspection.

## 15. Keep A Clean Project Structure

Generated pet projects get messy fast. Separate current work from legacy experiments.

Recommended structure:

```text
Project/
  README.md
  docs/
  10-references/
  20-states/
  30-sprite-tests/
  40-final-package/
  80-legacy/
  90-debug/
```

Example project mapping:

- current references are in `10-references`
- state references are in `20-states`
- sprite tests are in `30-sprite-tests`
- old packages are in `80-legacy`
- debug crops are in `90-debug`

## 16. QA Checklist Before Final Packaging

Before building the final `spritesheet.webp`, check every row:

- same pet identity
- same focal features
- same material and palette
- same marking and attached-feature placement
- no cropped pet parts or props
- no frame bleed
- no detached fragments
- no magenta halo
- no white/black background residue
- no shadows or glows
- no text or guide marks
- correct state meaning
- stable size across frames
- stable baseline across frames
- readable at `192x208`

For animation rows, also check:

- directional movement reads correctly
- the motion loop feels stable and intentional
- no structural artifacts
- no speed lines or dust
- no props suddenly appearing or disappearing

## 17. Suggested End-To-End Workflow

Use this as the reusable process:

1. Write the pet concept or collect source references.
2. Generate a main reference.
3. Iterate until the pet is emotionally and visually right.
4. Simplify the design if the original is too detailed at pet size.
5. Save a canonical reference.
6. Write a pet identity spec.
7. Define the 9 Codex states.
8. Generate single-image references for each state.
9. Make a `192x208` fit preview for all state references.
10. Generate a 4-frame test for the hardest motion state.
11. Cut it into transparent cells.
12. Inspect the cell preview and GIF.
13. Expand to 8 frames only after the 4-frame test works.
14. Clean chroma background, edge contamination, and detached fragments.
15. Repeat for all animation rows.
16. Compose the final atlas.
17. Validate the atlas.
18. Build `pet.json` and `spritesheet.webp`.
19. Review final contact sheet and GIF previews.
20. Move old experiments to `80-legacy` or `90-debug`.

## 18. Reusable Production Lessons

The biggest reusable lessons:

- A beautiful source image is not enough; it must survive `192x208`.
- Wide or trailing features need strict padding rules.
- Frame strips must be tested by actual slicing.
- Do not trust the original generated strip alone.
- A row can look good on magenta but fail on transparency.
- Component cleanup is essential for generated strips.
- Prompting alone cannot fix every artifact; deterministic post-processing is part of the pipeline.
- Keep versioned outputs so good ideas are not lost.
- Write down pet identity rules as soon as the design is approved.

## 19. Finished Case Study

Lanxi is retained as the finished visual case study. Its public package includes:

- a validated 9-row `spritesheet.webp`
- `pet.json`
- curated row strips under `examples/lanxi/rows/`
- English and Chinese README files
- GitHub Pages showcase assets

The reusable guides intentionally omit Lanxi's private prompt, styling specification, and state-action brief. Remaining project work is polish and release preparation:

- observe the installed pet inside Codex
- adjust any state that feels off in real use
- keep only curated assets in the public release
- move experiments and debug files to ignored legacy/debug folders
