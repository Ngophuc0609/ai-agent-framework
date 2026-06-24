#!/usr/bin/env python3
"""Validate final source-code handover docs against the quality checklist."""

from __future__ import annotations

import re
import sys
from pathlib import Path


EXPECTED_FILES = [
    "01_project_handover_full.md",
    "02_project_context.md",
    "03_repository_guide.md",
    "04_local_setup.md",
    "05_configuration_reference.md",
    "06_architecture.md",
    "07_database_reference.md",
    "08_auth_and_security.md",
    "09_api_catalog.md",
    "10_background_jobs.md",
    "11_realtime_signalr_socket.md",
    "12_external_integrations.md",
    "13_frontend_guide.md",
    "14_operations_runbook.md",
    "15_deployment_and_cicd.md",
    "16_testing_guide.md",
    "17_known_risks.md",
    "18_open_questions.md",
    "19_evidence_index.md",
    "20_documentation_coverage.md",
]

REQUIRED_FRONT_MATTER = [
    "document_id",
    "title",
    "run_id",
    "source_commit",
    "source_branch",
    "status",
    "primary_owner_agent",
    "evidence_ids",
    "last_verified_at",
]

REQUIRED_SECTIONS = [
    "## Phạm vi",
    "## Trạng thái",
    "## Nguồn dữ liệu / Evidence",
    "## Nội dung chính",
    "## Hạn chế",
    "## Câu hỏi mở",
    "## Rủi ro",
]

ALLOWED_LABELS = {
    "CONFIRMED",
    "INFERRED",
    "UNVERIFIED",
    "CONFLICT",
    "NOT_APPLICABLE",
    "BLOCKED",
    "UPSTREAM_REFERENCE",
    "DECISION",
}

ALLOWED_STATUS = {"Ready", "Partial", "Blocked", "Not Applicable"}

FORBIDDEN_PATTERNS = [
    r"\bdotnet\s+new\b",
    r"\bexample\.com\b",
    r"\bPassword123\b",
    r"\bSecret123\b",
    r"\byour-api-key\b",
    r"\byour-client-secret\b",
    r"\bHangfire\s+or\s+Quartz\b",
    r"\bHangfire\s+hoặc\s+Quartz\b",
    r"\bRedis\s+or\s+some\s+cache\b",
    r"\bRedis\s+hoặc\s+cache\s+nào\s+đó\b",
    r"\bNotificationHub\b",
    r"\bReceiveMessage\b",
    r"\bsample only\b",
    r"\bexample only\b",
    r"\bPayPal\b",
    r"\bPatreon\b",
    r"\bGitter\b",
    r"Security should be improved",
    r"How does production work\?",
    r"\|\s*API\s*\|\s*Many\s*\|\s*Most\s*\|\s*Good\s*\|",
]

