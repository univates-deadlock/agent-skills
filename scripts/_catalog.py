from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Skill:
    name: str
    description: str
    path: Path


class SkillMetadataError(ValueError):
    pass


def parse_frontmatter(skill_file: Path) -> dict[str, str]:
    text = skill_file.read_text(encoding="utf-8")
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        raise SkillMetadataError(f"{skill_file}: missing YAML frontmatter")

    try:
        end = next(i for i, line in enumerate(lines[1:], start=1) if line.strip() == "---")
    except StopIteration as exc:
        raise SkillMetadataError(f"{skill_file}: unterminated YAML frontmatter") from exc

    metadata: dict[str, str] = {}
    for raw_line in lines[1:end]:
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        metadata[key.strip()] = value.strip().strip('"').strip("'")
    return metadata


def load_skill(skill_dir: Path) -> Skill:
    skill_file = skill_dir / "SKILL.md"
    if not skill_file.is_file():
        raise SkillMetadataError(f"{skill_dir}: SKILL.md not found")
    metadata = parse_frontmatter(skill_file)
    name = metadata.get("name", "").strip()
    description = metadata.get("description", "").strip()
    if not name:
        raise SkillMetadataError(f"{skill_file}: missing 'name'")
    if not description:
        raise SkillMetadataError(f"{skill_file}: missing 'description'")
    return Skill(name=name, description=description, path=skill_dir)


def discover_skills(repo_root: Path) -> list[Skill]:
    skills_root = repo_root / "skills"
    if not skills_root.is_dir():
        return []

    skills: list[Skill] = []
    for skill_dir in sorted(path for path in skills_root.iterdir() if path.is_dir()):
        if (skill_dir / "SKILL.md").is_file():
            skills.append(load_skill(skill_dir))
    return sorted(skills, key=lambda skill: skill.name)
