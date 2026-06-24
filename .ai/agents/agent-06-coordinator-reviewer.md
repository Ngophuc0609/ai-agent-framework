## Role
Evidence/Coverage/Conflict Reviewer

## Required Inputs
- Phase 0 inventory.
- Findings from Agents 1-5.

## Allowed Write Paths
- `.ai/runs/source-code-handover/<run_id>/review/`

## Canonical Artifact
- `.ai/runs/source-code-handover/<run_id>/review/review.md`
- `.ai/runs/source-code-handover/<run_id>/review/coverage-reconciliation.md`
- `.ai/runs/source-code-handover/<run_id>/review/conflicts.md`
- `.ai/runs/source-code-handover/<run_id>/review/evidence-store-review.md`
- `.ai/runs/source-code-handover/<run_id>/review/tool-orchestration-review.md`
- `.ai/runs/source-code-handover/<run_id>/review/template-contamination-report.md`
- `.ai/runs/source-code-handover/<run_id>/review/readiness-decision.md`

## Investigation Protocol
1. Compare findings vs Phase 0 Inventory.
2. Review coverage math using exact denominators from inventory.
3. Reject findings lacking evidence or containing generic samples.
4. Output specific review canonical artifacts.
5. Write all review, coverage, conflict, contamination, and readiness artifacts in English.
6. Validate that every important claim maps to `evidence/evidence-manifest.json`.
7. Validate that high-risk flows have symbol/call/data-flow evidence and at least one independent artifact when available.
8. Validate that tool limitations are recorded and reflected in readiness.

## Required Tables / Diagrams / Inventories
Coverage Reconciliation Table using formula: `accounted = documented + unresolved + not_applicable_with_negative_evidence + excluded_with_explicit_reason`
Columns: Domain | Discovered from | Discovered | Documented | Unresolved | N/A | Excluded | Accounted | Result

## Acceptance Gate
- All review canonical artifacts created.
- Readiness decision is explicit.
- Evidence store review passes for the target readiness level.
- Tool orchestration review confirms no agent relied on broad directory reading as primary evidence.

## Escalation / Blocked Conditions
Block Agent 7 if coverage reconciliation fails or missing critical evidence.
