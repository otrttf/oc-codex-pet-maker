# How To Make A Polished Codex Pet

This guide summarizes the workflow and lessons learned while creating Lanxi, a custom Codex desktop pet. It is written as a reusable production checklist, not only as project notes.

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

## 3. Start With The Character, Not The Spritesheet

Do not begin by asking for a full spritesheet. First create and approve a single canonical character.

For Lanxi, the early versions looked nice as illustrations but were too detailed for a small desktop pet. The better path was:

1. Create the main avatar concept.
2. Simplify it into a Q-version / chibi version.
3. Lock a canonical reference.
4. Write a character spec.
5. Use that spec for every later state and row.

The character spec should include:

- fixed hair color and shape
- eyes
- signature accessories
- outfit
- shoes and socks
- palette
- body proportion
- personality
- forbidden changes
- motion-specific rules

For Lanxi, the spec also includes a special rule: running and jumping states must include white safety shorts / bloomers under the skirt.

## 4. Make The Character Sprite-Friendly

Pretty illustration detail does not automatically survive `192x208`.

Sprite-friendly means:

- large readable silhouette
- simple hair shapes
- clear face
- limited tiny accessories
- no thin loose decorations
- no floating effects
- no shadows or soft glows
- full body visible with padding

For long-haired characters, hair is the biggest risk. Long hair must be visually beautiful but physically compact enough to fit inside each frame.

Good rule:

```text
The character should occupy about 75-85% of the final cell height.
```

For motion-heavy rows like running and jumping, use smaller and more compact poses.

## 5. Define The Pet States Before Generating Rows

Do not let every state become a random cute pose. Define each state clearly.

Example Lanxi state plan:

| State | Meaning | Lanxi Direction |
| --- | --- | --- |
| `idle` | default calm state | relaxed standing, tiny breathing/blink |
| `running-right` | dragged/moving right | rightward skateboard glide |
| `running-left` | dragged/moving left | leftward skateboard glide |
| `waving` | greeting | hand wave, no wave marks |
| `jumping` | small energetic hop | light hip-hop bounce |
| `failed` | task failed | disappointed but motivated |
| `waiting` | waiting for user | stretch beside high standing desk |
| `running` | task processing | typing at high standing desk |
| `review` | reviewing result | focused checking pose |

Avoid semantic confusion:

- `running` is not literal foot-running. It means task processing.
- `running-right` and `running-left` are directional movement states. They do not have to be literal running; a skateboard glide, hover, tiny dance step, or other clear directional action can work better for complex characters.
- `waiting` should not duplicate `running`; make it a rest, stretch, or expectant pose.

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

- Does it still look like the same character?
- Are signature accessories preserved?
- Is the body readable at small size?
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
- full body visible in every frame

Why this matters:

The final pet needs transparent frames. A clean chroma background makes it possible to remove the background deterministically.

## 8. Keep Frames Far Apart

One major failure mode was frame bleed:

```text
The right side of one frame's hair appeared in the left side of the next frame.
```

This happened because the generated strip placed poses too close together. When the strip was split into equal cells, part of one character entered the neighboring frame.

Avoid it by prompting for:

- very wide empty gutters
- smaller character scale
- compact hair
- no wide flying hair
- no clothing or hair near frame edges

Also verify with actual cutting, not only with the original image.

For future prompts, use the stricter reusable spacing rules in:

```text
docs/SPRITE_STRIP_SPACING_RULES.md
```

Important generation rule:

```text
Leave at least 80px of pure #FF00FF empty background between every two neighboring poses.
If the character or prop is too wide, shrink the character and prop uniformly; never reduce the gutter.
```

## 9. Always Cut And Preview At 192x208

Do not approve a row by looking only at the generated strip. Always cut it into final cells and preview those cells.

For Lanxi, we use:

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

This mode detects each character's real bounding box across the full strip before cropping. It prevents equal-width cut lines from slicing off hair or clothing when the generated frames are not perfectly aligned.

Use `--mode equal-slots` only when the source strip was created from a strict grid and every frame is already guaranteed to stay inside its slot.

The current cutter also detects real spacing between neighboring components. If the source strip is too tight, it writes warnings into `<prefix>-metrics.json`:

```text
spacing_summary.min_gutter_px
spacing_summary.warnings
component_diagnostics[].effective_padding_px
```

