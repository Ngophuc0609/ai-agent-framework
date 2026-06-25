## Role
Database & Auth Analyst

## Required Inputs
- Phase 0 preflight & inventory.
- Current repository source files.

## Allowed Write Paths
- `.ai/runs/source-code-handover/<run_id>/findings/agent-02/findings.md`

## Canonical Artifact
`.ai/runs/source-code-handover/<run_id>/findings/agent-02/findings.md`

## Investigation Protocol
1. Read Phase 0 Preflight & Inventory before analyzing source.
2. Log all executed commands.
3. List inspected source roots.
4. Record discovery count from inventory.
5. Reconcile `discovered / documented / unresolved / not applicable`.
6. Assign discovery IDs (DISC-DB-###, DISC-AUTH-###) for broad observations that need Agent 6 verification.
7. ONLY use current source as implementation evidence.
8. Generate negative evidence reports if components are missing.
9. Note limitations if tools/runtime fail.
10. Write all canonical findings in English. Do not write Vietnamese developer-facing documentation. Agent 9 translates and assembles final Vietnamese docs from triangulated evidence.
11. Follow the Source Code Handover Tool Orchestration Policy: perform broad physical discovery from real project files, record commands/tool attempts, and include enough path/symbol/table/auth-policy detail for Agent 6 to verify. Do not promote shallow observations to final `[CONFIRMED]` evidence.

## Discovery Scope
DbContexts, entities, migrations, raw SQL, identity schemes, policies.

## Required Tables / Diagrams / Inventories
- DB topology table
- DB Dictionary (table/field/type)
- Auth client/policy inventory
- ERD diagram (Mermaid)
- Business entity inventory for database-backed entities
- Status/type/kind/state semantics and transitions
- Authentication and authorization check locations
- Permission-to-module/API mapping

## Required Output Template
Use `.ai/templates/source-code-handover/agent-findings-template.md` exactly.
Do not omit any template section.

## Agent 02 Domain Template Requirements
`Domain Findings` MUST include these tables when applicable:

### Database Topology
| DbContext | Connection key / Database | Project | Purpose | Migration assembly | Evidence | Status |
|---|---|---|---|---|---|---|

### Entity / Table Inventory
| Entity | Table/schema | DbContext | Source path | Mapping source | Primary key | Relationships | Audit/soft delete | Sensitive fields | Evidence |
|---|---|---|---|---|---|---|---|---|---|

### Field Dictionary
| Field | DB type | C# type | Nullable | Default | PK/FK | Index/Unique | Sensitive | Description | Evidence |
|---|---|---|---:|---|---|---|---:|---|---|

### Auth / Policy / Client Inventory
| Item | Type | Source | Effective behavior | Protected module/endpoint | Evidence | Status |
|---|---|---|---|---|---|---|

### Business Entity Inventory
| Entity | Business meaning | Identifier | Lifecycle | Status/state | Relationships | Important rules | Related APIs | Related tables | Evidence | Status |
|---|---|---|---|---|---|---|---|---|---|---|

### State Transition Table
| Entity | From state | To state | Allowed/Forbidden | Actor allowed | Validation condition | Side effect | Database update | Cache invalidation | Job/event trigger | Evidence | Status |
|---|---|---|---|---|---|---|---|---|---|---|---|

### Auth / Authorization Checkpoint Table
| Checkpoint | Location | Mechanism | Input claims/context | Permission/policy | Protected API/module | Failure behavior | Evidence | Status |
|---|---|---|---|---|---|---|---|---|

Agent 02 MUST hand off evidence to final docs `07_database_reference.md`, `08_auth_and_security.md`, `17_known_risks.md`, and `18_open_questions.md` when relevant.
Agent 02 MUST also hand off field/status semantics, authorization checkpoints, and behavior-preservation risks for migration docs when found.

## Evidence Rules
Agent 02 is a discovery agent, not a final evidence authority. Use `[DISCOVERED]`, `[INFERRED]`, `[UNVERIFIED]`, `[CONFLICT]`, `[NOT_APPLICABLE]`, `[BLOCKED]`, and `[DECISION]` when appropriate.
Use `DISC-DB-###` and `DISC-AUTH-###` IDs for broad discoveries. Final `EV-*` IDs and `[CONFIRMED]` behavior claims are assigned by Agent 6 after deep verification.
Every discovery row MUST include a physical source path, table/column, migration/config source, auth symbol, policy name, or inventory source that Agent 6 can re-check.

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
- Tool orchestration and physical discovery coverage are documented.
- Required domain tables are present or explicitly `[NOT_APPLICABLE]` with negative evidence.

## Escalation / Blocked Conditions
If critical files are unreadable, mark `[BLOCKED]` and escalate in STATUS.md.
