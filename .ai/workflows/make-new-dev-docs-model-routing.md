# Model Routing for Dev Docs

If the repository has: authentication, payment, SignalR, PII, Kubernetes, Background Jobs, or DB Migrations, `FAST_CHEAP` is FORBIDDEN for Agents 2, 3, 5, 6, 7, 8, 9, and 10.

## Antigravity Gemini-Only Policy

When running `source-code-handover` or `make-new-dev-docs` in Google Antigravity, use Gemini models only. Do not route any phase to `Claude Opus 4.6 Thinking` or `Claude Sonnet 4.6 Thinking`.

Cost-optimized Antigravity routing:

| Phase / Agent | Default Gemini model | Escalate to | Notes |
|---|---|---|---|
| Phase 0 inventory and simple extraction | Gemini 3.5 Flash (Low) | Gemini 3.5 Flash (Medium) | Use deterministic tools first; Low is only for low-risk classification and formatting. |
| Agent 1 Source/local/config | Gemini 3.5 Flash (Medium) | Gemini 3.5 Flash (High) | Escalate when startup/runtime/dependencies are unclear. |
| Agent 2 Database/auth | Gemini 3.5 Flash (High) | Gemini 3.1 Pro (High) | High-risk auth/schema work must not use Low. |
| Agent 3 API/Postman/contracts | Gemini 3.5 Flash (High) | Gemini 3.1 Pro (High) | Contract conflicts and auth-sensitive APIs require High. |
| Agent 4 Business/frontend/integrations | Gemini 3.5 Flash (Medium) | Gemini 3.5 Flash (High) | Escalate for critical business rules or external-system conflicts. |
| Agent 5 Operations/jobs/Redis | Gemini 3.5 Flash (High) | Gemini 3.1 Pro (High) | Jobs, Redis, retry, deploy, and rollback claims require High. |
| Agent 6 Source/symbol claim verification | Gemini 3.5 Flash (High) | Gemini 3.1 Pro (High) | Source and symbol verification must not use Low. |
| Agent 7 Cross-layer flow/conflict verification | Gemini 3.5 Flash (High) | Gemini 3.1 Pro (High) | Cross-domain reconciliation must not use Low. |
| Agent 8 Safety/build/test/runtime/ops evidence | Gemini 3.5 Flash (High) | Gemini 3.1 Pro (High) | Safety and runtime evidence must not use Low. |
| Agent 9 Final Vietnamese handbook | Gemini 3.5 Flash (High) | Gemini 3.1 Pro (High) | Final synthesis must use High; split docs into chunks if context is too large. |
| Agent 10 Independent publish validator | Gemini 3.5 Flash (High) | Gemini 3.1 Pro (High) | Validation must use High and remain independent from Agent 9. |

`Gemini 3.1 Pro (Low)` is allowed only for low-risk formatting, checklist normalization, or short summaries after evidence is already verified. It MUST NOT be used for Agents 2, 3, 5, 6, 7, 8, 9, or 10 on complex repositories.

Default routing for auth-heavy/IdentityServer projects:
- Agent 1: BALANCED
- Agent 2: REASONING_STRONG
- Agent 3: REASONING_STRONG
- Agent 4: BALANCED
- Agent 5: REASONING_STRONG
- Agent 6: REASONING_STRONG
- Agent 7: REASONING_STRONG
- Agent 8: REASONING_STRONG
- Agent 9: LONG_CONTEXT_STRONG
- Agent 10: REASONING_STRONG

## Routing Fallback
If the runner does not support model routing:
- Record the limitation in `STATUS.md`.
- Do not mark model quality as verified.
- If Agents 2/3/5/6/7/8/9/10 cannot run with at least a BALANCED-equivalent tier, maximum readiness is `Partial`.
- If independent validation (Agent 10) cannot run, maximum readiness is `Blocked`.
- In Antigravity, if the runner attempts to use Claude for this workflow, override to the Gemini-only matrix above and record the override in `STATUS.md`.

## Blocked Low-Capability Models

The following model class is not acceptable for executing the full workflow:

- low-capability/nano/random-router/non-generative/safety-only/embedding-only/rerank-only models, including `nvidia/nemotron-3-nano-30b-a3b:free`.

These models may summarize already-created artifacts but MUST NOT run Agents 1-10, generate final docs, publish to `docs/`, or recover from tool failures by writing generic onboarding content.

Free pricing alone is not a block. If the runner must use free models, prefer this order:

1. `Qwen: Qwen3 Coder 480B A35B (free)` for code/repo/tool-heavy phases.
2. `Qwen: Qwen3 Next 80B A3B Instruct (free)` for broad discovery and structured summaries.
3. `Google: Gemma 4 26B A4B (free)` for long-context extraction and structured output.
4. `Meta: Llama 3.3 70B Instruct (free)` for Vietnamese summaries and second-pass review.
5. `Nous: Hermes 3 405B Instruct (free)` only when endpoint reliability is verified.

## Rate-Limit Recovery

When a free provider returns `429`, `temporarily rate-limited`, `retry_after_seconds`, or a `Retry-After` header:

1. Wait for the provider retry interval when it is short.
2. Retry the same model once.
3. If the retry fails, move to the next approved free model in the fallback order above.
4. Record the original model, provider, error code, retry interval, fallback model, and readiness impact in `STATUS.md`.
5. Do not fall back to a blocked/non-generative/random-router model.

If no approved model is available:

- Mark the affected phase `BLOCKED_MODEL_RATE_LIMIT`.
- Do not run Agent 9 final docs.
- Do not publish to `docs/`.
- Keep already-created deterministic inventory/evidence artifacts for resume.
