# .NET Parity Migration

## Vietnamese User Summary

Workflow này migrate .NET legacy sang .NET 8+ bằng baseline, compatibility port và contract regression.

## Purpose

Migrate .NET legacy systems to .NET 8+ while preserving 1:1 external behavior.

This workflow is a parity workflow. It must not be used as a modernization, cleanup, or bug-fixing workflow unless a separate approved change explicitly exits parity mode.

## Trigger

Registered in:

- `.ai/registry/triggers.yml`

## Required Files

- `.ai/registry/skills.yml`
- `.ai/registry/workflows.yml`
- `.ai/registry/triggers.yml`
- `.ai/skills/dotnet-parity-migration/SKILL.md`
- `.ai/skills/dotnet-baseline-capture/SKILL.md`
- `.ai/skills/dotnet-compatibility-port/SKILL.md`
- `.ai/skills/dotnet-contract-regression/SKILL.md`
- `.ai/rules/16-dotnet-parity-migration-rules.md`
- `.ai/templates/dotnet-parity-migration/`

## Allowed Write Paths

- `.ai/runs/dotnet-parity-migration/<run_id>/`
- `docs/dotnet-parity-migration/`
- `docs/migration/`
- Test projects or snapshot fixture folders in the target repository when they already exist or are explicitly created for migration regression.
- Source files needed for the scoped migration slice when the current phase is compatibility porting.

Do not write directly to production configuration, deployment secrets, or unrelated modernization docs.

## Output Namespace

Runtime state should use:

```text
.ai/runs/dotnet-parity-migration/<run_id>/
```

Recommended subdirectories:

```text
migration-docs/
baseline/
contracts/
golden-master/
tests/
scaffold/
regression/
risks/
validation/
deferred/
```

Required deliverables:

```text
migration-docs/00_MIGRATION_SCOPE.md
migration-docs/01_LEGACY_INVENTORY.md
migration-docs/02_LEGACY_BASELINE.md
migration-docs/03_UNIT_TEST_SPEC_FROM_LEGACY_BASELINE.md
migration-docs/04_COMPATIBILITY_DESIGN.md
migration-docs/05_NEW_PROJECT_BASELINE.md
migration-docs/06_NEW_PROJECT_TEST_SCAFFOLD.md
migration-docs/07_ENDPOINT_VIEW_MIGRATION_TRACKER.md
migration-docs/08_CONTRACT_REGRESSION_REPORT.md
migration-docs/09_VIEW_UI_REGRESSION_REPORT.md
migration-docs/10_MIGRATION_RISK_REGISTER.md
migration-docs/11_ACCEPTANCE_CHECKLIST.md
migration-docs/15_DEFERRED_ISSUES_REPORT.md
migration-docs/legacy-baseline.json
```

## Execution

1. Resolve the requested phase:
   - baseline capture.
   - compatibility port.
   - contract regression.
   - full parity migration.
2. Check git status.
3. Inspect runtime state using safe local checks. Do not install SDKs, packages, or tools automatically.
4. Retrieve project memory when available. If memory is unavailable, use repository docs fallback and record the limitation.
5. Attempt CodeGraph for broad source inventory or dependency tracing. For localized endpoint work, use `rg`, IDE/LSP references, and narrow source reads when CodeGraph is unavailable.
6. Identify the target app type and target slice.
7. Create or update `00_MIGRATION_SCOPE.md` and `07_ENDPOINT_VIEW_MIGRATION_TRACKER.md`; every endpoint/view/business capability starts as `NOT_STARTED`.
8. If baseline is missing, stop porting and run `dotnet-baseline-capture`.
9. If baseline is partial, continue only for slices whose required evidence exists; otherwise mark the slice `BLOCKED: Missing legacy baseline/runtime evidence`.
10. If baseline conflicts, record the conflict and ask for clarification or runtime evidence.
11. Create baseline documentation before production migration code:
   - current architecture and module map.
   - endpoint/view/job inventory.
   - business logic summaries per API or capability.
   - request/response contracts including field names, object shapes, data types, status codes, headers, cookies, and dynamic fields.
   - database, external API, file, auth, and session side effects.
