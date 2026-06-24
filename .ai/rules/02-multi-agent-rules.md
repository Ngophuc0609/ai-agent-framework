# 02 Multi-Agent Rules

## Summary

This rule standardizes how work is divided across multiple agents for documentation or source review.

## Coordination

- Use the workflow file as the source of truth for agent order, responsibilities, and output paths.
- Each agent must write only to its assigned files.
- Each agent must include evidence paths for important findings.
- Agents must write open questions instead of guessing.
- The coordinator/reviewer is responsible for consistency, conflicts, readiness, and final synthesis.

## Execution Contract

When a workflow lists required agents, the runtime must not skip directly to the final output.

Required behavior:

1. Execute every listed agent unless the workflow explicitly marks it optional or not applicable.
2. Prefer real delegated/sub-agent execution only when the current AI runtime supports it and the user explicitly requested multi-agent, delegated, or parallel agent work.
3. If real delegated agents are unavailable, run the same agent specs sequentially as a fallback.
4. Preserve each agent boundary even in sequential fallback.
5. Write or update the required output file for each agent.
6. Record the execution mode in handoff status:
   - `delegated-parallel`
   - `delegated-sequential`
   - `single-runtime-sequential-fallback`
7. Do not generate the final handbook until Agent 1-5 outputs and Agent 6 review exist, or the missing outputs are explicitly marked not applicable with a reason.

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
- The execution mode is recorded.
- Open questions are listed.
- Conflicts are resolved or documented.
- Readiness is assigned.
- Final response summarizes status in Vietnamese.
