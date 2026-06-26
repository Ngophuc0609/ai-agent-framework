#!/usr/bin/env python3
"""Validate final source-code handover docs against the quality checklist."""

from __future__ import annotations

import json
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
WORD_RE = re.compile(r"\b[\wÀ-ỹ]+\b", flags=re.UNICODE)

IMPORTANT_DOC_MIN_WORDS = {
    "01_project_handover_full.md": 400,
    "03_repository_guide.md": 350,
    "04_local_setup.md": 400,
    "05_configuration_reference.md": 350,
    "06_architecture.md": 450,
    "07_database_reference.md": 450,
    "08_auth_and_security.md": 450,
    "09_api_catalog.md": 450,
    "10_background_jobs.md": 350,
    "12_external_integrations.md": 350,
    "14_operations_runbook.md": 450,
    "15_deployment_and_cicd.md": 350,
    "16_testing_guide.md": 350,
    "17_known_risks.md": 250,
    "18_open_questions.md": 250,
    "20_documentation_coverage.md": 350,
}

READINESS_DIMENSIONS = [
    "Documentation structure",
    "Source discovery",
    "Evidence quality",
    "Documentation coverage",
    "Local setup readiness",
    "Build readiness",
    "Test readiness",
    "Runtime readiness",
    "Operations readiness",
    "Production handover",
]

HTTP_ATTRIBUTE_RE = re.compile(r"\[(?:HttpGet|HttpPost|HttpPut|HttpDelete|HttpPatch|AcceptVerbs)\b")
TABLE_MAPPING_RE = re.compile(r"\b(?:ToTable|CreateTable)\s*\(\s*\"([^\"]+)\"")
SECRET_VALUE_RE = re.compile(
    r"(?i)\b(?:password|pwd|secret|clientsecret|apikey|api_key|token|signingkey)\s*=\s*(?!<redacted>|redacted|\*\*\*|xxxx|xxxxx)[^;\s`\"']{8,}"
)
DOC_CONFIG_PATH_RE = re.compile(r"`?\"([A-Za-z0-9_.-]+(?::[A-Za-z0-9_.-]+)+)\"`?")
URL_PATH_RE = re.compile(r"\bhttps?://[^`\s|)]+")
GENERATED_OR_DOC_DIRS = {"bin", "obj", ".git", ".ai", ".agents", ".claude", ".cline", ".cursor", ".github", "docs"}

UNCERTAIN_MARKERS = {
    "[UNVERIFIED]",
    "[BLOCKED]",
    "[CONFLICT]",
    "[NOT_APPLICABLE]",
    "Not Verified",
    "not verified",
    "not_found_after_scan",
    "unknown",
    "Unknown",
    "chưa xác minh",
    "Chưa xác minh",
}


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


def load_json(path: Path) -> object | None:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None


def inventory_items(data: object | None) -> list[object]:
    if isinstance(data, dict):
        items = data.get("items")
        if isinstance(items, list):
            return items
        tables = data.get("tables")
        if isinstance(tables, list):
            return tables
    if isinstance(data, list):
        return data
    return []


def inventory_status(data: object | None) -> str:
    if isinstance(data, dict):
        status = data.get("status")
        if isinstance(status, str):
            return status
    return ""


def parse_first_front_matter(final_dir: Path) -> dict[str, str] | None:
    for name in EXPECTED_FILES:
        path = final_dir / name
        if path.exists():
            front_matter, _ = split_front_matter(path.read_text(encoding="utf-8"))
            if front_matter:
                return front_matter
    return None


def find_repo_root_from_inventory(inventory_dir: Path) -> Path | None:
    # <repo>/.ai/runs/source-code-handover/<run_id>/inventory
    for parent in inventory_dir.parents:
        if parent.name == ".ai":
            return parent.parent
    return None


def find_inventory_dir(final_dir: Path) -> Path | None:
    if final_dir.name == "final":
        candidate = final_dir.parent / "inventory"
        if candidate.is_dir():
            return candidate

    front_matter = parse_first_front_matter(final_dir)
    run_id = front_matter.get("run_id") if front_matter else None
    if not run_id:
        return None

    candidates = []
    repo_root = final_dir.parent if final_dir.name == "docs" else None
    if repo_root:
        candidates.append(repo_root / ".ai" / "runs" / "source-code-handover" / run_id / "inventory")
    for parent in final_dir.parents:
        candidates.append(parent / ".ai" / "runs" / "source-code-handover" / run_id / "inventory")
    for candidate in candidates:
        if candidate.is_dir():
            return candidate
    return None


def find_run_dir(final_dir: Path) -> Path | None:
    if final_dir.name == "final":
        return final_dir.parent
    inventory_dir = find_inventory_dir(final_dir)
    if inventory_dir is not None:
        return inventory_dir.parent
    return None


def count_source_http_attributes(repo_root: Path) -> int:
    src = repo_root / "src"
    if not src.is_dir():
        return 0
    count = 0
    for path in src.rglob("*.cs"):
        try:
            count += len(HTTP_ATTRIBUTE_RE.findall(path.read_text(encoding="utf-8", errors="ignore")))
        except OSError:
            continue
    return count


def count_source_table_mappings(repo_root: Path) -> int:
    src = repo_root / "src"
    if not src.is_dir():
        return 0
    tables: set[str] = set()
    for path in src.rglob("*.cs"):
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        tables.update(match.group(1) for match in TABLE_MAPPING_RE.finditer(text))
    return len(tables)


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


def is_uncertain_text(text: str) -> bool:
    return any(marker in text for marker in UNCERTAIN_MARKERS)


def load_evidence_lookup(final_dir: Path) -> dict[str, str]:
    run_dir = find_run_dir(final_dir)
    if run_dir is None:
        return {}
    manifest = load_json(run_dir / "evidence" / "evidence-manifest.json")
    lookup: dict[str, str] = {}
    if isinstance(manifest, dict) and isinstance(manifest.get("evidence"), list):
        for item in manifest["evidence"]:
            if not isinstance(item, dict):
                continue
            evidence_id = str(item.get("evidence_id", ""))
            if not EVIDENCE_RE.fullmatch(evidence_id):
                continue
            lookup[evidence_id] = " ".join(
                str(item.get(key, ""))
                for key in [
                    "claim",
                    "source_type",
                    "source_path",
                    "range_or_symbol",
                    "verification_type",
                    "status",
                ]
            )
    return lookup


def evidence_text_for_line(line: str, evidence_lookup: dict[str, str]) -> str:
    evidence_ids = EVIDENCE_RE.findall(line)
    return " ".join(evidence_lookup.get(evidence_id, "") for evidence_id in evidence_ids)


def line_evidence_supports(line: str, evidence_lookup: dict[str, str], keywords: list[str]) -> bool:
    evidence_text = evidence_text_for_line(line, evidence_lookup).lower()
    return any(keyword.lower() in evidence_text for keyword in keywords)


def line_has_evidence_prefix(line: str, prefixes: tuple[str, ...]) -> bool:
    return any(evidence_id.startswith(prefixes) for evidence_id in EVIDENCE_RE.findall(line))


def collect_config_keys(repo_root: Path | None) -> set[str]:
    if repo_root is None:
        return set()
    keys: set[str] = set()
    for path in repo_root.rglob("*.json"):
        if any(part in GENERATED_OR_DOC_DIRS for part in path.parts):
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        for match in re.finditer(r'"([^"]+)"\s*:', text):
            key = match.group(1)
            if key and not key.startswith("//"):
                keys.add(key)
    return keys


