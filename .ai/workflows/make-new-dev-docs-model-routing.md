# Model Routing for Dev Docs

If the repository has: authentication, payment, SignalR, PII, Kubernetes, Background Jobs, or DB Migrations, `FAST_CHEAP` is FORBIDDEN for Agents 2, 3, 5, 6, and 8.

Default routing for auth-heavy/IdentityServer projects:
- Agent 1: BALANCED
- Agent 2: REASONING_STRONG
- Agent 3: REASONING_STRONG
- Agent 4: BALANCED
- Agent 5: REASONING_STRONG
- Agent 6: REASONING_STRONG
- Agent 7: LONG_CONTEXT_STRONG
- Agent 8: REASONING_STRONG

## Routing Fallback
If the runner does not support model routing:
- Record the limitation in `STATUS.md`.
- Do not mark model quality as verified.
- If Agents 2/3/5/6/8 cannot run with at least a BALANCED-equivalent tier, maximum readiness is `Partial`.
- If independent validation (Agent 8) cannot run, maximum readiness is `Blocked`.