12. Create `03_UNIT_TEST_SPEC_FROM_LEGACY_BASELINE.md` from the legacy baseline before creating or accepting .NET 8+ behavior.
13. Create or update .NET 8+ unit/integration/snapshot test projects before production migration code and document them in `06_NEW_PROJECT_TEST_SCAFFOLD.md`.
14. For each API or business capability, create tests from legacy evidence first:
   - request input parameters from query, route, form, body, header, and cookie.
   - expected business outcome.
   - exact response status, headers, content type, field names, data types, object shape, null/date/enum/numeric behavior, and body text or JSON.
   - database, external API, file, auth, session, and cookie side effects when applicable.
15. Scaffold corresponding .NET 8+ files for the selected slice only after baseline and test assets exist; mark it `BASE_PROJECT_READY` or `CONVERTING` as appropriate.
16. Design compatibility adapters before editing production behavior and document them in `04_COMPATIBILITY_DESIGN.md`.
17. Convert only one endpoint, view, job, integration, or business capability at a time.
18. Preserve legacy behavior exactly. Do not add features, fix latent bugs, or optimize behavior during parity migration.
19. If a latent bug, cleanup opportunity, security risk, or optimization is found, write it to `15_DEFERRED_ISSUES_REPORT.md` and continue preserving legacy behavior.
20. Run build, baseline-derived tests, and contract/view comparison.
21. Classify every difference as `MATCH`, `DYNAMIC_MATCH`, `APPROVED_BREAKING_CHANGE`, `MIGRATION_BUG`, or `BLOCKED`.
22. Mark the slice `PASS` only when baseline-derived tests and contract/view regression pass with no unapproved difference.
23. Report readiness per endpoint or view.

## Phase Prompts

### Baseline Capture

Use when the user asks to create a legacy baseline, capture Golden Master behavior, or prepare before migration. Do not edit source code. Do not call production write endpoints.

### Compatibility Port

Use when the baseline and baseline-derived tests exist and the user asks to port an endpoint, view, or code slice to .NET 8+. Read the relevant baseline and tests before editing.

### Contract Regression

Use after porting to compare .NET 8+ output with legacy Golden Master snapshots. Do not mark done while unapproved migration bugs remain.

## Quality Gates

- [ ] Skill, workflow, and trigger were resolved through `.ai/registry/`.
- [ ] `.ai/rules/16-dotnet-parity-migration-rules.md` was applied.
- [ ] Required deliverables are created or explicitly marked not applicable with evidence.
- [ ] Legacy baseline exists or the task is explicitly `BLOCKED: Missing legacy baseline/runtime evidence`.
- [ ] P0/P1 endpoints or views have Golden Master evidence before porting.
- [ ] Baseline documents preserve architecture, current business logic, request/response contracts, and side effects for the target slice.
- [ ] Unit/integration/snapshot tests were created from legacy evidence before production migration code.
- [ ] Tests cover request inputs, response outputs, field names, data types, object shape, status, headers, cookies, and side effects for the target slice.
- [ ] Compatibility risks were listed before source edits.
- [ ] No business rule refactor or unapproved contract change was introduced.
- [ ] Latent bugs, cleanup opportunities, and optimizations were documented but not fixed unless explicitly approved.
- [ ] `15_DEFERRED_ISSUES_REPORT.md` exists when any deferred issue is found.
- [ ] Build/test/regression commands were run or explicitly blocked with reason.
- [ ] All differences were classified.
- [ ] Secrets were not exposed.
- [ ] Runtime limitations and fallback evidence were recorded.

## Fallback Behavior

- Missing CodeGraph: use `rg`, project references, route maps, and narrowed source reads; mark confidence reduced for broad inventory.
- Missing runtime legacy environment: create `CODE_VERIFIED` baseline only and mark runtime snapshots `BLOCKED`.
- Missing baseline-derived tests: stop production code conversion for that slice; create the test project and tests first, or mark the slice `BLOCKED`.
- Missing test project: create a test project before production migration code when the repository permits it; otherwise create executable curl/Postman/snapshot assets and mark production conversion `BLOCKED` until test coverage exists or the user explicitly approves a documented exception.
- Missing memory: use repository docs fallback and do not claim memory was read or written.

## Final Response Contract

Report:

```text
Status: PASS / FAIL / BLOCKED / PARTIAL / DEFERRED
Endpoint/View:
Legacy evidence:
Baseline status:
Baseline-derived tests:
Migration unit status:
Changes made:
Compatibility risks:
Contract differences:
Deferred issues:
Tests run:
Fallbacks/limitations:
Next required action:
```
