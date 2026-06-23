---
name: developing-backend-feature-tdd
description: Use when creating a new backend feature, API endpoint, service method, database flow, integration flow, callback, webhook, background job, or business capability using brainstorming, API contract design, and test-driven development before implementation
---

# Developing Backend Feature With TDD

## Vietnamese User Summary

Skill này dùng khi tạo endpoint/tính năng backend mới. Agent bắt buộc brainstorm, chốt contract và viết test/test plan trước khi code.

## Overview

Use this skill to develop a new backend feature or endpoint using a TDD-first workflow.

The assistant must not jump directly into implementation. It must first clarify the feature behavior, brainstorm edge cases, design the API or behavior contract, define acceptance criteria, and create or propose tests before writing production code.

Announce at start:

```text
I'm using the developing-backend-feature-tdd skill to brainstorm, define tests, and implement this backend feature safely.
```

## Required Rules

- `.ai/rules/00-global-rules.md`
- `.ai/rules/10-codegraph-first-rules.md`
- `.ai/rules/12-memory-policy-rules.md`
- `.ai/rules/13-efficiency-cost-policy-rules.md`
- `.ai/rules/14-tdd-first-feature-rules.md`

## Core Rule

Do not implement production code until the following are defined:

- Feature goal.
- API or behavior contract.
- Acceptance criteria.
- Test scenarios.
- Failure cases.
- Data impact.
- Backward compatibility impact.
- Authentication and permission impact.

If the project has no test framework, create a test plan and executable API regression checks such as curl/Postman examples before implementation.

## Required Inputs

Collect or infer:

```text
Feature name
Actor/user role
Endpoint path
HTTP method
Request body/query params
Response shape
Authentication requirement
Permission requirement
Database tables affected
External services affected
Cache keys affected
Backward compatibility requirement
Validation rules
Error cases
```

If information is missing, continue with clear assumptions and mark them as `Need verify`.

## Workflow

### Step 1: Load Existing Context

Before designing the feature:

1. Search project memory if available.
2. Read `docs/PROJECT_CONTEXT.md` if it exists.
3. Read `docs/API_SUMMARY.md` if it exists.
4. Read `docs/DATABASE_SUMMARY.md` if it exists.
5. Read `docs/DECISIONS.md` if it exists.
6. Inspect only the smallest relevant code area.

Prefer reading:

```text
Controller/route
DTO/request model
Service/use-case
Repository/database access
Entity/model
Validation
Auth/permission middleware
Existing tests
```

### Step 2: Brainstorm Feature Behavior

Create a short feature brainstorm before coding.

Cover:

```text
What problem this feature solves
Who calls it
Main happy path
Alternative paths
Validation rules
Permission rules
Database changes
Cache changes
External calls
Idempotency requirement
Concurrency/race condition risk
Backward compatibility risk
Observability/logging need
```

### Step 3: Define API Or Behavior Contract

For endpoints, document:

```text
Method
Endpoint
Auth required
Headers
Query params
Route params
Request body
Success response
Error responses
Status codes
Example request
Example response
```

For non-HTTP backend features, document trigger, inputs, outputs, side effects, errors, idempotency, and observability.

Use project conventions when they already exist.

### Step 4: Define Acceptance Criteria

Write acceptance criteria before tests.

Format:

```text
Given ...
When ...
Then ...
```

### Step 5: Create Test Matrix

Before implementation, create test scenarios.

Minimum required test groups:

```text
Happy path
Invalid request
Unauthorized
Forbidden
Not found
Duplicate/conflict
Database failure
External API failure if any
Cache miss/cache stale if any
Backward compatibility case if any
```

For each scenario, specify:

```text
Test name
Input
Expected result
Expected status code
Expected database change
Expected log or side effect
```

### Step 6: Write Failing Tests First

Use `writing-backend-tests-first` or `generating-backend-tests` as supporting skills when available.

If the repo has test infrastructure:

1. Add unit tests for service/business logic.
2. Add integration/API tests for endpoint behavior.
3. Add repository tests only when database logic is complex.
4. Run tests and confirm new tests fail before implementation.

If the repo has no test infrastructure:

1. Create a manual regression test section.
2. Create curl/Postman examples.
3. Create SQL verification queries.
4. Mark missing automated test infrastructure as `Need verify`.

### Step 7: Implement Minimal Production Code

Implement only what is needed to pass the defined tests.

Typical backend implementation order:

```text
DTO/request/response model
Validation
Controller/route
Service/use-case
Repository/database code
Entity mapping
Auth/permission checks
Cache handling
External integration handling
Logging
Swagger/Postman update
```

Avoid unrelated refactoring during feature implementation.

### Step 8: Refactor Safely

After tests pass:

```text
Remove duplication
Improve naming
Simplify branching
Keep API contract stable
Keep backward compatibility
Avoid changing unrelated modules
```

