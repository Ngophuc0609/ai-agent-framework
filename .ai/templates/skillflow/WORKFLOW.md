# <Workflow Name>

## Vietnamese User Summary

<Mô tả ngắn bằng tiếng Việt để người dùng hiểu workflow này làm gì.>

## Purpose

<Describe what this workflow does.>

## Trigger

Registered in:

- `.ai/registry/triggers.yml`

## Required Files

- `.ai/README.md`
- `.ai/registry/skills.yml`
- `.ai/registry/workflows.yml`
- `.ai/registry/triggers.yml`
- `.ai/rules/00-global-rules.md`
- `.ai/rules/06-quality-gates.md`

If the workflow reads source code, also read:

- `.ai/rules/10-codegraph-first-rules.md`
- `.ai/rules/12-memory-policy-rules.md`

## Allowed Write Paths

- `.ai/runs/<skillflow_id>/<run_id>/`
- <Add public output paths here.>

## Execution

1. Resolve skill and workflow through the registry.
2. Create the run folder.
3. Run required preflight checks.
4. Retrieve memory when project knowledge is involved.
5. Execute agents or sequential fallback.
6. Validate outputs.
7. Store confirmed memory findings when available.
8. Respond to the user in Vietnamese.

## Fallbacks

If required tooling is unavailable:

1. Record the limitation.
2. Use only approved fallback tools.
3. Ask the user before continuing when correctness is materially reduced.

## Quality Gates

- [ ] Required rules were applied.
- [ ] Allowed paths were respected.
- [ ] Evidence exists or inference is labeled.
- [ ] Secrets are not exposed.
- [ ] Memory behavior is logged.
- [ ] Limitations are documented.

## Final Response

Summarize output files, status, validation, conflicts, and open questions in Vietnamese.