def validate_documented_config_paths(final_dir: Path, errors: list[str]) -> None:
    inventory_dir = find_inventory_dir(final_dir)
    repo_root = find_repo_root_from_inventory(inventory_dir) if inventory_dir else None
    config_keys = collect_config_keys(repo_root)
    if not config_keys:
        return
    docs_to_check = [
        "05_configuration_reference.md",
        "09_api_catalog.md",
        "12_external_integrations.md",
        "14_operations_runbook.md",
    ]
    for doc_name in docs_to_check:
        path = final_dir / doc_name
        if not path.exists():
            continue
        for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
            if is_uncertain_text(line):
                continue
            for match in DOC_CONFIG_PATH_RE.finditer(line):
                config_path = match.group(1)
                parts = [part for part in config_path.split(":") if part]
                missing = [part for part in parts if part not in config_keys]
                if missing:
                    errors.append(
                        f"{doc_name}:{line_no}: documented config path {config_path!r} contains keys not found in current config files: {', '.join(missing)}"
                    )


def source_contains_path(repo_root: Path | None, url_path: str) -> bool:
    if repo_root is None:
        return False
    needle = "/" + url_path.lstrip("/").split("?", 1)[0].strip("/")
    if needle == "/":
        return True
    path_pattern = re.compile(rf"(?<![A-Za-z0-9_/-]){re.escape(needle)}(?![A-Za-z0-9_-])")
    for path in repo_root.rglob("*"):
        if path.is_dir() or any(part in GENERATED_OR_DOC_DIRS for part in path.parts):
            continue
        if path.suffix.lower() not in {".cs", ".json", ".cshtml", ".md", ".yml", ".yaml"}:
            continue
        try:
            if path_pattern.search(path.read_text(encoding="utf-8", errors="ignore")):
                return True
        except OSError:
            continue
    return False


def validate_runbook_url_commands(final_dir: Path, errors: list[str]) -> None:
    inventory_dir = find_inventory_dir(final_dir)
    repo_root = find_repo_root_from_inventory(inventory_dir) if inventory_dir else None
    operations_path = final_dir / "14_operations_runbook.md"
    if not operations_path.exists():
        return
    for line_no, line in enumerate(operations_path.read_text(encoding="utf-8").splitlines(), start=1):
        if is_uncertain_text(line):
            continue
        for url in URL_PATH_RE.findall(line):
            if "localhost" not in url and "127.0.0.1" not in url:
                continue
            path_part = re.sub(r"^https?://[^/]+", "", url)
            if path_part and not source_contains_path(repo_root, path_part):
                errors.append(
                    f"14_operations_runbook.md:{line_no}: runbook command references {url!r}, but that path was not found in current source/config; mark it [UNVERIFIED] or provide evidence"
                )


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


def normalize_words(text: str) -> list[str]:
    return [word.lower() for word in WORD_RE.findall(text)]


def repeated_ngram_counts(words: list[str], size: int) -> dict[str, int]:
    counts: dict[str, int] = {}
    if len(words) < size:
        return counts
    for index in range(0, len(words) - size + 1):
        gram = " ".join(words[index : index + size])
        counts[gram] = counts.get(gram, 0) + 1
    return counts


def validate_repetition_and_line_shape(path: Path, text: str, body: str, errors: list[str]) -> None:
    lines = body.splitlines()
    body_chars = max(len(body), 1)
    for line_no, line in enumerate(lines, start=1):
        stripped = line.strip()
        if not stripped or stripped.startswith("|") or stripped.startswith("```"):
            continue
        if len(stripped) > 1200:
            errors.append(f"{path.name}: prose line {line_no} is too long ({len(stripped)} chars)")
        if len(stripped) / body_chars > 0.25:
            errors.append(f"{path.name}: prose line {line_no} dominates the document body")

    words = normalize_words(body)
    for size, max_count in [(20, 2), (40, 1)]:
        repeated = [
            (gram, count)
            for gram, count in repeated_ngram_counts(words, size).items()
            if count > max_count
        ]
        if repeated:
            gram, count = sorted(repeated, key=lambda item: item[1], reverse=True)[0]
            errors.append(
                f"{path.name}: repeated {size}-word prose block appears {count} times: {gram[:120]}"
            )


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

    validate_repetition_and_line_shape(path, text, body, errors)

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

    status = front_matter.get("status", "") if front_matter else ""
    word_count = len(re.findall(r"\b[\wÀ-ỹ]+\b", body, flags=re.UNICODE))
    min_words = IMPORTANT_DOC_MIN_WORDS.get(path.name)
    if min_words and status != "Not Applicable" and word_count < min_words:
        errors.append(
            f"{path.name}: likely skeleton document; {word_count} words is below minimum smoke threshold {min_words}"
        )

    if status == "Ready":
        if len(used_ids) < 3 and path.name not in {"18_open_questions.md", "19_evidence_index.md", "20_documentation_coverage.md"}:
            errors.append(f"{path.name}: Ready document has too few Evidence IDs for non-trivial handover content")

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

    if "asset-level" not in text.lower() and "asset level" not in text.lower() and "Phase 0" not in text:
        errors.append("20_documentation_coverage.md must state asset-level coverage denominators from Phase 0 inventory")

    category_one_count = 0
    for line in text.splitlines():
        if not line.strip().startswith("|"):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) < 4:
            continue
        domain = cells[0].lower()
        if any(token in domain for token in ["repository", "entry", "config", "dbcontext", "entity", "migration", "api", "background", "signalr", "docker", "ci/cd", "integration", "test"]):
            discovered = re.sub(r"[^0-9]", "", cells[2] if len(cells) > 2 else "")
            if discovered == "1":
                category_one_count += 1
    if category_one_count >= 5:
        errors.append(
            "20_documentation_coverage.md appears to use category-level 1/1 denominators instead of asset-level coverage"
        )


def parse_coverage_discovered_counts(text: str) -> dict[str, int]:
    counts: dict[str, int] = {}
    for line in text.splitlines():
        if not line.strip().startswith("|"):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) < 4:
            continue
        domain = cells[0]
        if domain.lower() in {"domain", "---"}:
            continue
        discovered_raw = re.sub(r"[^0-9]", "", cells[2])
        if discovered_raw:
            counts[domain.lower()] = int(discovered_raw)
    return counts


def require_text_contains_items(doc_name: str, text: str, item_names: set[str], errors: list[str], label: str) -> None:
    missing = sorted(name for name in item_names if name and name not in text)
    if missing:
        preview = ", ".join(missing[:12])
        suffix = "" if len(missing) <= 12 else f", ... (+{len(missing) - 12} more)"
        errors.append(f"{doc_name} missing {label} from inventory: {preview}{suffix}")


def collect_sql_tables_and_columns(data: object | None) -> tuple[set[str], set[str]]:
    tables: set[str] = set()
    columns: set[str] = set()
    if not isinstance(data, dict):
        return tables, columns
    table_items = data.get("tables")
    if not isinstance(table_items, list):
        table_items = data.get("items")
    if not isinstance(table_items, list):
        return tables, columns
    for table in table_items:
        if not isinstance(table, dict):
            continue
        table_name = table.get("table") or table.get("name") or table.get("table_name")
        if table_name:
            tables.add(str(table_name))
        column_items = table.get("columns")
        if isinstance(column_items, list):
            for column in column_items:
                if isinstance(column, dict):
                    column_name = column.get("column") or column.get("name") or column.get("column_name")
                    if column_name:
                        columns.add(str(column_name))
                elif isinstance(column, str):
                    columns.add(column)
    return tables, columns


