---
name: skill-registry-maintenance
description: Use when maintaining, validating, repairing, or extending AI skill registries, workflow registries, trigger registries, skill metadata, status fields, path references, duplicate triggers, or registry consistency checks
---

# Skill Registry Maintenance

## Vietnamese User Summary

Skill này kiểm tra và bảo trì registry skill/workflow/trigger: path tồn tại, ID hợp lệ, trigger trùng, status đúng và metadata nhất quán.

## REQUIRED BACKGROUND

Read `.ai/skills/using-superpowers/SKILL.md` before using this skill when available.

## Required Rules

- `.ai/rules/00-global-rules.md`
- `.ai/rules/06-quality-gates.md`
- `.ai/rules/11-skillflow-extension-rules.md`

## Workflow

1. Read `.ai/registry/skills.yml`, `.ai/registry/workflows.yml`, and `.ai/registry/triggers.yml`.
2. Check that every registered skill path exists and contains valid `SKILL.md` frontmatter with `name` and `description`.
3. Check that every workflow path exists and points to the expected skill.
4. Check that trigger `skill_id` and `workflow_id` values reference registered IDs.
5. Detect duplicate trigger phrases, ambiguous trigger ownership, stale paths, unregistered skill folders, and active user-facing skills without triggers.
6. Apply minimal registry fixes when requested.
7. Run a lightweight validation command or explain why validation is unavailable.
8. Respond to the user in Vietnamese with changed files and remaining registry risks.

## Guardrails

- Do not rename existing skill IDs unless the user explicitly requests a migration.
- Do not delete legacy references or runtime state without explicit approval.
- Keep support/internal skills callable only when trigger aliases are intentional.
- Preserve Vietnamese trigger aliases when editing.

## Quality Gates

- [ ] Skill, workflow, and trigger registries were checked together.
- [ ] Paths and IDs are consistent.
- [ ] Duplicate or ambiguous triggers are listed or fixed.
- [ ] Active/support status is intentional.
- [ ] Validation result is reported.
