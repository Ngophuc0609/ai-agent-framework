from __future__ import annotations

import hashlib
import json
import subprocess
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SYNC_SCRIPT = REPO_ROOT / "bin" / "ai-agent-adapter-sync"


class AdapterSyncTestCase(unittest.TestCase):
    def run_sync(
        self, *args: str, include_skills: bool = False
    ) -> tuple[subprocess.CompletedProcess[str], Path]:
        temporary_directory = tempfile.TemporaryDirectory()
        self.addCleanup(temporary_directory.cleanup)
        target = Path(temporary_directory.name)
        (target / ".ai").mkdir()
        command = [str(SYNC_SCRIPT), str(target), *args]
        if include_skills:
            skill_directory = target / ".ai/skills/sample-skill"
            skill_directory.mkdir(parents=True)
            (skill_directory / "SKILL.md").write_text(
                "---\n"
                "name: sample-skill\n"
                "description: Use when validating adapter skill output.\n"
                "---\n\n"
                "# Sample Skill\n",
                encoding="utf-8",
            )
        else:
            command.append("--no-skills")

        result = subprocess.run(
            command,
            check=False,
            capture_output=True,
            text=True,
        )
        return result, target


class AdapterSyncCodexTests(AdapterSyncTestCase):

    def test_default_generation_assigns_agents_md_to_codex(self) -> None:
        result, target = self.run_sync()

        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        content = (target / "AGENTS.md").read_text(encoding="utf-8")
        self.assertIn("# .ai Framework Instructions for codex", content)
        self.assertNotIn("duplicate target already handled: " + str(target / "AGENTS.md"), result.stdout)

    def test_explicit_codex_generation_uses_codex_header(self) -> None:
        result, target = self.run_sync("--agent", "codex")

        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        content = (target / "AGENTS.md").read_text(encoding="utf-8")
        self.assertIn("# .ai Framework Instructions for codex", content)

    def test_explicit_portable_agents_alias_remains_available(self) -> None:
        result, target = self.run_sync("--agent", "agents")

        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        content = (target / "AGENTS.md").read_text(encoding="utf-8")
        self.assertIn("# .ai Framework Instructions for agents", content)


class AdapterSyncNativeFormatTests(AdapterSyncTestCase):
    def test_cursor_rules_have_native_activation_frontmatter(self) -> None:
        result, target = self.run_sync("--agent", "cursor")

        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        always_rule = (target / ".cursor/rules/00-ai-framework.mdc").read_text(encoding="utf-8")
        self.assertFalse((target / ".cursor/rules/99-ai-framework-bundle.mdc").exists())
        self.assertTrue(always_rule.startswith("---\nalwaysApply: true\n---\n"))
        self.assertNotIn("Materialized .ai Rule Bundle", always_rule)

    def test_claude_deep_bundle_is_path_scoped(self) -> None:
        result, target = self.run_sync("--agent", "claude")

        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        compact = (target / "CLAUDE.md").read_text(encoding="utf-8")
        deep_rule = (target / ".claude/rules/00-ai-framework.md").read_text(encoding="utf-8")
        self.assertLess(len(compact.splitlines()), 100)
        self.assertTrue(
            deep_rule.startswith(
                "---\npaths:\n  - \".ai/**/*\"\n  - \"bin/ai-agent-*\"\n---\n"
            )
        )
        self.assertNotIn("Materialized .ai Rule Bundle", deep_rule)

    def test_copilot_deep_bundle_is_path_scoped(self) -> None:
        result, target = self.run_sync("--agent", "copilot")

        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        compact = (target / ".github/copilot-instructions.md").read_text(encoding="utf-8")
        deep_rule = (target / ".github/instructions/ai-framework.instructions.md").read_text(encoding="utf-8")
        self.assertLess(len(compact.splitlines()), 100)
        self.assertTrue(deep_rule.startswith('---\napplyTo: ".ai/**,bin/ai-agent-*"\n---\n'))
        self.assertNotIn("Materialized .ai Rule Bundle", deep_rule)

    def test_native_skill_directories_preserve_frontmatter(self) -> None:
        targets = {
            "cursor": ".agents/skills/sample-skill/SKILL.md",
            "claude": ".claude/skills/sample-skill/SKILL.md",
            "copilot": ".github/skills/sample-skill/SKILL.md",
        }

        for agent, relative_path in targets.items():
            with self.subTest(agent=agent):
                result, target = self.run_sync(
                    "--agent", agent, include_skills=True
                )
                self.assertEqual(0, result.returncode, result.stdout + result.stderr)
                content = (target / relative_path).read_text(encoding="utf-8")
                self.assertTrue(
                    content.startswith(
                        "---\n"
                        "name: sample-skill\n"
                        "description: Use when validating adapter skill output.\n"
                        "---\n\n"
                        "<!-- generated-by: ai-agent-adapter-sync -->\n"
                    )
                )


