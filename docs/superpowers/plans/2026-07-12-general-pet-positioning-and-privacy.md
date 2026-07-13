# General Pet Positioning and Privacy Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Reposition the project for all Codex pets, explain the practical problems it solves alongside Hatch Pet, replace private Lanxi specifications with user-fillable placeholders, and preserve the finished Lanxi showcase media.

**Architecture:** Treat root documentation, the self-contained installed Skill, reusable templates, and the bilingual GitHub Pages site as synchronized public surfaces. Keep Lanxi only as a labeled finished case study; generic instructions use neutral terminology, `…` placeholders, and user-owned paths. Verify with targeted privacy searches, template synchronization, JSON parsing, unchanged website asset references, and the existing package validator.

**Tech Stack:** Markdown, bilingual static HTML/CSS, JSON templates, Python 3 validation scripts, ripgrep, Git.

---

### Task 1: Reposition the root README files

**Files:**
- Modify: `README.md`
- Modify: `README.zh-CN.md`

- [ ] **Step 1: Capture current generic-copy failures**

Run:

```bash
rg -n -i 'OC Codex|your OC|自己的 OC|custom OC-specific|浅蓝长发|silver eyes|J hair|H earring|street-dance|hip-hop|skateboard' README.md README.zh-CN.md
```

Expected: matches show OC-only positioning or private Lanxi details.

- [ ] **Step 2: Replace visible positioning and starter requests**

Use `Codex Pet Maker Skill` as the visible title. Describe supported inputs as animal ideas, mascots, brand or product cues, existing art, avatars, references, and text concepts. Use this neutral starter shape in English and its equivalent in Chinese:

```text
Use the Codex Pet Maker skill to help me create a Codex pet.
Pet idea or source: …
Visual style or material: …
Signature traits to preserve: …
```

- [ ] **Step 3: Add the Hatch Pet relationship section**

State that the project grew from practical use of Hatch Pet and complements it with inspectable templates, intermediate assets, manual controls, and repair guidance. List: state-semantic confusion, identity drift, tight gutters/frame bleed, chroma and edge artifacts, unsafe mirroring, motion defects missed by geometry checks, and row-level repair. Note that Hatch Pet may evolve with Codex.

- [ ] **Step 4: Make generic commands user-owned**

Use:

```bash
python3 scripts/compose_spritesheet.py \
  --manifest /absolute/path/to/your-pet/rows-manifest.json \
  --out /absolute/path/to/your-pet/package/spritesheet.png \
  --webp-out /absolute/path/to/your-pet/package/spritesheet.webp

python3 scripts/validate_pet_package.py \
  --package-dir /absolute/path/to/your-pet/package
```

Keep Lanxi commands only in a clearly labeled case-study section.

- [ ] **Step 5: Verify both README files**

Run:

```bash
rg -n 'Codex Pet Maker Skill|Hatch Pet|absolute/path/to/your-pet' README.md README.zh-CN.md
rg -n -i 'Turn your OC|for my OC|自己的 OC|custom OC-specific' README.md README.zh-CN.md
```

Expected: first command matches both languages; second returns no generic-copy matches.

- [ ] **Step 6: Commit**

```bash
git add README.md README.zh-CN.md
git commit -m "Reposition Codex Pet Maker for general pets"
```

### Task 2: Generalize the reusable Skill and templates

**Files:**
- Modify: `skill/SKILL.md`
- Modify: `templates/state-action-plan.template.md`
- Modify: `templates/state-reference-prompt.template.md`
- Modify: `templates/sprite-strip-prompt.template.md`
- Modify: `templates/pet-json.template.json`
- Modify: `templates/rows-manifest.template.json`
- Modify: matching files under `skill/templates/`

- [ ] **Step 1: Capture OC, humanoid, and Lanxi assumptions**

Run:

```bash
rg -n -i 'OC/avatar|own OC|Lanxi|浅蓝长发|silver eyes|J hair|H earring|outfit|hair|hands|typing|hip-hop|skateboard' skill/SKILL.md templates skill/templates
```

Expected: matches identify assumptions or private details.

- [ ] **Step 2: Generalize Skill metadata and intake**

Define broad subject classes and use these exact fill-in concepts:

```text
Pet type or subject: …
Visual style or material: …
Primary palette: …
One to three signature traits: …
State action and emotion: …
Details that must stay consistent: …
Forbidden additions or changes: …
Directional asymmetry that makes mirroring unsafe: …
```

Use silhouette, surface/material, markings, attached features, greeting gesture, focused-work motion, and complete visible form. Hair, clothes, hands, or typing may appear only as optional examples.

- [ ] **Step 3: Replace the Lanxi plan example with placeholders**

