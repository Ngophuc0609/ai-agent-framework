# Source Code Handover Agent Findings Template

Use this template for every Agent 1-5 findings artifact:

```text
.ai/runs/source-code-handover/<run_id>/findings/agent-XX/findings.md
```

Do not remove sections. If a section has no findings, write `None.` or `[NOT_APPLICABLE]` with negative evidence.

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
  - "EV-XXX-001"
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

## Focused Evidence Slices

| Slice ID | Evidence ID | Source type | Source path/object | Range/symbol/query | Why admitted to context |
|---|---|---|---|---|---|
| SLICE-XXX-001 | EV-XXX-001 | Source / SQL / API contract / Runtime / Git history | `<path-or-object>` | `<line range, method, query, key>` | `<claim supported>` |

## Evidence List

| Evidence ID | Claim | Source path | Line/method | Verification type | Status |
|---|---|---|---|---|---|
| EV-XXX-001 | `<specific claim>` | `<path>` | `<line/method>` | Source / CodeGraph / Negative evidence | [CONFIRMED] |

## Discovery Reconciliation

| Domain item | Inventory source | Discovered | Documented | Unresolved | N/A | Excluded | Accounted | Result |
|---|---|---:|---:|---:|---:|---:|---:|---|
| `<item>` | `<inventory>.json` | 0 | 0 | 0 | 0 | 0 | 0 | PASS / PARTIAL / FAIL |

Formula: `Accounted = Documented + Unresolved + N/A + Excluded`

## Domain Findings

### <Finding Title>

[CONFIRMED] <One evidence-backed claim.>

Evidence:
- EV-XXX-001
- Source: `<path>`, method/line `<method-or-line>`
- Source commit: `<git_sha>`

Impact for final docs:
- Add/update `<final-doc-name>.md` section `<section-name>`.

## Required Domain Tables

<Insert the agent-specific required tables from the agent spec.>

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
| `<NN_doc.md>` | `<section>` | EV-XXX-001 | Ready / Partial / Blocked |
```

## Pass Criteria

- Every `[CONFIRMED]` claim has an Evidence ID.
- Every Evidence ID has source path, method/line, verification type, and source commit.
- Every important claim maps to the run evidence store.
- High-risk flows use focused slices plus symbol/call/data-flow or independent runtime/test/API evidence when available.
- Coverage math is valid.
- Missing components use negative evidence.
- Assumptions use `[UNVERIFIED]`, conflicts use `[CONFLICT]`, and migration/behavior-preservation decisions use `[DECISION]`.
- Final-doc handoff maps findings to one or more final documents.
