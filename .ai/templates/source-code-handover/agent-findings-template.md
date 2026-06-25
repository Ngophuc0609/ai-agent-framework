# Source Code Handover Agent Findings Template

Use this template for every Agent 1-5 findings artifact:

```text
.ai/runs/source-code-handover/<run_id>/findings/agent-XX/findings.md
```

Do not remove sections. If a section has no findings, write `None.` or `[NOT_APPLICABLE]` with negative evidence.

Agent 1-5 findings are broad physical discovery artifacts. They are not final evidence authority artifacts. Use `DISC-*` IDs for shallow discoveries and reserve final `EV-*` IDs for Agent 6 verified evidence unless the runner explicitly provides already-verified evidence.

This is an AI-facing intermediate artifact template. All prose in generated Agent 1-5 findings MUST be English.

## Required Front Matter

```yaml
---
run_id: "<run_id>"
source_commit: "<git_sha>"
source_branch: "<branch>"
created_at: "<ISO-8601 timestamp>"
status: "Ready | Partial | Blocked"
agent_id: "agent-XX"
agent_role: "<role>"
inventory_inputs:
  - "<inventory-file>.json"
evidence_ids:
  - "DISC-XXX-001"
---
```

## Required Body Template

```md
## Scope

| Item | Value |
|---|---|
| Agent | agent-XX |
| Domain | <domain> |
| Source roots inspected | `<path>`, `<path>` |
| Inventory files read | `<file>.json` |
| Source commit | `<git_sha>` |
| Status | Ready / Partial / Blocked |

## Commands Executed

| Command | Working directory | Purpose | Result | Evidence |
|---|---|---|---|---|
| `<command>` | `<path>` | `<why>` | `<summary>` | EV-XXX-001 |

## Tool Orchestration

| Tool category | Tool/query | Scope target | Output artifact | Status | Limitation |
|---|---|---|---|---|---|
| Fast search / Symbol / Semantic / SQL / Runtime | `<tool or query>` | `<route/symbol/table/key/job/config>` | `evidence/<artifact>.json` | complete / partial / tool_unavailable / not_applicable | `<limitation>` |

## Physical Discovery Inventory

| Discovery ID | Item type | Name/identifier | Physical source path/object | Range/symbol/query | Discovery method | Verification needed by Agent 6 | Status |
|---|---|---|---|---|---|---|---|
| DISC-XXX-001 | Project / Route / Table / Config / Redis key / Job / Integration / Business rule | `<identifier>` | `<path-or-object>` | `<line range, method, query, key, or unknown>` | `<rg/build/parser/manual focused read>` | yes / no | [DISCOVERED] / [INFERRED] / [UNVERIFIED] / [CONFLICT] |

## Focused Evidence Slices

| Slice ID | Evidence ID | Source type | Source path/object | Range/symbol/query | Why admitted to context |
|---|---|---|---|---|---|
| SLICE-XXX-001 | DISC-XXX-001 | Source / SQL / API contract / Runtime / Git history | `<path-or-object>` | `<line range, method, query, key>` | `<candidate supported; Agent 6 must verify before final docs>` |

## Evidence List / Discovery References

| ID | Claim or discovery candidate | Source path | Line/method/object | Verification type | Status |
|---|---|---|---|---|---|
| DISC-XXX-001 | `<specific observed item>` | `<path>` | `<line/method/object>` | Physical discovery / Inventory / Negative evidence | [DISCOVERED] |

## Discovery Reconciliation

| Domain item | Inventory source | Discovered | Documented | Unresolved | N/A | Excluded | Accounted | Result |
|---|---|---:|---:|---:|---:|---:|---:|---|
| `<item>` | `<inventory>.json` | 0 | 0 | 0 | 0 | 0 | 0 | PASS / PARTIAL / FAIL |

Formula: `Accounted = Documented + Unresolved + N/A + Excluded`

## Domain Findings

### <Finding Title>

[DISCOVERED] <One source-observed discovery candidate. Do not present as final proof until Agent 6 verifies it.>

Evidence:
- DISC-XXX-001
- Source: `<path>`, method/line `<method-or-line>`
- Source commit: `<git_sha>`

Impact for final docs:
- Add/update `<final-doc-name>.md` section `<section-name>`.

## Required Domain Tables

<Insert the agent-specific required tables from the agent spec.>

When the agent domain touches database, API, background jobs, or realtime, include these deep-discovery tables so Agent 6-8 can verify without rescanning from scratch.

### Database Discovery Table

| Discovery ID | DbContext | Entity/DbSet | Table/schema | Field count | Mapping source | Source path | Verification needed | Status |
|---|---|---|---|---:|---|---|---|---|
| DISC-DB-001 | `<DbContext>` | `<Entity>` | `<Table>` | 0 | DataAnnotations / Fluent API / Migration / SQL metadata / convention | `<path>` | yes | [DISCOVERED] |

### API Discovery Table

| Discovery ID | Route | Method | Controller/action | Request DTO/model | Response DTO/model | Auth marker | Source path | Verification needed | Status |
|---|---|---|---|---|---|---|---|---|---|
| DISC-API-001 | `<route>` | GET/POST/... | `<Controller.Action>` | `<RequestModel or none>` | `<ResponseModel or unknown>` | `<Authorize/policy/unknown>` | `<path>` | yes | [DISCOVERED] |

### Background Job Discovery Table

| Discovery ID | Job/worker | Registration source | Trigger/schedule | Handler | Queue/storage | Side-effect candidates | Source path | Verification needed | Status |
|---|---|---|---|---|---|---|---|---|---|
| DISC-JOB-001 | `<job>` | `<registration>` | `<cron/timer/queue/startup>` | `<handler>` | `<storage>` | SQL / Redis / external / log | `<path>` | yes | [DISCOVERED] |

### Realtime Discovery Table

| Discovery ID | Hub/socket/event | Route/event name | Producer | Consumer/client handler | Payload model/fields | Group/user mapping | Source path | Verification needed | Status |
|---|---|---|---|---|---|---|---|---|---|
| DISC-RT-001 | `<hub>` | `<route/event>` | `<producer>` | `<consumer or unknown>` | `<payload>` | `<mapping>` | `<path>` | yes | [DISCOVERED] |

## Negative Evidence

### <Component Not Found>

Status: [NOT_APPLICABLE]

Checked:
- Source roots: `<path>`
- Search patterns: `<pattern>`
- Command/tool: `<command>`
- Result: `<count/result>`

Impact:
- `<impact>`

Evidence:
- EV-NEG-XXX-001

## Limitations

| Limitation | Impact | Status | Follow-up |
|---|---|---|---|
| `<limitation>` | `<impact>` | [BLOCKED] / [UNVERIFIED] | `<next action>` |

## Open Questions

| Question ID | Question | Why it matters | Evidence checked | Suggested owner | Blocking level | Next action |
|---|---|---|---|---|---|---|
| Q-XXX-001 | `<question>` | `<impact>` | EV-XXX-001 | `<owner>` | Critical / High / Medium / Low | `<next action>` |

## Risks

| Risk ID | Severity | Status | Evidence | Impact | Precondition | Owner | Remediation | Next step |
|---|---|---|---|---|---|---|---|---|
| RISK-XXX-001 | Critical / High / Medium / Low | [CONFIRMED] / [INFERRED] | EV-XXX-001 | `<impact>` | `<precondition>` | `<owner>` | `<fix>` | `<next step>` |

## Final-Doc Handoff

| Final document | Section to update | Evidence IDs | Status |
|---|---|---|---|
| `<NN_doc.md>` | `<section>` | DISC-XXX-001 pending Agent 6 EV promotion | Ready / Partial / Blocked |
```

## Pass Criteria

- Every discovery candidate has a discovery ID and physical source path/object, or a clear limitation.
- Agent 1-5 do not present shallow findings as final `[CONFIRMED]` claims.
- Every important discovery candidate is specific enough for Agent 6 to verify without rescanning from scratch.
- High-risk flows are marked for Agent 6 deep verification.
- Coverage math is valid.
- Missing components use negative evidence.
- Assumptions use `[UNVERIFIED]`, conflicts use `[CONFLICT]`, and migration/behavior-preservation decisions use `[DECISION]`.
- Final-doc handoff maps findings to one or more final documents.

## Mini Examples

Good discovery row:

```md
| DISC-API-014 | Route | `POST /quiz-submit` | `src/WebApi/Controllers/QuizSubmitController.cs` | `QuizSubmitController.Submit` | `rg "quiz-submit|Submit"` | yes | [DISCOVERED] |
```

Bad discovery row:

```md
| DISC-BIZ-001 | Module | Accounts | unknown | unknown | model memory | no | [CONFIRMED] |
```

Reject the bad row because it uses model memory, has no physical source path, has no verifiable symbol/query, and marks a discovery as `[CONFIRMED]`.
