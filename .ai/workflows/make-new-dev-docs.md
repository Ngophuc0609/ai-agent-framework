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

## Mandatory Agent Output Gate

Before generating final documentation, verify that these outputs exist or are explicitly marked not applicable in `.ai/handoff/STATUS.md`:

- Agent 1: `draft-docs/01_SOURCE_AND_LOCAL_SETUP.md` or `.ai/runs/source-code-handover/<run_id>/findings/agent-01/`
- Agent 2: `draft-docs/02_DATABASE_AND_AUTH.md` or `.ai/runs/source-code-handover/<run_id>/findings/agent-02/`
- Agent 3: `draft-docs/03_API_AND_POSTMAN.md` or `.ai/runs/source-code-handover/<run_id>/findings/agent-03/`
- Agent 4: `draft-docs/04_BUSINESS_AND_FRONTEND.md` or `.ai/runs/source-code-handover/<run_id>/findings/agent-04/`
- Agent 5: `draft-docs/05_OPERATIONS.md` or `.ai/runs/source-code-handover/<run_id>/findings/agent-05/`
- Agent 6: `draft-docs/06_COORDINATOR_REVIEW.md` or `.ai/runs/source-code-handover/<run_id>/findings/agent-06/`

Agent 7 must read Agent 1-6 outputs before writing `docs/PROJECT_HANDOVER_FULL.md`.

If the runtime cannot spawn real sub-agents, it must run Agent 1-7 sequentially in the same session and record `single-runtime-sequential-fallback`.

The final chat response must list:

- Execution mode.
- Agent outputs created or marked not applicable.
- Final docs created.
- Validation result.

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

Do not mark `Ready` when required agent outputs were skipped, merged implicitly, or replaced by a direct final handbook.
