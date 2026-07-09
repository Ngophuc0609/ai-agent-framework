# Migration Acceptance Checklist

## Endpoint/View

```text
Name:
URL/View:
Owner:
Priority: P0/P1/P2/P3
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

- [ ] .NET 8+ test project exists before production behavior code.
- [ ] Tests are derived from legacy source and runtime evidence.
- [ ] Tests cover request inputs.
- [ ] Tests cover business outcome.
- [ ] Tests cover exact response status, headers, cookies, content type, field names, data types, object shape, and body.
- [ ] Tests cover side effects when applicable.
- [ ] Missing runtime evidence is marked `BLOCKED` instead of mocked.

## Migration

- [ ] Corresponding .NET 8+ files were scaffolded only after baseline and tests existed.
- [ ] Minimal compatibility change only.
- [ ] No business rule change.
- [ ] No DTO/contract change.
- [ ] No view output change.
- [ ] Latent bugs and optimization opportunities were documented separately, not fixed during parity migration.
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
PASS / FAIL / BLOCKED
Reason:
```
