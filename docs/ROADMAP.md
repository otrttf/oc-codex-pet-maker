# Roadmap

## Before GitHub Release

- Keep the reusable scripts in `scripts/` as the public entrypoint.
- Keep `skill/SKILL.md` aligned with the public scripts and templates.
- Decide whether to include all Lanxi experiment assets or only curated examples.
- Add a clear installation/use section for copying the skill into a Codex skills directory.
- Create the first Git commit after the release structure is stable.

## Later Improvements

- Improve magenta edge decontamination. The current output is usable, but some rows still show a slight magenta halo after chroma removal.
- Add a contact-sheet generator as a reusable script.
- Add an installer script for copying a finished package into `~/.codex/pets/<pet-id>` with backup.
- Add a motion-design guide for `running-right` / `running-left`. Complex travel motion is hard for image models because anatomy or structure, attached features, and frame continuity can drift. The guide should include readable motion phases, compact travel limits, and anatomy-neutral fallback actions.
- Support two-character pets. This needs explicit layout rules for shared center of mass, spacing between characters, synchronized vs. alternating actions, and stricter frame-boundary checks so one character does not bleed into the next slot.
- Add an external image-generation prompt pack. Codex should be able to produce copy-paste prompts for tools such as Kling, Jimeng, or other image/video generators, so users can spend fewer Codex tokens while still creating 8-frame strips that follow the project's spacing, chroma, identity, and `192x208` cell requirements.
- Add provider-specific prompt templates after more testing. Each template should include a short character identity lock, state action plan, frame count, large gutters, flat chroma background, no shadows/glows, and a checklist for rejecting bad strips before importing them into the cutter.
