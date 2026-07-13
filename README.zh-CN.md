# Codex Pet Maker Skill

[English](README.md) | [中文](README.zh-CN.md)

把动物创意、吉祥物、品牌或产品灵感、已有作品、头像、参考图片或纯文字概念，制作成可以在 Codex 桌面端使用的小宠物。这个项目整理了一套可复用流程：状态规划、图片生成或导入、动画横条、自动切图、质量检查和 Spritesheet 打包。

这个仓库包含：

- Codex Skill 入口：[`skill/SKILL.md`](skill/SKILL.md)
- 用于切图和打包的 Python 脚本
- 中英文制作指南
- 一个完整的 Lanxi 示例宠物包

## 效果展示

查看 Lanxi 中文展示页面：

[https://otrttf.github.io/oc-codex-pet-maker/index.zh-CN.html](https://otrttf.github.io/oc-codex-pet-maker/index.zh-CN.html)

页面源码在 [`docs/index.zh-CN.html`](docs/index.zh-CN.html)。

![Lanxi 动画状态展示](docs/assets/lanxi-state-overview.png)

## 快速开始

Python 脚本依赖 Pillow：

```bash
python3 -m pip install Pillow
```

### 1. 安装 Skill

把自包含的 `skill/` 目录复制到 Codex 的 skills 目录：

```bash
mkdir -p ~/.codex/skills/oc-codex-pet-maker
cp -R skill/* ~/.codex/skills/oc-codex-pet-maker/
```

安装后的 Skill 会包含入口文件、必要模板、Sprite 横条间距规则和 Python 脚本。也就是说，新开 Codex 对话后，Skill 引用的路径可以直接在已安装的 Skill 目录里找到，不依赖原始仓库目录。

然后新开一个 Codex 对话，可以这样说：

```text
请使用 Codex Pet Maker Skill 帮我制作一个 Codex 宠物。
宠物创意或素材来源：……
视觉风格或材质：……
必须保留的标志性特征：……
```

Skill 应该先向你说明 Codex 宠物的 9 个状态，并帮助你确认每个状态对应的动作方案，然后再开始生成图片。

第一次使用时，理想流程是：

1. 读取 Skill 入口。
2. 说明 Codex 宠物的 9 个状态。
3. 填写或调整状态动作方案。
4. 等你确认后，再进入图片生成。
5. 生成横条、切图、检查预览、合成 spritesheet，并验证宠物包。

### 2. 制定状态动作方案

Codex 宠物通常有 9 个动画状态：

| 行 | 状态 | 含义 |
| --- | --- | --- |
| 0 | `idle` | 默认待机 |
| 1 | `running-right` | 向右拖拽或移动 |
| 2 | `running-left` | 向左拖拽或移动 |
| 3 | `waving` | 打招呼 |
| 4 | `jumping` | 跳跃或开心反馈 |
| 5 | `failed` | 任务失败或可恢复错误 |
| 6 | `waiting` | 等待用户输入或确认 |
| 7 | `running` | 任务处理中，不是字面意义的跑步 |
| 8 | `review` | 检查、审阅结果 |

可以使用这个模板：

[`templates/state-action-plan.template.md`](templates/state-action-plan.template.md)

安装 Skill 后，同一个模板也会在已安装的 Skill 目录里。

### 3. 生成并切分动画横条

每一行动画可以先生成一张横向 sprite strip，再用脚本切成透明的 `192x208` 小格：

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

重点检查这些输出：

```text
<prefix>-cell-preview.png
<prefix>-preview.gif
<prefix>-metrics.json
```

### 4. 合成最终 Spritesheet

准备好 9 行通过检查的动画横条后，创建 manifest，再合成最终图集：

```bash
python3 scripts/compose_spritesheet.py \
  --manifest /absolute/path/to/your-pet/rows-manifest.json \
  --out /absolute/path/to/your-pet/package/spritesheet.png \
  --webp-out /absolute/path/to/your-pet/package/spritesheet.webp
```

验证宠物包：

```bash
python3 scripts/validate_pet_package.py \
  --package-dir /absolute/path/to/your-pet/package
```

创建宠物包元数据时，可以使用这个模板：

[`templates/pet-json.template.json`](templates/pet-json.template.json)

## 为什么需要这个项目

制作一个好看的 Codex 宠物，比制作一张漂亮插画更脆弱。最终宠物需要同时满足：

- 每格只有 `192x208`
- 9 个不同应用状态
- 干净的透明背景
- 宽轮廓、附着特征和道具不能被裁切
- 每行动画要稳定一致
- 最后必须打包成 `spritesheet.webp`

制作真实宠物时最常见的坑之一，是 AI 生成的横条里每一帧距离太近。结果切图时，上一帧的附着特征会被切到下一帧里。这个项目提供间距规范和 `smart-components` 切图模式，用代码识别主体边界，减少特征或道具串帧。

## 与 Hatch Pet 的关系

这个项目来源于一次真实使用 Codex Hatch Pet Skill 的制作实践。Hatch Pet 提供从创意或参考图到宠物打包的一体化、代理编排流程；Codex Pet Maker 则是配套工具箱，适合希望查看中间过程、自定义方案、理解制作原理或局部修复的用户。

它重点解决实际使用 Hatch Pet 时可能遇到的问题：

- 混淆 9 个应用状态，尤其是方向移动和任务处理状态 `running`
- 不同行之间出现身份、比例、颜色、材质或道具漂移
- 帧间距太窄，导致相邻特征被切进错误格子
- 色键残留、透明像素污染和有色边缘泛色
- 宠物存在左右不对称标记、附着特征或道具时盲目镜像
- 图集尺寸正确，但动作弱、大小跳变、方向错误或状态语义不清
- 只想检查和修复一行，却不得不重新生成整只宠物

仓库公开保留状态规划模板、中间文件约定、间距规则、确定性脚本和 QA 方法。它不是 Hatch Pet 的替代品；Hatch Pet 的能力也可能随着 Codex 持续更新。

## 文档

- English guide: [`docs/CODEX_PET_CREATION_GUIDE.md`](docs/CODEX_PET_CREATION_GUIDE.md)
- 中文制作指南：[`docs/CODEX_PET_CREATION_GUIDE.zh-CN.md`](docs/CODEX_PET_CREATION_GUIDE.zh-CN.md)
- Sprite 横条间距规则：[`docs/SPRITE_STRIP_SPACING_RULES.md`](docs/SPRITE_STRIP_SPACING_RULES.md)
- 安装说明：[`docs/INSTALLATION.md`](docs/INSTALLATION.md)
- 展示 GIF 阴影记录：[`docs/SHOWCASE_GIF_SHADOW_NOTES.md`](docs/SHOWCASE_GIF_SHADOW_NOTES.md)
- GitHub 发布经验：[`docs/GITHUB_PUBLISHING_NOTES.zh-CN.md`](docs/GITHUB_PUBLISHING_NOTES.zh-CN.md)
- Roadmap：[`docs/ROADMAP.md`](docs/ROADMAP.md)

## 仓库结构

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

## Lanxi 示例

Lanxi 是用于开发和验证这套流程的最终案例。公开展示会保留宠物成品图片和动画结果，但通用说明会有意省略其背后的私人创作设定和 prompt。

示例包含：

- 标准角色参考：[`10-references/`](10-references/)
- 各状态参考图：[`20-states/`](20-states/)
- 已确认的动画行：[`examples/lanxi/rows/`](examples/lanxi/rows/)
- 可验证的草稿宠物包：[`40-draft-package/`](40-draft-package/)

你可以这样验证 Lanxi 宠物包：

```bash
python3 scripts/validate_pet_package.py --package-dir 40-draft-package
```

## 当前限制

- 洋红色抠图边缘偶尔仍会有一点泛色，已经比早期版本好很多，后续还可以继续优化边缘清理。
- 当前 Skill 是一个工作流入口，已经能指导流程并调用本地脚本，但还不是一键安装器。
- 生成资产可能会让仓库变大，所以旧实验文件和 debug 文件默认不会纳入 Git。

## License

MIT。见 [`LICENSE`](LICENSE)。
