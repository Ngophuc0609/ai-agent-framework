# 14 TDD-First Feature Rules

## Vietnamese User Summary

Rule này bắt buộc mọi endpoint/tính năng backend mới phải brainstorm, chốt contract và có test plan trước khi implement.

## Mandatory Gate

For every new backend feature, endpoint, service method, database-backed flow, integration flow, callback, webhook, job, or business capability:

```text
No brainstorm + no contract + no test plan = no production implementation.
```

## Required Sequence

1. Brainstorm feature behavior.
2. Define the API or behavior contract.
3. Define acceptance criteria.
4. Create a test matrix.
5. Write failing tests first when test infrastructure exists.
6. Implement minimal production code.
7. Refactor safely.
8. Review the diff.
9. Update docs and memory.

## Production Code Restriction

Do not edit production code for a new feature until these items are defined:

- Feature goal.
- API or behavior contract.
- Acceptance criteria.
- Test scenarios.
- Failure cases.
- Data impact.
- Authentication and permission impact.
- Backward compatibility impact.

If the repository has no automated test framework, create an executable regression plan with curl/Postman examples, SQL verification queries, or equivalent project-native checks before implementation.

## Routing

Requests containing intent such as new endpoint, add API, create feature, add flow, backend feature, service method, webhook, callback, integration flow, or equivalent Vietnamese trigger phrases must route to `developing-backend-feature-tdd`.

Do not route new-feature work directly to API analysis, refactoring, or implementation-only skills.

## Refactor Boundary

Do not perform broad refactoring while implementing a new feature. Refactor only when required to pass tests, preserve the contract, or remove duplication introduced by the feature.

## Review Requirement

When reviewing a diff that adds a new feature or endpoint, warn if there is no automated test, test plan, or executable regression check.
