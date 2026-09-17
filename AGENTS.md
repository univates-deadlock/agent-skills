# Agent instructions

This repository is the canonical registry for Univates Deadlock Agent Skills.

## Source of truth

- Canonical skills live under `skills/<skill-name>/`.
- Do not store canonical skills under `.agents/` or `.claude/`; those are installation targets in consuming repositories.
- The installer must continue to discover skills from `skills/*/SKILL.md` without a separate manifest.

## Skill authoring

- Keep `SKILL.md` focused on reusable guidance and triggering conditions.
- Project-specific conventions belong in the consuming repository's instructions, such as `AGENTS.md`.
- Use `references/` for supporting material that does not need to load with every invocation.
- Skill directory names and `name` metadata must match and use lowercase kebab-case.

## Development

- Keep the installer dependency-free unless a dependency is clearly justified.
- Add or update tests before changing installer/validator behavior.
- Run `python scripts/validate.py` and `python -m unittest discover -s tests -v` before considering changes complete.
