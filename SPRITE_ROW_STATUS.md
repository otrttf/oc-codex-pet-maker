# Lanxi Sprite Row Status

This file tracks the current best candidate for each Codex pet row.

## Row Contract

| Row | State | Status |
| --- | --- | --- |
| 0 | `idle` | candidate exists |
| 1 | `running-right` | smart-magenta candidate exists |
| 2 | `running-left` | smart-magenta candidate exists |
| 3 | `waving` | candidate exists, motion may need improvement |
| 4 | `jumping` | smart-magenta candidate exists |
| 5 | `failed` | candidate exists |
| 6 | `waiting` | smart-magenta candidate exists |
| 7 | `running` | smart-magenta candidate exists |
| 8 | `review` | smart-magenta candidate exists |

## Current Best Candidates

| State | Candidate transparent strip |
| --- | --- |
| `idle` | `30-sprite-tests/lanxi-q-sprite-tests/idle-8frame-v2-isolated-component-clean-192x208-transparent.png` |
| `running-right` | `30-sprite-tests/lanxi-q-sprite-tests/running-right-8frame-v3-smart-magenta-192x208-transparent.png` |
| `running-left` | `30-sprite-tests/lanxi-q-sprite-tests/running-left-8frame-v1-smart-magenta-192x208-transparent.png` |
| `waving` | `30-sprite-tests/lanxi-q-sprite-tests/waving-8frame-v1-component-clean-192x208-transparent.png` |
| `jumping` | `30-sprite-tests/lanxi-q-sprite-tests/jumping-8frame-v1-smart-magenta-192x208-transparent.png` |
| `failed` | `30-sprite-tests/lanxi-q-sprite-tests/failed-8frame-v2-isolated-component-clean-192x208-transparent.png` |
| `waiting` | `30-sprite-tests/lanxi-q-sprite-tests/waiting-8frame-v1-smart-magenta-adaptive-test-192x208-transparent.png` |
| `running` | `30-sprite-tests/lanxi-q-sprite-tests/running-8frame-v1-smart-magenta-192x208-transparent.png` |
| `review` | `30-sprite-tests/lanxi-q-sprite-tests/review-8frame-v1-smart-magenta-192x208-transparent.png` |

## Notes

- Use `smart-components` for AI-generated motion rows, especially `running-right`, `running-left`, and `jumping`.
- Use magenta chroma key for future generated strips unless there is a strong reason to change it.
- `waving` v1 is technically clean, but the hand motion is subtle. It can be kept as a candidate or regenerated later.
- `review` v1 is technically clean and uses a focused hand-to-chin checking pose with a subtle blink.
- `waiting` v1 source frames are very close together. The adaptive smart cut keeps the row clean while warning that the source strip gutters are too tight for strict QA.
- `running` v1 is visually clean after adaptive smart cutting. The source strip gutters are still tighter than the 80px prompt target, with `min_gutter_px=10`, so strict QA would prefer a wider regenerated source if needed.

## Suggested Next Step

Review the new `running` row preview, then decide whether to keep it or regenerate with wider source gutters.
