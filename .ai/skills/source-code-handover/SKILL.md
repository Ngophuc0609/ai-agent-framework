---
name: source-code-handover
description: Use when creating source-code handover documentation, onboarding documentation for new developers, architecture summaries, repository maps, setup guides, API/database/auth documentation, or final project handbooks from source code
---

# Source Code Handover

## Required Background

Read `.ai/skills/using-superpowers/SKILL.md` and `.ai/workflows/make-new-dev-docs.md`.

## Goal

Create Vietnamese documentation that helps a new developer understand and work on the current system. The output is not an audit report and must not teach the project-analysis process.

## Internal Versus Published Content

Internal run artifacts may contain evidence IDs, discovery gaps, risks, conflicts, open questions, limitations, coverage, readiness, and tool failures.

Published documents must contain only verified current-system knowledge:

- system purpose and boundaries,
- repository and module map,
- local setup and commands,
- architecture and runtime flows,
- business behavior and data movement,
- database, auth, API, job, realtime, and integration details,
- frontend, operations, deployment, and testing guidance,
- common modification and debugging entry points.

Do not publish risk registers, open questions, limitations, readiness matrices, evidence indexes, coverage reports, claim labels, or agent/validator details.

## Evidence Workflow

1. Phase 0 creates deterministic inventories from physical files.
2. Agents 1-5 discover repository, database/auth, API, business/frontend, and operations domains.
3. Agent 6 verifies source and symbols.
4. Agent 7 verifies cross-layer flows and consistency.
5. Agent 8 verifies build, test, runtime, operations, and secret safety.
6. Agent 9 writes exactly 20 developer documents from verified facts.
7. Agent 10 validates source accuracy and developer usability before publish.

Unknown or conflicting information stays internal. Agent 9 omits it rather than adding uncertainty commentary to developer docs.

## Required Final Set

Use the 20 filenames and content requirements from `.ai/rules/08-source-code-handover-quality-checklist.md`. Documents `01` through `16` are topic-focused; documents `17` through `20` centralize mapping and audit references.

## Quality Requirements

- Explain behavior, not only component names.
- Trace important flows from entry point through services to data stores/external effects.
- Use exact source paths, symbols, routes, config keys, tables, commands, and verified examples.
- Include working directory, prerequisites, expected result, and smoke check for commands.
- Provide diagrams for non-trivial architecture and behavior flows.
- Explain where developers commonly make changes and how to verify them.
- Keep secrets redacted.
- Write final prose in Vietnamese.

## Required Rules And Templates

- `.ai/rules/07-handover-documentation-dod.md`
- `.ai/rules/08-source-code-handover-quality-checklist.md`
- `.ai/rules/10-codegraph-first-rules.md`
- `.ai/rules/12-memory-policy-rules.md`
- `.ai/rules/15-agent-runtime-tool-policy.md`
- `.ai/templates/source-code-handover/agent-findings-template.md`
- `.ai/templates/source-code-handover/evidence-store-template.md`
- `.ai/templates/source-code-handover/final-document-template.md`

## Publish Gate

Publish only when Agent 10 writes a structured `Verdict: PASS` and `.ai/scripts/validate-source-code-handover-run.sh <run_id>` succeeds.
