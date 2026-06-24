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
Nếu runner không hỗ trợ model routing:
- Ghi limitation vào STATUS.md.
- Không được tự đánh dấu model quality là verified.
- Nếu Agent 2/3/5/6/8 không thể chạy bằng tier tối thiểu BALANCED (hoặc tương đương), readiness tối đa là `Partial`.
- Nếu không thể chạy independent validation (Agent 8), readiness tối đa là `Blocked`.
