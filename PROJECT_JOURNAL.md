# Project Journal

按日期记录项目当天完成的工作、关键决定、验证结果和下一步。只记录已经发生的事实；尚未执行的工作放在“下一步”，不写成已完成。

---

## 2026-07-12

### 今日完成

- 阅读并核对 `docs/HANDOFF.zh-CN.md`，正式接手项目。
- 确认仓库位于 `main` 分支，交接前的 Skill 自包含改动仍保留在工作区。
- 重跑基础验证：
  - `git diff --check` 通过。
  - `templates/pet-json.template.json` 是合法 JSON。
  - `templates/rows-manifest.template.json` 是合法 JSON。
  - `python3 scripts/validate_pet_package.py --package-dir 40-draft-package` 通过。
  - Lanxi spritesheet 为 `1536x1872`、`RGBA`。
- 确认项目公开定位需要从“OC 专用”扩展为适用于各种 Codex 宠物：
  - 动物、吉祥物、品牌或产品灵感；
  - 已有角色或头像；
  - 参考图片；
  - 纯文字概念；
  - 非人形主体，例如机器人、植物、物品或抽象图标。
- 确认可见项目名称改为 **Codex Pet Maker Skill**；现有 GitHub 仓库地址暂时保留，避免链接失效。
- 确认 Lanxi 隐私边界：
  - 保留 Lanxi 名称、最终作品图片、GIF、WebP 和案例展示；
  - 删除或抽象可还原私人创作设定的 prompt、服饰、H/J 配饰、街舞和专属动作描述；
  - 通用模板使用 `…` 或 `……` 占位符，提醒用户填写自己的信息。
- 阅读本机 Hatch Pet Skill，确认公开叙事：
  - 本项目源于实际使用 Hatch Pet 的经历；
  - 它不是 Hatch Pet 的替代品；
  - 它重点沉淀使用过程中踩坑后形成的模板、间距规则、切帧工具、诊断方法和局部修复流程。
- 明确本项目重点解决的问题：
  - 九个 Codex 状态语义容易混淆；
  - 多行动画之间出现身份、比例、颜色或道具漂移；
  - 横条帧间距太窄，导致头发、肢体或道具串帧；
  - 色键清理、透明像素残留和洋红边缘污染；
  - 左右不对称宠物不能盲目镜像；
  - 尺寸验证通过但动作、方向或循环观感仍有问题；
  - 单行动画失败时难以检查和局部修复。
- 创建独立 Codex 任务，以零背景新用户身份只读模拟 Skill 使用流程：
  - 审查发现两个最高优先级断点：素材生成/导入流程没有闭环；成品复制后在 Codex Desktop 中如何启用和确认安装没有闭环。
  - 审查还发现 OC/人形硬编码、Lanxi 私有细节、Lanxi 默认命令路径以及验证器能力边界表述等问题。
- 完成并提交设计规格：
  - `docs/superpowers/specs/2026-07-12-general-pet-positioning-and-privacy-design.md`
  - 提交 `83c74c9`：`Document general pet positioning and privacy design`
  - 提交 `c34175b`：`Expand first-time pet maker journey design`
- 完成实施计划：
  - `docs/superpowers/plans/2026-07-12-general-pet-positioning-and-privacy.md`
- 在开始实施前保存了中英文网站现有 `assets/lanxi-*` 素材引用基线，用于修改后证明最终作品展示素材没有变化。

### 继续执行

- 将 README 和中文 README 的可见名称统一为 **Codex Pet Maker Skill**。
- 将项目入口从“为我的 OC 制作宠物”改为适用于动物、吉祥物、品牌或产品灵感、已有作品、头像、参考图、纯文字概念和现有 sprite 素材。
- 把通用合成和验证命令改为 `/absolute/path/to/your-pet/...`，不再默认操作 Lanxi 文件。
- 在 README 和中英文网站加入与 Hatch Pet 的关系：本项目源于真实 Hatch Pet 使用经历，重点补充可检查的中间过程、模板、间距与切图规则、诊断和单行修复能力。
- 把 Skill 与通用模板改为非人形宠物也可使用的描述方式：轮廓、材质、标记、附着特征、配色和运动；不再强制使用头发、服装、手、打字等人形概念。
- 删除通用模板中的 Lanxi 填写示例，改为 `…` / `……` 占位符。
- 清理中英文长指南中的 Lanxi 私人造型、H/J 配饰、街舞和专属动作描述，保留可复用的技术经验。
- 补充四种首次使用入口：纯文字、已有参考图、非人物主体、已有 sprite 修复。
- 明确仓库脚本只负责切分、清理、合成和验证已有图片，不负责凭空生成视觉作品。
- 明确结构验证通过不等于视觉 QA 通过，也不等于 Codex Desktop 已经发现并启用宠物。
- 更新中英文介绍网站的标题、定位、状态文案与 Hatch Pet 对比说明。
- 对比网站修改前后的全部 `assets/lanxi-*` 引用，结果无差异；Lanxi 最终展示图片、GIF 和 WebP 没有变化。
- 完成验证：
  - `git diff --check` 通过；
  - JSON 模板解析通过；
  - 中英文 HTML 解析通过；
  - 根目录模板与 `skill/templates/` 副本一致；
  - 根目录安装/间距文档与 `skill/docs/` 副本一致；
  - 私有 Lanxi 设定和 OC 专用措辞搜索无结果；
  - Lanxi 宠物包继续验证通过，尺寸 `1536x1872`、模式 `RGBA`。

### 当前仍未做

- 尚未修改任何 Lanxi 最终展示图片、GIF 或 WebP。
- 尚未提交本轮通用化、隐私清理和交接前遗留的 Skill 自包含改动。
- 尚未 push 到 GitHub。
- 尚未更新线上 GitHub Pages。

### 下一步

1. 用户审阅本轮文案、模板和网站改动。
2. 根据审阅意见做必要调整。
3. 确认满意后，整理并提交当前工作区改动。
4. push 到 GitHub。
5. 检查线上 GitHub Pages 是否正确展示新版文案和未变的 Lanxi 成品素材。

---

## 2026-07-14

### 今日目标

- 整理已经完成并验证过的通用化、隐私清理、Skill 自包含和网站文案改动。
- 排除内部交接文档及不适合公开的内部标识。
- 提交到本地 `main` 并推送到 GitHub `origin/main`。

### 提交前验证

- `git diff --check` 通过。
- 两个 JSON 模板解析通过。
- 中英文 HTML 解析通过。
- Lanxi 宠物包验证通过，尺寸 `1536x1872`、模式 `RGBA`。
- 网站修改前后的 `assets/lanxi-*` 引用一致，最终展示素材未变。
- 通用 Skill 和模板中没有 Lanxi 名称、私人造型细节或 OC 专用请求句式。

### 发布状态

- 等待本次提交和推送完成后更新。