Use this bilingual structure and `……` for every custom state action:

```markdown
## Your pet / 你的宠物

- Pet name / 宠物名称：……
- Pet type or subject / 宠物类型或主体：……
- Style or material / 风格或材质：……
- Primary palette / 主要颜色：……
- Signature traits / 标志性特征：……
- Must stay consistent / 必须保持一致：……
- Must not appear or change / 禁止出现或改变：……
- Directional asymmetry / 左右不对称特征：……
```

- [ ] **Step 4: Generalize prompt templates**

Keep exact state, chroma, frame-count, spacing, and artifact constraints. Replace the private identity/action examples with user-filled `……` values and anatomy-neutral wording.

- [ ] **Step 5: Synchronize root and installed copies**

Run:

```bash
for f in state-action-plan.template.md state-reference-prompt.template.md sprite-strip-prompt.template.md pet-json.template.json rows-manifest.template.json; do
  diff -u "templates/$f" "skill/templates/$f"
done
```

Expected: no differences.

- [ ] **Step 6: Validate privacy and JSON**

Run:

```bash
python3 -m json.tool templates/pet-json.template.json >/tmp/pet-json-template.txt
python3 -m json.tool templates/rows-manifest.template.json >/tmp/rows-manifest-template.txt
rg -n -i 'Lanxi|浅蓝长发|silver eyes|J hair|H earring|hip-hop|skateboard' templates skill/templates skill/SKILL.md
```

Expected: JSON succeeds; privacy search returns no matches.

- [ ] **Step 7: Commit**

```bash
git add skill/SKILL.md templates skill/templates
git commit -m "Generalize pet planning templates"
```

### Task 3: Sanitize and close the public guides

**Files:**
- Modify: `docs/CODEX_PET_CREATION_GUIDE.md`
- Modify: `docs/CODEX_PET_CREATION_GUIDE.zh-CN.md`
- Modify: `docs/INSTALLATION.md`
- Modify: `skill/docs/INSTALLATION.md`
- Modify: `docs/SPRITE_STRIP_SPACING_RULES.md`
- Modify: `skill/docs/SPRITE_STRIP_SPACING_RULES.md`

- [ ] **Step 1: Locate private details and unsupported claims**

Run:

```bash
rg -n -i 'Lanxi|浅蓝长发|silver eyes|J hair|H earring|安全裤|裙摆|hip-hop|skateboard|高桌|typing|Common local target|my-oc-pet' docs/CODEX_PET_CREATION_GUIDE* docs/INSTALLATION.md skill/docs
```

Expected: matches identify content to generalize.

- [ ] **Step 2: Rewrite private lessons as general patterns**

Replace named accessory and action stories with neutral rules. For example: “If markings, attached features, symbols, or props are asymmetric, generate both directions separately or visually approve mirroring.” Use `……` for user-specific actions.

- [ ] **Step 3: Add generation/import decision paths**

Document text-only, existing-reference, non-character, and repair starts. Explain that Codex image generation or external tools create artwork; repository scripts only cut, clean, compose, and validate supplied images. Specify canonical-reference naming, approval criteria, row naming, and retry steps when separated pose counts fail.

- [ ] **Step 4: Correct installation and validation claims**

Separate “structurally valid package” from “confirmed loaded in Codex Desktop.” Document only verified directory behavior. State that validation does not prove identity, state meaning, clipping, frame bleed, chroma artifacts, motion, or loop quality.

- [ ] **Step 5: Synchronize self-contained guide copies**

Run:

```bash
diff -u docs/INSTALLATION.md skill/docs/INSTALLATION.md
diff -u docs/SPRITE_STRIP_SPACING_RULES.md skill/docs/SPRITE_STRIP_SPACING_RULES.md
```

Expected: no differences.

- [ ] **Step 6: Verify privacy and workflow coverage**

Run:

```bash
rg -n -i 'J hair|H earring|安全裤|hip-hop|skateboard|高桌' docs/CODEX_PET_CREATION_GUIDE* docs/INSTALLATION.md skill/docs
rg -n 'text-only|reference|repair|结构验证|视觉检查|structural validation|visual QA' docs/CODEX_PET_CREATION_GUIDE* docs/INSTALLATION.md
```

Expected: privacy search returns no matches; workflow search covers both languages where applicable.

- [ ] **Step 7: Commit**

```bash
git add docs/CODEX_PET_CREATION_GUIDE.md docs/CODEX_PET_CREATION_GUIDE.zh-CN.md docs/INSTALLATION.md docs/SPRITE_STRIP_SPACING_RULES.md skill/docs
git commit -m "Generalize and clarify pet creation guides"
```

### Task 4: Reposition the bilingual website without changing showcase media

