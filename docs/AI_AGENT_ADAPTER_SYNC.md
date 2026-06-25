# Generate Native Agent Instructions

## Vietnamese User Summary

Lệnh `ai-agent-adapter-sync` dùng `.ai/` làm nguồn chuẩn rồi sinh các file rule/instruction và Agent Skills đúng cấu trúc riêng của từng agent như Codex, Cursor, Copilot, Claude, Cline và Antigravity.

## Usage

From a target repository that already has `.ai/`:

```bash
ai-agent-adapter-sync
```

If the command is not in `PATH`, run from the framework repository or synced target repository:

```bash
bin/ai-agent-adapter-sync
```

Preview without writing:

```bash
ai-agent-adapter-sync --dry-run
```

Generate only one or more agent targets:

```bash
ai-agent-adapter-sync --agent cline --agent cursor
```

Overwrite non-generated files only when you intentionally want to replace user-authored instructions:

```bash
ai-agent-adapter-sync --force
```

## Generated Files

| Agent | Generated path |
|---|---|
| Cross-tool / Codex | `AGENTS.md` |
| Cross-tool / Codex | `.agents/skills/<skill>/SKILL.md` |
| Cursor | `.cursor/rules/00-ai-framework.mdc` |
| Cursor | `.cursor/rules/99-ai-framework-bundle.mdc` |
| Cursor | `.agents/skills/<skill>/SKILL.md` |
| GitHub Copilot | `.github/copilot-instructions.md` |
| GitHub Copilot | `.github/instructions/ai-framework.instructions.md` |
| GitHub Copilot | `.github/skills/<skill>/SKILL.md` |
| Claude Code | `CLAUDE.md` |
| Claude Code | `.claude/rules/00-ai-framework.md` |
| Claude Code | `.claude/skills/<skill>/SKILL.md` |
| Cline | `.clinerules/00-ai-framework.md` |
| Cline | `.cline/skills/<skill>/SKILL.md` |
| Google Antigravity | `GEMINI.md` |
| Google Antigravity | `.agent/rules/00-ai-framework.md` |
| Google Antigravity / managed agent | `.agents/AGENTS.md` |
| Google Antigravity / portable skills | `.agents/skills/<skill>/SKILL.md` |

## Design

- `.ai/` remains the source of truth.
- Native files are generated, not hand-maintained.
- Compact entry files tell each agent how to initialize tools, route through `.ai/registry/`, and apply core rules.
- Bundle files materialize `.ai/README.md`, `.ai/BOOTSTRAP_ONCE.md`, `.ai/registry/*`, `.ai/rules/*`, and the matching adapter file so rule systems that prefer native files can load the framework without a manual bootstrap prompt.
- Native Agent Skills are generated from `.ai/skills/*/SKILL.md` into the target agent's skill directory.
- Existing user-authored files are not overwritten unless `--force` is passed.

## Runtime Tool Policy

All generated native instructions include `.ai/rules/15-agent-runtime-tool-policy.md`. This rule prevents the class of failures where an agent emits malformed tool calls, repeats the same failed call, scans the whole repository without bounds, or writes source-code handover docs from model context instead of physical evidence.

Adapter-specific optimization profiles are maintained in `.ai/adapters/*.md`:

| Adapter | Optimization focus |
|---|---|
| Codex | Deterministic shell validation, source edits, git diff review, commit/push delivery, sequential fallback for required agents. |
| Cline | Strict `execute_command` schema, bounded commands, source-code-handover run initialization with one safe script call. |
| Cursor | Workspace navigation, scoped Composer/Agent edits, symbol search, portable `.agents/skills` fallback. |
| Claude | Deep reasoning, cross-layer synthesis, critique, sub-agent use only when the runtime exposes it. |
| GitHub Copilot | PR/code review, CI/GitHub evidence, small scoped edits, no unverified build/test claims. |
| Antigravity | Gemini-only model routing for source handover, cost-aware discovery, evidence-first multi-agent documentation. |

Optional tool candidates for deeper workflows live in `.ai/registry/tool-candidates.json`. Keep mandatory bootstrap tools in `.ai/registry/tool-bootstrap.json`; do not auto-install cloud or production-facing tools by default.

## Recommended Sync Flow

From the target repository:

```bash
ai-agent-sync --install-tools --yes
ai-agent-adapter-sync
```

Or use the integrated one-command flow:

```bash
ai-agent-sync --install-tools --yes --generate-adapters
```

For one agent in the current repository, use the shortcut form:

```bash
ai-agent-sync cline
ai-agent-sync codex
ai-agent-sync cursor
ai-agent-sync copilot
ai-agent-sync claude
ai-agent-sync agy
```

This first syncs and initializes `.ai`, MCP Memory, MCP Filesystem, MCP Git, and CodeGraph when available, then generates the native instruction structures for each agent.

Skip native skills only when you intentionally want rule/instruction files without Agent Skills:

```bash
ai-agent-adapter-sync --no-skills
```

## Maintenance Rule

When `.ai/` rules, registry, bootstrap, or adapters change, rerun:

```bash
ai-agent-adapter-sync
```

Do not edit generated native files by hand unless you intend to stop regenerating them.