def validate_inventory_backed_coverage(final_dir: Path, errors: list[str]) -> None:
    inventory_dir = find_inventory_dir(final_dir)
    if inventory_dir is None:
        errors.append("cannot locate Phase 0 inventory for inventory-backed coverage validation")
        return

    coverage_path = final_dir / "20_documentation_coverage.md"
    coverage_text = coverage_path.read_text(encoding="utf-8") if coverage_path.exists() else ""
    coverage_counts = parse_coverage_discovered_counts(coverage_text)

    inventory_specs = {
        "dbcontext": ("dbcontexts.json", "DbContext"),
        "entity": ("entities.json", "Entity"),
        "migration": ("migrations.json", "Migration"),
        "api": ("routes.json", "API"),
        "background": ("background-jobs.json", "Background"),
        "signalr": ("hubs.json", "SignalR"),
        "test": ("tests.json", "Test"),
    }
    for coverage_key, (filename, display) in inventory_specs.items():
        data = load_json(inventory_dir / filename)
        items = inventory_items(data)
        if not items and inventory_status(data) == "scan_failed":
            errors.append(f"{filename} scan_failed; coverage cannot be PASS")
            continue
        documented_count = coverage_counts.get(coverage_key)
        if documented_count is not None and documented_count != len(items):
            errors.append(
                f"20_documentation_coverage.md {display} discovered count {documented_count} does not match Phase 0 {filename} count {len(items)}"
            )

    database_doc = (final_dir / "07_database_reference.md").read_text(encoding="utf-8") if (final_dir / "07_database_reference.md").exists() else ""
    dbsets = inventory_items(load_json(inventory_dir / "dbsets.json"))
    entities = inventory_items(load_json(inventory_dir / "entities.json"))
    dbset_names = {
        str(item.get("dbset"))
        for item in dbsets
        if isinstance(item, dict) and item.get("dbset")
    }
    entity_names = {
        str(item.get("class") or item.get("entity"))
        for item in entities
        if isinstance(item, dict) and (item.get("class") or item.get("entity"))
    }
    table_names = {
        str(item.get("mapped_table") or item.get("table"))
        for item in entities
        if isinstance(item, dict) and (item.get("mapped_table") or item.get("table"))
    }
    sql_tables, sql_columns = collect_sql_tables_and_columns(load_json(inventory_dir / "sql-metadata.json"))
    table_names.update(sql_tables)
    require_text_contains_items("07_database_reference.md", database_doc, dbset_names, errors, "DbSet names")
    require_text_contains_items("07_database_reference.md", database_doc, entity_names, errors, "entity names")
    require_text_contains_items("07_database_reference.md", database_doc, table_names, errors, "table names")
    if table_names and sql_columns:
        require_text_contains_items("07_database_reference.md", database_doc, sql_columns, errors, "column names")

    api_doc = (final_dir / "09_api_catalog.md").read_text(encoding="utf-8") if (final_dir / "09_api_catalog.md").exists() else ""
    routes = inventory_items(load_json(inventory_dir / "routes.json"))
    route_names = {
        str(item.get("route"))
        for item in routes
        if isinstance(item, dict) and item.get("route")
    }
    action_names = {
        str(item.get("action"))
        for item in routes
        if isinstance(item, dict) and item.get("action")
    }
    controller_names = {
        str(item.get("controller"))
        for item in routes
        if isinstance(item, dict) and item.get("controller")
    }
    require_text_contains_items("09_api_catalog.md", api_doc, route_names, errors, "routes")
    require_text_contains_items("09_api_catalog.md", api_doc, action_names, errors, "actions")
    require_text_contains_items("09_api_catalog.md", api_doc, controller_names, errors, "controllers")

    repo_root = find_repo_root_from_inventory(inventory_dir)
    if repo_root is not None:
        route_inventory = load_json(inventory_dir / "routes.json")
        route_items = inventory_items(route_inventory)
        source_http_count = count_source_http_attributes(repo_root)
        if inventory_status(route_inventory) == "complete" and source_http_count > max(len(route_items) * 2, len(route_items) + 10):
            errors.append(
                f"routes.json appears incomplete: Phase 0 has {len(route_items)} routes but source scan found {source_http_count} HTTP method attributes"
            )

        entity_inventory = load_json(inventory_dir / "entities.json")
        entity_items = inventory_items(entity_inventory)
        table_mapping_count = count_source_table_mappings(repo_root)
        if inventory_status(entity_inventory) == "complete" and table_mapping_count > max(len(entity_items) * 2, len(entity_items) + 10):
            errors.append(
                f"entities.json/sql metadata appears incomplete: Phase 0 has {len(entity_items)} entities but source scan found {table_mapping_count} table mappings"
            )


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

    for doc in final_dir.glob("*.md"):
        text = doc.read_text(encoding="utf-8")
        match = SECRET_VALUE_RE.search(text)
        if match:
            errors.append(f"{doc.name}: possible unredacted secret/credential literal in final documentation: {match.group(0)[:80]}")