**Files:**
- Modify: `docs/index.html`
- Modify: `docs/index.zh-CN.html`

- [ ] **Step 1: Record current Lanxi media references**

Run:

```bash
rg -o 'assets/lanxi-[^" ]+' docs/index.html docs/index.zh-CN.html | sort > /tmp/lanxi-site-assets-before.txt
```

Expected: output records all current hero, GIF, WebP, overview, and spritesheet references.

- [ ] **Step 2: Rewrite public website copy**

Use `Codex Pet Maker Skill` as the visible brand. Explain broad pet inputs, Hatch Pet origins, and the problems this companion toolkit solves. Replace OC-only and private action copy with neutral state semantics. Keep Lanxi as the labeled finished case study.

- [ ] **Step 3: Add the Hatch Pet comparison block**

Say Hatch Pet offers a streamlined hatch workflow while this repository exposes planning templates, intermediate files, spacing/cutting rules, diagnosis, and row-level repair. Avoid “better than,” “replacement,” or unsupported official claims.

- [ ] **Step 4: Prove showcase media references did not change**

Run:

```bash
rg -o 'assets/lanxi-[^" ]+' docs/index.html docs/index.zh-CN.html | sort > /tmp/lanxi-site-assets-after.txt
diff -u /tmp/lanxi-site-assets-before.txt /tmp/lanxi-site-assets-after.txt
```

Expected: no differences.

- [ ] **Step 5: Verify bilingual positioning and privacy**

Run:

```bash
rg -n 'Codex Pet Maker Skill|Hatch Pet' docs/index.html docs/index.zh-CN.html
rg -n -i 'Turn your OC|custom OC-specific|浅蓝长发|J hair|H earring|hip-hop|skateboard' docs/index.html docs/index.zh-CN.html
```

Expected: both languages contain new positioning; privacy/OC search returns no matches.

- [ ] **Step 6: Commit**

```bash
git add docs/index.html docs/index.zh-CN.html
git commit -m "Update Codex Pet Maker website positioning"
```

### Task 5: Prove generic surfaces no longer default to Lanxi

**Files:**
- Modify only files identified by verification failures

- [ ] **Step 1: Search for private Lanxi specifications**

Run:

```bash
rg -n -i '浅蓝长发|silver eyes|J hair|H earring|安全裤|hip-hop|skateboard|高桌|street-dance' README.md README.zh-CN.md docs skill templates --glob '!HANDOFF.zh-CN.md' --glob '!superpowers/**'
```

Expected: no matches. Finished image filenames and simple “Lanxi is the finished case study” statements are allowed.

- [ ] **Step 2: Search for Lanxi-default generic paths**

Run:

```bash
rg -n 'examples/lanxi|40-draft-package' README.md README.zh-CN.md skill/SKILL.md templates skill/templates docs/INSTALLATION.md skill/docs/INSTALLATION.md
```

Expected: no generic workflow matches; any README match is inside a clearly labeled Lanxi case-study section.

- [ ] **Step 3: Search for OC-only or humanoid-required language**

Run:

```bash
rg -n -i 'Turn your OC|for my OC|自己的 OC|replace Lanxi|OC-specific behavior|must have hair|must wear|must wave with (a )?hand' README.md README.zh-CN.md docs skill templates
```

Expected: no matches. “OC is one supported input” is allowed.

- [ ] **Step 4: Run structural verification**

Run:

```bash
git diff --check
python3 -m json.tool templates/pet-json.template.json >/tmp/pet-json-template.txt
python3 -m json.tool templates/rows-manifest.template.json >/tmp/rows-manifest-template.txt
python3 scripts/validate_pet_package.py --package-dir 40-draft-package
```

Expected: all commands exit zero; validator reports `ok: true`, size `1536x1872`, mode `RGBA`.

- [ ] **Step 5: Review final diff and media proof**

Run:

```bash
git diff --stat
git status --short
diff -u /tmp/lanxi-site-assets-before.txt /tmp/lanxi-site-assets-after.txt
```

Expected: only intended public text/template files changed, unrelated work is preserved, and media reference diff is empty.

- [ ] **Step 6: Commit verification-only corrections if needed**

If verification required corrections, stage only those files and commit:

```bash
git add README.md README.zh-CN.md docs/CODEX_PET_CREATION_GUIDE.md docs/CODEX_PET_CREATION_GUIDE.zh-CN.md docs/INSTALLATION.md docs/SPRITE_STRIP_SPACING_RULES.md docs/index.html docs/index.zh-CN.html skill/SKILL.md skill/docs skill/templates templates
git commit -m "Finish general pet privacy cleanup"
```

If no corrections were needed, do not create an empty commit.
