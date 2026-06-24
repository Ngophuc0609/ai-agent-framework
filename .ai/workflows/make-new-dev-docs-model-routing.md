# Model Routing for Dev Docs

If the repository involves authentication, payment, SignalR, PII, Kubernetes, Background Jobs, or DB Migrations, FAST_CHEAP is forbidden for Agents 2, 3, 5, 6, and 8.

Default routing for auth-heavy projects:
- Agent 1: BALANCED
- Agent 2: REASONING_STRONG
- Agent 3: REASONING_STRONG
- Agent 4: BALANCED
- Agent 5: REASONING_STRONG
- Agent 6: REASONING_STRONG
- Agent 7: LONG_CONTEXT_STRONG
- Agent 8: REASONING_STRONG

If runner lacks routing:
- Log limitation in STATUS.md.
- Max readiness is `Partial` if critical review cannot be reliable.
