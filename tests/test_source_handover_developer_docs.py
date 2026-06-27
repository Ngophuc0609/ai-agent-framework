from __future__ import annotations

import subprocess
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
QUALITY_VALIDATOR = REPO_ROOT / ".ai/scripts/validate-source-code-handover-quality.py"


class DeveloperDocumentationContractTests(unittest.TestCase):
    def test_final_template_excludes_internal_audit_sections(self) -> None:
        template = (
            REPO_ROOT / ".ai/templates/source-code-handover/final-document-template.md"
        ).read_text(encoding="utf-8")

        for heading in ["## Hạn chế", "## Câu hỏi mở", "## Rủi ro", "## Trạng thái"]:
            self.assertNotIn(heading, template)

    def test_agent_9_keeps_twenty_documents_with_centralized_mapping(self) -> None:
        agent = (
            REPO_ROOT / ".ai/agents/agent-09-final-documentation-writer.md"
        ).read_text(encoding="utf-8")

        self.assertIn("exactly 20", agent)
        self.assertIn("17_known_risks.md", agent)
        self.assertIn("18_open_questions.md", agent)
        self.assertIn("19_evidence_index.md", agent)
        self.assertIn("20_documentation_coverage.md", agent)

    def test_quality_validator_keeps_centralized_mapping_documents(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            result = subprocess.run(
                [str(QUALITY_VALIDATOR), temporary_directory],
                check=False,
                capture_output=True,
                text=True,
            )

        output = result.stdout + result.stderr
        self.assertEqual(1, result.returncode)
        for name in [
            "17_known_risks.md",
            "18_open_questions.md",
            "19_evidence_index.md",
            "20_documentation_coverage.md",
        ]:
            self.assertIn(name, output)

    def test_quality_validator_does_not_require_audit_sections_in_topic_docs(self) -> None:
        expected_files = [
            "01_project_handover_full.md", "02_project_context.md",
            "03_repository_guide.md", "04_local_setup.md",
            "05_configuration_reference.md", "06_architecture.md",
            "07_database_reference.md", "08_auth_and_security.md",
            "09_api_catalog.md", "10_background_jobs.md",
            "11_realtime_signalr_socket.md", "12_external_integrations.md",
            "13_frontend_guide.md", "14_operations_runbook.md",
            "15_deployment_and_cicd.md", "16_testing_guide.md",
            "17_known_risks.md", "18_open_questions.md",
            "19_evidence_index.md", "20_documentation_coverage.md",
        ]
        with tempfile.TemporaryDirectory() as temporary_directory:
            final_dir = Path(temporary_directory)
            for name in expected_files:
                (final_dir / name).write_text(f"# {name}\n", encoding="utf-8")
            result = subprocess.run(
                [str(QUALITY_VALIDATOR), str(final_dir)],
                check=False,
                capture_output=True,
                text=True,
            )

        output = result.stdout + result.stderr
        self.assertNotIn("01_project_handover_full.md: missing section ## Hạn chế", output)
        self.assertNotIn("07_database_reference.md: missing section ## Câu hỏi mở", output)


if __name__ == "__main__":
    unittest.main()
