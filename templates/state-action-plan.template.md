# Codex Pet State Action Plan

Use this template before generating state references or animation strips.

The goal is to make the hidden Codex pet state contract visible to the user early, then ask whether each state should keep the default action or use a custom action.

## Pet Identity

```text
Pet name:
One-sentence personality:
Visual style:
Important identity details:
Forbidden changes:
```

## State Contract

| Row | State | Default Meaning | Suggested Default Action | User Custom Action | Approved |
| --- | --- | --- | --- | --- | --- |
| 0 | `idle` | Default calm state | Subtle breathing, blink, tiny hair sway |  | no |
| 1 | `running-right` | Drag/move right | Compact right-facing run or energetic step |  | no |
| 2 | `running-left` | Drag/move left | Compact left-facing run or energetic step |  | no |
| 3 | `waving` | Greeting | Hand wave, no floating wave marks |  | no |
| 4 | `jumping` | Upbeat jump | Small hop or bounce, full body visible |  | no |
| 5 | `failed` | Task failed/error | Slightly disappointed but recoverable reaction |  | no |
| 6 | `waiting` | Waiting for user input/approval | Expectant pose, stretching, looking at user, or waiting beside a prop |  | no |
| 7 | `running` | Task is processing | Focused work/typing/thinking; not literal foot-running |  | no |
| 8 | `review` | Reviewing/checking result | Focused checking pose, head tilt, blink |  | no |

## User Confirmation Prompt

Before image generation, ask the user:

```text
Codex pets use these 9 animation states:

0 idle: default calm state
1 running-right: moving/dragging right
2 running-left: moving/dragging left
3 waving: greeting
4 jumping: upbeat jump
5 failed: task failed or needs recovery
6 waiting: waiting for your input or approval
7 running: task is processing, not literal running
8 review: checking or reviewing the result

I can propose default actions for each state, or you can customize any of them.
Do you want to keep the default action plan, or modify specific states?
```

## Approval Rules

Do not generate state images until the user has either:

- approved the default plan, or
- customized the states they care about and approved the revised plan.

If the user is unsure, propose 2-3 action options for each unclear state. Keep `waiting`, `running`, and `review` semantically distinct.

## Common Pitfalls

- Do not confuse `running` with `running-right` / `running-left`.
- Do not let `waiting` and `running` both become typing-at-laptop states.
- Do not add props to every state unless the user wants that.
- Do not design actions that require wide motion unless the character can still fit inside `192x208`.
- Do not use detached effects, shadows, text, labels, or symbols unless they are intentionally part of the pet and can be cleanly cut.

