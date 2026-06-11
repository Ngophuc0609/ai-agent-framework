# Developing Backend Feature TDD Workflow

## Vietnamese User Summary

Workflow này bắt buộc brainstorm, contract và test-first trước khi implement endpoint/tính năng backend mới.

## Skill

Use `.ai/skills/developing-backend-feature-tdd/SKILL.md`.

## Required Chain

For a new endpoint:

```text
routing-ai-task
  -> developing-backend-feature-tdd
  -> writing-backend-tests-first
  -> generating-api-test-assets
  -> reviewing-git-diff
  -> writing-vietnamese-commit-message
```

For a bug fix:

```text
routing-ai-task
  -> debugging-backend-issue
  -> writing-backend-tests-first
  -> reviewing-git-diff
  -> writing-vietnamese-commit-message
```

For a feature with DB or migration:

```text
developing-backend-feature-tdd
  -> reviewing-sql-migration
  -> writing-backend-tests-first
  -> generating-api-test-assets
```

For a new background job:

```text
developing-backend-feature-tdd
  -> analyzing-background-jobs
  -> writing-backend-tests-first
  -> reviewing-git-diff
```

## Gate

Do not implement production code until brainstorm, contract, acceptance criteria, and test plan exist.

## Allowed Write Paths

- Source files required by the feature.
- Test files required by the feature.
- Existing API docs or generated API test assets when project convention supports them.
- `docs/API_SUMMARY.md`
- `docs/DATABASE_SUMMARY.md`
- `docs/DEBUG_PLAYBOOK.md`
- `docs/DECISIONS.md`
- `docs/PROJECT_CONTEXT.md`
- `.ai/runs/developing-backend-feature-tdd/<run_id>/`

## Final Response

Respond in Vietnamese with brainstorm status, contract, tests, changed files, validation, risks, and remaining `Need verify` items.
