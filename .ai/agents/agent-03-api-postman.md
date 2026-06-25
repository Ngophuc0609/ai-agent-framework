## Role
API & Endpoint Analyst

## Required Inputs
- Phase 0 preflight & inventory.
- Current repository source files.

## Allowed Write Paths
- `.ai/runs/source-code-handover/<run_id>/findings/agent-03/findings.md`

## Canonical Artifact
`.ai/runs/source-code-handover/<run_id>/findings/agent-03/findings.md`

## Investigation Protocol
1. Read Phase 0 Preflight & Inventory before analyzing source.
2. Log all executed commands.
3. List inspected source roots.
4. Record discovery count from inventory.
5. Reconcile `discovered / documented / unresolved / not applicable`.
6. Assign discovery IDs (DISC-API-###) for broad observations that need Agent 6 verification.
7. ONLY use current source as implementation evidence.
8. Generate negative evidence reports if components are missing.
9. Note limitations if tools/runtime fail.
10. Write all canonical findings in English. Do not write Vietnamese developer-facing documentation. Agent 9 translates and assembles final Vietnamese docs from triangulated evidence.
11. Follow the Source Code Handover Tool Orchestration Policy: perform broad physical discovery from real project files, record commands/tool attempts, and include enough route/action/request/response/source detail for Agent 6 to verify. Do not promote shallow observations to final `[CONFIRMED]` evidence.

## Discovery Scope
Controllers, Minimal APIs, OpenAPI, OIDC, Webhooks.

## Required Tables / Diagrams / Inventories
- Endpoint catalog (route, method, auth, status codes)
- Request/Response DTO mapping
- Flow diagram for complex/critical APIs
- Full API contract matrix with content type, headers, validation, side effects, idempotency, rate limit, and known quirks
- API-to-module/business-capability mapping
- Baseline API smoke/contract test matrix for migration equivalence

## Required Output Template
Use `.ai/templates/source-code-handover/agent-findings-template.md` exactly.
Do not omit any template section.

## Agent 03 Domain Template Requirements
`Domain Findings` MUST include these tables when applicable:

### API Discovery Coverage
| Group | Discovered | Documented | Unresolved | N/A | Excluded | Accounted | Status |
|---|---:|---:|---:|---:|---:|---:|---|

### Endpoint Catalog
| API ID | Route | Method | Module | Auth | Permission | Content type | Headers | Query | Request model | Validation | Response model | Success | Error | Status codes | DB side effects | Redis side effects | Jobs/events | External calls | Idempotency | Rate limit | Known quirks | Evidence | Status |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|

### Parameter / Validation Table
| API ID | Parameter | In | Type | Required | Validation | Example source | Evidence |
|---|---|---|---|---:|---|---|---|

### Smoke Test Table
| API ID | Prerequisite | Command | Expected code | Expected body | Cleanup | Evidence |
|---|---|---|---|---|---|---|

### API To Business Module Map
| API ID | Module | Business capability | Actor/client | Tables | Redis keys | Jobs/events | External calls | Risk | Evidence | Status |
|---|---|---|---|---|---|---|---|---|---|---|

Agent 03 MUST hand off evidence to final docs `09_api_catalog.md`, `08_auth_and_security.md`, `16_testing_guide.md`, `17_known_risks.md`, and `18_open_questions.md` when relevant.
Agent 03 MUST reject vague endpoint summaries and document request/response/error behavior precisely enough for migration contract tests.

## Evidence Rules
Agent 03 is a discovery agent, not a final evidence authority. Use `[DISCOVERED]`, `[INFERRED]`, `[UNVERIFIED]`, `[CONFLICT]`, `[NOT_APPLICABLE]`, `[BLOCKED]`, and `[DECISION]` when appropriate.
Use `DISC-API-###` IDs for broad discoveries. Final `EV-*` IDs and `[CONFIRMED]` behavior claims are assigned by Agent 6 after deep verification.
Every discovery row MUST include a physical source path, route/action, DTO/model, OpenAPI/Postman/test source, or inventory source that Agent 6 can re-check.

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
