# 08 Model Routing Rules

## Vietnamese User Summary

Rule này quy định cách chọn model/tier cho từng agent để cân bằng chi phí và độ chính xác.

## Model Classes

- `FAST_CHEAP`: Use for broad scans, file inventory, simple extraction, and low-risk summaries.
- `BALANCED`: Use for normal reasoning, moderate cross-file analysis, and most implementation work.
- `REASONING_STRONG`: Use for synthesis, conflict resolution, security-sensitive analysis, production-critical decisions, and final review.
- `LONG_CONTEXT_STRONG`: Use when the task needs large context plus strong synthesis.

## Routing Principles

- Use the cheapest model that can satisfy the required correctness.
- Use small or cheap models for discovery, file classification, keyword search, summarization, formatting, checklist generation, simple edits, simple curl generation, and commit message drafting.
- Use strong models only after the relevant scope has been narrowed.
- Escalate when evidence is conflicting, source is large, behavior is critical, or reasoning depends on multiple modules.
- Final reviewer and final handbook writer should use `REASONING_STRONG` or `LONG_CONTEXT_STRONG` when available.
- If the runner does not support per-agent model selection, record the limitation.

## Antigravity Gemini-Only Rule

For Google Antigravity runs, route `source-code-handover` and `make-new-dev-docs` through Gemini models only.

- Do not use `Claude Opus 4.6 Thinking`.
- Do not use `Claude Sonnet 4.6 Thinking`.
- Prefer `Gemini 3.5 Flash (Medium)` for normal discovery/findings after deterministic tools narrow the scope.
- Prefer `Gemini 3.5 Flash (High)` for Agents 2, 3, 5, 6, 7, 8, 9, and 10, and for high-risk business/auth/API/Redis/job/migration evidence.
- Use `Gemini 3.5 Flash (Low)` only for low-risk inventory classification, formatting, and checklist normalization.
- Use `Gemini 3.1 Pro (High)` only as a Gemini-family fallback for complex synthesis/review when `Gemini 3.5 Flash (High)` is unavailable or performs poorly.
- Use `Gemini 3.1 Pro (Low)` only for low-risk helper tasks; it is not acceptable for final synthesis or final validation on non-trivial repositories.

If an Antigravity runner proposes a non-Gemini model, override it to the closest Gemini tier and record the override in `STATUS.md`.

## Required Logging

Each agent should record:

- Requested model class.
- Actual model used when known.
- Reason for escalation or downgrade.
- Impact on readiness.

## Readiness Constraint

If critical review or final synthesis cannot be run with a sufficiently capable model, final readiness must not exceed `Partial` unless the source evidence is simple and fully verified.

## Low-Capability Model Block

For source-code handover and new-developer documentation workflows, low-capability, nano, random-router, non-generative, safety-only, embedding-only, rerank-only, or unknown instruction-following models are not approved for final documentation generation, publication, independent validation, or tool-orchestration recovery.

Free pricing alone does not block a model. A free model can be used only when it is explicitly capable enough for the assigned workflow phase and the selected adapter/runtime can reliably execute tools and read `.ai/` files.

Example blocked model for this workflow:

- `nvidia/nemotron-3-nano-30b-a3b:free`

Allowed use for these models is limited to:

- reading and summarizing already-created artifacts,
- checking whether expected files exist,
- listing blocked preflight status,
- formatting non-authoritative notes.

If a blocked low-capability model is active, maximum workflow state is `BLOCKED` until a BALANCED-equivalent or stronger model/tool runtime is used. It MUST NOT write final docs or fallback onboarding docs.

## Free Model Suitability For Source Handover

Recommended free models from the current evaluated list:

| Model | Allowed role | Not allowed for | Notes |
|---|---|---|---|
| `Qwen: Qwen3 Coder 480B A35B (free)` | Best free choice for code discovery, API/database/source analysis, Agent 1-8, and draft synthesis when tool access is stable. | Final publish without Agent 10 evidence gate. | Strong code/tool/repo fit and very long context. |
| `Qwen: Qwen3 Next 80B A3B Instruct (free)` | Good balanced choice for Agent 1-5 discovery, structured summaries, and moderate verification. | High-risk final validation on complex auth/payment/runtime repos unless no stronger free model is available. | Good instruction following and long context. |
| `Google: Gemma 4 26B A4B (free)` | Good for structured extraction, long-context inventory, multimodal docs/images, and Agent 1/4 formatting-heavy work. | Sole final validator for complex repos. | Useful context and structured output support, but less code-specialized than Qwen Coder. |
| `Meta: Llama 3.3 70B Instruct (free)` | Good general reasoning, Vietnamese summaries, and second-pass review. | Deep code/tool orchestration as primary model when Qwen Coder is available. | Strong general assistant; code/repo agent behavior may be less consistent. |
| `Nous: Hermes 3 405B Instruct (free)` | Optional strong critique/synthesis model when the endpoint is stable. | Deterministic publish gate unless tool behavior is verified. | Potentially strong, but free endpoint reliability must be recorded. |

## Free Model Rate-Limit Fallback

Free model endpoints often return provider-level `429` rate limits. When a model call fails with `429`, `rate_limit`, `temporarily rate-limited`, or an OpenRouter `retry_after_seconds` / `Retry-After` value:

1. Record the failure in `STATUS.md` or the active run's model/tool limitation artifact.
2. Respect `Retry-After` when it is short and the current step is safe to wait for.
3. Retry the same model at most once after the wait.
4. If it fails again, switch to the next approved model in the same or stronger capability class.
5. Do not downgrade a high-risk agent to a weak model just because it is available.
6. If no approved model is available, stop the phase as `BLOCKED_MODEL_RATE_LIMIT`.

Preferred free fallback ladder for source-code handover:

```text
Qwen3 Coder 480B A35B (free)
  -> Qwen3 Next 80B A3B Instruct (free)
  -> Gemma 4 26B A4B (free)
  -> Llama 3.3 70B Instruct (free)
  -> Hermes 3 405B Instruct (free, only if endpoint stability is verified)
  -> BLOCKED_MODEL_RATE_LIMIT
```

For Agents 6-10 on complex repositories, if the fallback drops below `REASONING_STRONG` / `LONG_CONTEXT_STRONG`, the final readiness must be `Partial` at best. If Agent 10 cannot run with an approved model, publish readiness is `Blocked`.

Do not use `OpenRouter Free Models Router` as a rate-limit fallback for this workflow because random model selection makes evidence quality non-reproducible.

Not recommended for executing this workflow:

| Model | Reason |
|---|---|
| `OpenRouter Free Models Router` | Random model selection makes evidence quality and instruction following non-reproducible. |
| `NVIDIA: Llama Nemotron Embed VL 1B V2 (free)` | Embedding/retrieval model, not a documentation writer/verifier. |
| `NVIDIA: Llama Nemotron Rerank VL 1B V2 (free)` | Reranker, not a documentation writer/verifier. |
| `NVIDIA: Nemotron 3.5 Content Safety (free)` | Safety classifier, not a source-handover model. |
| `LiquidAI: LFM2.5-1.2B-Thinking (free)` | Too small for source-handover execution; may only classify/tidy existing artifacts. |
| `LiquidAI: LFM2.5-1.2B-Instruct (free)` | Too small for source-handover execution; may only classify/tidy existing artifacts. |
| `Meta: Llama 3.2 3B Instruct (free)` | Too small for reliable tool orchestration and source evidence synthesis. |
| `Venice: Uncensored (free)` | Not suitable for controlled enterprise documentation because safety/alignment and instruction reliability are uncertain. |