### Step 9: Verify Data And Side Effects

Check:

```text
Tables inserted/updated/deleted
Transactions
Unique constraints
Foreign keys
Status values
Cache invalidation
Background job trigger
External API call
Logs
Audit fields
created_by/created_date/updated_by/updated_date
```

### Step 10: Generate API Test Assets

Use `generating-api-test-assets` when applicable.

Create or update:

```text
curl examples
Postman request
Environment variables
Auth token usage
Swagger/OpenAPI notes
SQL verify queries
```

### Step 11: Review Diff

Use `reviewing-git-diff` before finalizing.

Review changed files only:

```text
Breaking changes
Auth/permission
Validation
Error handling
Transaction safety
Test coverage
Logs
Docs updated
```

### Step 12: Update Docs And Memory

Update relevant docs:

```text
docs/API_SUMMARY.md
docs/DATABASE_SUMMARY.md
docs/DEBUG_PLAYBOOK.md
docs/DECISIONS.md
docs/PROJECT_CONTEXT.md
```

Store only verified reusable facts in memory if memory tools are available.

## Output Format

When responding before implementation, structure the work as:

```text
1. Brainstorm
2. API Contract
3. Acceptance Criteria
4. Test Plan
5. Implementation Plan
6. Files to Change
7. Risks
8. Done Criteria
```

When code is implemented, add:

```text
Changed files
Tests added
How to run tests
curl/Postman examples
Database verification
Remaining Need verify items
```

Chat responses to the user must be in Vietnamese.

## TDD Quality Gate

Before coding:

- [ ] Feature goal is clear.
- [ ] API or behavior contract is defined.
- [ ] Acceptance criteria are defined.
- [ ] Test cases are listed.
- [ ] Error cases are listed.
- [ ] Data impact is known.
- [ ] Auth/permission impact is known.
- [ ] Backward compatibility impact is known.

Before final response:

- [ ] Tests were added or test plan was created.
- [ ] Happy path is covered.
- [ ] Invalid request is covered.
- [ ] Unauthorized/forbidden behavior is covered.
- [ ] Database side effects are verified.
- [ ] External side effects are verified if any.
- [ ] Logs/debug notes are added.
- [ ] API examples are provided.
- [ ] Docs are updated or listed as pending.
- [ ] No unrelated refactor was introduced.
- [ ] No secrets were exposed.

## Cost Optimization Checklist

- [ ] Memory was searched before scanning code.
- [ ] `docs/PROJECT_CONTEXT.md` was read when present.
- [ ] The whole repository was not read for a module-scoped task.
- [ ] File reading was limited to the smallest useful set.
- [ ] Git diff was used when the task involved existing code changes.
- [ ] Findings were summarized for reuse.
- [ ] Durable information was written to memory or docs.
- [ ] Secrets, logs, and large raw code were not stored in memory.
- [ ] Strong models were not used for simple formatting or summarization steps.

## Common Mistakes

| Mistake | Fix |
|---|---|
| Implementing immediately | Brainstorm, contract, and tests first |
| Testing only happy path | Include validation, auth, not found, conflict, and failure cases |
| Ignoring database impact | List tables and verify SQL side effects |
| Ignoring permissions | Define auth and role requirements before coding |
| Over-refactoring | Keep refactor scoped to the feature |
| No regression check | Add automated test or curl/Postman verification |
| Inventing behavior | Mark uncertain behavior as `Need verify` |

## Final Handoff Template

```text
Feature:
Status:

Brainstorm completed:
- ...

API contract:
- METHOD /path

Tests:
- Added:
- Manual verification:

Changed files:
- ...

How to verify:
- ...

Risks:
- ...

Need verify:
- ...

Recommended next step:
- ...
```


## Memory Policy & Source of Truth

Current repository source, configuration, migrations, CI/CD, and verified runtime output are authoritative. Project memory and existing documentation are supplementary context only. Any memory-derived claim that is not verified against current source must be marked `[UNVERIFIED]`.

## Secret Safety

Never copy secret values (connection strings, JWT signing keys, OAuth secrets, API keys, passwords) into documentation, findings, memory, logs, status files, or chat output. Redact sensitive values while preserving variable names and setup requirements.

## Evidence Policy

All technical claims must be labeled as one of: `[CONFIRMED]`, `[INFERRED]`, `[UNVERIFIED]`, `[CONFLICT]`, `[NOT_APPLICABLE]`, or `[BLOCKED]`.

Each agent finding must include: inspected scope, evidence references, commands executed, findings, assumptions, open questions, risks, and completion state.

## Final Validation

Before publishing final docs or committing changes, run required-output validation, STATUS.md consistency validation, git diff --check, secret scan, markdown/link validation, and stack-appropriate build or test commands when environment permits.
