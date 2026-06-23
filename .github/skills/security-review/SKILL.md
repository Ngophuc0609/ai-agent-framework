---
name: security-review
description: Use when reviewing backend or API security risks including authentication, authorization, input validation, secrets exposure, dependency risk, insecure configuration, logging leaks, or security-sensitive git diffs
---

<!-- generated-by: ai-agent-adapter-sync -->


# Security Review

## Vietnamese User Summary

Skill này review rủi ro bảo mật trong backend/API, auth, validation, cấu hình, dependency, logging và diff nhạy cảm.

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

1. Define the review scope: diff, endpoint, module, dependency, config, or full security pass.
2. Retrieve relevant memory for auth, permission, validation, known bugs, and security conventions.
3. Run CodeGraph preflight for source-reading work.
4. Inspect only the scoped files and direct security dependencies.
5. Check authentication, authorization, validation, secret handling, injection risk, CORS/CSRF/rate limiting, logging, error disclosure, dependency risk, and insecure defaults.
6. For API changes, verify the request/response contract does not weaken auth, permissions, validation, or data exposure.
7. Report findings by severity with evidence, exploitability, impact, and concrete remediation.
8. Mark uncertain items as `Need verify` instead of guessing.
9. Store only durable verified security conventions or confirmed root causes when memory is available.
10. Respond to the user in Vietnamese.

## Guardrails

- Do not expose secrets or reproduce sensitive values.
- Do not provide offensive exploitation steps beyond what is needed to explain risk and remediation.
- Do not recommend disabling auth, validation, logging, rate limits, or TLS checks.
- Do not flag theoretical issues without connecting them to reachable code or configuration.

## Quality Gates

- [ ] Scope and evidence are explicit.
- [ ] Findings are ordered by severity.
- [ ] Auth, permission, validation, secrets, logging, and dependency risks were considered.
- [ ] False-positive uncertainty is marked as `Need verify`.
- [ ] Remediation is actionable and scoped.
