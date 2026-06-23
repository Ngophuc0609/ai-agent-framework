---
name: maintaining-existing-apis
description: Use when maintaining or changing existing API endpoints, routes, handlers, gateway routes, request/response contracts, API documentation, or API tests; for new endpoints or new API features, use developing-backend-feature-tdd instead
---

<!-- generated-by: ai-agent-adapter-sync -->


# Maintaining Existing APIs

## Vietnamese User Summary

Skill này duy trì hoặc chỉnh API đã có sẵn. Nếu bạn yêu cầu tạo endpoint/API mới, agent phải chuyển sang `developing-backend-feature-tdd`.

## REQUIRED BACKGROUND

Read `.ai/skills/using-superpowers/SKILL.md` before using this skill.

## Required Rules

- `.ai/rules/00-global-rules.md`
- `.ai/rules/10-codegraph-first-rules.md`
- `.ai/rules/12-memory-policy-rules.md`
- `.ai/rules/06-quality-gates.md`

## Memory Policy

Use memory tools only for durable, reusable, verified information.

Before starting, retrieve memory for:

- Existing API conventions.
- Route/controller/service naming.
- Auth and permission rules.
- Validation conventions.
- Known API bugs.
- Documentation conventions.

During work, store only verified facts such as confirmed API flows, route conventions, auth rules, validation behavior, and known bugs with root causes.

Do not store secrets, tokens, passwords, private keys, temporary logs, unverified guesses, large raw source code, or full stack traces.

After each major step, save a short memory summary with what was analyzed, what was confirmed, what remains uncertain, and which files prove the finding.

Before editing or documenting a module, retrieve memory for that module first.

If memory conflicts with current source code, trust current source code and update memory.

## Workflow

1. If the request is for a new endpoint or new API feature, stop and route to `developing-backend-feature-tdd`.
2. Check git status.
3. Run CodeGraph preflight.
4. Retrieve project and API-related memory.
5. Identify the API framework, routing style, middleware, validation, auth, error handling, and test patterns.
6. Find the existing endpoint or closest related endpoint.
7. Confirm the current or target contract:
   - HTTP method.
   - Path.
   - Request body/query/headers.
   - Response shape.
   - Auth and permission requirements.
   - Validation rules.
   - Side effects.
   - Persistence or integration dependencies.
8. If a critical contract detail is missing, ask one concise clarification question in Vietnamese.
9. Add or update focused tests when feasible before changing behavior.
10. Implement the smallest coherent change following existing patterns.
11. Update OpenAPI, Postman, README, or other API docs only if the repository already maintains them.
12. Run validation commands available in the repo.
13. Store confirmed findings back to memory when memory tools are available.
14. Respond to the user in Vietnamese with changed files, validation result, and remaining risks.

## Guardrails

- Follow existing project patterns before introducing new abstractions.
- Do not bypass service, validation, authorization, middleware, or gateway layers.
- Do not weaken auth, CORS, rate limiting, validation, logging, or error handling.
- Do not hard-code secrets or environment-specific values.
- Do not change unrelated production configuration.
- Do not fabricate API documentation when behavior is uncertain.

## Quality Gates

- Existing API style was checked.
- Contract details are explicit or documented as open questions.
- Auth and validation behavior are preserved.
- Tests or smoke checks were run, added, or explicitly skipped with reason.
- API documentation was updated when required by repo convention.
- Memory writes were logged or skipped with limitation.
