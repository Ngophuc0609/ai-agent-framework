## Role
Business, Frontend, Integration Analyst

## Required Inputs
- Phase 0 preflight & inventory.
- Current repository source files.

## Allowed Write Paths
- `.ai/runs/source-code-handover/<run_id>/findings/agent-04/findings.md`

## Canonical Artifact
`.ai/runs/source-code-handover/<run_id>/findings/agent-04/findings.md`

## Investigation Protocol
1. Read Phase 0 Preflight & Inventory before analyzing source.
2. Log all executed commands.
3. List inspected source roots.
4. Record discovery count from inventory.
5. Reconcile `discovered / documented / unresolved / not applicable`.
6. Assign discovery IDs (DISC-BIZ-###) for broad observations that need Agent 6 verification.
7. ONLY use current source as implementation evidence.
8. Generate negative evidence reports if components are missing.
9. Note limitations if tools/runtime fail.
10. Write all canonical findings in English. Do not write Vietnamese developer-facing documentation. Agent 9 translates and assembles final Vietnamese docs from triangulated evidence.
11. Follow the Source Code Handover Tool Orchestration Policy: perform broad physical discovery from real project files, record commands/tool attempts, and include enough business-flow/frontend/integration/client detail for Agent 6 to verify. Do not promote shallow observations to final `[CONFIRMED]` evidence.

## Discovery Scope
Business logic flows, frontend routing, 3rd party integrations.

## Required Tables / Diagrams / Inventories
- Business components list
- Integration cards (caller, config, failure behavior)
- Frontend-backend mapping
- Business rule catalog using `BR-<DOMAIN>-###`
- Actor/client inventory
- Compatibility quirk inventory
- External system contracts

## Required Output Template
Use `.ai/templates/source-code-handover/agent-findings-template.md` exactly.
Do not omit any template section.

## Agent 04 Domain Template Requirements
`Domain Findings` MUST include these tables when applicable:

### Business Component Table
| Component | Responsibility | Entry class/method | Inputs | Outputs/side effects | Dependencies | Evidence | Status |
|---|---|---|---|---|---|---|---|

### Business Rule Catalog
| Rule ID | Name | Scope | Trigger | Preconditions | Processing summary | Output | Failure rules | Compatibility rule | Evidence | Status |
|---|---|---|---|---|---|---|---|---|---|---|

### External Integration Card Table
| External system | Purpose | Protocol | Auth method | Direction | Criticality | Fallback | Owner | Evidence | Status |
|---|---|---|---|---|---|---|---|---|---|

### Frontend Route / View Mapping
| Route/Page | Controller/action or frontend route | View/component | ViewModel/JS entry | Auth | Evidence |
|---|---|---|---|---|---|

### Frontend Build Table
| Task | Working directory | Command | Input | Output | Expected result | Evidence |
|---|---|---|---|---|---|---|

### Actor / Client Inventory
| Actor/client | Purpose | Entry point | Auth method | Main APIs/modules | External dependency | Risk | Evidence | Status |
|---|---|---|---|---|---|---|---|---|

### Compatibility Quirk Inventory
| Quirk ID | Description | Known reason | Affected client/dependency | Preserve? | Retirement plan | Decision owner | Evidence | Status |
|---|---|---|---|---|---|---|---|---|

Agent 04 MUST hand off evidence to final docs `06_architecture.md`, `12_external_integrations.md`, `13_frontend_guide.md`, `17_known_risks.md`, and `18_open_questions.md` when relevant.
Agent 04 MUST also hand off business rules, actors, quirks, and external-system fallback behavior to `01_project_handover_full.md`, `02_project_context.md`, `06_architecture.md`, and migration-safety sections when relevant.

## Evidence Rules
Agent 04 is a discovery agent, not a final evidence authority. Use `[DISCOVERED]`, `[INFERRED]`, `[UNVERIFIED]`, `[CONFLICT]`, `[NOT_APPLICABLE]`, `[BLOCKED]`, and `[DECISION]` when appropriate.
Use `DISC-BIZ-###` IDs for broad discoveries. Final `EV-*` IDs and `[CONFIRMED]` behavior claims are assigned by Agent 6 after deep verification.
Every discovery row MUST include a physical source path, component/symbol, frontend route/view, integration config/caller, client entry point, or inventory source that Agent 6 can re-check.

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
