# Codex Pet State Action Plan / Codex 宠物状态动作方案

Use this template before generating state references or animation strips.

在生成状态参考图或动画横条之前，先使用这份模板。

The goal is to make the hidden Codex pet state contract visible to the user early, then ask whether each state should keep the default action or use a custom action.

这份模板的目的，是在制作早期就让用户知道 Codex 宠物有哪些固定状态，然后确认每个状态是使用默认动作，还是根据用户自己的宠物创意进行自定义。

## Pet Identity

```text
Pet name / 宠物名称：……

Pet type or subject / 宠物类型或主体：……

Personality or overall feeling / 性格或整体感觉：……

Visual style or material / 视觉风格或材质：……

Primary palette / 主要颜色：……

One to three signature traits / 1–3 个标志性特征：……

Must stay consistent / 必须保持一致：……

Must not appear or change / 禁止出现或改变：……

Directional asymmetry / 左右不对称特征：……
```

## State Contract / 状态契约

| Row 行 | State 状态 | Meaning 含义 | Suggested Default Action 默认动作建议 | User Custom Action 用户自定义动作 | Approved 是否确认 |
| --- | --- | --- | --- | --- | --- |
| 0 | `idle` | Default calm state / 默认待机 | Subtle breathing, blink, surface sway, or quiet shape change / 轻微呼吸、眨眼、表面摆动或安静的形变 | …… | no |
| 1 | `running-right` | Drag/move right / 向右拖拽或移动 | Compact rightward travel appropriate to the pet's form / 符合宠物形态的紧凑向右移动 | …… | no |
| 2 | `running-left` | Drag/move left / 向左拖拽或移动 | Compact leftward travel appropriate to the pet's form / 符合宠物形态的紧凑向左移动 | …… | no |
| 3 | `waving` | Greeting / 打招呼 | A readable greeting gesture using the pet's available form / 使用宠物自身形态做清楚的问候动作 | …… | no |
| 4 | `jumping` | Upbeat jump / 跳跃或开心反馈 | Small hop, bounce, lift, or upbeat shape change; complete form visible / 小跳、弹起、上浮或开心形变，主体始终完整可见 | …… | no |
| 5 | `failed` | Task failed/error / 任务失败或错误 | Slightly disappointed but recoverable reaction / 有点沮丧但仍能恢复的反应 | …… | no |
| 6 | `waiting` | Waiting for user input/approval / 等待用户输入或确认 | Expectant, asking, or paused motion distinct from idle / 期待、询问或暂停动作，并与待机区分 | …… | no |
| 7 | `running` | Task is processing / 任务处理中 | Focused work, thinking, scanning, or active processing; not literal travel / 专注工作、思考、扫描或处理，不是字面移动 | …… | no |
| 8 | `review` | Reviewing/checking result / 检查或审阅结果 | Deliberate checking motion distinct from waiting and processing / 明确的检查动作，并与等待和处理中区分 | …… | no |

## Fill-In Example / 填写句式

Replace every `……` with the user's own information. Do not copy another pet's private design.

请把每个 `……` 替换成用户自己的信息，不要套用其他宠物的私人设定。

```text
Pet name / 宠物名称：……
Pet type or subject / 宠物类型或主体：……
Personality or overall feeling / 性格或整体感觉：……
Visual style or material / 视觉风格或材质：……
Primary palette / 主要颜色：……
Signature traits / 标志性特征：……
Must stay consistent / 必须保持一致：……
Must not appear or change / 禁止出现或改变：……
Directional asymmetry / 左右不对称特征：……
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
- Do not let `waiting` and `running` become the same motion.
- Do not add props to every state unless the user wants that.
- Do not design actions that require wide motion unless the character can still fit inside `192x208`.
- Do not use detached effects, shadows, text, labels, or symbols unless they are intentionally part of the pet and can be cleanly cut.

中文提醒：

- 不要把 `running` 和 `running-right` / `running-left` 混在一起。
- 不要让 `waiting` 和 `running` 变成同一个动作。
- 不要给每个状态都加道具，除非用户明确想要。
- 不要设计动作幅度过大的姿态，除非角色仍然能完整放进 `192x208`。
- 不要加漂浮特效、阴影、文字、标签或符号，除非它们是角色设计的一部分，并且能被干净抠图。
