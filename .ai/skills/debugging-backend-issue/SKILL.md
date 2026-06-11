---
name: debugging-backend-issue
description: Use when investigating, reproducing, and fixing backend bugs using evidence, narrowed scope, regression tests, and documented findings
---

# Debugging Backend Issue

## Vietnamese User Summary

Skill này dùng để debug lỗi backend theo hướng evidence-first và thêm regression test.

## Workflow

1. Retrieve memory and debug notes.
2. Read `docs/DEBUG_PLAYBOOK.md` when present.
3. Reproduce or narrow the issue.
4. Identify the smallest affected scope.
5. Add a failing regression test or executable reproduction.
6. Implement the minimal fix.
7. Review diff.
8. Update debug notes and memory with verified root cause.
