import tempfile
import unittest
from pathlib import Path

from scripts.install import ConflictError, discover_skills, install_skill


SKILL_TEXT = """---
name: example-skill
description: Use when testing the installer.
---

# Example Skill
"""


class InstallerTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.catalog = self.root / "catalog"
        self.target = self.root / "target"
        (self.catalog / "skills" / "example-skill" / "references").mkdir(parents=True)
        self.target.mkdir()
        (self.catalog / "skills" / "example-skill" / "SKILL.md").write_text(SKILL_TEXT, encoding="utf-8")
        (self.catalog / "skills" / "example-skill" / "references" / "guide.md").write_text("guide\n", encoding="utf-8")

    def tearDown(self):
        self.tmp.cleanup()

    def test_discovers_skills_from_skill_directories(self):
        skills = discover_skills(self.catalog)
        self.assertEqual([s.name for s in skills], ["example-skill"])
        self.assertEqual(skills[0].description, "Use when testing the installer.")

    def test_installs_skill_for_agents_target(self):
        result = install_skill(self.catalog, self.target, "example-skill", ["agents"])
        installed = self.target / ".agents" / "skills" / "example-skill"
        self.assertEqual(result[0].status, "installed")
        self.assertTrue((installed / "SKILL.md").exists())
        self.assertEqual((installed / "references" / "guide.md").read_text(encoding="utf-8"), "guide\n")

    def test_installs_skill_for_both_targets(self):
        install_skill(self.catalog, self.target, "example-skill", ["agents", "claude"])
        self.assertTrue((self.target / ".agents" / "skills" / "example-skill" / "SKILL.md").exists())
        self.assertTrue((self.target / ".claude" / "skills" / "example-skill" / "SKILL.md").exists())

    def test_identical_existing_skill_is_up_to_date(self):
        install_skill(self.catalog, self.target, "example-skill", ["agents"])
        result = install_skill(self.catalog, self.target, "example-skill", ["agents"])
        self.assertEqual(result[0].status, "up-to-date")

    def test_different_existing_skill_requires_force(self):
        install_skill(self.catalog, self.target, "example-skill", ["agents"])
        installed = self.target / ".agents" / "skills" / "example-skill" / "SKILL.md"
        installed.write_text("local modification\n", encoding="utf-8")
        with self.assertRaises(ConflictError):
            install_skill(self.catalog, self.target, "example-skill", ["agents"])

    def test_force_replaces_different_existing_skill(self):
        install_skill(self.catalog, self.target, "example-skill", ["agents"])
        installed = self.target / ".agents" / "skills" / "example-skill" / "SKILL.md"
        installed.write_text("local modification\n", encoding="utf-8")
        result = install_skill(self.catalog, self.target, "example-skill", ["agents"], force=True)
        self.assertEqual(result[0].status, "updated")
        self.assertEqual(installed.read_text(encoding="utf-8"), SKILL_TEXT)

    def test_dry_run_does_not_write_files(self):
        result = install_skill(self.catalog, self.target, "example-skill", ["agents"], dry_run=True)
        self.assertEqual(result[0].status, "would-install")
        self.assertFalse((self.target / ".agents").exists())


if __name__ == "__main__":
    unittest.main()
