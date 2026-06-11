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
- Final reviewer and final handbook aggregator should use `REASONING_STRONG` or `LONG_CONTEXT_STRONG` when available.
- If the runner does not support per-agent model selection, record the limitation.

## Required Logging

Each agent should record:

- Requested model class.
- Actual model used when known.
- Reason for escalation or downgrade.
- Impact on readiness.

## Readiness Constraint

If critical review or final synthesis cannot be run with a sufficiently capable model, final readiness must not exceed `Partial` unless the source evidence is simple and fully verified.