class AdapterSyncPointerModeTests(AdapterSyncTestCase):
    INSTRUCTION_PATHS = {
        "codex": ["AGENTS.md"],
        "cursor": [".cursor/rules/00-ai-framework.mdc"],
        "copilot": [
            ".github/copilot-instructions.md",
            ".github/instructions/ai-framework.instructions.md",
        ],
        "claude": ["CLAUDE.md", ".claude/rules/00-ai-framework.md"],
        "cline": [".clinerules/00-ai-framework.md"],
        "antigravity": [
            "GEMINI.md",
            ".agent/rules/00-ai-framework.md",
            ".agents/AGENTS.md",
        ],
    }

    MANIFEST_PATHS = {
        "codex": ".agents/00-ai-framework.manifest.json",
        "cursor": ".cursor/rules/00-ai-framework.manifest.json",
        "copilot": ".github/instructions/00-ai-framework.manifest.json",
        "claude": ".claude/rules/00-ai-framework.manifest.json",
        "cline": ".clinerules/00-ai-framework.manifest.json",
        "antigravity": ".agent/rules/00-ai-framework.manifest.json",
    }

    def seed_framework_source(self, target: Path, agent: str) -> None:
        files = {
            ".ai/README.md": "# Framework\n",
            ".ai/BOOTSTRAP_ONCE.md": "# Setup only\n",
            ".ai/registry/triggers.yml": "triggers: []\n",
            ".ai/rules/00-global-rules.md": "# Global\n",
            ".ai/rules/15-agent-runtime-tool-policy.md": "# Tools\n",
            f".ai/adapters/{agent}.md": f"# {agent}\n",
        }
        for relative_path, content in files.items():
            path = target / relative_path
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")

    def test_default_outputs_are_bounded_pointer_files(self) -> None:
        for agent, paths in self.INSTRUCTION_PATHS.items():
            with self.subTest(agent=agent):
                result, target = self.run_sync("--agent", agent)
                self.assertEqual(0, result.returncode, result.stdout + result.stderr)
                for relative_path in paths:
                    content = (target / relative_path).read_text(encoding="utf-8")
                    self.assertLessEqual(len(content.splitlines()), 250)
                    self.assertLessEqual(len(content.encode("utf-8")), 12000)
                    self.assertNotIn("Materialized .ai Rule Bundle", content)
                    self.assertNotIn("<!-- BEGIN SOURCE:", content)
                    self.assertNotIn(".ai/BOOTSTRAP_ONCE.md", content)

    def test_manifest_contains_source_checksums(self) -> None:
        result, target = self.run_sync("--agent", "cline")
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.seed_framework_source(target, "cline")

        result = subprocess.run(
            [str(SYNC_SCRIPT), str(target), "--agent", "cline", "--no-skills"],
            check=False,
            capture_output=True,
            text=True,
        )

        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        manifest_path = target / self.MANIFEST_PATHS["cline"]
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        self.assertEqual(1, manifest["schema_version"])
        self.assertEqual("cline", manifest["agent"])
        self.assertEqual("pointer", manifest["mode"])
        self.assertEqual("2", manifest["framework_version"])
        self.assertEqual("ai-agent-adapter-sync", manifest["generator"]["name"])
        self.assertRegex(manifest["generator"]["version"], r"^\d+\.\d+$")
        self.assertIn("source_commit", manifest)
        sources = {entry["path"]: entry["sha256"] for entry in manifest["sources"]}
        source_path = target / ".ai/rules/00-global-rules.md"
        expected_hash = hashlib.sha256(source_path.read_bytes()).hexdigest()
        self.assertEqual(expected_hash, sources[".ai/rules/00-global-rules.md"])

    def test_check_detects_source_drift_without_writing(self) -> None:
        temporary_directory = tempfile.TemporaryDirectory()
        self.addCleanup(temporary_directory.cleanup)
        target = Path(temporary_directory.name)
        (target / ".ai").mkdir()
        self.seed_framework_source(target, "cline")
        generate = subprocess.run(
            [str(SYNC_SCRIPT), str(target), "--agent", "cline", "--no-skills"],
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(0, generate.returncode, generate.stdout + generate.stderr)
        instruction = target / ".clinerules/00-ai-framework.md"
        before = instruction.read_bytes()

        clean_check = subprocess.run(
            [str(SYNC_SCRIPT), str(target), "--agent", "cline", "--no-skills", "--check"],
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(0, clean_check.returncode, clean_check.stdout + clean_check.stderr)
        self.assertEqual(before, instruction.read_bytes())

        source = target / ".ai/rules/00-global-rules.md"
        source.write_text("# Changed\n", encoding="utf-8")
        drift_check = subprocess.run(
            [str(SYNC_SCRIPT), str(target), "--agent", "cline", "--no-skills", "--check"],
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(1, drift_check.returncode)
        self.assertIn("DRIFT", drift_check.stdout)
        self.assertEqual(before, instruction.read_bytes())

    def test_materialized_mode_is_explicit(self) -> None:
        result, target = self.run_sync("--agent", "cline", "--materialized")

        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        content = (target / ".clinerules/00-ai-framework.md").read_text(encoding="utf-8")
        self.assertIn("## Materialized .ai Rule Bundle", content)

    def test_pointer_mode_removes_generated_legacy_cursor_bundle(self) -> None:
        temporary_directory = tempfile.TemporaryDirectory()
        self.addCleanup(temporary_directory.cleanup)
        target = Path(temporary_directory.name)
        (target / ".ai").mkdir()
        bundle = target / ".cursor/rules/99-ai-framework-bundle.mdc"
        bundle.parent.mkdir(parents=True)
        bundle.write_text(
            "<!-- generated-by: ai-agent-adapter-sync -->\nlegacy\n",
            encoding="utf-8",
        )

        result = subprocess.run(
            [str(SYNC_SCRIPT), str(target), "--agent", "cursor", "--no-skills"],
            check=False,
            capture_output=True,
            text=True,
        )

        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertFalse(bundle.exists())

    def test_pointer_mode_preserves_user_legacy_cursor_bundle(self) -> None:
        temporary_directory = tempfile.TemporaryDirectory()
        self.addCleanup(temporary_directory.cleanup)
        target = Path(temporary_directory.name)
        (target / ".ai").mkdir()
        bundle = target / ".cursor/rules/99-ai-framework-bundle.mdc"
        bundle.parent.mkdir(parents=True)
        bundle.write_text("# User rule\n", encoding="utf-8")

        result = subprocess.run(
            [str(SYNC_SCRIPT), str(target), "--agent", "cursor", "--no-skills"],
            check=False,
            capture_output=True,
            text=True,
        )

        self.assertEqual(1, result.returncode)
        self.assertIn("SKIP obsolete user file", result.stdout)
        self.assertEqual("# User rule\n", bundle.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
