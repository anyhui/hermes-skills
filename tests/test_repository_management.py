import importlib
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

generate_catalog = importlib.import_module("scripts.generate_catalog")
validate_repo = importlib.import_module("scripts.validate_repo")


class RepositoryFixture(unittest.TestCase):
    def setUp(self):
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary_directory.name)
        subprocess.run(["git", "init", "-q", str(self.root)], check=True)

    def tearDown(self):
        self.temporary_directory.cleanup()

    def write(self, relative_path, content):
        path = self.root / relative_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        subprocess.run(["git", "add", "--", relative_path], cwd=self.root, check=True)

    def skill(self, directory, name=None, description="A useful test skill.", body="Body\n"):
        name = name or directory
        self.write(
            f"{directory}/SKILL.md",
            f"---\nname: {name}\ndescription: {description}\n---\n{body}",
        )

    def messages(self):
        return [issue.message for issue in validate_repo.validate(self.root, check_catalog=False)]


class ValidatorTests(RepositoryFixture):
    def test_rejects_malformed_frontmatter(self):
        self.write("broken/SKILL.md", "---\nname broken\ndescription: Missing colon\n---\n")
        self.assertTrue(any("frontmatter" in message for message in self.messages()))

    def test_rejects_duplicate_names(self):
        self.skill("first", name="same-name")
        self.skill("second", name="same-name")
        self.assertTrue(any("duplicate skill name" in message for message in self.messages()))

    def test_rejects_broken_local_markdown_link(self):
        self.skill("linked", body="See [missing](references/missing.md).\n")
        self.assertTrue(any("broken local link" in message for message in self.messages()))

    def test_detects_actual_secret_fixture(self):
        secret = "gh" + "p_" + ("A" * 36)
        self.write("credential.txt", f"token={secret}\n")
        self.assertTrue(any("possible secret" in message for message in self.messages()))

    def test_rejects_stale_catalog(self):
        self.skill("catalog-test")
        self.write("CATALOG.md", "stale\n")
        issues = validate_repo.validate(self.root, check_catalog=True)
        self.assertTrue(any(issue.code == "catalog-stale" for issue in issues))


class CatalogTests(RepositoryFixture):
    def test_catalog_is_deterministic_and_reports_static_status_only(self):
        self.skill("lark-example", description="Example integration.")
        first = generate_catalog.render_catalog(self.root)
        second = generate_catalog.render_catalog(self.root)
        self.assertEqual(first, second)
        self.assertIn("静态检查", first)
        self.assertNotIn("运行时已测试", first)


if __name__ == "__main__":
    unittest.main()
