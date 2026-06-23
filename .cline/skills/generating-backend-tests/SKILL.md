---
name: generating-backend-tests
description: Use when generating or updating backend tests for an already-scoped feature, bug fix, service method, endpoint, database behavior, or integration behavior
---

<!-- generated-by: ai-agent-adapter-sync -->


# Generating Backend Tests

## Vietnamese User Summary

Skill này là skill phụ để tạo/cập nhật test backend cho phạm vi đã rõ.

## Usage Rule

Do not run this as the primary skill for a new feature. New features must start with `developing-backend-feature-tdd`, which may call this skill during the test-first step.

## Workflow

1. Read the scoped behavior and expected outcomes.
2. Locate existing test patterns.
3. Add focused tests.
4. Run relevant tests.
5. Report pass/fail and any missing test infrastructure.
