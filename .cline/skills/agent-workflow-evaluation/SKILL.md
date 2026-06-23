---
name: agent-workflow-evaluation
description: Use when designing, running, or reviewing evaluations for AI agent skills, workflows, routing behavior, prompt changes, regression suites, expected outputs, pass-fail criteria, or benchmark tasks
---

<!-- generated-by: ai-agent-adapter-sync -->


# Agent Workflow Evaluation

## Vietnamese User Summary

Skill này tạo hoặc review eval cho skill/workflow agent: bộ case, expected output, pass/fail criteria, regression và benchmark routing.

## REQUIRED BACKGROUND

Read `.ai/skills/using-superpowers/SKILL.md` before using this skill when available.

## Required Rules

- `.ai/rules/00-global-rules.md`
- `.ai/rules/06-quality-gates.md`
- `.ai/rules/11-skillflow-extension-rules.md`
- `.ai/rules/13-efficiency-cost-policy-rules.md`

## Workflow

1. Define the skill, workflow, routing rule, prompt, or behavior being evaluated.
2. Collect representative prompts, edge cases, negative cases, and previous failure cases.
3. Define expected behavior, forbidden behavior, evidence requirements, and pass/fail criteria.
4. Separate deterministic checks from judgment-based checks.
5. Create a small regression suite before expanding coverage.
6. Run or simulate evaluations when tooling exists; otherwise produce an executable manual eval plan.
7. Summarize failures, likely root causes, and recommended skill or trigger changes.
8. Respond to the user in Vietnamese with coverage, results, and next eval gaps.

## Guardrails

- Do not tune the skill only to pass a single narrow example.
- Do not include secrets or production-only data in eval cases.
- Do not hide ambiguous expected behavior; mark it as `Need decide`.
- Keep eval artifacts scoped to the target skillflow namespace.

## Quality Gates

- [ ] Positive, negative, and edge cases are included.
- [ ] Pass/fail criteria are explicit.
- [ ] Routing and safety failures are tested when relevant.
- [ ] Results separate evidence from judgment.
- [ ] Follow-up changes are traceable to failed cases.
