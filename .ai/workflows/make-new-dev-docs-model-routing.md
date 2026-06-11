# Make New Developer Documentation Model Routing

## Vietnamese User Summary

Workflow mở rộng này chọn model/tier cho workflow tạo tài liệu để cân bằng chi phí và độ chính xác.

## Parent Workflow

Use with `.ai/workflows/make-new-dev-docs.md`.

## Modes

### LOW_COST

Use when the user prioritizes cost savings.

- Agent 1: `FAST_CHEAP`
- Agent 2: `FAST_CHEAP`, escalate for auth/security conflicts.
- Agent 3: `FAST_CHEAP`
- Agent 4: `FAST_CHEAP`
- Agent 5: `FAST_CHEAP`
- Agent 6: `BALANCED`
- Agent 7: `REASONING_STRONG` or `LONG_CONTEXT_STRONG`

Final readiness must not exceed `Partial` if critical evidence is weak.

### BALANCED_BUDGET

Default mode.

- Agent 1: `FAST_CHEAP` or `BALANCED`
- Agent 2: `BALANCED`
- Agent 3: `BALANCED`
- Agent 4: `BALANCED`
- Agent 5: `BALANCED`
- Agent 6: `REASONING_STRONG`
- Agent 7: `REASONING_STRONG` or `LONG_CONTEXT_STRONG`

### HIGH_ACCURACY

Use for large, complex, production-critical, or handover-critical systems.

- Agent 1: `BALANCED`
- Agent 2: `REASONING_STRONG`
- Agent 3: `REASONING_STRONG`
- Agent 4: `REASONING_STRONG`
- Agent 5: `REASONING_STRONG`
- Agent 6: `REASONING_STRONG`
- Agent 7: `LONG_CONTEXT_STRONG`

## Runner Behavior

If the runner supports per-agent model selection:

1. Apply the selected model class per agent.
2. Record actual model usage in each finding.
3. Have Agent 6 review the routing summary.

If the runner does not support per-agent model selection:

1. Use the current model.
2. Keep agent output boundaries.
3. Record the limitation.
4. Cap readiness at `Partial` when critical review could not run on a strong model.
