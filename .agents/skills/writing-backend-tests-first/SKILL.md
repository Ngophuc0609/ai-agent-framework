---
name: writing-backend-tests-first
description: Use when writing failing backend tests before implementing a new feature, endpoint, service method, database flow, bug fix, or integration behavior
---

<!-- generated-by: ai-agent-adapter-sync -->


# Writing Backend Tests First

## Vietnamese User Summary

Skill này viết test backend trước production code.

## Workflow

1. Read the brainstorm, contract, acceptance criteria, and test matrix.
2. Identify the existing test framework and test style.
3. Add the smallest tests that define the intended behavior.
4. Cover happy path, invalid input, auth/permission, not found, conflict, and side effects when applicable.
5. Run tests and confirm new tests fail before implementation.
6. If no test framework exists, create executable regression checks and mark automated test infrastructure as `Need verify`.

## Guardrails

- Do not change production code in this skill.
- Do not weaken existing tests.
- Do not invent behavior outside the accepted contract.
