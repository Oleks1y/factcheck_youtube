import os
import stat
import subprocess
import tempfile
import textwrap
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "extract-video-transcript.sh"


def make_executable(path: Path, contents: str) -> None:
    path.write_text(contents, encoding="utf-8")
    path.chmod(path.stat().st_mode | stat.S_IXUSR)


class ExtractVideoTranscriptTests(unittest.TestCase):
    def run_script(self, summarize_body: str):
        with tempfile.TemporaryDirectory() as temp_dir:
            bin_dir = Path(temp_dir) / "bin"
            bin_dir.mkdir()
            make_executable(
                bin_dir / "summarize",
                "#!/usr/bin/env bash\nset -euo pipefail\n" + summarize_body,
            )

            output_path = Path(temp_dir) / "transcript.txt"
            env = os.environ.copy()
            env["PATH"] = f"{bin_dir}:{env['PATH']}"

            result = subprocess.run(
                ["bash", str(SCRIPT), "https://www.youtube.com/watch?v=test", str(output_path)],
                cwd=ROOT,
                env=env,
                text=True,
                capture_output=True,
            )
            output = output_path.read_text(encoding="utf-8") if output_path.exists() else ""
            return result, output

    def test_prefers_raw_extract_output(self) -> None:
        result, output = self.run_script(
            textwrap.dedent(
                """
                if [[ "$*" == *"--extract"* && "$*" != *"yt-dlp"* ]]; then
                  printf 'Raw transcript line. 0123456789 %.0s' {1..8}
                  exit 0
                fi
                exit 1
                """
            )
        )

        self.assertEqual(0, result.returncode, msg=result.stderr)
        self.assertIn("Raw transcript line.", output)
        self.assertNotIn("LLM-generated summary", output)

    def test_falls_back_to_ytdlp_extract(self) -> None:
        result, output = self.run_script(
            textwrap.dedent(
                """
                if [[ "$*" == *"--extract"* && "$*" != *"yt-dlp"* ]]; then
                  printf 'short'
                  exit 0
                fi
                if [[ "$*" == *"--youtube yt-dlp --extract"* ]]; then
                  printf 'Fallback transcript line. 0123456789 %.0s' {1..8}
                  exit 0
                fi
                exit 1
                """
            )
        )

        self.assertEqual(0, result.returncode, msg=result.stderr)
        self.assertIn("Fallback transcript line.", output)

    def test_marks_summary_fallback(self) -> None:
        result, output = self.run_script(
            textwrap.dedent(
                """
                if [[ "$*" == *"--extract"* ]]; then
                  exit 1
                fi
                if [[ "$*" == *"--length xxl"* ]]; then
                  printf 'Model summary line. 0123456789 %.0s' {1..4}
                  exit 0
                fi
                exit 1
                """
            )
        )

        self.assertEqual(0, result.returncode, msg=result.stderr)
        self.assertIn("LLM-generated summary", output)
        self.assertIn("Model summary line.", output)


if __name__ == "__main__":
    unittest.main()
