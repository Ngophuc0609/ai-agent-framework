# 01 Documentation Skill Rules

## Summary

This rule describes how to trigger and control the source-code handover documentation workflow.

## Trigger Resolution

When the user asks for source-code handover documentation, onboarding documentation, or equivalent Vietnamese trigger phrases, resolve the request through `.ai/registry/triggers.yml` and run workflow `make-new-dev-docs`.

Do not run the full documentation workflow when the user only asks to edit rules, review docs, or discuss the framework.

## Required Inputs

Before generating documentation, read:

- `.ai/README.md`
- `.ai/registry/skills.yml`
- `.ai/registry/workflows.yml`
- `.ai/registry/triggers.yml`
- `.ai/rules/00-global-rules.md`
- `.ai/rules/10-codegraph-first-rules.md`
- `.ai/rules/12-memory-policy-rules.md`
- `.ai/rules/07-handover-documentation-dod.md`
- `.ai/rules/08-source-code-handover-quality-checklist.md`
- The selected skill and workflow files.

If a required file is missing, record the limitation and continue only with the safe subset of the workflow.

## Documentation Goals

The final documentation must help a new developer understand:

- What the system is.
- How to run it locally.
- Which files to read first.
- Runtime configuration and environment requirements.
- Main modules, APIs, database, auth, integrations, jobs, and deployment behavior when present.
- Debugging, logging, and smoke-test paths.
- Unknowns that require maintainer confirmation.

## Output Policy

The current legacy documentation workflow may write to:

- `draft-docs/`
- `docs/`
- `.ai/handoff/`

New skillflows must use isolated namespaces as defined in `.ai/rules/11-skillflow-extension-rules.md`.

The final chat response must summarize changed files, conflicts, open questions, and readiness. Do not paste full generated documentation into chat.

## Missing Areas

Each repository may omit database, frontend, background jobs, realtime features, or deployment config.

When an area is not detected:

1. Do not invent content.
2. State that it was not found in the current source.
3. Add an open question when the area is operationally important.
4. Complete all evidence-backed sections.
