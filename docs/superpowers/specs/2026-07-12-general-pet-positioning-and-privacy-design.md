# Codex Pet Maker: General Pet Positioning and Privacy Design

## Goal

Reposition the project from an OC-specific maker to a broadly applicable Codex pet-making toolkit, explain its relationship to the Codex Hatch Pet Skill, and remove public text that exposes the private creative specification behind Lanxi.

## Public Positioning

Use **Codex Pet Maker Skill** as the visible project name. Keep the existing GitHub repository slug and URLs so current links continue to work.

The project supports pets created from animal ideas, mascots, brand or product cues, existing character art, avatars, reference images, or text-only concepts. OC creation remains one supported use case, not the defining scope.

## Relationship to Hatch Pet

Describe the project as a companion toolkit derived from practical experience using the Codex Hatch Pet Skill. Do not frame it as an official replacement or as a competing implementation.

Hatch Pet provides a streamlined, agent-orchestrated path from an idea or references to generation, validation, packaging, and installation. Codex Pet Maker makes the difficult parts of that process easier to understand, inspect, customize, and repair.

Public explanations should emphasize the recurring problems addressed by this repository:

- confusion between the nine Codex app states, especially directional `running-left` / `running-right` and task-processing `running`;
- identity, proportions, palette, prop, and style drift across independently generated rows;
- generated sprite frames placed too close together, causing hair, limbs, or props to bleed into neighboring cells;
- chroma removal artifacts, transparent-background residue, and colored edge halos;
- unsafe mirroring when a pet has directional markings, accessories, text-like shapes, or asymmetric props;
- output that passes geometry checks but still has weak motion, size popping, wrong direction, or unclear state semantics;
- difficulty reviewing intermediate assets and repairing one failed row without regenerating the whole pet;
- lack of reusable prompt-planning, manifest, spacing, cutting, composition, and validation templates for users who want manual control.

State that Hatch Pet can evolve with Codex, so the comparison describes the current practical emphasis rather than a permanent feature guarantee.

## Lanxi Privacy Boundary

Keep Lanxi's name, finished images, animation previews, and role as the real project case study.

Remove public text that could reconstruct the private creative brief, including:

- original or near-original prompts;
- detailed clothing and styling descriptions;
- H/J or other identifying accessory details;
- street-dance and other private action concepts;
- Lanxi-specific action tables, negative prompts, repair prompts, and mirroring decisions.

Replace those details with general lessons or neutral placeholders. The handoff document is internal project context and is not part of this public-copy cleanup.

## Reusable Description Template

Public templates and examples should teach a sentence structure rather than disclose a private character specification. They should prompt for:

- pet type or subject;
- overall visual style or material;
- primary palette;
- one to three readable signature traits;
- desired action and emotion for each state;
- details that must remain consistent;
- forbidden additions or changes;
- directional asymmetry that makes mirroring unsafe.

Examples should use placeholders or a deliberately generic fictional pet. They must not reuse Lanxi's private traits.

## Files in Scope

- `README.md` and `README.zh-CN.md`;
- `docs/index.html` and `docs/index.zh-CN.html`;
- public creation and installation guides under `docs/`;
- `skill/SKILL.md` and its self-contained copies under `skill/docs/` and `skill/templates/`;
- reusable templates under `templates/`;
- public metadata or visible labels that still define the tool as OC-only.

Generated assets and finished Lanxi showcase media remain unchanged.

## Verification

- Search public files for OC-only positioning and private Lanxi details.
- Confirm the visible English and Chinese project names and descriptions agree.
- Confirm Hatch Pet comparison text is present in both languages and is framed as complementary.
- Validate JSON templates.
- Run `git diff --check`.
- Run the existing pet-package validator.
- Use the separate first-time-user simulation task to identify remaining scope, privacy, and onboarding problems.

