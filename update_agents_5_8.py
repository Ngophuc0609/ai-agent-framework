import os

def write_file(path, content):
    with open(path, "w") as f:
        f.write(content.strip() + "\n")

common_sections = """
## Role
{role}

## Inputs bắt buộc
- Phase 0 preflight & inventory.
- Current repository source files.

## Allowed Write Paths
- `.ai/runs/source-code-handover/<run_id>/findings/{agent_id}/findings.md`

## Canonical Artifact
`.ai/runs/source-code-handover/<run_id>/findings/{agent_id}/findings.md`

## Investigation Protocol
1. Read Phase 0 Preflight & Inventory before analyzing source.
2. Log all executed commands.
3. List inspected source roots.
4. Record discovery count from inventory.
5. Reconcile `discovered / documented / unresolved / not applicable`.
6. Assign Evidence IDs (EV-{prefix}-###) for claims.
7. ONLY use current source as implementation evidence.
8. Generate negative evidence reports if components are missing.
9. Note limitations if tools/runtime fail.

## Discovery Scope
{scope}

## Required Tables / Diagrams / Inventories
{tables}

## Evidence Rules
Must use `[CONFIRMED]`, `[INFERRED]`, `[UNVERIFIED]`, `[CONFLICT]`, `[NOT_APPLICABLE]`, `[BLOCKED]`.
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

## Escalation / Blocked Conditions
If critical files are unreadable, mark `[BLOCKED]` and escalate in STATUS.md.
"""

agent_5 = common_sections.format(
    role="Operations, Jobs, Realtime Analyst",
    agent_id="agent-05",
    prefix="OPS",
    scope="Background jobs, Realtime hubs, Docker, CI/CD runbooks, healthchecks, logging sinks.",
    tables="- Job inventory (with exact engine, no 'Hangfire or Quartz' guesses)\n- Realtime Hub inventory\n- Sequence diagrams for critical jobs and realtime flows\n- Incident runbooks (confirmed vs recommended)"
)

agent_6 = """
## Role
Evidence/Coverage/Conflict Reviewer

## Inputs bắt buộc
- Phase 0 inventory.
- Findings from Agents 1-5.

## Allowed Write Paths
- `.ai/runs/source-code-handover/<run_id>/review/`

## Canonical Artifact
- `.ai/runs/source-code-handover/<run_id>/review/review.md`
- `.ai/runs/source-code-handover/<run_id>/review/coverage-reconciliation.md`
- `.ai/runs/source-code-handover/<run_id>/review/conflicts.md`
- `.ai/runs/source-code-handover/<run_id>/review/template-contamination-report.md`
- `.ai/runs/source-code-handover/<run_id>/review/readiness-decision.md`

## Investigation Protocol
1. Compare findings vs Phase 0 Inventory.
2. Review coverage math using exact denominators from inventory.
3. Reject findings lacking evidence or containing generic samples.
4. Output specific review canonical artifacts.

## Required Tables / Diagrams / Inventories
Coverage Reconciliation Table using formula: `accounted = documented + unresolved + not_applicable_with_negative_evidence + excluded_with_explicit_reason`
Columns: Domain | Discovered from | Discovered | Documented | Unresolved | N/A | Excluded | Accounted | Result

## Acceptance Gate
- All review canonical artifacts created.
- Readiness decision is explicit.

## Escalation / Blocked Conditions
Block Agent 7 if coverage reconciliation fails or missing critical evidence.
"""

agent_7 = """
## Role
Single Handbook Aggregator

## Inputs bắt buộc
- Phase 0 Preflight + Inventory.
- Phase 1 (Agents 1-5) canonical findings.
- Phase 2 (Agent 6) review artifacts (coverage, conflicts, readiness).
- `STATUS.md`.
Note: Agent 7 MUST NOT read Agent 8 output before the first validation.

## Allowed Write Paths
- `.ai/runs/source-code-handover/<run_id>/final/`

## Canonical Artifact
- `.ai/runs/source-code-handover/<run_id>/final/01_project_handover_full.md` to `20_documentation_coverage.md`

## Investigation Protocol
1. ONLY aggregate from Phase 1-6 canonical artifacts.
2. DO NOT add new technical claims.
3. Do NOT reduce coverage data to generic summaries.
4. Add YAML front matter to EVERY final document (`run_id`, `source_commit`, `status`, `primary_owner_agent`).
5. Write ONLY in Vietnamese (Tiếng Việt) for prose.

## Required Output
Must output exactly 20 files from `01_project_handover_full.md` to `20_documentation_coverage.md`.
Files without components MUST be marked `[NOT_APPLICABLE]` with negative evidence. No generic tutorials.

## Acceptance Gate
Exactly 20 files exist in `final/` directory.

## Publishing Rule
Docs in `final/` MUST NOT be copied to `docs/` unless Agent 8 replies with PASS.
"""

agent_8 = """
## Role
Final Documentation Quality Validator

## Inputs bắt buộc
- `.ai/runs/source-code-handover/<run_id>/inventory/`
- `.ai/runs/source-code-handover/<run_id>/review/`
- `.ai/runs/source-code-handover/<run_id>/final/`
- Current git repository source files.
- `STATUS.md`

## Allowed Write Paths
- `.ai/runs/source-code-handover/<run_id>/validation/`

## Canonical Artifact
- `final-quality-report.md`
- `provenance-scan.md`
- `evidence-validation.md`
- `coverage-validation.md`
- `links-validation.md`
- `secret-scan.md`
- `final-verdict.md`

## Validation Rules
1. **Provenance & Template Guard**: Check configurable patterns (dotnet new, github.com/skoruba, example.com, Password123, Hangfire or Quartz, NotificationHub, sample only, etc.). Fail if present without `[UPSTREAM_REFERENCE]`.
2. **Evidence**: `[CONFIRMED]` claims must have Evidence IDs in `19_evidence_index.md`.
3. **Coverage**: 20 files must exist. YAML front matter exists. Status matches inventory.
4. **Safety**: Secret scan executed and passed.
5. **Links**: Internal relative links must not be broken.

## Required Output
Output exactly ONE of the following verdicts in `final-verdict.md`:
`PASS`
`REJECT_REQUIRES_REVISION`
`BLOCKED`
"""

write_file(".ai/agents/agent-05-operation.md", agent_5)
write_file(".ai/agents/agent-06-coordinator-reviewer.md", agent_6)
write_file(".ai/agents/agent-07-single-handbook-aggregator.md", agent_7)
write_file(".ai/agents/agent-08-final-documentation-validator.md", agent_8)
print("Updated Agents 5-8")
