# Migration Acceptance Checklist

## Endpoint/View

```text
Name:
URL/View:
Owner:
Priority: P0/P1/P2/P3
Migration Unit Status: NOT_STARTED / BASELINE_READY / TEST_SPEC_READY / BASE_PROJECT_READY / CONVERTING / REGRESSION_RUNNING / PASS / FAIL / BLOCKED / DEFERRED
```

## Baseline

- [ ] Legacy source identified.
- [ ] Current architecture documented.
- [ ] Current business logic documented.
- [ ] Runtime snapshot captured.
- [ ] Request captured.
- [ ] Response status captured.
- [ ] Response headers captured.
- [ ] Cookies captured.
- [ ] Body captured.
- [ ] Field names, data types, and object shapes documented.
- [ ] Dynamic fields documented.
- [ ] Side effects documented.

## Test First

- [ ] `03_UNIT_TEST_SPEC_FROM_LEGACY_BASELINE.md` exists and is derived from legacy baseline evidence.
- [ ] .NET 8+ test project exists before production behavior code.
- [ ] Tests are derived from legacy source and runtime evidence.
- [ ] Tests were not generated from migrated .NET 8+ output.
- [ ] Tests cover request inputs.
- [ ] Tests cover business outcome.
- [ ] Tests cover exact response status, headers, cookies, content type, field names, data types, object shape, and body.
- [ ] Tests cover side effects when applicable.
- [ ] Missing runtime evidence is marked `BLOCKED` instead of mocked.

## Migration

- [ ] `07_ENDPOINT_VIEW_MIGRATION_TRACKER.md` status was updated for this slice.
- [ ] Corresponding .NET 8+ files were scaffolded only after baseline and tests existed.
- [ ] Minimal compatibility change only.
- [ ] No business rule change.
- [ ] No DTO/contract change.
- [ ] No view output change.
- [ ] `Request.Params` behavior uses verified compatibility logic, not method-based mapping.
- [ ] `Json(responseString)` behavior is based on Golden Master raw-object versus escaped-string evidence.
- [ ] Latent bugs and optimization opportunities were documented separately, not fixed during parity migration.
- [ ] Deferred issues were recorded in `15_DEFERRED_ISSUES_REPORT.md`.
- [ ] No secret leakage.

## Regression

- [ ] Build pass.
- [ ] Unit tests pass.
- [ ] Integration/contract tests pass.
- [ ] Browser/view test pass.
- [ ] DB/external side effects match.
- [ ] No unapproved differences.

## Decision

```text
PASS / FAIL / BLOCKED / PARTIAL / DEFERRED
Reason:
```
