#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import shutil
import sys
from dataclasses import dataclass
from pathlib import Path

try:
    from ._catalog import Skill, SkillMetadataError, discover_skills as _discover_skills
except ImportError:  # Direct execution: python scripts/install.py
    from _catalog import Skill, SkillMetadataError, discover_skills as _discover_skills


TARGET_DIRS = {
    "agents": Path(".agents") / "skills",
    "claude": Path(".claude") / "skills",
}


class ConflictError(RuntimeError):
    pass


@dataclass(frozen=True)
class InstallResult:
    skill: str
    target: str
    destination: Path
    status: str


def discover_skills(repo_root: Path) -> list[Skill]:
    return _discover_skills(Path(repo_root))


def _directory_digest(directory: Path) -> str:
    digest = hashlib.sha256()
    for path in sorted(p for p in directory.rglob("*") if p.is_file()):
        relative = path.relative_to(directory).as_posix().encode("utf-8")
        digest.update(relative)
        digest.update(b"\0")
        digest.update(path.read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()


def _resolve_skill(repo_root: Path, skill_name: str) -> Skill:
    matches = {skill.name: skill for skill in discover_skills(repo_root)}
    try:
        return matches[skill_name]
    except KeyError as exc:
        available = ", ".join(sorted(matches)) or "none"
        raise ValueError(f"Unknown skill '{skill_name}'. Available: {available}") from exc


def install_skill(
    catalog_root: Path,
    target_repo: Path,
    skill_name: str,
    targets: list[str],
    *,
    force: bool = False,
    dry_run: bool = False,
) -> list[InstallResult]:
    catalog_root = Path(catalog_root).resolve()
    target_repo = Path(target_repo).resolve()
    if not target_repo.is_dir():
        raise ValueError(f"Target repository does not exist or is not a directory: {target_repo}")

    skill = _resolve_skill(catalog_root, skill_name)
    unknown_targets = [target for target in targets if target not in TARGET_DIRS]
    if unknown_targets:
        raise ValueError(f"Unknown target(s): {', '.join(unknown_targets)}")

    results: list[InstallResult] = []
    source_digest = _directory_digest(skill.path)

    for target in targets:
        destination = target_repo / TARGET_DIRS[target] / skill.name
        if destination.exists():
            if not destination.is_dir():
                raise ConflictError(f"Destination exists and is not a directory: {destination}")
            if _directory_digest(destination) == source_digest:
                results.append(InstallResult(skill.name, target, destination, "up-to-date"))
                continue
            if not force:
                raise ConflictError(
                    f"Skill '{skill.name}' differs at {destination}. "
                    "Re-run with --force to replace it."
                )
            status = "would-update" if dry_run else "updated"
            if not dry_run:
                shutil.rmtree(destination)
                destination.parent.mkdir(parents=True, exist_ok=True)
                shutil.copytree(skill.path, destination)
        else:
            status = "would-install" if dry_run else "installed"
            if not dry_run:
                destination.parent.mkdir(parents=True, exist_ok=True)
                shutil.copytree(skill.path, destination)

        results.append(InstallResult(skill.name, target, destination, status))

    return results


def _parse_targets(value: str) -> list[str]:
    return ["agents", "claude"] if value == "both" else [value]


def _print_catalog(skills: list[Skill]) -> None:
    if not skills:
        print("No skills found.")
        return
    print("Available skills:\n")
    for index, skill in enumerate(skills, start=1):
        print(f"[{index}] {skill.name}")
        print(f"    {skill.description}")


def _interactive_selection(skills: list[Skill]) -> list[str]:
    _print_catalog(skills)
    if not skills:
        return []
    raw = input("\nSelect skills (comma-separated numbers/names, or 'all'): ").strip()
    if raw.lower() == "all":
        return [skill.name for skill in skills]

    by_name = {skill.name: skill.name for skill in skills}
    selected: list[str] = []
    for token in [part.strip() for part in raw.split(",") if part.strip()]:
        if token.isdigit() and 1 <= int(token) <= len(skills):
            name = skills[int(token) - 1].name
        elif token in by_name:
            name = token
        else:
            raise ValueError(f"Invalid skill selection: {token}")
        if name not in selected:
            selected.append(name)
    return selected


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Install Univates Deadlock agent skills into a repository.")
    parser.add_argument("--repo", type=Path, help="Target repository path")
    parser.add_argument("--skill", action="append", dest="skills", help="Skill name (repeatable)")
    parser.add_argument("--all", action="store_true", help="Install all available skills")
    parser.add_argument("--target", choices=["agents", "claude", "both"], help="Installation target")
    parser.add_argument("--list", action="store_true", help="List available skills and exit")
    parser.add_argument("--force", action="store_true", help="Replace a differing installed skill")
    parser.add_argument("--dry-run", action="store_true", help="Show what would change without writing files")
    return parser


def main(argv: list[str] | None = None) -> int:
    catalog_root = Path(__file__).resolve().parents[1]
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        skills = discover_skills(catalog_root)
        if args.list:
            _print_catalog(skills)
            return 0

        interactive = args.repo is None and not args.skills and not args.all and args.target is None
        if interactive:
            print("Univates Deadlock Agent Skills Installer\n")
            repo_raw = input("Target repository path: ").strip()
            if not repo_raw:
                raise ValueError("A target repository path is required")
            target_repo = Path(repo_raw).expanduser()
            selected = _interactive_selection(skills)
            target_raw = input("\nInstall for [agents/claude/both] (both): ").strip().lower() or "both"
            if target_raw not in {"agents", "claude", "both"}:
                raise ValueError(f"Invalid target: {target_raw}")
            targets = _parse_targets(target_raw)
            if not selected:
                raise ValueError("No skills selected")
            print("\nInstallation plan:")
            for name in selected:
                for target in targets:
                    print(f"  {name} -> {target_repo / TARGET_DIRS[target] / name}")
            if input("\nProceed? [Y/n] ").strip().lower() not in {"", "y", "yes"}:
                print("Cancelled.")
                return 0
        else:
            if args.repo is None:
                parser.error("--repo is required in non-interactive mode")
            target_repo = args.repo.expanduser()
            if args.all and args.skills:
                parser.error("Use either --all or --skill, not both")
            if args.all:
                selected = [skill.name for skill in skills]
            elif args.skills:
                selected = list(dict.fromkeys(args.skills))
            else:
                parser.error("Provide --skill NAME or --all")
            targets = _parse_targets(args.target or "both")

        all_results: list[InstallResult] = []
        for skill_name in selected:
            all_results.extend(
                install_skill(
                    catalog_root,
                    target_repo,
                    skill_name,
                    targets,
                    force=args.force,
                    dry_run=args.dry_run,
                )
            )

        print()
        for result in all_results:
            print(f"[{result.status}] {result.skill} -> {result.destination}")
        return 0
    except (ValueError, ConflictError, SkillMetadataError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
