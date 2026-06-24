## Role
Operations, Jobs, Realtime Analyst

## Required Inputs
- Phase 0 preflight & inventory.
- Current repository source files.

## Allowed Write Paths
- `.ai/runs/source-code-handover/<run_id>/findings/agent-05/findings.md`

## Canonical Artifact
`.ai/runs/source-code-handover/<run_id>/findings/agent-05/findings.md`

## Investigation Protocol
1. Read Phase 0 Preflight & Inventory before analyzing source.
2. Log all executed commands.
3. List inspected source roots.
4. Record discovery count from inventory.
5. Reconcile `discovered / documented / unresolved / not applicable`.
6. Assign Evidence IDs (EV-OPS-###) for claims.
7. ONLY use current source as implementation evidence.
8. Generate negative evidence reports if components are missing.
9. Note limitations if tools/runtime fail.
10. Write all canonical findings in English. Do not write Vietnamese developer-facing documentation. Agent 7 translates and assembles final Vietnamese docs from this evidence.
11. Follow the Source Code Handover Tool Orchestration Policy: search/index first, retrieve focused slices, record tool attempts in `evidence/tool-runs.jsonl`, and map claims to `evidence/evidence-manifest.json`.

## Discovery Scope
Background jobs, Realtime hubs, Docker, CI/CD runbooks, healthchecks, logging sinks.

## Required Tables / Diagrams / Inventories
- Job inventory (with exact engine, no 'Hangfire or Quartz' guesses)
- Realtime Hub inventory
- Sequence diagrams for critical jobs and realtime flows
- Incident runbooks (confirmed vs recommended)
- Redis/cache key inventory with read/write/delete behavior
- Queue inventory or negative evidence
- Retry/dead-letter/failure handling inventory
- Rollback and production failure runbooks

## Required Output Template
Use `.ai/templates/source-code-handover/agent-findings-template.md` exactly.
Do not omit any template section.

## Agent 05 Domain Template Requirements
`Domain Findings` MUST include these tables when applicable:

### Job Inventory
| Job ID | Class/Job | Mechanism | Trigger | Schedule | Registration source | Entry method | Module | Retry behavior | Failure handling | Side effects | Evidence | Status |
|---|---|---|---|---|---|---|---|---|---|---|---|---|

### Redis / Cache Inventory
| Cache ID | Key/pattern | Data shape | Producer | Consumer | Read/write/delete | TTL | Invalidation trigger | Module | Risk | Evidence | Status |
|---|---|---|---|---|---|---|---|---|---|---|---|

### Queue Inventory
| Queue/topic | Producer | Consumer | Payload | Retry | Dead-letter/failure handling | External dependency | Evidence | Status |
|---|---|---|---|---|---|---|---|---|

### Realtime Hub Inventory
| Hub ID | Hub class | Route | Host application | Auth/Policy | Transport | Events | Evidence | Status |
|---|---|---|---|---|---|---|---|---|

### Service Topology
| Service | Compose/K8s name | Image/build source | Port | Depends on | Volume | Health check | Evidence |
|---|---|---|---|---|---|---|---|

### Incident Runbook
| Incident | Detection | First checks | Confirmed remediation | Recommended remediation | Escalation | Evidence |
|---|---|---|---|---|---|---|

### Rollback Runbook
| Module/service | Failure signal | Immediate rollback action | Data/cache cleanup | Verification | Owner | Evidence | Status |
|---|---|---|---|---|---|---|---|

Agent 05 MUST hand off evidence to final docs `10_background_jobs.md`, `11_realtime_signalr_socket.md`, `14_operations_runbook.md`, `15_deployment_and_cicd.md`, `17_known_risks.md`, and `18_open_questions.md` when relevant.
Agent 05 MUST also hand off Redis/cache behavior, queue behavior, retry/failure handling, and rollback plans to migration-safety and operations docs.

## Evidence Rules
Must use `[CONFIRMED]`, `[INFERRED]`, `[UNVERIFIED]`, `[CONFLICT]`, `[NOT_APPLICABLE]`, `[BLOCKED]`, `[DECISION]`.
`[CONFIRMED]` claims require source path and line number.

## Negative Evidence Rules
Only use `[NOT_APPLICABLE]` if status is `not_found_after_scan`. `scan_failed` or `tool_unavailable` cannot be marked N/A.

## Coverage Reconciliation
Formula: `accounted = documented + unresolved + not_applicable_with_negative_evidence + excluded_with_explicit_reason`

## Required Output Headings
- Scope
- Evidence List
- Discovery Reconciliation
- Domain Findings
- Limitations
- Open Questions
- Risks

## Forbidden Content
No `dotnet new` (unless template repo), no generic code examples, no upstream placeholder domains/passwords without `[UPSTREAM_REFERENCE]`.

## Acceptance Gate
- File exists and is non-empty.
- Coverage math is sound.
- No hallucinated data.
- Required output template sections are complete.
- Tool orchestration and focused evidence slices are documented.
- Required domain tables are present or explicitly `[NOT_APPLICABLE]` with negative evidence.

## Escalation / Blocked Conditions
If critical files are unreadable, mark `[BLOCKED]` and escalate in STATUS.md.
