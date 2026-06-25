#!/usr/bin/env python3
"""Validate final docs against verified physical evidence.

This validator enforces the Source Code Handover discovery/evidence split:
- Agent 1-5 may produce DISC-* discovery candidates.
- Final documents may only use verified EV-* evidence from Agents 6-8.
- Final EV-* IDs must exist in the machine-readable evidence manifest.
- Source evidence must point to real repository files.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any


EV_RE = re.compile(r"\bEV-(?:REPO|CONFIG|DB|MIGRATION|AUTH|API|JOB|RT|OPS|CICD|TEST|NEG(?:-[A-Z]+)?)-\d{3}\b")
DISC_RE = re.compile(r"\bDISC-(?:REPO|CONFIG|DB|AUTH|API|BIZ|OPS|JOB|RT|CICD|TEST|NEG(?:-[A-Z]+)?)-\d{3}\b")
AGENT_1_5 = {"agent-01", "agent-02", "agent-03", "agent-04", "agent-05"}


def load_json(path: Path, errors: list[str]) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        errors.append(f"{path}: invalid JSON: {exc}")
        return None


def extract_ids_from_markdown(path: Path, pattern: re.Pattern[str]) -> set[str]:
    return set(pattern.findall(path.read_text(encoding="utf-8", errors="replace")))


def resolve_source_path(repo_root: Path, source_path: str) -> Path:
    candidate = Path(source_path)
    if candidate.is_absolute():
        return candidate
    return repo_root / source_path


def is_probably_repo_file_source(source_path: str) -> bool:
    if not source_path or source_path.startswith("<"):
        return False
    lowered = source_path.lower()
    non_file_markers = (
        "sql:",
        "table:",
        "procedure:",
        "view:",
        "index:",
        "redis:",
        "api:",
        "route:",
        "runtime:",
        "log:",
        "git:",
        "postman:",
        "openapi:",
        "swagger:",
    )
    return not lowered.startswith(non_file_markers)


def main() -> int:
    if len(sys.argv) not in {2, 3}:
        print("Usage: validate-source-code-handover-physical-evidence.py <run_dir> [repo_root]")
        return 2

    run_dir = Path(sys.argv[1])
    repo_root = Path(sys.argv[2]) if len(sys.argv) == 3 else Path.cwd()
    final_dir = run_dir / "final"
    evidence_dir = run_dir / "evidence"
    errors: list[str] = []

    if not final_dir.is_dir():
        print(f"FAIL: final directory not found: {final_dir}")
        return 1
    if not evidence_dir.is_dir():
        print(f"FAIL: evidence directory not found: {evidence_dir}")
        return 1

    manifest_path = evidence_dir / "evidence-manifest.json"
    focused_path = evidence_dir / "focused-slices.json"
    index_path = final_dir / "19_evidence_index.md"

    if not manifest_path.is_file():
        errors.append(f"missing evidence manifest: {manifest_path}")
    if not focused_path.is_file():
        errors.append(f"missing focused slices: {focused_path}")
    if not index_path.is_file():
        errors.append(f"missing final evidence index: {index_path}")

    manifest_ids: set[str] = set()
    manifest_by_id: dict[str, dict[str, Any]] = {}
    if manifest_path.is_file():
        manifest = load_json(manifest_path, errors)
        if isinstance(manifest, dict) and isinstance(manifest.get("evidence"), list):
            for item in manifest["evidence"]:
                if not isinstance(item, dict):
                    continue
                evidence_id = str(item.get("evidence_id", ""))
                if EV_RE.fullmatch(evidence_id):
                    manifest_ids.add(evidence_id)
                    manifest_by_id[evidence_id] = item
        else:
            errors.append("evidence-manifest.json: expected top-level object with evidence list")

    focused_ids: set[str] = set()
    if focused_path.is_file():
        focused = load_json(focused_path, errors)
        if isinstance(focused, dict) and isinstance(focused.get("slices"), list):
            for item in focused["slices"]:
                if isinstance(item, dict):
                    evidence_id = str(item.get("evidence_id", ""))
                    if EV_RE.fullmatch(evidence_id):
                        focused_ids.add(evidence_id)
        else:
            errors.append("focused-slices.json: expected top-level object with slices list")

    index_ids = extract_ids_from_markdown(index_path, EV_RE) if index_path.is_file() else set()
    final_ids: set[str] = set()
    final_disc_ids: dict[str, set[str]] = {}
    for doc in sorted(final_dir.glob("*.md")):
        doc_ev = extract_ids_from_markdown(doc, EV_RE)
        final_ids.update(doc_ev)
        disc_ids = extract_ids_from_markdown(doc, DISC_RE)
        if disc_ids:
            final_disc_ids[doc.name] = disc_ids

    for doc_name, disc_ids in final_disc_ids.items():
        errors.append(
            f"{doc_name}: final docs must not use DISC-* discovery IDs as proof: {', '.join(sorted(disc_ids))}"
        )

    for evidence_id in sorted(final_ids):
        if evidence_id not in index_ids:
            errors.append(f"{evidence_id}: used in final docs but missing from final/19_evidence_index.md")
        if evidence_id not in manifest_ids:
            errors.append(f"{evidence_id}: used in final docs but missing from evidence/evidence-manifest.json")
        manifest_item = manifest_by_id.get(evidence_id, {})
        source_type = str(manifest_item.get("source_type", "")).lower()
        if evidence_id not in focused_ids and source_type != "negative":
            errors.append(f"{evidence_id}: used in final docs but missing from evidence/focused-slices.json")

    for evidence_id in sorted(index_ids):
        if evidence_id not in manifest_ids:
            errors.append(f"{evidence_id}: indexed in 19_evidence_index.md but missing from evidence manifest")

    for evidence_id, item in sorted(manifest_by_id.items()):
        source_type = str(item.get("source_type", "")).lower()
        source_path = str(item.get("source_path", ""))
        range_or_symbol = str(item.get("range_or_symbol", ""))
        producing_agent = str(item.get("producing_agent", ""))
        status = str(item.get("status", ""))

        if not source_path:
            errors.append(f"{evidence_id}: missing source_path in evidence manifest")
        if not range_or_symbol:
            errors.append(f"{evidence_id}: missing range_or_symbol in evidence manifest")
        if evidence_id in final_ids and producing_agent in AGENT_1_5:
            errors.append(
                f"{evidence_id}: final evidence is produced by {producing_agent}; Agent 1-5 discoveries must be promoted by Agents 6-8 before final docs"
            )
        if source_type == "source" and "[BLOCKED]" not in status and is_probably_repo_file_source(source_path):
            resolved = resolve_source_path(repo_root, source_path)
            if not resolved.is_file():
                errors.append(f"{evidence_id}: source file not found for source_path={source_path!r}")

    if errors:
        print("FAIL: source-code handover physical evidence validation failed")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Physical evidence validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
