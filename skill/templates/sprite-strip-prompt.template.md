# Sprite Strip Prompt Template

Use this after the corresponding state reference is approved. The output is an intermediate source strip, not the final packed spritesheet.

```text
Create an 8-frame horizontal sprite strip for a Codex desktop pet.

Pet identity must remain unchanged:
- Pet name: …
- Pet type or subject: …
- Visual style or material: …
- Must preserve: …
- Forbidden additions or changes: …
- Directional asymmetry: …

State:
- Codex state: …
- Action: …
- Motion notes: …

Frame and motion requirements:
- 8 frames in one horizontal row.
- The motion must loop smoothly from frame 8 back to frame 1.
- Keep scale, silhouette, proportions, palette, material, markings, and attached features stable across all frames.
- Keep the complete pet form and all important props visible in every frame.
- Use small, readable motion; avoid wide poses that cannot fit into 192x208.

Source strip spacing is mandatory:
- The 8 frames are intermediate source frames, not the final packed spritesheet.
- Leave at least 80px of pure #FF00FF empty background between every two neighboring poses.
- No part of the pet, attached feature, prop, or effect may enter the gutter area.
- If the pet or prop is too wide, shrink both uniformly; never reduce the gutter.
- Keep each frame as one isolated component on the chroma background, with no overlap between neighboring frames.
- The final Codex cells will be packed later by code; do not pack the source strip tightly.

Background:
- Solid #FF00FF chroma background.
- No shadows, no glow, no text, no labels, no scenery.
```
