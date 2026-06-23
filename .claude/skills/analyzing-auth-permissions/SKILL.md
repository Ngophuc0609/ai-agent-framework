---
name: analyzing-auth-permissions
description: Use when analyzing, documenting, debugging, or reviewing authentication, session, token, middleware, role-based access control, permission checks, ownership checks, or authorization flows
---

<!-- generated-by: ai-agent-adapter-sync -->


# Analyzing Auth Permissions

## Vietnamese User Summary

Skill này phân tích auth, session/token, middleware, RBAC, permission, ownership check và luồng phân quyền.

## REQUIRED BACKGROUND

Read `.ai/skills/using-superpowers/SKILL.md` before using this skill when available.

## Required Rules

- `.ai/rules/00-global-rules.md`
- `.ai/rules/03-safety-rules.md`
- `.ai/rules/06-quality-gates.md`
- `.ai/rules/10-codegraph-first-rules.md`
- `.ai/rules/12-memory-policy-rules.md`
- `.ai/rules/13-efficiency-cost-policy-rules.md`

## Workflow

1. Resolve the target: login flow, token/session handling, middleware, role mapping, permission check, ownership rule, or endpoint access.
2. Retrieve auth-related memory and project docs when available.
3. Run CodeGraph preflight.
4. Trace identity creation, credential verification, token/session creation, middleware enforcement, permission decisions, and error behavior.
5. Identify bypass risks, missing ownership checks, inconsistent role names, stale permissions, token lifetime issues, and unsafe defaults.
6. Check tests and API docs when present.
7. Summarize the effective access rules, evidence files, risks, and open questions.
8. Store verified auth conventions or confirmed bugs when memory is available.
9. Respond to the user in Vietnamese.

## Guardrails

- Do not print secrets, passwords, tokens, private keys, or session values.
- Do not weaken auth or permission checks while fixing related code.
- Do not infer access rules from naming alone; verify enforcement points.
- Treat current source code as the source of truth when docs or memory conflict.

## Quality Gates

- [ ] Identity source and enforcement points were traced.
- [ ] Roles, permissions, and ownership rules are explicit.
- [ ] Missing or inconsistent checks are listed with file evidence.
- [ ] Tests or verification gaps are noted.
- [ ] Sensitive values were not exposed.
