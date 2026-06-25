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
    require_text_contains_items("07_database_reference.md", database_doc, dbset_names, errors, "DbSet names")
    require_text_contains_items("07_database_reference.md", database_doc, entity_names, errors, "entity names")
    require_text_contains_items("07_database_reference.md", database_doc, table_names, errors, "table names")

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


def validate_anti_skeleton(final_dir: Path, indexed_ids: set[str], errors: list[str]) -> None:
    docs = {path.name: path.read_text(encoding="utf-8") for path in final_dir.glob("*.md")}
    combined = "\n".join(docs.values())
    total_words = len(re.findall(r"\b[\wÀ-ỹ]+\b", combined, flags=re.UNICODE))
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
            "Field",
            "Type",
            "Required",
            "Validation",
            "Auth",
            "Status codes",
            "DB side effects",
        ]
        for token in required_api_tokens:
            if token.lower() not in api_catalog.lower():
                errors.append(f"09_api_catalog.md missing deep API contract token/section: {token}")

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
    validate_document_capabilities(final_dir, errors)
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
