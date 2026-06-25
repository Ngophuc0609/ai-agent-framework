#!/usr/bin/env python3
"""Validate Source Code Handover machine-readable evidence store."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


REQUIRED_FILES = [
    "tool-runs.jsonl",
    "evidence-manifest.json",
    "focused-slices.json",
    "symbol-reference-map.json",
    "data-flow-map.json",
    "sql-metadata.json",
    "api-contract-sources.json",
    "runtime-artifacts.json",
    "tool-limitations.json",
]

EVIDENCE_RE = re.compile(r"\bEV-(?:REPO|CONFIG|DB|MIGRATION|AUTH|API|JOB|RT|OPS|CICD|TEST|NEG(?:-[A-Z]+)?)-\d{3}\b")
REQUIRED_AGENTS = {f"agent-{index:02d}" for index in range(1, 11)}
REQUIRED_TOOL_CATEGORIES = {
    "fast_search",
    "build",
    "symbol",
    "semantic",
    "pattern_scan",
    "api_contract",
    "runtime_artifact",
}

CATEGORY_ALIASES = {
    "build_compile_context": "build",
    "symbol_navigation": "symbol",
    "semantic_analysis": "semantic",
    "api_contract_parser": "api_contract",
    "runtime_artifact_parser": "runtime_artifact",
}


def load_json(path: Path, errors: list[str]) -> object | None:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        errors.append(f"{path.name}: invalid JSON: {exc}")
        return None


def validate_tool_runs(path: Path, errors: list[str]) -> None:
    lines = [line for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    if len(lines) < 10:
        errors.append("tool-runs.jsonl: must contain at least 10 agent/tool attempts for a full source handover run")
        if not lines:
            return
    required = {"run_id", "agent_id", "tool_category", "tool", "status"}
    agents_seen: set[str] = set()
    categories_seen: set[str] = set()
    for index, line in enumerate(lines, start=1):
        try:
            item = json.loads(line)
        except json.JSONDecodeError as exc:
            errors.append(f"tool-runs.jsonl:{index}: invalid JSON: {exc}")
            continue
        missing = sorted(required - set(item))
        if missing:
            errors.append(f"tool-runs.jsonl:{index}: missing keys: {', '.join(missing)}")
        agent_id = str(item.get("agent_id", ""))
        if agent_id:
            agents_seen.add(agent_id)
        category = str(item.get("tool_category", "")).lower().replace(" ", "_").replace("/", "_")
        category = CATEGORY_ALIASES.get(category, category)
        if category:
            categories_seen.add(category)
    missing_agents = sorted(REQUIRED_AGENTS - agents_seen)
    if missing_agents:
        errors.append("tool-runs.jsonl: missing tool attempts for agents: " + ", ".join(missing_agents))
    missing_categories = sorted(REQUIRED_TOOL_CATEGORIES - categories_seen)
    if missing_categories:
        errors.append("tool-runs.jsonl: missing required tool categories: " + ", ".join(missing_categories))


def validate_evidence_manifest(path: Path, errors: list[str]) -> set[str]:
    data = load_json(path, errors)
    if not isinstance(data, dict):
        errors.append("evidence-manifest.json: top-level value must be an object")
        return set()
    evidence = data.get("evidence")
    if not isinstance(evidence, list) or not evidence:
        errors.append("evidence-manifest.json: evidence must be a non-empty list")
        return set()
    ids: set[str] = set()
    required = {"evidence_id", "claim", "source_type", "verification_type", "producing_agent", "status"}
    for index, item in enumerate(evidence, start=1):
        if not isinstance(item, dict):
            errors.append(f"evidence-manifest.json evidence[{index}]: must be an object")
            continue
        missing = sorted(required - set(item))
        if missing:
            errors.append(f"evidence-manifest.json evidence[{index}]: missing keys: {', '.join(missing)}")
        evidence_id = str(item.get("evidence_id", ""))
        if not EVIDENCE_RE.fullmatch(evidence_id):
            errors.append(f"evidence-manifest.json evidence[{index}]: invalid evidence_id: {evidence_id!r}")
        else:
            ids.add(evidence_id)
    return ids


def validate_focused_slices(path: Path, evidence_ids: set[str], errors: list[str]) -> None:
    data = load_json(path, errors)
    if not isinstance(data, dict):
        errors.append("focused-slices.json: top-level value must be an object")
        return
    slices = data.get("slices")
    if not isinstance(slices, list) or not slices:
        errors.append("focused-slices.json: slices must be a non-empty list")
        return
    required = {"slice_id", "evidence_id", "source_type", "source_path", "range_or_symbol", "reason"}
    for index, item in enumerate(slices, start=1):
        if not isinstance(item, dict):
            errors.append(f"focused-slices.json slices[{index}]: must be an object")
            continue
        missing = sorted(required - set(item))
        if missing:
            errors.append(f"focused-slices.json slices[{index}]: missing keys: {', '.join(missing)}")
        evidence_id = str(item.get("evidence_id", ""))
        if evidence_ids and evidence_id not in evidence_ids:
            errors.append(f"focused-slices.json slices[{index}]: evidence_id not in manifest: {evidence_id}")


def validate_json_file(path: Path, errors: list[str]) -> None:
    data = load_json(path, errors)
    if data is None:
        return
    if data in ({}, []):
        errors.append(f"{path.name}: file must contain a status, items, limitations, or records")
    if isinstance(data, dict) and len(json.dumps(data, ensure_ascii=False)) < 80:
        errors.append(f"{path.name}: file is too small to be meaningful evidence")


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: validate-source-code-handover-evidence-store.py <evidence_dir>")
        return 2
    evidence_dir = Path(sys.argv[1])
    errors: list[str] = []
    if not evidence_dir.is_dir():
        print(f"FAIL: evidence directory not found: {evidence_dir}")
        return 1

    for name in REQUIRED_FILES:
        if not (evidence_dir / name).is_file():
            errors.append(f"missing evidence store file: {name}")

    tool_runs = evidence_dir / "tool-runs.jsonl"
    if tool_runs.exists():
        validate_tool_runs(tool_runs, errors)

    evidence_ids: set[str] = set()
    manifest = evidence_dir / "evidence-manifest.json"
    if manifest.exists():
        evidence_ids = validate_evidence_manifest(manifest, errors)

    focused = evidence_dir / "focused-slices.json"
    if focused.exists():
        validate_focused_slices(focused, evidence_ids, errors)

    for name in REQUIRED_FILES:
        if name in {"tool-runs.jsonl", "evidence-manifest.json", "focused-slices.json"}:
            continue
        path = evidence_dir / name
        if path.exists():
            validate_json_file(path, errors)

    if errors:
        print("FAIL: source-code handover evidence store validation failed")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Evidence store validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
