# Installation Notes

This project has two installation targets:

1. Install the reusable Skill.
2. Install a finished pet package.

## Install The Skill

From the repository root:

```bash
mkdir -p ~/.codex/skills/oc-codex-pet-maker
cp -R skill/* ~/.codex/skills/oc-codex-pet-maker/
```

The `skill/` folder is self-contained. It includes `SKILL.md`, templates, sprite-strip rules, and the Python scripts needed by the workflow.

### Beginner-Friendly Installation From Codex

A user who only has Codex can open an empty project folder, start a conversation, and ask Codex to download this repository and follow this file. Do not assume that completing a clone also completed Skill installation.

When acting as the installer, inspect the target and use the matching branch below.

#### Target Does Not Exist

Copy the self-contained `skill/` folder, verify that `SKILL.md`, `docs/`, `templates/`, and `scripts/` exist in the target, then report:

1. where the repository was downloaded;
2. where the Skill was installed;
3. that the user should start a **new Codex conversation** so the installed Skill can be discovered;
4. the exact minimal next message:

```text
请使用 OC Codex Pet Maker Skill 帮我制作一个 Codex 宠物，并一步一步引导我。
```

Explain that the user does not need a reference image or a completed prompt. The Skill should next ask whether they want to start from text, a reference image, or existing sprite assets.

#### Target Exists And Is Identical

Do not copy or overwrite. State that the installed copy matches the downloaded copy, then provide the same new-conversation instruction and minimal next message above.

#### Target Exists And Is Different

Do not describe “the directory exists” as “the Skill is installed and ready.” Stop before overwriting and explain three concrete choices:

1. keep the existing installed copy for now;
2. back it up and replace it with the downloaded copy;
3. cancel and inspect the differences first.

Ask the user to choose one. Recommend backup-and-replace when they explicitly want the newly downloaded version, but never replace without approval. Only after the conflict is resolved should you provide the new-conversation instruction and minimal creation message.

Every installation response must end with a concrete next action or question. Never end with only a path, status, or warning.

## Install A Finished Pet Package

A finished pet package should contain:

```text
<pet-id>/
  pet.json
  spritesheet.webp
```

The `pet.json` file should follow:

```text
templates/pet-json.template.json
```

Field rules:

- `id`: lowercase, stable, filesystem-friendly pet id, such as `my-pet`.
- `displayName`: short user-facing name shown in Codex.
- `description`: one-sentence description of the pet identity.
- `spritesheetPath`: relative path from `pet.json` to the generated spritesheet, usually `spritesheet.webp`.

Before copying, run structural validation:

```bash
python3 scripts/validate_pet_package.py --package-dir <package-dir>
```

Passing this command proves the required files exist and the spritesheet has the expected dimensions and image mode. It does not prove correct state semantics, visual identity, clipping, frame bleed, chroma cleanup, motion quality, or loop quality. Review the contact sheet and animation previews separately.

A commonly used local package location is:

```text
~/.codex/pets/<pet-id>/
```

Treat this as a package location, not a guaranteed activation contract. The exact Codex Desktop behavior for discovering, reloading, selecting, and removing custom pets can change between app versions. Confirm the current app workflow before claiming that a copied package is installed and active.

If a package with the same id already exists, make a backup or ask the user before replacing it.
