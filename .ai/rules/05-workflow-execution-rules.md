# 05 Workflow Execution Rules

## Vietnamese User Summary

Rule này quy định thứ tự chạy workflow, preflight, output và fallback.

## Standard Execution Sequence

1. Resolve the trigger through `.ai/registry/triggers.yml`.
2. Use `routing-ai-task` when the correct specialized skill is not obvious.
3. Read the selected skill.
4. Read the selected workflow.
5. Read referenced rules.
6. Create or select a run namespace.
7. Search memory and project summary docs before detailed source reads.
8. Run CodeGraph preflight when source code is involved.
9. Limit file reads to the smallest useful scope.
10. Execute the workflow.
11. Run validation and quality gates.
12. Save confirmed memory findings when memory tools are available.
13. Respond to the user in Vietnamese.

## Run Namespace

New workflows should write runtime state to:

```text
.ai/runs/<skillflow_id>/<run_id>/
```

Suggested subdirectories:

```text
handoff/
findings/
artifacts/
logs/
```

## Fallbacks

If an expected tool is unavailable:

1. Record the limitation.
2. Use an approved fallback only when the workflow allows it.
3. Ask the user before continuing when the fallback weakens correctness materially.

## Validation

Before completion:

- Check output files exist.
- Check evidence exists for important claims.
- Check open questions are recorded.
- Check secrets are not exposed.
- Check memory writes are logged or explicitly skipped.
- Check the cost optimization checklist from `.ai/rules/13-efficiency-cost-policy-rules.md`.
- Check final response does not include full generated documentation.
