---
name: routing-ai-task
description: Use when deciding which specialized skill should handle a coding, documentation, debugging, refactoring, testing, migration, review, commit, or backend feature task
---

# Routing AI Task

## Vietnamese User Summary

Skill này chọn đúng skill con trước khi agent bắt đầu làm việc.

## Required Rules

- `.ai/rules/00-global-rules.md`
- `.ai/rules/13-efficiency-cost-policy-rules.md`
- `.ai/rules/14-tdd-first-feature-rules.md`

## Workflow

1. Classify the user request.
2. Search project memory.
3. Read project summary docs when relevant.
4. Choose the smallest applicable skill.
5. Avoid broad documentation or debugging skills for small tasks.
6. Prefer diff-based analysis when code changes already exist.
7. Respond to the user in Vietnamese when asking clarifying questions or reporting routing.

## Mandatory Routing Rules

If the request asks to create a new endpoint, add an API, create a feature, add a flow, create a backend capability, add a service method, add a webhook, add a callback, or implement a database-backed business flow, route to:

```text
developing-backend-feature-tdd
```

Do not route new endpoint or new feature requests directly to `analyzing-api-endpoint`; that skill is only for existing endpoints.

## Routing Table

| Request type | Skill |
|---|---|
| Create new backend feature or endpoint | `developing-backend-feature-tdd` |
| Analyze existing API endpoint | `analyzing-api-endpoint` |
| Generate tests for an existing target | `generating-backend-tests` |
| Write failing backend tests first | `writing-backend-tests-first` |
| Generate curl/Postman/API verification assets | `generating-api-test-assets` |
| Debug backend issue | `debugging-backend-issue` |
| Refactor backend code safely | `refactoring-backend-safely` |
| Review changed code | `reviewing-git-diff` |
| Review SQL migration | `reviewing-sql-migration` |
| Analyze background jobs | `analyzing-background-jobs` |
| Write Vietnamese commit message | `writing-vietnamese-commit-message` |
| Create handover docs | `source-code-handover` |

## Cost Optimization Checklist

- [ ] Memory was searched before scanning code.
- [ ] `docs/PROJECT_CONTEXT.md` was read when present.
- [ ] The whole repository was not read for a module-scoped task.
- [ ] File reading was limited to the smallest useful set.
- [ ] Git diff was used when the task involved existing code changes.
- [ ] Findings were summarized for reuse.
- [ ] Durable information was written to memory or docs when appropriate.
- [ ] Secrets, logs, and large raw code were not stored in memory.
- [ ] Strong models were not used for simple routing or formatting.
