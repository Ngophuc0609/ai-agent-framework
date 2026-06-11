# <Agent Name>

## Vietnamese User Summary

<Mô tả ngắn bằng tiếng Việt để người dùng hiểu agent này phụ trách phần nào.>

## Role

<Describe the agent responsibility.>

## Inputs

- <Input file or source area.>

## Allowed Write Paths

- `.ai/runs/<skillflow_id>/<run_id>/findings/<agent-id>/`
- <Additional workflow-approved paths.>

## Required Rules

- `.ai/rules/00-global-rules.md`
- `.ai/rules/06-quality-gates.md`
- Add task-specific rules here.

## Execution

1. Retrieve relevant memory.
2. Inspect current source or assigned artifacts.
3. Compare memory with current evidence.
4. Produce findings with evidence paths.
5. Record uncertainty and open questions.
6. Store confirmed findings back to memory when available.

## Output Requirements

- Use English for findings and operational notes unless the workflow requires Vietnamese.
- Include evidence paths for important claims.
- Do not expose secrets.
- Do not write outside allowed paths.
- Do not modify source code unless explicitly assigned.

## Completion Checklist

- [ ] Inputs were reviewed.
- [ ] Evidence paths are included.
- [ ] Open questions are recorded.
- [ ] Memory behavior is logged.
- [ ] Allowed write paths were respected.
