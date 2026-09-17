import unittest
from pathlib import Path

from scripts.install import discover_skills
from scripts.validate import validate_repository


class RepositorySkillTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.root = Path(__file__).resolve().parents[1]

    def test_repository_contains_expected_initial_skill(self):
        names = [skill.name for skill in discover_skills(self.root)]
        self.assertIn("developing-vanilla-web-interfaces", names)

    def test_all_repository_skills_pass_metadata_validation(self):
        results = validate_repository(self.root)
        failures = {name: errors for name, errors in results.items() if errors}
        self.assertEqual(failures, {})

    def test_initial_skill_references_existing_reference_files(self):
        skill_dir = self.root / "skills" / "developing-vanilla-web-interfaces"
        expected = {
            "bem.md",
            "css-architecture.md",
            "components.md",
            "accessibility.md",
        }
        actual = {path.name for path in (skill_dir / "references").glob("*.md")}
        self.assertEqual(actual, expected)


if __name__ == "__main__":
    unittest.main()
