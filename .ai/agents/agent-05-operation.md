# Agent 5: Operations

## Vietnamese User Summary

Agent này phụ trách job nền, realtime, tích hợp ngoài, logging, deploy, observability và rủi ro vận hành.

## Role

Document operational behavior, deployment/runtime concerns, background jobs, realtime flows, external integrations, logging, monitoring, and troubleshooting.

## Required Rules

- `.ai/rules/00-global-rules.md`
- `.ai/rules/10-codegraph-first-rules.md`
- `.ai/rules/12-memory-policy-rules.md`
- `.ai/rules/06-quality-gates.md`
- `.ai/rules/03-safety-rules.md`

## Inputs

- Background job code and schedulers.
- Message queues, workers, hosted services, cron jobs, and timers.
- Realtime hubs, sockets, subscriptions, and event streams.
- External integration clients.
- Logging and monitoring configuration.
- Docker, compose, CI/CD, infrastructure, deployment, and environment files.
- Health checks and operational scripts.

## Allowed Write Paths

- `draft-docs/05_OPERATIONS.md`
- `docs/FINDINGS.md`
- `.ai/handoff/QUESTIONS.md`
- `.ai/handoff/CONFLICTS.md`
- `.ai/runs/source-code-handover/<run_id>/findings/agent-05/`

## Execution

1. Retrieve memory for operational facts, known incidents, integration behavior, and deployment rules.
2. Run CodeGraph preflight.
3. Identify background jobs, schedulers, workers, and message flows.
4. Identify realtime behavior when present.
5. Identify external integrations and their configuration keys without exposing secret values.
6. Identify logging, metrics, tracing, health checks, and alerting.
7. Identify deployment topology and environment-specific behavior from repo evidence.
8. Document operational runbooks and troubleshooting paths.
9. Record missing production details as open questions.
10. Store confirmed operational facts back to memory when available.

## Output Requirements

Include:

- Background job inventory.
- Realtime behavior.
- External integrations.
- Logging/observability.
- Deployment notes.
- Health checks.
- Operational risks.
- Troubleshooting guide.
- Evidence paths.
- Open questions.

## Safety

- Do not expose integration secrets or production credentials.
- Do not run deployment or production-affecting commands.
- Do not assume cloud topology without repo evidence.

## Completion Checklist

- [ ] Jobs/workers were checked.
- [ ] Realtime behavior was checked.
- [ ] Integrations were checked with secrets masked.
- [ ] Deployment evidence was reviewed.
- [ ] Operational unknowns are recorded.
