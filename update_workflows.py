import os

def write_file(path, content):
    with open(path, "w") as f:
        f.write(content.strip() + "\n")

workflow_md = """
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
"""

routing_md = """
# Model Routing for Dev Docs

If the repository has: authentication, payment, SignalR, PII, Kubernetes, Background Jobs, or DB Migrations, `FAST_CHEAP` is FORBIDDEN for Agents 2, 3, 5, 6, and 8.

Default routing for auth-heavy/IdentityServer projects:
- Agent 1: BALANCED
- Agent 2: REASONING_STRONG
- Agent 3: REASONING_STRONG
- Agent 4: BALANCED
- Agent 5: REASONING_STRONG
- Agent 6: REASONING_STRONG
- Agent 7: LONG_CONTEXT_STRONG
- Agent 8: REASONING_STRONG

## Routing Fallback
Nếu runner không hỗ trợ model routing:
- Ghi limitation vào STATUS.md.
- Không được tự đánh dấu model quality là verified.
- Nếu Agent 2/3/5/6/8 không thể chạy bằng tier tối thiểu BALANCED (hoặc tương đương), readiness tối đa là `Partial`.
- Nếu không thể chạy independent validation (Agent 8), readiness tối đa là `Blocked`.
"""

dod_md = """
# Documentation Definition of Done (DoD)

Mọi agent tham gia quá trình Handover phải tuân thủ nghiêm ngặt chuẩn này.

## 1. Quy tắc chung: mỗi claim phải có Evidence
- Status: `[CONFIRMED]`, `[INFERRED]`, `[UNVERIFIED]`, `[CONFLICT]`, `[NOT_APPLICABLE]`, `[BLOCKED]`
- Mọi `[CONFIRMED]` claim BẮT BUỘC có Evidence ID.

## 2. Bộ tài liệu mục tiêu (20 files in lowercase with prefix)
- `01_project_handover_full.md`
- `02_project_context.md`
- `03_repository_guide.md`
- `04_local_setup.md`
- `05_configuration_reference.md`
- `06_architecture.md`
- `07_database_reference.md`
- `08_auth_and_security.md`
- `09_api_catalog.md`
- `10_background_jobs.md`
- `11_realtime_signalr_socket.md`
- `12_external_integrations.md`
- `13_frontend_guide.md`
- `14_operations_runbook.md`
- `15_deployment_and_cicd.md`
- `16_testing_guide.md`
- `17_known_risks.md`
- `18_open_questions.md`
- `19_evidence_index.md`
- `20_documentation_coverage.md`

## 3. Mandatory Coverage Rule
Coverage math denominator MUST come from Phase 0 inventory.
`accounted = documented + unresolved + not_applicable_with_negative_evidence + excluded_with_explicit_reason`

## 4. Documentation Coverage Manifest (20_documentation_coverage.md)
Must use structural tables grouping by domain (Repository, Database, API, Background Jobs, Realtime) listing: `discovered`, `documented`, `accounted`, `unresolved`, `status`, `gaps`.

## 5. Negative Evidence Rule
`[NOT_APPLICABLE]` is ONLY valid when documented with: Component/scope, source roots, search patterns, tools used, results, impact, and negative evidence ID. It cannot be used if status is `scan_failed` or `tool_unavailable`.

## 6. Evidence Index chuẩn hóa
`19_evidence_index.md` MUST contain table:
`Evidence ID | Topic | Claim | Source Path | Line/Method | Verification Type | Source Commit | Status`
Valid ID patterns: `EV-REPO-###`, `EV-CONFIG-###`, `EV-DB-###`, `EV-MIGRATION-###`, `EV-AUTH-###`, `EV-API-###`, `EV-JOB-###`, `EV-RT-###`, `EV-OPS-###`, `EV-TEST-###`, `EV-CICD-###`, `EV-NEG-###`.
"""

write_file(".ai/workflows/make-new-dev-docs.md", workflow_md)
write_file(".ai/workflows/make-new-dev-docs-model-routing.md", routing_md)
write_file(".ai/rules/07-handover-documentation-dod.md", dod_md)

print("Updated Workflows and Rules")
