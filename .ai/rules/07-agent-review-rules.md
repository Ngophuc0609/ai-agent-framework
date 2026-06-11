# 07 Agent Review Rules

## Vietnamese User Summary

Rule này hướng dẫn agent reviewer kiểm tra lại kết quả của các agent khác.

## Review Stance

The reviewer must prioritize:

- Incorrect claims.
- Missing evidence.
- Cross-file inconsistencies.
- Security risks.
- Missing tests or validation.
- Unclear ownership or unresolved open questions.

## Review Method

1. Read the workflow and assigned outputs.
2. Check whether each agent stayed within scope.
3. Compare claims against source evidence.
4. Check handoff questions and conflicts.
5. Assign readiness.
6. Write a concise review summary.

## Findings Format

For each issue, include:

- Severity.
- File path and line when available.
- Claim or behavior under review.
- Evidence.
- Recommended correction.

## Reviewer Boundaries

- Do not silently rewrite another agent's findings unless the workflow assigns synthesis to the reviewer.
- Do not fabricate missing evidence.
- Do not downgrade security concerns without evidence.
- Do not mark `Ready` when critical checks were skipped.
