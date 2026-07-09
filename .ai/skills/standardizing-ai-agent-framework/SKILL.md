---
name: standardizing-ai-agent-framework
description: Use when auditing, designing, or updating the shared .ai framework, native agent adapters, Agent Skills, rule files, workflow registries, or cross-agent bootstrap behavior for Codex, Claude, Cline, Copilot, Cursor, Antigravity, or other coding agents
---

# Standardizing AI Agent Framework

## Vietnamese User Summary

Skill này dùng để chuẩn hóa bộ `.ai`, rule, skill, workflow và adapter native cho nhiều AI coding agent.

## Required Rules

- `.ai/rules/00-global-rules.md`
- `.ai/rules/05-workflow-execution-rules.md`
- `.ai/rules/06-quality-gates.md`
- `.ai/rules/10-codegraph-first-rules.md`
- `.ai/rules/11-skillflow-extension-rules.md`
- `.ai/rules/12-memory-policy-rules.md`
- `.ai/rules/13-efficiency-cost-policy-rules.md`

## Vendor And Canonical Baseline

Prefer official vendor documentation before changing adapter behavior. When the user provides current vendor/runtime notes for a runtime that is not publicly documented, treat those notes as local canonical source and record the assumption.

- Codex: `AGENTS.md`, `.agents/skills`, `.codex/config.toml`, `.codex/agents`.
- Claude Code: `CLAUDE.md`, `.claude/CLAUDE.md`, `.claude/rules`, `.claude/skills`.
- Cline: `.clinerules`, `.cline/skills`, Agent Skills compatible `SKILL.md`.
- GitHub Copilot: `.github/copilot-instructions.md`, `.github/instructions/*.instructions.md`, `.github/skills`.
- Cursor: `.cursor/rules/*.mdc`; `AGENTS.md` and `.agents/skills` are portable fallbacks unless the runtime explicitly documents them for the selected mode.
- Antigravity latest CLI (`agy`): `GEMINI.md` for workspace instructions and `.agents/skills/<skill>/SKILL.md` for project-scoped native skills. `.agent/rules` and `.agents/AGENTS.md` remain fallback-only unless the selected sync profile explicitly requests them.

When official docs are unavailable or incomplete and no user-provided canonical runtime note exists, label the mapping as a portable fallback instead of a verified native format.

## Workflow

1. Inspect the current `.ai` registry, rules, skills, workflows, adapters, and sync scripts.
2. Verify the relevant official agent documentation or local canonical notes.
3. Identify the canonical `.ai` source files and the generated native outputs.
4. Apply `.ai/rules/17-agent-targeted-sync-rules.md` before changing sync behavior.
5. Keep always-on native instructions compact.
6. Materialize full bundles only as secondary/deep-reference files.
7. Materialize Agent Skills only into verified native skill directories by default.
8. Generate portable fallback surfaces only when the sync profile explicitly requests them.
9. Add or update registry entries and triggers when a new skill/workflow is introduced.
10. Validate generated files in a temporary target repository.
11. Report source docs, changed files, validation, and any mappings that are fallback-only.

## Guardrails

- Do not duplicate `.ai` content manually across native files; update the generator instead.
- Do not overwrite user-authored native rule files unless the sync command receives an explicit force option.
- Do not put large rule bundles into always-on files when the agent supports scoped or on-demand rules.
- Do not generate multiple equivalent entrypoints for one selected agent by default.
- Do not treat portable fallback directories as verified native surfaces.
- Preserve skill frontmatter exactly enough for Agent Skills parsers to recognize `name` and `description`.
- Keep generated files marked with `generated-by: ai-agent-adapter-sync`.

## Quality Gates

- [ ] Every registered skill path exists.
- [ ] Every registered workflow path exists.
- [ ] Every trigger references an existing skill and workflow when non-null.
- [ ] Native generated files are reproducible from `.ai`.
- [ ] Native skills are generated in the documented target directories.
- [ ] Official-source gaps are labeled as fallbacks.


## Memory Policy & Source of Truth

Current repository source, configuration, migrations, CI/CD, and verified runtime output are authoritative. Project memory and existing documentation are supplementary context only. Any memory-derived claim that is not verified against current source must be marked `[UNVERIFIED]`.

## Secret Safety

Never copy secret values (connection strings, JWT signing keys, OAuth secrets, API keys, passwords) into documentation, findings, memory, logs, status files, or chat output. Redact sensitive values while preserving variable names and setup requirements.

## Evidence Policy

All technical claims must be labeled as one of: `[CONFIRMED]`, `[INFERRED]`, `[UNVERIFIED]`, `[CONFLICT]`, `[NOT_APPLICABLE]`, or `[BLOCKED]`.

Each agent finding must include: inspected scope, evidence references, commands executed, findings, assumptions, open questions, risks, and completion state.

## Final Validation

Before publishing final docs or committing changes, run required-output validation, STATUS.md consistency validation, git diff --check, secret scan, markdown/link validation, and stack-appropriate build or test commands when environment permits.