def validate_evidence_bound_claims(final_dir: Path, errors: list[str]) -> None:
    evidence_lookup = load_evidence_lookup(final_dir)
    if not evidence_lookup:
        errors.append("cannot validate evidence-bound claims because evidence-manifest.json is unavailable")
        return

    semantic_rules = [
        (
            re.compile(r"\b(?:timeout|retry|retries|fallback|rate limit|req/min|requests/min|RetryAfter)\b", re.IGNORECASE),
            ["timeout", "retry", "fallback", "rate", "ratelimit", "requesttimeout", "RetryAfter"],
            "timeout/retry/fallback/rate-limit",
        ),
        (
            re.compile(r"\b(?:Bearer|Authorization|JWT|token-based|auth header|ApiSecret|SigningKey)\b", re.IGNORECASE),
            ["auth", "authorize", "authorization", "jwt", "bearer", "token", "signingkey", "ids4"],
            "auth/header/token",
        ),
        (
            re.compile(r"\b(?:401|403|404|502|504|status code|unauthorized|forbidden|not found|bad gateway|gateway timeout)\b", re.IGNORECASE),
            ["status", "401", "403", "404", "502", "504", "exception", "error", "runtime", "health"],
            "status/error behavior",
        ),
        (
            re.compile(r"\b(?:Postman|OpenAPI|Swagger|integration test|unit tests|traffic sample)\b", re.IGNORECASE),
            ["postman", "openapi", "swagger", "test", "traffic", "runtime", "contract"],
            "contract/test artifact",
        ),
        (
            re.compile(r"\b(?:Health endpoint|Health API|health check|Ping check|curl\s+-?i?)\b", re.IGNORECASE),
            ["health", "runtime", "smoke", "curl", "test", "ops"],
            "health/smoke command",
        ),
    ]

    docs_to_check = [
        "09_api_catalog.md",
        "12_external_integrations.md",
        "14_operations_runbook.md",
        "15_deployment_and_cicd.md",
        "16_testing_guide.md",
    ]
    for doc_name in docs_to_check:
        path = final_dir / doc_name
        if not path.exists():
            continue
        for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
            stripped = line.strip()
            if not stripped or stripped.startswith("|---") or stripped.lower().startswith("| api id ") or stripped.lower().startswith("| integration id ") or stripped.lower().startswith("| symptom "):
                continue
            if "[CONFIRMED]" not in stripped:
                continue
            if is_uncertain_text(stripped):
                errors.append(
                    f"{doc_name}:{line_no}: line mixes [CONFIRMED] with uncertainty markers; use a non-confirmed status for unverified cells"
                )
                continue
            evidence_ids = EVIDENCE_RE.findall(stripped)
            if not evidence_ids:
                errors.append(f"{doc_name}:{line_no}: [CONFIRMED] operational/integration claim has no Evidence ID")
                continue
            for pattern, keywords, label in semantic_rules:
                if pattern.search(stripped) and not line_evidence_supports(stripped, evidence_lookup, keywords):
                    errors.append(
                        f"{doc_name}:{line_no}: [CONFIRMED] {label} claim is not supported by same-line evidence; mark it [UNVERIFIED] or cite specific evidence"
                    )

            if re.search(r"\b(?:Owner|Team|Admin|Partner|DevOps|Release Manager|Security Admin|DB Admin)\b", stripped):
                if not line_evidence_supports(stripped, evidence_lookup, ["owner", "team", "admin", "maintainer", "devops", "contact"]):
                    errors.append(
                        f"{doc_name}:{line_no}: [CONFIRMED] owner/escalation value is not source-backed; use Unknown/[UNVERIFIED] or cite owner evidence"
                    )

            if re.search(r"\b(?:AIMusicLab|external partner|REST JSON API contract|/api/songs)\b", stripped, flags=re.IGNORECASE):
                if not line_evidence_supports(stripped, evidence_lookup, ["aimusiclab", "music-cluster", "destination", "external", "api/songs"]):
                    errors.append(
                        f"{doc_name}:{line_no}: [CONFIRMED] external API contract/path is not supported by same-line evidence"
                    )

            if re.search(r"\b(?:Database|DB)\b", stripped) and "N/A" in stripped:
                if not line_has_evidence_prefix(stripped, ("EV-NEG-DB-",)):
                    errors.append(
                        f"{doc_name}:{line_no}: database N/A claim must cite EV-NEG-DB-* evidence"
                    )


def collect_background_job_inventory(final_dir: Path) -> list[dict[str, str]]:
    inventory_dir = find_inventory_dir(final_dir)
    if inventory_dir is None:
        return []
    data = load_json(inventory_dir / "background-jobs.json")
    jobs: list[dict[str, str]] = []
    for item in inventory_items(data):
        if not isinstance(item, dict):
            continue
        name = str(item.get("name") or item.get("class") or item.get("job") or "").strip()
        if not name:
            continue
        jobs.append(
            {
                "name": name,
                "handler": str(item.get("handler") or item.get("method") or "").strip(),
                "schedule": str(item.get("schedule") or item.get("trigger") or item.get("cron") or "").strip(),
                "source_path": str(item.get("source_path") or item.get("path") or item.get("file") or "").strip(),
            }
        )
    return jobs


def validate_background_job_detail(final_dir: Path, errors: list[str]) -> None:
    jobs = collect_background_job_inventory(final_dir)
    if not jobs:
        return

    doc_path = final_dir / "10_background_jobs.md"
    if not doc_path.exists():
        errors.append("10_background_jobs.md missing while background job inventory is non-empty")
        return

    text = doc_path.read_text(encoding="utf-8")
    lowered = text.lower()
    if "[NOT_APPLICABLE]" in text:
        errors.append("10_background_jobs.md is [NOT_APPLICABLE] while background job inventory is non-empty")
        return

    if "required background jobs keywords" in lowered or "keywords checklist" in lowered:
        errors.append("10_background_jobs.md contains validator keyword stuffing instead of real job documentation")

    missing_names = [job["name"] for job in jobs if job["name"] not in text]
    if missing_names:
        preview = ", ".join(missing_names[:12])
        suffix = "" if len(missing_names) <= 12 else f", ... (+{len(missing_names) - 12} more)"
        errors.append(f"10_background_jobs.md missing discovered background jobs from inventory: {preview}{suffix}")

    missing_handlers = [
        f"{job['name']} -> {job['handler']}"
        for job in jobs
        if job["handler"] and job["handler"] not in text
    ]
    if missing_handlers:
        preview = ", ".join(missing_handlers[:10])
        suffix = "" if len(missing_handlers) <= 10 else f", ... (+{len(missing_handlers) - 10} more)"
        errors.append(f"10_background_jobs.md missing discovered job handlers from inventory: {preview}{suffix}")

    detailed_tokens = [
        "Job ID",
        "Job name",
        "Registration source",
        "Source path",
        "Trigger",
        "Schedule",
        "Cron",
        "Handler",
        "Queue",
        "Storage",
        "Service",
        "Repository",
        "DB",
        "Redis",
        "External",
        "Retry",
        "Timeout",
        "Idempotency",
        "Failure",
        "Logging",
        "Shutdown",
        "Evidence",
        "Status",
    ]
    for token in detailed_tokens:
        if token.lower() not in lowered:
            errors.append(f"10_background_jobs.md missing per-job lifecycle detail token/column: {token}")

    if "sequenceDiagram" not in text:
        errors.append("10_background_jobs.md missing Mermaid sequenceDiagram for scheduler/worker/handler/data-store/failure flow")

    job_table_rows = 0
    for line in text.splitlines():
        if not line.strip().startswith("|"):
            continue
        if any(job["name"] in line for job in jobs):
            job_table_rows += 1
    if job_table_rows < len(jobs):
        errors.append(
            f"10_background_jobs.md has {job_table_rows} job table rows but inventory discovered {len(jobs)} background jobs"
        )


def markdown_section_after_heading(text: str, heading_pattern: str) -> str:
    match = re.search(heading_pattern, text, flags=re.IGNORECASE | re.MULTILINE)
    if not match:
        return ""
    next_heading = re.search(r"\n#{2,6}\s+", text[match.end():])
    if not next_heading:
        return text[match.end():]
    return text[match.end(): match.end() + next_heading.start()]


def markdown_row_contains_token(section: str, token: str) -> bool:
    token_patterns = [
        f"`{token}`",
        token,
    ]
    for line in section.splitlines():
        if not line.strip().startswith("|"):
            continue
        if any(pattern in line for pattern in token_patterns):
            return True
    return False


def collect_redis_store_inventory(final_dir: Path) -> list[dict[str, str]]:
    inventory_dir = find_inventory_dir(final_dir)
    if inventory_dir is None:
        return []
    data = load_json(inventory_dir / "redis-cache.json")
    stores: list[dict[str, str]] = []
    for item in inventory_items(data):
        if not isinstance(item, dict):
            continue
        name = str(item.get("name") or item.get("store") or item.get("key") or "").strip()
        if not name:
            continue
        stores.append(
            {
                "name": name,
                "type": str(item.get("type") or item.get("data_type") or "").strip(),
                "purpose": str(item.get("purpose") or "").strip(),
            }
        )
    return stores


