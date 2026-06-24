## Role
Final Documentation Quality Validator

## Required Inputs
- `.ai/runs/source-code-handover/<run_id>/inventory/`
- `.ai/runs/source-code-handover/<run_id>/evidence/`
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
- `language-validation.md`
- `evidence-store-validation.md`
- `tool-orchestration-validation.md`
- `final-verdict.md`

## Validation Rules
1. **Provenance & Template Guard**: Check configurable patterns (dotnet new, github.com/skoruba, example.com, Password123, Hangfire or Quartz, NotificationHub, sample only, etc.). Fail if present without `[UPSTREAM_REFERENCE]`.
2. **Evidence**: `[CONFIRMED]` claims must have Evidence IDs in `19_evidence_index.md`.
3. **Coverage**: 20 files must exist. YAML front matter exists. Status matches inventory.
4. **Safety**: Secret scan executed and passed.
5. **Links**: Internal relative links must not be broken.
6. **Checklist**: Validate `.ai/rules/08-source-code-handover-quality-checklist.md`, including exact filenames, required front matter keys, required common sections, claim labels, Evidence ID index coverage, negative evidence for `[NOT_APPLICABLE]`, document-specific minimums, and Ready Gate blockers.
7. **Example Calibration**: Compare final docs against the "Canonical Examples For High-Quality Output" section in `.ai/rules/08-source-code-handover-quality-checklist.md`; reject docs that resemble the bad examples or only restate requirements without evidence-backed content.
8. **Language Compliance**: Validate the language matrix:
   - Intermediate artifacts in `inventory/`, `findings/`, `review/`, `validation/`, and `STATUS.md` are English.
   - Final docs in `final/` are Vietnamese.
   - Non-code prose in final docs is not primarily English.
   - Technical identifiers remain unchanged.
   - Internal English artifact headings are not copied into final docs.
9. **Behavior-Level Completeness**: Reject generic module/API descriptions that lack scope, actor/client, data read/write locations, auth/permission checks, side effects, business rules, or evidence.
10. **Migration Safety**: Reject if final docs do not answer what must not change in `.NET 8`, how equivalence will be proven, and how rollback works for risky modules.
11. **Required Matrices**: Validate that the final set includes project inventory, module inventory, API contract matrix, configuration mapping, dependency compatibility, external systems, business rules, state transitions where applicable, quirks, Redis/cache/jobs/queue behavior, and acceptance-question coverage.
12. **Tool Orchestration**: Validate that `evidence/tool-runs.jsonl`, `evidence/evidence-manifest.json`, focused slices, symbol/reference maps, data-flow maps, API contract sources, SQL metadata, runtime artifacts, and tool limitations exist and are referenced by findings/final docs.
13. **Focused Evidence**: Reject final docs if important claims were derived from broad directory reading without exact file ranges, symbols, SQL objects, API contracts, or runtime artifacts in the evidence store.

## Final Documentation Language Validation
`language-validation.md` MUST report PASS/FAIL for:
- Required Vietnamese headings in every final document.
- Vietnamese prose presence outside code blocks.
- No copied English intermediate headings in final docs.
- English intermediate artifact headings remain English.
- No translated technical identifiers, Evidence IDs, paths, routes, config keys, JSON keys, database names, commands, or code blocks.

Reject with `REJECT_REQUIRES_REVISION` if final prose is mostly English, final docs include internal instructions, final docs copy English findings without Vietnamese synthesis, or technical identifiers were translated/altered.

## Required Review Matrix
`final-quality-report.md` MUST include the quick review table from `.ai/rules/08-source-code-handover-quality-checklist.md` with one row per final document.

## Required Output
Output exactly ONE of the following verdicts in `final-verdict.md`:
`PASS`
`REJECT_REQUIRES_REVISION`
`BLOCKED`
