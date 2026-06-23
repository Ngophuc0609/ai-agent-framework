---
name: standardizing-ai-agent-framework
description: Use when auditing, designing, or updating the shared .ai framework, native agent adapters, Agent Skills, rule files, workflow registries, or cross-agent bootstrap behavior for Codex, Claude, Cline, Copilot, Cursor, Antigravity, or other coding agents
---

<!-- generated-by: ai-agent-adapter-sync -->


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

## Official Baseline

Prefer official vendor documentation before changing adapter behavior:

- Codex: `AGENTS.md`, `.agents/skills`, `.codex/config.toml`, `.codex/agents`.
- Claude Code: `CLAUDE.md`, `.claude/CLAUDE.md`, `.claude/rules`, `.claude/skills`.
- Cline: `.clinerules`, `.cline/skills`, Agent Skills compatible `SKILL.md`.
- GitHub Copilot: `.github/copilot-instructions.md`, `.github/instructions/*.instructions.md`, `.github/skills`.
- Cursor: Cursor rules plus portable `AGENTS.md` and Agent Skills when supported by the runtime.
- Antigravity/Gemini-style agents: `GEMINI.md`, `.agent/rules`, portable `.agents/skills`.

When official docs are unavailable or incomplete, label the mapping as a portable fallback instead of a verified native format.

## Workflow

1. Inspect the current `.ai` registry, rules, skills, workflows, adapters, and sync scripts.
2. Verify the relevant official agent documentation or local canonical notes.
3. Identify the canonical `.ai` source files and the generated native outputs.
4. Keep always-on native instructions compact.
5. Materialize full bundles only as secondary/deep-reference files.
6. Materialize Agent Skills into native skill directories where the agent supports them.
7. Add or update registry entries and triggers when a new skill/workflow is introduced.
8. Validate generated files in a temporary target repository.
9. Report source docs, changed files, validation, and any mappings that are fallback-only.

## Guardrails

- Do not duplicate `.ai` content manually across native files; update the generator instead.
- Do not overwrite user-authored native rule files unless the sync command receives an explicit force option.
- Do not put large rule bundles into always-on files when the agent supports scoped or on-demand rules.
- Preserve skill frontmatter exactly enough for Agent Skills parsers to recognize `name` and `description`.
- Keep generated files marked with `generated-by: ai-agent-adapter-sync`.

## Quality Gates

- [ ] Every registered skill path exists.
- [ ] Every registered workflow path exists.
- [ ] Every trigger references an existing skill and workflow when non-null.
- [ ] Native generated files are reproducible from `.ai`.
- [ ] Native skills are generated in the documented target directories.
- [ ] Official-source gaps are labeled as fallbacks.