def validate_database_store_contract(final_dir: Path, errors: list[str]) -> None:
    doc_path = final_dir / "07_database_reference.md"
    if not doc_path.exists():
        return
    text = doc_path.read_text(encoding="utf-8")
    lowered = text.lower()
    inventory_dir = find_inventory_dir(final_dir)
    if inventory_dir is None:
        return

    if "required database reference keywords" in lowered or "keywords checklist" in lowered:
        errors.append("07_database_reference.md contains validator keyword stuffing instead of real database documentation")

    sql_data = load_json(inventory_dir / "sql-metadata.json")
    sql_tables = sql_data.get("tables") if isinstance(sql_data, dict) else None
    if isinstance(sql_tables, list):
        for table in sql_tables:
            if not isinstance(table, dict):
                continue
            table_name = str(table.get("table") or "").strip()
            if not table_name:
                continue
            table_section = markdown_section_after_heading(
                text,
                rf"^#+\s*(?:Table|Bảng)\s*:?\s*`?{re.escape(table_name)}`?",
            )
            if not table_section:
                errors.append(f"07_database_reference.md missing detailed schema section for table {table_name}")
                continue
            columns = table.get("columns")
            if not isinstance(columns, list):
                continue
            missing_columns = []
            for column in columns:
                if not isinstance(column, dict):
                    continue
                column_name = str(column.get("name") or "").strip()
                if column_name and not markdown_row_contains_token(table_section, column_name):
                    missing_columns.append(column_name)
            if missing_columns:
                preview = ", ".join(missing_columns[:12])
                suffix = "" if len(missing_columns) <= 12 else f", ... (+{len(missing_columns) - 12} more)"
                errors.append(f"07_database_reference.md table {table_name} missing column rows: {preview}{suffix}")

    entity_items = inventory_items(load_json(inventory_dir / "entities.json"))
    redis_entities = [
        str(item.get("class") or item.get("entity"))
        for item in entity_items
        if isinstance(item, dict) and "redis" in str(item.get("mapped_table") or item.get("table") or "").lower()
    ]
    mongo_entities = [
        str(item.get("class") or item.get("entity"))
        for item in entity_items
        if isinstance(item, dict) and "mongo" in str(item.get("mapped_table") or item.get("table") or "").lower()
    ]
    redis_stores = collect_redis_store_inventory(final_dir)

    if redis_entities or redis_stores:
        required_redis_tokens = [
            "Redis key pattern",
            "Key pattern",
            "Data type",
            "Key inputs",
            "Field/member/value shape",
            "Field/value shape",
            "TTL",
            "Producer/write path",
            "Consumer/read path",
            "Jobs/APIs affected",
            "Rebuild/invalidation",
            "SQL/Mongo",
            "Drift risk",
            "Data asset",
            "Operation",
            "Entry point",
            "ID/key source",
            "Field/value changed",
            "Value source",
            "Call chain",
            "Also updates",
            "Read consumers",
            "Consistency rule",
            "Debug query/command",
        ]
        for token in required_redis_tokens:
            if token.lower() not in lowered:
                errors.append(f"07_database_reference.md missing Redis database contract token/section: {token}")

        missing_stores = [store["name"] for store in redis_stores if store["name"] not in text]
        if missing_stores:
            errors.append(
                "07_database_reference.md missing discovered Redis stores from inventory: " + ", ".join(missing_stores[:12])
            )

        redis_contract_rows = 0
        redis_names = set(redis_entities + [store["name"] for store in redis_stores])
        for line in text.splitlines():
            if line.strip().startswith("|") and any(name and name in line for name in redis_names):
                if "key" in line.lower() or "redis" in line.lower() or "ttl" in line.lower():
                    redis_contract_rows += 1
        if redis_contract_rows < max(1, len(redis_stores)):
            errors.append(
                f"07_database_reference.md has {redis_contract_rows} Redis contract rows but inventory/source discovered {len(redis_stores)} Redis stores and {len(redis_entities)} Redis-backed entities"
            )

        weak_redis_patterns = ["None (Redis Hash)", "None (Redis ZSet)", "None (Redis List)", "Redis Hash)", "Redis ZSet)"]
        if any(pattern in text for pattern in weak_redis_patterns) and "Key pattern" not in text:
            errors.append("07_database_reference.md documents Redis storage labels without concrete Redis key patterns")

        lineage_rows = 0
        lineage_tokens = [
            "operation",
            "entry point",
            "id/key source",
            "field/value changed",
            "value source",
            "call chain",
            "read consumers",
        ]
        for line in text.splitlines():
            if not line.strip().startswith("|"):
                continue
            lowered_line = line.lower()
            if any(name and name in line for name in redis_names) and sum(token in lowered_line for token in lineage_tokens) >= 2:
                lineage_rows += 1
        if lineage_rows < max(1, len(redis_stores)):
            errors.append(
                f"07_database_reference.md has {lineage_rows} Redis mutation lineage rows but inventory/source discovered {len(redis_stores)} Redis stores and {len(redis_entities)} Redis-backed entities"
            )

    if mongo_entities:
        required_mongo_tokens = [
            "Collection",
            "Document model",
            "Field path",
            "Producer/write path",
            "Consumer/read path",
            "Index/retention",
            "Data asset",
            "Operation",
            "Entry point",
            "ID/key source",
            "Field/value changed",
            "Value source",
            "Call chain",
            "Read consumers",
        ]
        for token in required_mongo_tokens:
            if token.lower() not in lowered:
                errors.append(f"07_database_reference.md missing MongoDB document contract token/section: {token}")


def inventory_has_items(final_dir: Path, filename: str) -> bool:
    inventory_dir = find_inventory_dir(final_dir)
    if inventory_dir is None:
        return False
    return bool(inventory_items(load_json(inventory_dir / filename)))


def require_doc_tokens(doc_name: str, text: str, tokens: list[str], errors: list[str]) -> None:
    if "[NOT_APPLICABLE]" in text:
        return
    lowered = text.lower()
    for token in tokens:
        if token.lower() not in lowered:
            errors.append(f"{doc_name} missing behavior-depth token/section: {token}")


def table_rows_with_route(section: str, routes: list[str]) -> set[str]:
    found: set[str] = set()
    for line in section.splitlines():
        if not line.strip().startswith("|"):
            continue
        if line.strip().startswith("|---"):
            continue
        for route in routes:
            if route and route in line:
                found.add(route)
    return found


def table_header_contains(section: str, required_columns: list[str]) -> list[str]:
    header = ""
    for line in section.splitlines():
        stripped = line.strip()
        if stripped.startswith("|") and not stripped.startswith("|---"):
            header = stripped.lower()
            break
    return [column for column in required_columns if column.lower() not in header]


def first_table_header(section: str) -> str:
    for line in section.splitlines():
        stripped = line.strip()
        if stripped.startswith("|") and not stripped.startswith("|---"):
            return stripped
    return ""


