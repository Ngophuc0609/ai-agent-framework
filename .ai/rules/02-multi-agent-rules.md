# 02 Multi-Agent Rules

## Vietnamese User Summary

Rule này chuẩn hóa cách chia việc giữa nhiều agent khi tạo tài liệu hoặc rà soát source.

## Coordination

- Use the workflow file as the source of truth for agent order, responsibilities, and output paths.
- Each agent must write only to its assigned files.
- Each agent must include evidence paths for important findings.
- Agents must write open questions instead of guessing.
- The coordinator/reviewer is responsible for consistency, conflicts, readiness, and final synthesis.

## Handoff

Use handoff files only for coordination facts that other agents need:

- `.ai/handoff/STATUS.md`
- `.ai/handoff/QUESTIONS.md`
- `.ai/handoff/CONFLICTS.md`
- `.ai/handoff/DECISIONS.md`

For new workflows, prefer `.ai/runs/<skillflow_id>/<run_id>/handoff/`.

## Parallel Work

Agents may run in parallel only when their output paths do not conflict and their inputs are stable.

If parallel execution is unavailable:

1. Run agents sequentially.
2. Preserve each agent's output boundary.
3. Record the fallback in status.

## Conflict Handling

When two agents disagree:

1. Compare the evidence.
2. Trust current source code over memory or prior notes.
3. Prefer direct runtime/config evidence over inference.
4. Record unresolved conflicts for reviewer or human confirmation.

## Completion

A multi-agent workflow is complete only when:

- Required agent outputs exist or are explicitly marked not applicable.
- Open questions are listed.
- Conflicts are resolved or documented.
- Readiness is assigned.
- Final response summarizes status in Vietnamese.
