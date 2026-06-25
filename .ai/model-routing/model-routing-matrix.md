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
| Agent 6 | Source/symbol claim verifier | REASONING_STRONG | Always prefer strong source/symbol verification |
| Agent 7 | Cross-layer flow/conflict verifier | REASONING_STRONG | Cross-domain reasoning or conflicts exist |
| Agent 8 | Safety/build/test/runtime/ops evidence verifier | REASONING_STRONG | Safety, runtime, secret, or ops evidence is needed |
| Agent 9 | Final Vietnamese handbook writer | LONG_CONTEXT_STRONG | Always prefer long-context synthesis |
| Agent 10 | Independent publish validator | REASONING_STRONG | Always prefer strong independent validation |

## Antigravity Gemini Matrix

Use this matrix when the runner is Google Antigravity. Claude models are not allowed for this workflow.

| Agent / Phase | Responsibility | Default Gemini model | Escalate/Fallback Gemini model |
|---|---|---|---|
| Phase 0 | Inventory and simple extraction | Gemini 3.5 Flash (Low) | Gemini 3.5 Flash (Medium) |
| Agent 1 | Source and local setup | Gemini 3.5 Flash (Medium) | Gemini 3.5 Flash (High) |
| Agent 2 | Database and auth | Gemini 3.5 Flash (High) | Gemini 3.1 Pro (High) |
| Agent 3 | API and Postman | Gemini 3.5 Flash (High) | Gemini 3.1 Pro (High) |
| Agent 4 | Business and frontend | Gemini 3.5 Flash (Medium) | Gemini 3.5 Flash (High) |
| Agent 5 | Operations, jobs, Redis | Gemini 3.5 Flash (High) | Gemini 3.1 Pro (High) |
| Agent 6 | Source/symbol claim verifier | Gemini 3.5 Flash (High) | Gemini 3.1 Pro (High) |
| Agent 7 | Cross-layer flow/conflict verifier | Gemini 3.5 Flash (High) | Gemini 3.1 Pro (High) |
| Agent 8 | Safety/build/test/runtime/ops evidence verifier | Gemini 3.5 Flash (High) | Gemini 3.1 Pro (High) |
| Agent 9 | Final Vietnamese handbook writer | Gemini 3.5 Flash (High) | Gemini 3.1 Pro (High) |
| Agent 10 | Independent publish validator | Gemini 3.5 Flash (High) | Gemini 3.1 Pro (High) |

`Gemini 3.1 Pro (Low)` is not acceptable for Agent 2, 3, 5, 6, 7, 8, 9, or 10 on source-code handover runs.

## Logging

Each agent should record:

- Requested model class.
- Actual model when known.
- Escalation or downgrade reason.
- Impact on readiness.
