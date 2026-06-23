# Standardizing AI Agent Framework

## Vietnamese User Summary

Workflow này phân tích và chuẩn hóa bộ `.ai` để dùng đồng nhất cho Codex, Claude, Cline, Copilot, Cursor, Antigravity và các agent tương thích.

## Purpose

Create a single-source `.ai` framework that can generate native instruction, rule, and Agent Skills structures for multiple AI coding agents without requiring a manual bootstrap prompt.

## Trigger

Registered in:

- `.ai/registry/triggers.yml`

## Required Files

- `.ai/README.md`
- `.ai/BOOTSTRAP_ONCE.md`
- `.ai/registry/skills.yml`
- `.ai/registry/workflows.yml`
- `.ai/registry/triggers.yml`
- `.ai/registry/adapters.yml`
- `.ai/registry/tool-bootstrap.json`
- `.ai/rules/00-global-rules.md`
- `.ai/rules/05-workflow-execution-rules.md`
- `.ai/rules/06-quality-gates.md`
- `.ai/rules/11-skillflow-extension-rules.md`
- `.ai/rules/12-memory-policy-rules.md`
- `bin/ai-agent-sync`
- `bin/ai-agent-adapter-sync`

## Allowed Write Paths

- `.ai/skills/`
- `.ai/workflows/`
- `.ai/registry/`
- `.ai/adapters/`
- `.ai/rules/`
- `bin/ai-agent-sync`
- `bin/ai-agent-adapter-sync`
- `docs/`

Generated native files should be validated in a temporary target repository unless the user explicitly asks to generate them in the current repository.

## Evidence Policy

All technical claims must be labeled as one of: `[CONFIRMED]`, `[INFERRED]`, `[UNVERIFIED]`, `[CONFLICT]`, `[NOT_APPLICABLE]`, or `[BLOCKED]`.

## Source of Truth

Current repository source, configuration, migrations, CI/CD, and verified runtime output are authoritative. Project memory and existing documentation are supplementary context only, not source of truth. Any memory-derived claim that is not verified against current source must be marked `[UNVERIFIED]`.

## Secret Safety

Never copy secret values into documentation, findings, memory, logs, status files, or chat output. Redact sensitive values while preserving variable names and setup requirements.

## Execution

1. Resolve the workflow from `.ai/registry/workflows.yml`. Expected key: `standardizing-ai-agent-framework`. If missing, record a blocking finding and continue in fallback mode.
2. Resolve the requested target agent set.
3. Inspect current `.ai` registry, rule, skill, workflow, and adapter structure.
4. Compare target behavior with official agent documentation.
5. Classify each target path as verified native format or portable fallback.
6. Update source `.ai` files, registry entries, and sync scripts.
7. Generate adapters in a temporary repository for at least one representative agent.
8. Run final validation (syntax, registry consistency, generated file placement, secret scan).
9. Respond in Vietnamese with changed files, official sources, validation, and fallback notes.

## Agent Output Matrix

| Agent | Always-on entry | Deep/reference rules | Native skills |
|---|---|---|---|
| Codex | `AGENTS.md` | `.ai/` source files | `.agents/skills/<skill>/SKILL.md` |
| Cline | `.clinerules/00-ai-framework.md` | `.ai/` source files | `.cline/skills/<skill>/SKILL.md` |
| GitHub Copilot | `.github/copilot-instructions.md` | `.github/instructions/ai-framework.instructions.md` | `.github/skills/<skill>/SKILL.md` |
| Claude Code | `CLAUDE.md` | `.claude/rules/00-ai-framework.md` | `.claude/skills/<skill>/SKILL.md` |
| Cursor | `.cursor/rules/00-ai-framework.mdc` | `.cursor/rules/99-ai-framework-bundle.mdc` | `.agents/skills/<skill>/SKILL.md` portable fallback |
| Antigravity | `GEMINI.md`, `.agents/AGENTS.md` | `.agent/rules/00-ai-framework.md` | `.agents/skills/<skill>/SKILL.md` portable fallback |

## Quality Gates

- [ ] Official docs or local canonical notes were consulted.
- [ ] Registry consistency was checked.
- [ ] `ai-agent-adapter-sync --dry-run` or temp-repo generation was exercised.
- [ ] `python3 -m py_compile` passed for changed Python scripts.
- [ ] Generated native skills preserve valid frontmatter.
- [ ] Fallback-only mappings are disclosed.
- [ ] No secrets were exposed.
