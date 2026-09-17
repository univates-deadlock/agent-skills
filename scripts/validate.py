#!/usr/bin/env python3
from __future__ import annotations

import re
import sys
from pathlib import Path

try:
    from ._catalog import SkillMetadataError, load_skill
except ImportError:  # Direct execution: python scripts/validate.py
    from _catalog import SkillMetadataError, load_skill


NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def validate_skill(skill_dir: Path) -> list[str]:
    skill_dir = Path(skill_dir)
    errors: list[str] = []
    skill_file = skill_dir / "SKILL.md"
    if not skill_file.is_file():
        return ["SKILL.md not found"]

    try:
        skill = load_skill(skill_dir)
    except SkillMetadataError as exc:
        return [str(exc)]

    if skill.name != skill_dir.name:
        errors.append(f"Skill name '{skill.name}' must match directory '{skill_dir.name}'")
    if not NAME_RE.fullmatch(skill.name):
        errors.append("Skill name must contain only lowercase letters, numbers, and hyphens")
    if not skill.description.startswith("Use when"):
        errors.append("Description should start with 'Use when' and describe trigger conditions")

    text = skill_file.read_text(encoding="utf-8")
    frontmatter_end = text.find("\n---", 4)
    if frontmatter_end != -1 and len(text[: frontmatter_end + 4]) > 1024:
        errors.append("YAML frontmatter should stay under 1024 characters")
    return errors


def validate_repository(repo_root: Path) -> dict[str, list[str]]:
    skills_root = Path(repo_root) / "skills"
    if not skills_root.is_dir():
        return {}
    return {
        skill_dir.name: validate_skill(skill_dir)
        for skill_dir in sorted(path for path in skills_root.iterdir() if path.is_dir())
    }


def main() -> int:
    repo_root = Path(__file__).resolve().parents[1]
    results = validate_repository(repo_root)
    if not results:
        print("No skills found.")
        return 1

    has_errors = False
    for name, errors in results.items():
        if errors:
            has_errors = True
            print(f"[FAIL] {name}")
            for error in errors:
                print(f"  - {error}")
        else:
            print(f"[OK]   {name}")
    return 1 if has_errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
