---
name: refactoring-backend-safely
description: Use when refactoring backend code with controlled scope, tests, compatibility checks, and review
---

<!-- generated-by: ai-agent-adapter-sync -->


# Refactoring Backend Safely

## Vietnamese User Summary

Skill này dùng để refactor backend an toàn, không trộn refactor lớn vào lúc implement feature mới.

## Feature Boundary Rule

Do not perform broad refactoring while implementing a new feature. Refactor only when required to pass tests, preserve the contract, or remove duplication introduced by the feature.

## Workflow

1. Inventory usages.
2. Create a refactor checklist.
3. Add or confirm tests.
4. Apply changes in small groups.
5. Test each group.
6. Review diff.
7. Update memory/docs with confirmed conventions.