By default, `smart-components` uses adaptive left/right padding. This means a requested `--component-padding 22` will automatically shrink near a tight neighboring frame instead of cutting in hair or prop fragments from the next frame.

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
3. Keep the main character component.
4. Keep small nearby components that belong to the character.
5. Remove far-away detached fragments.

This prevents a strand of hair from one frame appearing in the next frame.

## 11. Clean Magenta Edge Contamination

Another failure mode was magenta halo:

```text
The character looked like it had a pink glow after chroma removal.
```

This happens because anti-aliased edge pixels blend the character with the magenta background.

Mitigation:

- use a hard, flat chroma background
- prompt for crisp edges and no glow
- remove pixels close to magenta
- decontaminate edge colors after resizing
- inspect on a checkerboard background

Do not approve a row only on a pink background. A halo can hide there.

## 12. Watch For Anatomy Artifacts

AI-generated animation rows often create tiny but distracting anatomy errors.

Lanxi-specific examples:

- a small round flesh-colored bump beside the front leg
- upper thigh crossing that looked like a fork
- the silver `X` charm falling between the legs
- skirt and leg shapes merging during running

Prompt against these explicitly:

```text
No small round protrusion beside the front leg.
No stray thigh blob.
No X-shaped crossing between the legs.
The X waist charm must not fall between the thighs.
The skirt hem, safety shorts, socks, and legs must be visually separate.
```

For skirted characters, add safety shorts / bloomers for running and jumping states. This is both a design choice and a practical animation-safety rule.

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

For Lanxi, literal running caused repeated anatomy drift, accessory drift, and skirt/leg ambiguity. The final directional movement uses an 8-frame skateboard glide instead, with very stable lower-body motion.

Recommended strategy:

1. Generate a 4-frame or 6-frame test.
2. Validate style, pose, anatomy, and cleanup.
3. Only then expand to 8 frames.
4. If literal running keeps failing, change the action design instead of forcing it. A skateboard, hover, or compact glide can preserve the character better.

## 14. Mirror Only When It Is Semantically Safe

Mirroring one directional row to make the other sounds tempting, but it can break identity.

For Lanxi, mirroring can flip:

- `J` hair clip side
- `H` earring side
- accessory placement
- hairstyle asymmetry

If side-specific identity matters, generate both directions separately. If the character is symmetric enough at pet size, mirroring may be acceptable after visual inspection. Lanxi's final skateboard row accepts mirroring because the motion quality mattered more than tiny side-specific accessory placement in the directional drag state.

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

For Lanxi:

- current references are in `10-references`
- state references are in `20-states`
- sprite tests are in `30-sprite-tests`
- old packages are in `80-legacy`
- debug crops are in `90-debug`

## 16. QA Checklist Before Final Packaging

Before building the final `spritesheet.webp`, check every row:

- same character identity
- same face
- same outfit
- same accessory placement
- no cropped hair or shoes
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
- no anatomy artifacts
- no speed lines or dust
- no props suddenly appearing or disappearing

## 17. Suggested End-To-End Workflow

Use this as the reusable process:

1. Write the character concept.
2. Generate a main reference.
3. Iterate until the character is emotionally and visually right.
4. Simplify into a Q-version if the original is too detailed.
5. Save a canonical reference.
6. Write a character spec.
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

## 18. Current Lanxi Lessons

The biggest lessons from Lanxi:

- A beautiful character image is not enough; it must survive `192x208`.
- Long hair needs strict padding rules.
- Frame strips must be tested by actual slicing.
- Do not trust the original generated strip alone.
- A row can look good on magenta but fail on transparency.
- Component cleanup is essential for generated strips.
- Prompting alone cannot fix every artifact; deterministic post-processing is part of the pipeline.
- Keep versioned outputs so good ideas are not lost.
- Write down character rules as soon as the design is approved.

## 19. Lanxi Current Status

Lanxi now has a complete draft package:

- a validated 9-row `spritesheet.webp`
- `pet.json`
- curated row strips under `examples/lanxi/rows/`
- English and Chinese README files
- GitHub Pages showcase assets

Remaining work is polish and release preparation:

- observe the installed pet inside Codex
- adjust any state that feels off in real use
- keep only curated assets in the public release
- move experiments and debug files to ignored legacy/debug folders
