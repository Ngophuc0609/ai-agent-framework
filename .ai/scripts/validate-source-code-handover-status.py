#!/usr/bin/env python3
"""Validate source-code handover run status before publish."""

from __future__ import annotations

import re
import sys
from pathlib import Path


REQUIRED_AGENTS = [f"agent-{index:02d}" for index in range(1, 11)]
VALID_EXECUTION_MODES = {"subagent-isolated-worktrees", "isolated-sequential-sessions"}
COMPLETE_STATUSES = {"Complete", "Completed", "Ready", "PASS", "Passed"}
PUBLISH_PHASE_RE = re.compile(r"(phase\s*8|publish|complete|completed)", re.IGNORECASE)


def parse_status_table(text: str) -> dict[str, str]:
    fields: dict[str, str] = {}
    for line in text.splitlines():
        if not line.startswith("|"):
            continue
        cells = [cell.strip().strip("`") for cell in line.strip().strip("|").split("|")]
        if len(cells) >= 2 and cells[0] and cells[0] not in {"Field", "---"}:
            fields[cells[0]] = cells[1]
    return fields


def parse_agent_rows(text: str) -> dict[str, list[str]]:
    rows: dict[str, list[str]] = {}
    for line in text.splitlines():
        if not line.startswith("| agent-"):
            continue
        cells = [cell.strip().strip("`") for cell in line.strip().strip("|").split("|")]
        if cells:
            rows[cells[0]] = cells
    return rows


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: validate-source-code-handover-status.py <run_dir>")
        return 2

    run_dir = Path(sys.argv[1])
    status_path = run_dir / "STATUS.md"
    errors: list[str] = []

    if not status_path.is_file():
        print(f"FAIL: STATUS.md not found: {status_path}")
        return 1

    text = status_path.read_text(encoding="utf-8", errors="replace")
    fields = parse_status_table(text)
    agent_rows = parse_agent_rows(text)

    execution_mode = fields.get("Execution Mode", "")
    if execution_mode not in VALID_EXECUTION_MODES:
        errors.append(
            "STATUS.md Execution Mode must be one of "
            f"{sorted(VALID_EXECUTION_MODES)}, got {execution_mode!r}"
        )

    isolation = fields.get("Isolation Verified", "").lower()
    if isolation != "yes":
        errors.append(f"STATUS.md Isolation Verified must be yes before publish, got {isolation!r}")

    current_phase = fields.get("Current Phase", "")
    if not PUBLISH_PHASE_RE.search(current_phase):
        errors.append(f"STATUS.md Current Phase must indicate publish/complete, got {current_phase!r}")

    for agent in REQUIRED_AGENTS:
        row = agent_rows.get(agent)
        if not row:
            errors.append(f"STATUS.md missing execution row for {agent}")
            continue
        if len(row) < 6:
            errors.append(f"STATUS.md row for {agent} must include session/worktree/artifact/status/gate")
            continue
        session_id, worktree, artifact, status = row[1], row[2], row[3], row[4]
        if session_id in {"", "TBD", "N/A"}:
            errors.append(f"STATUS.md {agent} missing verified session/subagent id")
        if worktree in {"", "TBD", "N/A"}:
            errors.append(f"STATUS.md {agent} missing verified isolated worktree/session path")
        if artifact in {"", "TBD", "N/A"}:
            errors.append(f"STATUS.md {agent} missing canonical artifact")
        if status not in COMPLETE_STATUSES:
            errors.append(f"STATUS.md {agent} status must be complete before publish, got {status!r}")

    if errors:
        print("FAIL: source-code handover STATUS.md validation failed")
        for error in errors:
            print(f"- {error}")
        return 1

    print("STATUS.md validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