def validate_per_route_api_contract_coverage(final_dir: Path, errors: list[str]) -> None:
    inventory_dir = find_inventory_dir(final_dir)
    if inventory_dir is None:
        return
    route_items = inventory_items(load_json(inventory_dir / "routes.json"))
    routes = [
        str(item.get("route")).strip()
        for item in route_items
        if isinstance(item, dict) and item.get("route")
    ]
    if not routes:
        return
    doc_path = final_dir / "09_api_catalog.md"
    if not doc_path.exists():
        return
    text = doc_path.read_text(encoding="utf-8")
    if "[NOT_APPLICABLE]" in text:
        return

    contract_section = markdown_section_after_heading(
        text,
        r"^#+\s*(?:API\s+Contract\s+Matrix|API\s+Matrix|Endpoint\s+Contract|Route\s+Contract)",
    )
    behavior_section = markdown_section_after_heading(
        text,
        r"^#+\s*(?:Behavior\s+Flow\s+Table|Business\s+Flow|Behavior\s+Flows?|Luồng\s+nghiệp\s+vụ)",
    )
    inventory_section = markdown_section_after_heading(
        text,
        r"^#+\s*(?:Complete\s+Discovered\s+Routes\s+and\s+Actions|Discovered\s+Routes)",
    )

    if inventory_section:
        inventory_routes = table_rows_with_route(inventory_section, routes)
        if len(inventory_routes) == len(routes):
            contract_routes = table_rows_with_route(contract_section, routes)
            behavior_routes = table_rows_with_route(behavior_section, routes)
            if len(contract_routes) < len(routes):
                missing = [route for route in routes if route not in contract_routes]
                errors.append(
                    "09_api_catalog.md Complete Discovered Routes covers "
                    f"{len(routes)} routes but API Contract Matrix covers only {len(contract_routes)}; missing endpoint contracts: "
                    + ", ".join(missing[:12])
                    + ("" if len(missing) <= 12 else f", ... (+{len(missing) - 12} more)")
                )
            if len(behavior_routes) < len(routes):
                missing = [route for route in routes if route not in behavior_routes]
                errors.append(
                    "09_api_catalog.md Complete Discovered Routes covers "
                    f"{len(routes)} routes but Behavior Flow Table covers only {len(behavior_routes)}; missing behavior flows: "
                    + ", ".join(missing[:12])
                    + ("" if len(missing) <= 12 else f", ... (+{len(missing) - 12} more)")
                )

    required_contract_columns = [
        "Route",
        "Method",
        "Action",
        "Request fields",
        "Request example",
        "Response fields",
        "Success example",
        "Error example",
        "Status codes",
        "Validation",
        "Auth",
        "Header",
        "Content type",
        "DB",
        "Redis",
        "External",
        "Evidence",
        "Status",
    ]
    missing_contract_columns = table_header_contains(contract_section, required_contract_columns)
    if missing_contract_columns:
        errors.append(
            "09_api_catalog.md API Contract Matrix missing endpoint-level columns: "
            + ", ".join(missing_contract_columns)
        )

    contract_header = first_table_header(contract_section)
    contract_header_lower = contract_header.lower()
    forbidden_main_columns = [
        "Client path",
        "Versioning",
        "Timeout",
        "Retry",
        "Idempotency",
        "Rate limit",
        "Postman",
    ]
    present_forbidden = [
        column
        for column in forbidden_main_columns
        if re.search(rf"(?i)(?:^|\|)\s*{re.escape(column)}\s*(?:\||$)", contract_header)
    ]
    if present_forbidden:
        errors.append(
            "09_api_catalog.md API Contract Matrix contains policy/duplicate columns that must be moved out of the main matrix: "
            + ", ".join(present_forbidden)
        )
    if "route" in contract_header_lower and "client path" in contract_header_lower:
        errors.append("09_api_catalog.md API Contract Matrix duplicates Route and Client path; keep Route only unless a separate gateway mapping table has evidence")

    required_behavior_columns = [
        "Flow ID",
        "Entry point",
        "Actor/client",
        "Trigger",
        "Input/source data",
        "Processing logic",
        "Internal call chain",
        "External/downstream calls",
        "Data-store side effects",
        "Operation",
        "ID/key source",
        "Field/value changed",
        "Value source",
        "Read consumers",
        "Success/error behavior",
        "Debug/smoke check",
        "Evidence",
        "Status",
    ]
    missing_behavior_columns = table_header_contains(behavior_section, required_behavior_columns)
    if missing_behavior_columns:
        errors.append(
            "09_api_catalog.md Behavior Flow Table missing endpoint-level columns: "
            + ", ".join(missing_behavior_columns)
        )

    synthetic_patterns = [
        r"\bX-Secret-Key-\d+\b",
        r"\bValidationRulesV\d+\b",
        r"\bError\s+\d+\b",
        r"\bRequest Body\s+\d+\s+data\b",
        r"\bNone\s+\d+\b",
        r"\bappsettings\.json\s*\(\d+\)",
        r"\bnews_ids_\d+\b",
        r"\bTotalView_\d+\b",
        r"\bRedis Cache\s+\d+\b",
        r"\bAPI Call\s+\d+\b",
        r"\bPhản ánh DB\s+\d+\b",
        r"\bv1\.\d+\b",
        r"\b\d{4}ms\b",
        r"\b\d{2,4}/min\b",
    ]
    for pattern in synthetic_patterns:
        match = re.search(pattern, text, flags=re.IGNORECASE)
        if match:
            errors.append(
                f"09_api_catalog.md contains synthetic/filler API contract value {match.group(0)!r}; use source/runtime evidence or mark the cell [UNVERIFIED]"
            )
            break

    for line_no, line in enumerate(text.splitlines(), start=1):
        if "[CONFIRMED]" not in line:
            continue
        if re.search(r"\|\s*[^|]*\.sln\s*\|\s*line\s+1\s*\|", line, flags=re.IGNORECASE):
            errors.append(
                f"09_api_catalog.md:{line_no}: [CONFIRMED] API evidence cites only a solution file line 1; use controller/action/DTO/service/test source paths"
            )


