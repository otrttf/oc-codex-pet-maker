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
