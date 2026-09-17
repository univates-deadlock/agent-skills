import tempfile
import unittest
from pathlib import Path

from scripts.validate import validate_repository, validate_skill


class ValidationTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def write_skill(self, dirname: str, content: str) -> Path:
        skill_dir = self.root / "skills" / dirname
        skill_dir.mkdir(parents=True)
        (skill_dir / "SKILL.md").write_text(content, encoding="utf-8")
        return skill_dir

    def test_valid_skill_has_no_errors(self):
        skill = self.write_skill(
            "good-skill",
            "---\nname: good-skill\ndescription: Use when a good skill is needed.\n---\n\n# Good Skill\n",
        )
        self.assertEqual(validate_skill(skill), [])

    def test_missing_frontmatter_is_reported(self):
        skill = self.write_skill("bad-skill", "# Bad Skill\n")
        errors = validate_skill(skill)
        self.assertTrue(any("frontmatter" in error.lower() for error in errors))

    def test_directory_must_match_skill_name(self):
        skill = self.write_skill(
            "folder-name",
            "---\nname: another-name\ndescription: Use when testing mismatched names.\n---\n",
        )
        errors = validate_skill(skill)
        self.assertTrue(any("directory" in error.lower() for error in errors))

    def test_repository_validates_all_skill_directories(self):
        self.write_skill(
            "good-skill",
            "---\nname: good-skill\ndescription: Use when a good skill is needed.\n---\n",
        )
        self.write_skill("bad-skill", "# Missing metadata\n")
        result = validate_repository(self.root)
        self.assertIn("good-skill", result)
        self.assertIn("bad-skill", result)
        self.assertEqual(result["good-skill"], [])
        self.assertTrue(result["bad-skill"])


if __name__ == "__main__":
    unittest.main()
