---
name: mcp-integration-planning
description: Use when planning, reviewing, or documenting Model Context Protocol integrations, MCP servers, tool permissions, resources, prompts, auth, transport, sandboxing, memory use, or agent access to external systems
---

<!-- generated-by: ai-agent-adapter-sync -->


# MCP Integration Planning

## Vietnamese User Summary

Skill này lập plan hoặc review tích hợp MCP: server, tools/resources/prompts, quyền truy cập, auth, transport, sandbox, memory và hệ thống ngoài.

## REQUIRED BACKGROUND

Read `.ai/skills/using-superpowers/SKILL.md` before using this skill when available.

## Required Rules

- `.ai/rules/00-global-rules.md`
- `.ai/rules/03-safety-rules.md`
- `.ai/rules/06-quality-gates.md`
- `.ai/rules/12-memory-policy-rules.md`
- `.ai/rules/13-efficiency-cost-policy-rules.md`

## Workflow

1. Identify the intended MCP integration and business goal.
2. List required tools, resources, prompts, auth method, transport, environment variables, and data sensitivity.
3. Define least-privilege permissions and allowed operations.
4. Define sandboxing, approval gates, rate limits, audit logging, and secret handling.
5. Check whether existing project adapters or rules already cover the integration.
6. Produce an implementation plan with setup steps, validation checks, fallback behavior, and rollback.
7. For high-risk integrations, recommend a read-only first phase before write operations.
8. Respond to the user in Vietnamese.

## Guardrails

- Do not add secrets to docs, memory, examples, or config templates.
- Do not recommend broad filesystem, database, GitHub, Slack, or cloud permissions when narrower scopes work.
- Do not connect production systems without explicit approval.
- Treat third-party MCP servers as untrusted until reviewed.

## Quality Gates

- [ ] Tools/resources/prompts and permissions are explicit.
- [ ] Auth and secret handling are defined.
- [ ] Read/write risk is separated.
- [ ] Validation and rollback steps are included.
- [ ] High-risk operations require confirmation gates.
