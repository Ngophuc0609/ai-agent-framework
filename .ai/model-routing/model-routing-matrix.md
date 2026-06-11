# Model Routing Matrix

## Vietnamese User Summary

File này mô tả tier model nên dùng cho từng agent trong workflow tạo tài liệu.

## Model Classes

- `FAST_CHEAP`: broad scan, inventory, simple extraction.
- `BALANCED`: normal analysis and implementation.
- `REASONING_STRONG`: critical reasoning, review, security, conflict handling.
- `LONG_CONTEXT_STRONG`: final synthesis across many files.

## Default Matrix

| Agent | Responsibility | Default | Escalate When |
|---|---|---:|---|
| Agent 1 | Source and local setup | FAST_CHEAP | Startup/runtime is unclear |
| Agent 2 | Database and auth | BALANCED | Auth/security/schema conflicts |
| Agent 3 | API and Postman | BALANCED | Contract conflicts or security-sensitive APIs |
| Agent 4 | Business and frontend | BALANCED | Business rules are unclear or critical |
| Agent 5 | Operations | BALANCED | Jobs, realtime, deploy, or incident risk is critical |
| Agent 6 | Coordinator reviewer | REASONING_STRONG | Always prefer strong review |
| Agent 7 | Handbook aggregator | LONG_CONTEXT_STRONG | Always prefer long-context synthesis |

## Logging

Each agent should record:

- Requested model class.
- Actual model when known.
- Escalation or downgrade reason.
- Impact on readiness.
