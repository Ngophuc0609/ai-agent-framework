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

For source-code handover and new-developer documentation workflows, low-capability, nano, random-router, non-generative, safety-only, embedding-only, rerank-only, or unproven instruction-following models are not approved for final documentation generation, publication, independent validation, or tool-orchestration recovery.

Free pricing alone does not block a model. Model names are not a pass/fail gate. A model can be used when it satisfies the required capability class for the phase and the selected adapter/runtime can reliably execute tools, read `.ai/` files, follow the workflow, preserve evidence discipline, and produce the required structured artifacts.

Do not hard-code exact free model names as required or forbidden in skill/workflow rules. Model names may be listed only as non-binding suggestions for the user. Runtime gates must be based on observed capability, tool reliability, phase risk, and validation output.

Example blocked model classes for this workflow:

- embedding-only or rerank-only models,
- safety-classifier-only models,
- random routers where the actual model cannot be pinned,
- models that cannot read required `.ai` files or cannot reliably call required tools,
- models that fail the preflight contract or replace workflow execution with generic/chatty content.

Allowed use for these models is limited to:

- reading and summarizing already-created artifacts,
- checking whether expected files exist,
- listing blocked preflight status,
- formatting non-authoritative notes.

If a blocked low-capability model/runtime is active, maximum workflow state is `BLOCKED` until a BALANCED-equivalent or stronger model/tool runtime is used. It MUST NOT write final docs or fallback onboarding docs.

## Blocked-Model Response Contract

When a model/runtime cannot execute the workflow because of capability, routing, tool access, rate limit, or instruction-following uncertainty, it MUST stop with a structured blocked status. It MUST NOT write a humorous refusal, non-technical excuse, encouragement for the user to do the work manually, or generic advice in place of workflow artifacts.

Required blocked response:

```text
BLOCKED_MODEL_CAPABILITY
Workflow: source-code-handover / make-new-dev-docs
Requested model: <model name>
Reason: <capability/routing/tool limitation>
Required action: switch to an approved BALANCED/REASONING_STRONG/LONG_CONTEXT_STRONG model or run with Codex/Claude/Gemini High-equivalent tooling
Artifacts preserved: <run dir or none>
```

If `.ai/runs/` is writable, also write the same information to `.ai/runs/source-code-handover/<run_id>/validation/blocked-report.md`.

## Model Selection Guidance For Source Handover

Model suggestions are advisory only. Users and runners may choose any model that meets the required capability class for the phase. If a local team maintains a list of preferred free or paid models, keep it as user-facing guidance and do not turn it into a hard workflow whitelist.

Minimum capability expectations by phase:

| Phase | Minimum model/runtime capability |
|---|---|
| Phase 0 / Agents 1, 4 | `FAST_CHEAP` or stronger when deterministic tools produce structured inventory. |
| Agents 2, 3, 5 | `REASONING_STRONG` for auth, API, Redis, DB, jobs, migrations, and external integration claims. |
| Agents 6, 7, 8 | `REASONING_STRONG` with reliable tool access and evidence discipline. |
| Agent 9 | `LONG_CONTEXT_STRONG` or equivalent for final Vietnamese synthesis from frozen evidence. |
| Agent 10 | `REASONING_STRONG` or equivalent for independent validation. |

## Free Model Rate-Limit Fallback

Free model endpoints often return provider-level `429` rate limits. When a model call fails with `429`, `rate_limit`, `temporarily rate-limited`, or an OpenRouter `retry_after_seconds` / `Retry-After` value:

1. Record the failure in `STATUS.md` or the active run's model/tool limitation artifact.
2. Respect `Retry-After` when it is short and the current step is safe to wait for.
3. Retry the same model at most once after the wait.
4. If it fails again, switch to another available model in the same or stronger capability class.
5. Do not downgrade a high-risk agent to a weak model just because it is available.
6. If no approved model is available, stop the phase as `BLOCKED_MODEL_RATE_LIMIT`.

Fallback is capability-based, not name-based:

```text
same model after Retry-After, once
  -> another model with the same or stronger required capability class
  -> stronger model/runtime if evidence is conflicting or the phase is high risk
  -> BLOCKED_MODEL_RATE_LIMIT
```

For Agents 6-10 on complex repositories, if the fallback drops below `REASONING_STRONG` / `LONG_CONTEXT_STRONG`, the final readiness must be `Partial` at best. If Agent 10 cannot run with an approved model, publish readiness is `Blocked`.

Do not use `OpenRouter Free Models Router` as a rate-limit fallback for this workflow because random model selection makes evidence quality non-reproducible.

Not recommended model classes for executing this workflow:

| Model class | Reason |
|---|---|
| Random router | Actual model is not pinned, so evidence quality and instruction following are non-reproducible. |
| Embedding/retrieval/rerank model | Not a documentation writer or verifier. |
| Safety-classifier-only model | Not a source-handover model. |
| Very small instruction model | Usually too small for reliable tool orchestration and source evidence synthesis; may only classify/tidy existing artifacts. |
| Uncontrolled/uncurated chat model | Not suitable unless it passes project preflight and validation. |
