# Univates Deadlock Agent Skills

Reusable Agent Skills maintained by the Univates Deadlock team for coding agents such as Codex, Claude Code, and Google Antigravity.

The canonical skills live in `skills/`. The included installer copies selected skills into a target repository under `.agents/skills/`, `.claude/skills/`, or both. Generated copies in consuming repositories are not the source of truth for this registry.

## Available skills

### `building-typescript-rest-apis`

Guidance for project-aware TypeScript REST API work, covering HTTP boundaries, runtime validation, authentication and authorization, error handling, Prisma/PostgreSQL persistence, transactions, security, and behavior-focused API testing.

### `developing-nextjs-app-router-interfaces`

Guidance for Next.js App Router and React interface work, covering Server/Client Component boundaries, component composition, data fetching, API integration, forms, UI states, responsive behavior, accessibility, and implementation quality.

### `developing-vanilla-web-interfaces`

Guidance for framework-free frontend work with HTML, CSS, and vanilla JavaScript, covering project-aware reuse, BEM, design tokens, CSS architecture, responsive behavior, components, and accessibility.

## Requirements

- Python 3.10+
- No third-party Python dependencies

## List skills

```bash
python scripts/install.py --list
```

## Interactive installation

Run the installer without arguments:

```bash
python scripts/install.py
```

It asks for the target repository, skills to install, and the destination (`agents`, `claude`, or `both`).

## Non-interactive installation

Install one skill in both supported project locations:

```bash
python scripts/install.py \
  --repo ../techpro-web-landing-page \
  --skill developing-vanilla-web-interfaces \
  --target both
```

Install every available skill:

```bash
python scripts/install.py \
  --repo ../my-project \
  --all \
  --target both
```

Install only for Antigravity/Codex-style discovery:

```bash
python scripts/install.py \
  --repo ../my-project \
  --skill developing-vanilla-web-interfaces \
  --target agents
```

Install only for Claude Code:

```bash
python scripts/install.py \
  --repo ../my-project \
  --skill developing-vanilla-web-interfaces \
  --target claude
```

Preview changes:

```bash
python scripts/install.py \
  --repo ../my-project \
  --all \
  --target both \
  --dry-run
```

If an installed skill differs from the canonical version, the installer stops instead of overwriting it. Use `--force` when replacement is intentional.

## Validate skills

```bash
python scripts/validate.py
```

Validation checks the required skill metadata and repository naming conventions.

## Run tests

```bash
python -m unittest discover -s tests -v
```

## Repository structure

```text
agent-skills/
├── skills/                         # canonical skill definitions
│   └── <skill-name>/
│       ├── SKILL.md
│       ├── references/             # optional on-demand documentation
│       ├── scripts/                # optional skill-specific helpers
│       └── assets/                 # optional skill-specific assets
├── scripts/
│   ├── install.py                  # installer / catalog CLI
│   ├── validate.py                 # repository validator
│   └── _catalog.py                 # shared catalog/frontmatter helpers
└── tests/
```

## Adding a skill

1. Create `skills/<skill-name>/SKILL.md`.
2. Use lowercase letters, numbers, and hyphens for the directory/name.
3. Add YAML frontmatter with `name` and a trigger-oriented `description`.
4. Keep large reference material in `references/` instead of bloating `SKILL.md`.
5. Run `python scripts/validate.py` and the test suite before opening a PR.

A separate catalog file is intentionally unnecessary: any valid `skills/*/SKILL.md` is automatically discovered by the installer.
