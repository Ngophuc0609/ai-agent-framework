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
- [ ] Runtime snapshot captured.
- [ ] Request captured.
- [ ] Response status captured.
- [ ] Response headers captured.
- [ ] Cookies captured.
- [ ] Body captured.
- [ ] Dynamic fields documented.
- [ ] Side effects documented.

## Migration

- [ ] Minimal compatibility change only.
- [ ] No business rule change.
- [ ] No DTO/contract change.
- [ ] No view output change.
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