def validate_80_percent_understanding_contract(final_dir: Path, errors: list[str]) -> None:
    docs = {path.name: path.read_text(encoding="utf-8") for path in final_dir.glob("*.md")}
    combined = "\n".join(docs.values())

    keyword_patterns = [
        r"Required\s+[A-Za-z0-9 /_-]+\s+Keywords",
        r"Keywords checklist",
        r"for validation\)",
        r"validation keyword",
    ]
    for doc_name, text in docs.items():
        for pattern in keyword_patterns:
            if re.search(pattern, text, flags=re.IGNORECASE):
                errors.append(f"{doc_name} contains validator-facing keyword text instead of user-facing behavior documentation")
                break

    global_tokens = [
        "Entry point",
        "Actor/client",
        "Trigger",
        "Input/source data",
        "Processing logic",
        "Internal call chain",
        "External/downstream calls",
        "Data-store side effects",
        "Config keys",
        "Success/error behavior",
        "Debug/smoke check",
        "Evidence",
        "Status",
    ]
    if not any(token.lower() in combined.lower() for token in ["Flow ID", "Business flow", "Behavior flow"]):
        errors.append("final documentation set missing behavior-flow table/section")
    for token in global_tokens:
        if token.lower() not in combined.lower():
            errors.append(f"final documentation set missing 80-percent-understanding token: {token}")

    doc_requirements = {
        "01_project_handover_full.md": [
            "System purpose",
            "Actor/client",
            "Business capability",
            "End-to-end flow",
            "Data store",
            "External system",
            "Risk",
        ],
        "02_project_context.md": [
            "Business capability",
            "Actor/client",
            "Source of truth",
            "External system",
            "Non-goal",
            "Business rule",
        ],
        "03_repository_guide.md": [
            "Project path",
            "Project type",
            "Entry point",
            "Dependency direction",
            "Generated",
            "Manual code",
        ],
        "04_local_setup.md": [
            "Working directory",
            "Prerequisites",
            "Required services",
            "Environment",
            "Port",
            "Smoke",
            "Expected log",
            "Troubleshooting",
        ],
        "05_configuration_reference.md": [
            "Key",
            "Source file",
            "Environment",
            "Used by",
            "Behavior impact",
            "Reload/restart",
            "Secret",
            "Rotation",
        ],
        "06_architecture.md": [
            "Runtime topology",
            "Entry point",
            "Request lifecycle",
            "Data flow",
            "Failure boundary",
            "sequenceDiagram",
            "DB",
            "Redis",
            "External",
        ],
        "08_auth_and_security.md": [
            "Auth scheme",
            "Header",
            "Middleware",
            "Filter",
            "Claim",
            "Permission",
            "Failure status",
            "Bypass risk",
            "Secret",
        ],
        "09_api_catalog.md": [
            "Controller",
            "Service",
            "Repository",
            "Data source",
            "Processing logic",
            "External call",
            "Downstream call",
            "DB",
            "Redis",
            "Side effects",
            "Operation",
            "ID/key source",
            "Field/value changed",
            "Value source",
            "Read consumers",
            "sequenceDiagram",
        ],
        "14_operations_runbook.md": [
            "Fault isolation",
            "Likely layer",
            "Verification command",
            "Log",
            "Query",
            "Fix/next action",
            "Rollback",
            "Escalation",
            "Redis",
            "Database",
            "External",
        ],
        "15_deployment_and_cicd.md": [
            "Build",
            "Test",
            "Package",
            "Deploy",
            "Environment",
            "Secret",
            "Migration",
            "Health gate",
            "Rollback",
        ],
        "16_testing_guide.md": [
            "Test asset",
            "Command",
            "Coverage",
            "API",
            "Background",
            "Database",
            "Redis",
            "External",
            "Gap",
        ],
        "17_known_risks.md": [
            "Risk ID",
            "Trigger",
            "Impact",
            "Detection",
            "Mitigation",
            "Owner",
            "Evidence",
        ],
        "18_open_questions.md": [
            "Question ID",
            "Blocked area",
            "Decision needed",
            "Evidence needed",
            "Owner",
            "Impact",
        ],
        "20_documentation_coverage.md": [
            "Discovered",
            "Documented",
            "Unresolved",
            "Excluded",
            "Gaps",
            "Evidence",
        ],
    }
    for doc_name, tokens in doc_requirements.items():
        text = docs.get(doc_name)
        if text:
            require_doc_tokens(doc_name, text, tokens, errors)

    if inventory_has_items(final_dir, "routes.json"):
        require_doc_tokens(
            "09_api_catalog.md",
            docs.get("09_api_catalog.md", ""),
            [
                "Flow ID",
                "Entry point",
                "Input/source data",
                "Processing logic",
                "Internal call chain",
                "External/downstream calls",
                "Data-store side effects",
                "Operation",
                "ID/key source",
                "Field/value changed",
                "Value source",
                "Read consumers",
                "Config keys",
                "Debug/smoke check",
            ],
            errors,
        )

    if inventory_has_items(final_dir, "background-jobs.json"):
        require_doc_tokens(
            "10_background_jobs.md",
            docs.get("10_background_jobs.md", ""),
            [
                "Flow ID",
                "Entry point",
                "Trigger",
                "Config keys",
                "Processing logic",
                "Internal call chain",
                "External/downstream calls",
                "Data-store side effects",
                "Operation",
                "ID/key source",
                "Field/value changed",
                "Value source",
                "Read consumers",
                "Success/error behavior",
                "Debug/smoke check",
            ],
            errors,
        )

    if inventory_has_items(final_dir, "hubs.json") or inventory_has_items(final_dir, "realtime-events.json"):
        require_doc_tokens(
            "11_realtime_signalr_socket.md",
            docs.get("11_realtime_signalr_socket.md", ""),
            [
                "Event contract",
                "Producer",
                "Consumer",
                "Payload fields",
                "Group/user mapping",
                "Auth",
                "Failure",
                "sequenceDiagram",
            ],
            errors,
        )

    if inventory_has_items(final_dir, "integrations.json"):
        require_doc_tokens(
            "12_external_integrations.md",
            docs.get("12_external_integrations.md", ""),
            [
                "Caller",
                "Trigger",
                "Request contract",
                "Response contract",
                "Data mapping",
                "Auth",
                "Timeout",
                "Retry",
                "Fallback",
                "Failure mode",
                "Debug/smoke check",
            ],
            errors,
        )

    if "sequenceDiagram" not in combined and (
        inventory_has_items(final_dir, "routes.json")
        or inventory_has_items(final_dir, "background-jobs.json")
        or inventory_has_items(final_dir, "integrations.json")
        or inventory_has_items(final_dir, "hubs.json")
    ):
        errors.append("final documentation set missing Mermaid sequenceDiagram for discovered behavioral flows")


def validate_anti_skeleton(final_dir: Path, indexed_ids: set[str], errors: list[str]) -> None:
    docs = {path.name: path.read_text(encoding="utf-8") for path in final_dir.glob("*.md")}
    combined = "\n".join(docs.values())
    total_words = len(WORD_RE.findall(combined))
    if total_words < 7000:
        errors.append(
            f"final documentation set is likely skeleton-only; total word count {total_words} is below minimum smoke threshold 7000"
        )

    statuses: dict[str, str] = {}
    evidence_usage: dict[str, set[str]] = {}
    for name, text in docs.items():
        front_matter, _ = split_front_matter(text)
        if front_matter:
            statuses[name] = front_matter.get("status", "")
        if name == "19_evidence_index.md":
            continue
        for evidence_id in set(EVIDENCE_RE.findall(text)):
            evidence_usage.setdefault(evidence_id, set()).add(name)

    ready_count = sum(1 for status in statuses.values() if status == "Ready")
    if len(statuses) >= 20 and ready_count == len(statuses):
        if not any(eid.startswith("EV-TEST-") for eid in indexed_ids):
            errors.append("all final docs are Ready but no EV-TEST-* evidence exists")
        if not any(eid.startswith(("EV-RT-", "EV-OPS-")) for eid in indexed_ids):
            errors.append("all final docs are Ready but no EV-RT-* or EV-OPS-* runtime/ops evidence exists")
        if "Not Verified" in combined or "NOT VERIFIED" in combined or "Chưa xác minh" in combined:
            errors.append("all final docs are Ready while readiness text still contains Not Verified / Chưa xác minh")

    broad_reuse = [
        f"{evidence_id} used in {len(names)} docs"
        for evidence_id, names in sorted(evidence_usage.items())
        if not evidence_id.startswith("EV-NEG-") and len(names) >= 8
    ]
    if broad_reuse:
        errors.append("evidence appears too broad/reused across unrelated docs: " + "; ".join(broad_reuse[:5]))

    repeated_cross_doc = [
        (gram, count)
        for gram, count in repeated_ngram_counts(normalize_words(combined), 30).items()
        if count >= 10
    ]
    if repeated_cross_doc:
        gram, count = sorted(repeated_cross_doc, key=lambda item: item[1], reverse=True)[0]
        errors.append(f"final documentation repeats the same 30-word block {count} times across docs: {gram[:120]}")

    for dimension in READINESS_DIMENSIONS:
        if dimension not in combined:
            errors.append(f"final documentation missing readiness dimension: {dimension}")

    local_setup = docs.get("04_local_setup.md", "")
    for token in ["Prerequisites", "Working directory", "Command", "Expected", "Smoke", "Troubleshooting"]:
        if token.lower() not in local_setup.lower():
            errors.append(f"04_local_setup.md missing local setup token/section: {token}")

    testing = docs.get("16_testing_guide.md", "")
    if "dotnet test" in testing and not any(eid.startswith("EV-TEST-") for eid in indexed_ids):
        errors.append("16_testing_guide.md mentions dotnet test but no EV-TEST-* observed test evidence exists")

    operations = docs.get("14_operations_runbook.md", "")
    for token in ["Health", "Log", "Rollback", "Incident", "Escalation"]:
        if token.lower() not in operations.lower():
            errors.append(f"14_operations_runbook.md missing operations runbook token/section: {token}")


