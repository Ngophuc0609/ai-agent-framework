# 00 Global Rules

## Summary

This rule defines the baseline for `.ai`: use registries for skill/workflow selection, use English for agent-facing instructions, and use Vietnamese only for final chat responses to the Vietnamese-speaking user unless another language is requested.

## Language Policy

- Write all machine-facing rules, workflows, skill bodies, agent specs, templates, and operational notes in English.
- Vietnamese is allowed only in user-facing chat responses, explicit Vietnamese trigger aliases, or final developer-facing deliverables that explicitly require Vietnamese.
- Final chat responses to the user must be in Vietnamese unless the user requests another language.
- Do not mix Vietnamese into execution instructions.

## Registry First

- Read `.ai/registry/triggers.yml` before choosing a workflow.
- Read `.ai/registry/skills.yml` before loading a skill.
- Read `.ai/registry/workflows.yml` before loading a workflow.
- Do not hard-code trigger phrases in isolated rule files.

## Skill First

- If a request matches a registered skill, read that skill's `SKILL.md` before taking action.
- If the skill declares required background or a required supporting skill, read it before execution.
- Keep loaded context minimal; load references only when needed.
- Use `.ai/skills/routing-ai-task/SKILL.md` for skill selection when the request could match multiple skills or when no specialized skill is obvious.

## CodeGraph First

Before any source-code review, source-code documentation, debugging, refactor planning, or API implementation:

1. Check whether CodeGraph is available for the current project.
2. If unavailable, try the approved local setup command from `.ai/rules/10-codegraph-first-rules.md`.
3. If setup fails, stop and ask the user whether to continue without CodeGraph or use another tool.
4. Record any fallback in the run status and final response.

## Memory First

Before editing or documenting a module:

1. Retrieve memory for the current project namespace and target module.
2. Scan current source code.
3. Compare memory with source code.
4. Trust source code when memory conflicts with code.
5. Write or update the deliverable.
6. Store only verified, durable findings back to memory.

Never store secrets, tokens, passwords, private keys, temporary logs, unverified guesses, large raw source code, or full stack traces in memory.

## Evidence

- Every important claim must cite file paths, commands, tests, or observed runtime evidence.
- If a conclusion is inferred, label it as inference.
- If evidence is missing, mark the item as uncertain and add an open question.

## Efficiency

- Follow `.ai/rules/13-efficiency-cost-policy-rules.md`.
- Do not read the whole repository unless the task explicitly requires it.
- Use memory and project summary docs before detailed source reads.
- Use small or cheap models for discovery, classification, summarization, formatting, and checklist generation.
- Use strong models only for difficult reasoning, debugging, architecture, security, or multi-file refactoring.

## Write Scope

- Keep writes inside the project folder.
- Prefer run-scoped output under `.ai/runs/<skillflow_id>/<run_id>/`.
- Write public deliverables only to paths explicitly allowed by the selected workflow.
- Do not modify unrelated skillflows, rules, agents, or docs unless the user requests it.

## Safety

- Do not expose secrets in memory, docs, handoff files, vector stores, or chat responses.
- Mask secrets when referencing their existence.
- Do not grant filesystem access outside the active project folder.
- Do not run destructive commands unless explicitly requested and confirmed.
