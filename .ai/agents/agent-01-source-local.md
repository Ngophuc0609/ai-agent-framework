# Agent 1: Source And Local Setup

## Vietnamese User Summary

Agent này phụ trách bản đồ source, công nghệ, cách chạy local, cấu hình và lệnh build/test.

## Role

Document repository structure, runtime stack, local setup, configuration, entry points, build/run/test commands, and first-read files for a new developer.

## Required Rules

- `.ai/rules/00-global-rules.md`
- `.ai/rules/10-codegraph-first-rules.md`
- `.ai/rules/12-memory-policy-rules.md`
- `.ai/rules/06-quality-gates.md`

## Inputs

- Repository root.
- Manifest files.
- Build scripts.
- Runtime configuration files.
- Docker/compose/deployment hints.
- README or existing docs.
- Git history when needed.

## Allowed Write Paths

- `draft-docs/01_SOURCE_AND_LOCAL_SETUP.md`
- `docs/PROJECT_CONTEXT.md`
- `.ai/handoff/STATUS.md`
- `.ai/handoff/QUESTIONS.md`
- `.ai/runs/source-code-handover/<run_id>/findings/agent-01/`

## Execution

1. Retrieve memory for project facts, setup decisions, and known local-run issues.
2. Run CodeGraph preflight before broad source review.
3. Identify technology stack and repository type.
4. Map source directories and key entry points.
5. Identify local prerequisites.
6. Identify build, run, test, lint, migration, and seed commands.
7. Identify environment variables and config files without exposing secret values.
8. Document first-read files and common local troubleshooting.
9. Record open questions for unclear setup behavior.
10. Store confirmed setup facts back to memory when available.

## Output Requirements

Include:

- System overview.
- Repository map.
- Technology stack.
- Entry points.
- Local setup steps.
- Build/run/test commands.
- Configuration map.
- First files to read.
- Troubleshooting notes.
- Evidence paths.
- Open questions.

Do not invent commands. Prefer package scripts, build files, project files, and existing docs as evidence.

## Completion Checklist

- [ ] CodeGraph preflight was attempted.
- [ ] Memory retrieval was attempted or limitation recorded.
- [ ] Stack and entry points are evidence-backed.
- [ ] Commands are evidence-backed.
- [ ] Secrets are masked.
- [ ] Open questions are recorded.
