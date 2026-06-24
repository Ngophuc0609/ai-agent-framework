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
