# Codex Pet State Action Plan / Codex 宠物状态动作方案

Use this template before generating state references or animation strips.

在生成状态参考图或动画横条之前，先使用这份模板。

The goal is to make the hidden Codex pet state contract visible to the user early, then ask whether each state should keep the default action or use a custom action.

这份模板的目的，是在制作早期就让用户知道 Codex 宠物有哪些固定状态，然后确认每个状态是使用默认动作，还是根据用户的 OC / 虚拟形象进行自定义。

## Pet Identity

```text
Pet name:
宠物名字：

One-sentence personality:
一句话性格：

Visual style:
视觉风格：

Important identity details:
必须保留的形象特征：

Forbidden changes:
禁止改变的内容：
```

## State Contract / 状态契约

| Row 行 | State 状态 | Meaning 含义 | Suggested Default Action 默认动作建议 | User Custom Action 用户自定义动作 | Approved 是否确认 |
| --- | --- | --- | --- | --- | --- |
| 0 | `idle` | Default calm state / 默认待机 | Subtle breathing, blink, tiny hair sway / 轻微呼吸、眨眼、头发小幅摆动 |  | no |
| 1 | `running-right` | Drag/move right / 向右拖拽或移动 | Clear rightward movement, such as a small run, skateboard glide, hover, or dance step / 清晰向右移动，比如小跑、滑板、悬浮或舞步 |  | no |
| 2 | `running-left` | Drag/move left / 向左拖拽或移动 | Clear leftward movement, such as a small run, skateboard glide, hover, or dance step / 清晰向左移动，比如小跑、滑板、悬浮或舞步 |  | no |
| 3 | `waving` | Greeting / 打招呼 | Hand wave, no floating wave marks / 挥手，不加漂浮波纹或文字 |  | no |
| 4 | `jumping` | Upbeat jump / 跳跃或开心反馈 | Small hop or bounce, full body visible / 小幅跳跃，全身始终可见 |  | no |
| 5 | `failed` | Task failed/error / 任务失败或错误 | Slightly disappointed but recoverable reaction / 有点沮丧但仍有动力继续 |  | no |
| 6 | `waiting` | Waiting for user input/approval / 等待用户输入或确认 | Expectant pose, stretching, looking at user, or waiting beside a prop / 期待、伸懒腰、看向用户，或在道具旁等待 |  | no |
| 7 | `running` | Task is processing / 任务处理中 | Focused work/typing/thinking; not literal foot-running / 专注工作、打字或思考，不是字面意义的跑步 |  | no |
| 8 | `review` | Reviewing/checking result / 检查或审阅结果 | Focused checking pose, head tilt, blink / 专注检查、歪头、眨眼 |  | no |

## Filled Example / 填写示例

```text
Pet name / 宠物名字：
Lanxi

One-sentence personality / 一句话性格：
Cute, bright, and a little cool; sweet-looking but loves hip-hop energy.

一句话性格：
乖巧甜甜的外表，但有一点街舞感和酷酷的能量。

Visual style / 视觉风格：
Modern chibi sticker style, clean outline, readable at 192x208.

视觉风格：
现代简洁 Q 版贴纸风，缩小到 192x208 后仍然清楚。

Important identity details / 必须保留的形象特征：
Long aqua hair, silver eyes, silver J hair clip, H earring, white uniform outfit, sporty jacket, X charm, white socks, black shoes.

Forbidden changes / 禁止改变的内容：
Do not crop hair, do not add unrelated effects, do not make the character look too childish, do not remove key accessories.
```

## User Confirmation Prompt / 给用户的确认话术

Before image generation, ask the user:

生成图片前，先问用户：

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

中文版本：

```text
Codex 宠物通常有 9 个动画状态：

0 idle：默认待机
1 running-right：向右移动或拖拽
2 running-left：向左移动或拖拽
3 waving：打招呼
4 jumping：跳跃或开心反馈
5 failed：任务失败或需要恢复
6 waiting：等待你的输入或确认
7 running：任务处理中，不是字面意义的跑步
8 review：检查或审阅结果

我可以先为每个状态提供一套默认动作方案，也可以根据你的想法自定义某些状态。
你希望直接使用默认方案，还是修改其中几个状态？
```

## Approval Rules / 确认规则

Do not generate state images until the user has either:

- approved the default plan, or
- customized the states they care about and approved the revised plan.

If the user is unsure, propose 2-3 action options for each unclear state. Keep `waiting`, `running`, and `review` semantically distinct.

在用户确认默认方案或修改后的方案之前，不要开始生成状态图。

如果用户不确定，可以为不明确的状态提供 2-3 个动作选项。尤其要注意让 `waiting`、`running` 和 `review` 在语义和动作上保持区分。

## Common Pitfalls / 常见坑

- Do not confuse `running` with `running-right` / `running-left`.
- Do not let `waiting` and `running` both become typing-at-laptop states.
- Do not add props to every state unless the user wants that.
- Do not design actions that require wide motion unless the character can still fit inside `192x208`.
- Do not use detached effects, shadows, text, labels, or symbols unless they are intentionally part of the pet and can be cleanly cut.

中文提醒：

- 不要把 `running` 和 `running-right` / `running-left` 混在一起。
- 不要让 `waiting` 和 `running` 都变成“坐在电脑前打字”。
- 不要给每个状态都加道具，除非用户明确想要。
- 不要设计动作幅度过大的姿态，除非角色仍然能完整放进 `192x208`。
- 不要加漂浮特效、阴影、文字、标签或符号，除非它们是角色设计的一部分，并且能被干净抠图。
