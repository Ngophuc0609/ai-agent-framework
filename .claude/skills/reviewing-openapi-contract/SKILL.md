---
name: reviewing-openapi-contract
description: Use when reviewing or reconciling OpenAPI, Swagger, Postman, curl examples, API documentation, or generated API contracts against implemented routes, validation, authentication, and response behavior
---

<!-- generated-by: ai-agent-adapter-sync -->


# Reviewing OpenAPI Contract

## Vietnamese User Summary

Skill này review và đối chiếu OpenAPI/Swagger/Postman/curl/API docs với route, validation, auth và response thật trong source code.

## REQUIRED BACKGROUND

Read `.ai/skills/using-superpowers/SKILL.md` before using this skill when available.

## Required Rules

- `.ai/rules/00-global-rules.md`
- `.ai/rules/06-quality-gates.md`
- `.ai/rules/10-codegraph-first-rules.md`
- `.ai/rules/12-memory-policy-rules.md`
- `.ai/rules/13-efficiency-cost-policy-rules.md`

## Workflow

1. Identify the contract artifact: OpenAPI, Swagger, Postman, curl examples, README, or generated client schema.
2. Retrieve memory for API conventions and documentation conventions.
3. Run CodeGraph preflight.
4. Locate matching routes, controllers, request models, validation, auth middleware, services, and response mapping.
5. Compare method, path, parameters, request body, headers, auth, permissions, status codes, response schema, error schema, pagination, and side effects.
6. Check whether examples use placeholders for tokens and environment-specific values.
7. Produce a mismatch report with source-backed evidence and recommended doc or code updates.
8. If asked to edit, update the smallest contract/docs surface that matches repository convention.
9. Respond to the user in Vietnamese.

## Guardrails

- Do not fabricate API behavior that is not implemented.
- Do not include real tokens, passwords, keys, or connection strings in examples.
- Do not change public API semantics unless explicitly requested.
- Mark contract ambiguity as `Need verify`.

## Quality Gates

- [ ] Implemented route and contract artifact were both checked.
- [ ] Auth, validation, response, and error behavior were compared.
- [ ] Mismatches are evidence-backed.
- [ ] Placeholder values are used for secrets and environment-specific data.
- [ ] Docs were updated only when repository convention supports them.
