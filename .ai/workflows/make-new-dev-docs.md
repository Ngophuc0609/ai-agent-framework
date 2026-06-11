# Make New Developer Documentation Workflow

## Vietnamese User Summary

Workflow này tạo tài liệu bàn giao source code cho developer mới.

## Skill

Use `.ai/skills/source-code-handover/SKILL.md`.

## Required Rules

- `.ai/rules/00-global-rules.md`
- `.ai/rules/01-documentation-skill.md`
- `.ai/rules/02-multi-agent-rules.md`
- `.ai/rules/06-quality-gates.md`
- `.ai/rules/10-codegraph-first-rules.md`
- `.ai/rules/12-memory-policy-rules.md`

## Allowed Write Paths

Legacy workflow paths:

- `draft-docs/`
- `docs/`
- `.ai/handoff/`

Preferred runtime namespace for new runs:

- `.ai/runs/source-code-handover/<run_id>/`

## Execution

1. Resolve the workflow through the registry.
2. Read the source-code handover skill.
3. Check git status.
4. Run CodeGraph preflight.
5. Retrieve project memory.
6. Create or reuse the run/handoff namespace.
7. Run the agents below, in parallel when safe or sequentially when not.
8. Review conflicts and open questions.
9. Generate final documentation.
10. Store confirmed durable findings back to memory when available.
11. Respond to the user in Vietnamese.

## Agents

### Agent 1: Source And Local Setup

Use `.ai/agents/agent-01-source-local.md`.

Responsibilities:

- Repository map.
- Runtime stack.
- Local setup.
- Configuration.
- Entry points.
- Build/run/test commands.

### Agent 2: Database And Auth

Use `.ai/agents/agent-02-database-auth.md`.

Responsibilities:

- Database engine and schema.
- ORM/data access.
- Migrations and seed data.
- Auth, roles, permissions, tokens, and policies.

### Agent 3: API And Postman

Use `.ai/agents/agent-03-api-postman.md`.

Responsibilities:

- API routes.
- Request/response contracts.
- Error conventions.
- OpenAPI/Postman artifacts.
- API smoke tests.

### Agent 4: Business And Frontend

Use `.ai/agents/agent-04-business-frontend.md`.

Responsibilities:

- Business modules.
- Domain flows.
- Frontend routes/components when present.
- User-facing behavior.

### Agent 5: Operations

Use `.ai/agents/agent-05-operation.md`.

Responsibilities:

- Background jobs.
- Realtime behavior.
- Logging.
- Deployment.
- Observability.
- Operational risks.

### Agent 6: Coordinator Reviewer

Use `.ai/agents/agent-06-coordinator-reviewer.md`.

Responsibilities:

- Review evidence.
- Resolve or record conflicts.
- Check completeness.
- Assign readiness.

### Agent 7: Single Handbook Aggregator

Use `.ai/agents/agent-07-single-handbook-aggregator.md`.

Responsibilities:

- Merge reviewed outputs.
- Produce final handbook.
- Preserve open questions and limitations.

## Final Documentation Targets

The workflow may produce:

- `docs/PROJECT_HANDOVER_FULL.md`
- `docs/PROJECT_CONTEXT.md`
- `docs/FINDINGS.md`
- `docs/DECISIONS.md`
- Additional focused docs when the agents produce them.

## Readiness

Use:

- `Ready`
- `Partial`
- `Blocked`

Do not mark `Ready` when CodeGraph, memory retrieval, critical source evidence, or final review was skipped without a safe reason.
