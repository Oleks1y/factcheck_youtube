import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class SkillPackageTests(unittest.TestCase):
    def test_required_paths_exist(self) -> None:
        required_paths = [
            ROOT / "SKILL.md",
            ROOT / "agents" / "openai.yaml",
            ROOT / "references" / "claim-extraction.md",
            ROOT / "references" / "verification-methodology.md",
            ROOT / "scripts" / "extract-video-transcript.sh",
        ]

        missing = [str(path.relative_to(ROOT)) for path in required_paths if not path.exists()]
        self.assertEqual([], missing)

    def test_skill_frontmatter_and_codex_requirements(self) -> None:
        skill_text = (ROOT / "SKILL.md").read_text(encoding="utf-8")

        self.assertRegex(skill_text, r"(?s)^---\s*name:\s*factcheck_youtube\s+description:\s*>")
        self.assertIn("spawn_agent", skill_text)
        self.assertIn("official guidance", skill_text)
        self.assertIn("primary sources", skill_text)
        self.assertIn("factcheck_youtube-YYYY-MM-DD", skill_text)

    def test_openai_metadata_references_skill(self) -> None:
        metadata = (ROOT / "agents" / "openai.yaml").read_text(encoding="utf-8")

        self.assertIn('display_name: "factcheck_youtube"', metadata)
        self.assertIn('short_description: "Fact-check videos and produce sourced reports"', metadata)
        self.assertIn("$factcheck_youtube", metadata)
        self.assertRegex(metadata, r"allow_implicit_invocation:\s+true")

    def test_reference_docs_cover_extraction_and_verification(self) -> None:
        extraction = (ROOT / "references" / "claim-extraction.md").read_text(encoding="utf-8")
        verification = (
            ROOT / "references" / "verification-methodology.md"
        ).read_text(encoding="utf-8")

        self.assertIn("Claim Categories", extraction)
        self.assertIn("Verification queue", extraction)
        self.assertIn("Adversarial Search", verification)
        self.assertIn("Source hierarchy", verification)


if __name__ == "__main__":
    unittest.main()
