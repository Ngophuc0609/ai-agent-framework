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

## Evidence Policy

All technical claims must be labeled as one of:

- `[CONFIRMED]`: directly verified from source, config, runtime output, database schema, or test result.
- `[INFERRED]`: reasonable conclusion from multiple source references.
- `[UNVERIFIED]`: mentioned by memory, comments, docs, or naming only.
- `[CONFLICT]`: contradictory evidence exists.
- `[NOT_APPLICABLE]`: verified absent after documented inspection.
- `[BLOCKED]`: cannot verify due to missing access, missing files, or failed tooling.

## Source of Truth

Current repository source, configuration, migrations, CI/CD, and verified runtime output are authoritative. Project memory and existing documentation are supplementary context only, not source of truth. Any memory-derived claim that is not verified against current source must be marked `[UNVERIFIED]`.

## Secret Safety

Never copy secret values (connection strings, JWT signing keys, OAuth secrets, API keys, passwords) into documentation, findings, memory, logs, status files, or chat output. Redact sensitive values while preserving variable names and setup requirements.

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

## Final Validation

Final validation must include:
- git diff --check
- no secret scan
- stack-appropriate build or test commands when environment permits.
- markdown link validation where available.

A failed or skipped validation must be documented and lowers readiness accordingly.

## Final Response

1. Resolve the workflow from `.ai/registry/workflows.yml`. Expected key: `developing-backend-feature-tdd`. If missing, record a blocking finding and continue in fallback mode.
2. Respond in Vietnamese with brainstorm status, contract, tests, changed files, validation, risks, and remaining `Need verify` items.
