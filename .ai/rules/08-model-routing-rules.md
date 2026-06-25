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
