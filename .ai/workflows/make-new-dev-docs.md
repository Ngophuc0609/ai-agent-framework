# Source Code Handover Workflow

## Execution Isolation Policy
Isolation mode hierarchy:
1. `subagent-isolated-worktrees`
2. `isolated-sequential-sessions`
3. `blocked-no-isolation-capability`

**Forbidden Legacy Modes**:
- `single-runtime-sequential-fallback`
- `single-session-multi-role-execution`
- `memory-only-agent-handoff`
- `implicit-agent-output`
- `direct-final-handbook-without-artifacts`

**No Isolation Capability Fallback**:
If the runtime cannot spawn subagents and cannot create isolated sessions:
- MUST STOP before Agent 1.
- Log `blocked-no-isolation-capability` in STATUS.md.
- MUST NOT run Agent 7.
- MUST NOT publish to `docs/`.
- MUST NOT mark `Partial`.
- Generate block report stating exact reason.

## STATUS.md Contract
Must create `.ai/runs/source-code-handover/<run_id>/STATUS.md` with:
- Run ID
- Source Commit
- Git Remote
- Branch
- Execution Mode
- Started At
- Current Phase
- Coordinator Session ID
- Table mapping: Agent | Session ID/Subagent ID | Worktree | Canonical Artifact | Status | Gate
If missing `session_id`, `subagent_id`, or `worktree`, Isolation Verified CANNOT be `yes`.

## Phase 0: Preflight + Deterministic Discovery
Coordinator MUST create `.ai/runs/source-code-handover/<run_id>/inventory/` before Agent 1 runs.
Mandatory JSON files:
- projects.json, entry-points.json, configuration-files.json, dbcontexts.json, dbsets.json, entities.json, entity-configurations.json, migrations.json, seed-data.json, raw-sql.json, controllers.json, routes.json, hubs.json, realtime-events.json, background-jobs.json, integrations.json, docker-services.json, ci-cd-files.json, tests.json.

Inventory Metadata Required:
`run_id`, `source_commit`, `generated_at`, `source_roots`, `discovery_method`, `status` (complete | partial | scan_failed), `items`, `limitations`.
Count 0 is ONLY allowed if scan succeeds but finds nothing. If scan fails, mark `scan_failed`.

## Pipeline Phases
Phase 1: Agent 1–5 Domain Analysis
Phase 2: Agent 6 Evidence/Coverage/Conflict Review (produces coverage reconciliation).
Phase 3: Agent 7 Final Documentation Assembly (outputs to `final/`).
Phase 4: Agent 8 Independent Quality Validation (outputs to `validation/`).
Phase 5: Revision if Agent 8 REJECTS.
Phase 6: Final publish (copies `final/` to `docs/`).

## Publish Gate Rule
Docs from `.ai/runs/.../final/` MUST NOT be copied/published to `docs/` unless Agent 8 outputs `PASS` in `final-verdict.md`.
If `REJECT_REQUIRES_REVISION`, `docs/` must not be overwritten.