def validate_deep_document_requirements(final_dir: Path, errors: list[str]) -> None:
    docs = {path.name: path.read_text(encoding="utf-8") for path in final_dir.glob("*.md")}

    database = docs.get("07_database_reference.md", "")
    database_has_assets = any(token.lower() in database.lower() for token in ["EV-DB-", "DbContext", "DbSet", "Entity", "Migration", "Connection string"])
    if "[NOT_APPLICABLE]" not in database or database_has_assets:
        required_database_tokens = [
            "DbContext",
            "DbSet",
            "Entity",
            "Table",
            "Column",
            "CLR type",
            "DB type",
            "Nullable",
            "PK",
            "FK",
            "Migration",
            "Read/write path",
        ]
        for token in required_database_tokens:
            if token.lower() not in database.lower():
                errors.append(f"07_database_reference.md missing deep database token/section: {token}")

    api_catalog = docs.get("09_api_catalog.md", "")
    api_has_assets = any(token.lower() in api_catalog.lower() for token in ["EV-API-", "Controller", "Action", "Route", "Endpoint", "HTTP"])
    if "[NOT_APPLICABLE]" not in api_catalog or api_has_assets:
        required_api_tokens = [
            "API ID",
            "Route",
            "Method",
            "Action",
            "Request",
            "Response",
            "Success",
            "Error",
            "Field",
            "Type",
            "Required",
            "Validation",
            "Auth",
            "Header",
            "Content type",
            "Status codes",
            "DB side effects",
            "Redis",
            "External",
            "Curl",
            "Smoke",
        ]
        for token in required_api_tokens:
            if token.lower() not in api_catalog.lower():
                errors.append(f"09_api_catalog.md missing deep API contract token/section: {token}")

    database = docs.get("07_database_reference.md", "")
    database_has_assets = any(token.lower() in database.lower() for token in ["EV-DB-", "DbContext", "DbSet", "Entity", "Migration", "Connection string"])
    if "[NOT_APPLICABLE]" not in database or database_has_assets:
        extra_database_tokens = [
            "Relationship",
            "Consumer",
            "Seed",
            "Reset",
            "Backup",
            "Restore",
            "Data risk",
            "Coverage",
        ]
        for token in extra_database_tokens:
            if token.lower() not in database.lower():
                errors.append(f"07_database_reference.md missing operations database token/section: {token}")

    external = docs.get("12_external_integrations.md", "")
    external_has_assets = any(
        token.lower() in external.lower()
        for token in ["EV-CONFIG-", "EV-API-", "EV-OPS-", "Consul", "Redis", "HTTP", "Webhook", "External", "Integration", "Cluster", "Destination"]
    )
    if "[NOT_APPLICABLE]" not in external or external_has_assets:
        required_external_tokens = [
            "Integration ID",
            "External system",
            "Caller",
            "Trigger",
            "Protocol",
            "Direction",
            "Auth method",
            "Config keys",
            "Contract",
            "Timeout",
            "Retry",
            "Fallback",
            "Failure",
            "Health",
            "Test strategy",
            "Owner",
        ]
        for token in required_external_tokens:
            if token.lower() not in external.lower():
                errors.append(f"12_external_integrations.md missing external integration token/section: {token}")

    operations = docs.get("14_operations_runbook.md", "")
    if "[NOT_APPLICABLE]" not in operations:
        required_ops_tokens = [
            "Runtime topology",
            "Service map",
            "Domain",
            "Port",
            "Environment",
            "Dependency",
            "Health",
            "Log",
            "Trace",
            "Correlation",
            "Reverse proxy",
            "Upstream",
            "Fault isolation",
            "Symptom",
            "Likely layer",
            "First check",
            "Verification command",
            "Fix/next action",
            "Rollback",
            "Escalation",
            "401",
            "403",
            "404",
            "502",
            "504",
            "Redis",
            "Database",
            "External API",
            "CORS",
            "TLS",
        ]
        for token in required_ops_tokens:
            if token.lower() not in operations.lower():
                errors.append(f"14_operations_runbook.md missing operations/debug token/section: {token}")

    background = docs.get("10_background_jobs.md", "")
    background_has_assets = any(
        token.lower() in background.lower()
        for token in ["EV-JOB-", "BackgroundService", "IHostedService", "ExecuteAsync", "HostedService", "worker", "job"]
    )
    if "[NOT_APPLICABLE]" not in background or background_has_assets:
        required_job_tokens = [
            "Registration",
            "Trigger",
            "Handler",
            "Side effects",
            "Retry",
            "Failure",
            "```mermaid",
            "flowchart",
        ]
        for token in required_job_tokens:
            if token.lower() not in background.lower():
                errors.append(f"10_background_jobs.md missing background job flow token/section: {token}")

    realtime = docs.get("11_realtime_signalr_socket.md", "")
    realtime_has_assets = any(
        token.lower() in realtime.lower()
        for token in ["EV-RT-", "SignalR", "Hub", "IHubContext", "WebSocket", "SendAsync", "HubConnectionBuilder"]
    )
    if "[NOT_APPLICABLE]" not in realtime or realtime_has_assets:
        required_realtime_tokens = [
            "Hub",
            "Route",
            "Event",
            "Direction",
            "Producer",
            "Consumer",
            "Payload",
            "Group",
            "Auth",
            "```mermaid",
            "sequenceDiagram",
        ]
        for token in required_realtime_tokens:
            if token.lower() not in realtime.lower():
                errors.append(f"11_realtime_signalr_socket.md missing realtime flow token/section: {token}")


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
    validate_inventory_backed_coverage(final_dir, errors)
    validate_per_route_api_contract_coverage(final_dir, errors)
    validate_document_capabilities(final_dir, errors)
    validate_evidence_bound_claims(final_dir, errors)
    validate_documented_config_paths(final_dir, errors)
    validate_runbook_url_commands(final_dir, errors)
    validate_background_job_detail(final_dir, errors)
    validate_database_store_contract(final_dir, errors)
    validate_80_percent_understanding_contract(final_dir, errors)
    validate_anti_skeleton(final_dir, indexed_ids, errors)
    validate_deep_document_requirements(final_dir, errors)

    if errors:
        print("FAIL: source-code handover quality checklist failed")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Quality checklist passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
