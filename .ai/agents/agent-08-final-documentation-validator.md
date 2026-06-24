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
