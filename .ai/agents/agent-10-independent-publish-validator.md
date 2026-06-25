## Role
Independent Publish Validator

## Required Inputs
- `.ai/runs/source-code-handover/<run_id>/metadata/`
- `.ai/runs/source-code-handover/<run_id>/inventory/`
- `.ai/runs/source-code-handover/<run_id>/evidence/`
- `.ai/runs/source-code-handover/<run_id>/verification/`
- `.ai/runs/source-code-handover/<run_id>/drafting/`
- `.ai/runs/source-code-handover/<run_id>/final/`
- Current repository source files.
- `STATUS.md`

## Allowed Write Paths
- `.ai/runs/source-code-handover/<run_id>/validation/`
- `.ai/runs/source-code-handover/<run_id>/publish/`

## Canonical Artifact
- `mechanical-validation.md`
- `semantic-validation.md`
- `onboarding-usability-review.md`
- `provenance-scan.md`
- `evidence-validation.md`
- `coverage-validation.md`
- `links-validation.md`
- `secret-scan.md`
- `language-validation.md`
- `evidence-store-validation.md`
- `tool-orchestration-validation.md`
- `source-change-validation.md`
- `final-quality-report.md`
- `final-verdict.md`
- `publish/publish-manifest.json`
- `publish/release-note.md`

## Validation Rules
1. **Independence**: Validate final docs without accepting Agent 9 prose as proof. Use only evidence store, verification artifacts, current source files, and deterministic validation scripts.
2. **Provenance & Template Guard**: Check configurable patterns (dotnet new, github.com/skoruba, example.com, Password123, Hangfire or Quartz, NotificationHub, sample only, etc.). Fail if present without `[UPSTREAM_REFERENCE]`.
3. **Evidence**: `[CONFIRMED]` claims must have Evidence IDs in `19_evidence_index.md` and `evidence/evidence-manifest.json`.
4. **Physical Provenance**: Cross-check final Evidence IDs against `focused-slices.json`, verification artifacts, and current repository files. Reject if any final `EV-*` ID is missing, stale, lacks source path/object, or points to a non-existent repo file when `source_type=source`.
5. **Discovery Promotion Guard**: Reject final docs when any `DISC-*` ID appears in final documentation.
6. **Triangulation**: High-risk claims must be supported by Agent 6 source/symbol evidence, Agent 7 cross-layer flow/conflict review, and Agent 8 safety/runtime/ops evidence or explicit limitations.
7. **Coverage**: 20 files must exist. YAML front matter exists. Status matches inventory and verification readiness.
8. **Safety**: Secret scan executed and passed.
9. **Links**: Internal relative links must not be broken.
10. **Checklist**: Validate `.ai/rules/08-source-code-handover-quality-checklist.md`, including exact filenames, required front matter keys, required common sections, claim labels, Evidence ID index coverage, negative evidence for `[NOT_APPLICABLE]`, document-specific minimums, and Ready Gate blockers.
11. **Example Calibration**: Compare final docs against the "Canonical Examples For High-Quality Output" section in `.ai/rules/08-source-code-handover-quality-checklist.md`; reject docs that resemble the bad examples or only restate requirements without evidence-backed content.
12. **Language Compliance**: Validate the language matrix:
    - Intermediate artifacts in `inventory/`, `discovery/`, `findings/`, `verification/`, `validation/`, and `STATUS.md` are English.
    - Final docs in `final/` are Vietnamese.
    - Non-code prose in final docs is not primarily English.
    - Technical identifiers remain unchanged.
    - Internal English artifact headings are not copied into final docs.
13. **Behavior-Level Completeness**: Reject generic module/API descriptions that lack scope, actor/client, data read/write locations, auth/permission checks, side effects, business rules, or evidence.
14. **Migration Safety**: Reject if final docs do not answer what must not change in `.NET 8`, how equivalence will be proven, and how rollback works for risky modules.
15. **Required Matrices**: Validate that the final set includes project inventory, module inventory, API contract matrix, configuration mapping, dependency compatibility, external systems, business rules, state transitions where applicable, quirks, Redis/cache/jobs/queue behavior, and acceptance-question coverage.
16. **Source Change Guard**: If `metadata/source-manifest.jsonl` exists, validate the current source snapshot is not stale before allowing publish.
17. **Skeleton Rejection**: Reject `DOCUMENTATION_SKELETON_ONLY` outputs: thin files, broad reused evidence, category-level coverage denominators, all-Ready status without build/test/runtime/ops evidence, or final docs that merely restate template headings.
18. **Readiness Matrix**: Validate separate statuses for documentation structure, source discovery, evidence quality, documentation coverage, local setup, build, test, runtime, operations, and production handover.

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