EVIDENCE_RE = re.compile(r"\bEV-(?:REPO|CONFIG|DB|MIGRATION|AUTH|API|JOB|RT|OPS|CICD|TEST|NEG(?:-[A-Z]+)?)-\d{3}\b")
LABEL_RE = re.compile(r"\[([A-Z_]+)\]")
LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+\.md(?:#[^)]+)?)\)")


def split_front_matter(text: str) -> tuple[dict[str, str], str] | tuple[None, str]:
    if not text.startswith("---\n"):
        return None, text
    end = text.find("\n---", 4)
    if end == -1:
        return None, text
    raw = text[4:end].strip().splitlines()
    data: dict[str, str] = {}
    current_key = None
    for line in raw:
        if not line.strip():
            continue
        if re.match(r"^\s+-\s+", line):
            if current_key:
                data[current_key] = data.get(current_key, "") + "\n" + line.strip()
            continue
        if ":" in line:
            key, value = line.split(":", 1)
            current_key = key.strip()
            data[current_key] = value.strip().strip('"')
    body_start = text.find("\n", end + 4)
    return data, text[body_start + 1 :] if body_start != -1 else ""


def line_has_upstream_reference(text: str, match_start: int) -> bool:
    line_start = text.rfind("\n", 0, match_start) + 1
    line_end = text.find("\n", match_start)
    if line_end == -1:
        line_end = len(text)
    if "[UPSTREAM_REFERENCE]" in text[line_start:line_end]:
        return True
    prior_context_start = max(0, text.rfind("\n##", 0, match_start))
    prior_context = text[prior_context_start:match_start]
    return "[UPSTREAM_REFERENCE]" in prior_context


def collect_evidence_index(final_dir: Path, errors: list[str]) -> set[str]:
    evidence_file = final_dir / "19_evidence_index.md"
    if not evidence_file.exists():
        errors.append("missing 19_evidence_index.md")
        return set()
    text = evidence_file.read_text(encoding="utf-8")
    required_headers = [
        "Evidence ID",
        "Topic",
        "Claim",
        "Source path",
        "Line/method",
        "Verification type",
        "Source commit",
        "Status",
    ]
    for header in required_headers:
        if header not in text:
            errors.append(f"19_evidence_index.md missing column/header: {header}")
    return set(EVIDENCE_RE.findall(text))


def validate_links(path: Path, text: str, final_dir: Path, errors: list[str]) -> None:
    for match in LINK_RE.finditer(text):
        target = match.group(1)
        if target.startswith(("http://", "https://", "mailto:")):
            continue
        target_path = target.split("#", 1)[0]
        resolved = (path.parent / target_path).resolve()
        try:
            resolved.relative_to(final_dir.resolve())
        except ValueError:
            continue
        if not resolved.exists():
            errors.append(f"{path.name}: broken markdown link to {target_path}")


def validate_document(path: Path, final_dir: Path, indexed_ids: set[str], errors: list[str]) -> None:
    text = path.read_text(encoding="utf-8")
    front_matter, body = split_front_matter(text)
    expected_doc_id = f"DOC-{path.name[:2]}"
    if front_matter is None:
        errors.append(f"{path.name}: missing YAML front matter")
    else:
        for key in REQUIRED_FRONT_MATTER:
            if key not in front_matter or not front_matter[key]:
                errors.append(f"{path.name}: missing front matter key {key}")
        if front_matter.get("document_id") != expected_doc_id:
            errors.append(f"{path.name}: document_id must be {expected_doc_id}")
        status = front_matter.get("status", "")
        if status and status not in ALLOWED_STATUS:
            errors.append(f"{path.name}: invalid status {status!r}")

    for section in REQUIRED_SECTIONS:
        if section not in body:
            errors.append(f"{path.name}: missing section {section}")

    for label in LABEL_RE.findall(text):
        if label.startswith("EV-"):
            continue
        if label not in ALLOWED_LABELS:
            errors.append(f"{path.name}: invalid claim label [{label}]")

    used_ids = set(EVIDENCE_RE.findall(text))
    for evidence_id in sorted(used_ids - indexed_ids):
        errors.append(f"{path.name}: evidence id not indexed in 19_evidence_index.md: {evidence_id}")

    if front_matter is not None:
        front_matter_ids = set(EVIDENCE_RE.findall(front_matter.get("evidence_ids", "")))
        for evidence_id in sorted(front_matter_ids - indexed_ids):
            errors.append(f"{path.name}: front matter evidence id not indexed: {evidence_id}")

    if "[NOT_APPLICABLE]" in text:
        if "EV-NEG" not in text:
            errors.append(f"{path.name}: [NOT_APPLICABLE] without EV-NEG evidence")
        required_negative_details = [
            ("source roots", ["Source roots", "Source roots đã kiểm tra"]),
            ("search patterns", ["Search patterns", "Pattern đã tìm"]),
            ("command/tool", ["Command", "Command/tool", "Lệnh/công cụ"]),
            ("result", ["Kết quả", "Result"]),
            ("impact", ["Tác động", "Impact"]),
        ]
        for detail_name, accepted_tokens in required_negative_details:
            if not any(token in text for token in accepted_tokens):
                errors.append(f"{path.name}: [NOT_APPLICABLE] missing negative-evidence detail: {detail_name}")

    for pattern in FORBIDDEN_PATTERNS:
        for match in re.finditer(pattern, text, flags=re.IGNORECASE):
            if not line_has_upstream_reference(text, match.start()):
                errors.append(f"{path.name}: forbidden pattern without [UPSTREAM_REFERENCE]: {match.group(0)}")

    validate_links(path, text, final_dir, errors)


def validate_handover_links(final_dir: Path, errors: list[str]) -> None:
    path = final_dir / "01_project_handover_full.md"
    if not path.exists():
        return
    text = path.read_text(encoding="utf-8")
    for expected in EXPECTED_FILES[1:]:
        if expected not in text:
            errors.append(f"01_project_handover_full.md missing relative link/reference to {expected}")


def validate_coverage(final_dir: Path, errors: list[str]) -> None:
    path = final_dir / "20_documentation_coverage.md"
    if not path.exists():
        return
    text = path.read_text(encoding="utf-8")
    for token in ["Discovered", "Documented", "Unresolved", "N/A", "Excluded", "Accounted", "Gaps"]:
        if token not in text:
            errors.append(f"20_documentation_coverage.md missing coverage column/token: {token}")
    for domain in [
        "Repository",
        "Entry",
        "Config",
        "DbContext",
        "Entity",
        "Migration",
        "API",
        "Background",
        "SignalR",
        "Docker",
        "CI/CD",
        "Integration",
        "Test",
    ]:
        if domain.lower() not in text.lower():
            errors.append(f"20_documentation_coverage.md missing minimum domain hint: {domain}")


def validate_document_capabilities(final_dir: Path, errors: list[str]) -> None:
    combined = "\n".join(path.read_text(encoding="utf-8") for path in final_dir.glob("*.md"))
    required_tokens = {
        "system purpose": ["Mục đích hệ thống", "System purpose"],
        "user/client groups": ["Nhóm người dùng", "Actor/client", "User / Client"],
        "module inventory": ["| Module | Chức năng | API | Tables | Redis | Jobs | Risk | Evidence | Status |"],
        "project inventory": ["| Project name | Project path | Project type | Target framework | Startup point"],
        "external systems": ["External system", "Hệ thống tích hợp"],
        "dependency compatibility": ["| Dependency | Current Version | Used By | Purpose | .NET 8 Compatibility"],
        "configuration mapping": ["| Key | Purpose | Environment | Required/Optional | Secret/Non-secret | Legacy location | .NET 8 target location"],
        "architecture flow": ["Application layers", "Request lifecycle", "HTTP Request"],
        "C4 diagrams": ["C1 System Context", "C2 Container Diagram", "C3 Component Diagram"],
        "business rules": ["Rule ID: BR-", "Business rule"],
        "api contract matrix": ["| API ID | Route | Method | Module | Auth | Permission | Content type"],
        "migration safety": ["Must not change", "Baseline proof", "Rollback plan"],
        "redis/cache behavior": ["Redis", "Cache"],
        "jobs/queues behavior": ["Jobs", "Queue"],
        "auth checks": ["Authentication", "Authorization"],
    }
    for capability, tokens in required_tokens.items():
        if not any(token in combined for token in tokens):
            errors.append(f"final documentation set missing capability: {capability}")

    generic_patterns = [
        r"Module\s+\w+\s+quản lý\s+[^.\n]+\.?\s*$",
        r"\bmanage[s]?\s+\w+\s*$",
        r"\bhandles\s+\w+\s*$",
    ]
    for pattern in generic_patterns:
        if re.search(pattern, combined, flags=re.IGNORECASE | re.MULTILINE):
            errors.append(f"final documentation contains likely generic module description matching: {pattern}")


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: validate-source-code-handover-quality.py <final_dir>")
        return 2
    final_dir = Path(sys.argv[1])
    errors: list[str] = []
    if not final_dir.is_dir():
        print(f"FAIL: final directory not found: {final_dir}")
        return 1

    actual_files = sorted(path.name for path in final_dir.glob("*.md"))
    if actual_files != EXPECTED_FILES:
        missing = sorted(set(EXPECTED_FILES) - set(actual_files))
        extra = sorted(set(actual_files) - set(EXPECTED_FILES))
        if missing:
            errors.append(f"missing final docs: {', '.join(missing)}")
        if extra:
            errors.append(f"unexpected final docs: {', '.join(extra)}")

    indexed_ids = collect_evidence_index(final_dir, errors)
    for name in EXPECTED_FILES:
        path = final_dir / name
        if path.exists():
            validate_document(path, final_dir, indexed_ids, errors)
    validate_handover_links(final_dir, errors)
    validate_coverage(final_dir, errors)
    validate_document_capabilities(final_dir, errors)

    if errors:
        print("FAIL: source-code handover quality checklist failed")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Quality checklist passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
