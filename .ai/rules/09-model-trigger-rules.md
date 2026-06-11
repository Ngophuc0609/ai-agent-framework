# 09 Model Trigger Rules

## Vietnamese User Summary

Rule này cho phép người dùng chọn chế độ tiết kiệm, cân bằng hoặc chính xác cao khi chạy workflow.

## Trigger Modes

Trigger phrases may request one of these modes:

- `LOW_COST`: prioritize cost savings.
- `BALANCED_BUDGET`: default mode.
- `HIGH_ACCURACY`: prioritize correctness and stronger review.

Vietnamese trigger aliases may appear in `.ai/registry/triggers.yml`; keep the routing instructions here in English.

## Selection

- If the user explicitly asks for a mode, use it.
- If no mode is specified, use `BALANCED_BUDGET`.
- If the requested mode conflicts with safety or correctness requirements, escalate to the safer model class and record why.

## Output

Record the selected mode in workflow status and final summary.
