# AI Agent Framework Standardization

## Vietnamese User Summary

Tài liệu này là baseline để chuẩn hóa `.ai` thành một nguồn sự thật duy nhất, rồi sinh ra cấu trúc native cho từng agent như Codex, Claude, Cline, Copilot, Cursor và Antigravity.

## Official Baseline

| Area | Official source used | Local mapping |
|---|---|---|
| Codex instructions | OpenAI Codex manual: `AGENTS.md`, Agent Skills, MCP, memories, subagents | `AGENTS.md`, `.agents/skills`, `.codex/config.toml` guidance |
| Agent Skills standard | Agent Skills specification and VS Code Agent Skills docs | `SKILL.md` plus optional `scripts/`, `references/`, `assets/` |
| Cline rules and skills | Cline customization docs for Cline Rules and Skills | `.clinerules/00-ai-framework.md`, `.cline/skills/<skill>/SKILL.md` |
| GitHub Copilot instructions and skills | GitHub Copilot repository instructions and skills docs | `.github/copilot-instructions.md`, `.github/instructions/*.instructions.md`, `.github/skills` |
| Claude Code memory/rules | Claude Code memory docs | `CLAUDE.md`, `.claude/skills`; `.claude/rules` only when deep rules are requested |
| Cursor rules | Cursor rules docs | `.cursor/rules/*.mdc`; `.agents/skills` only as portable/legacy fallback |
| Antigravity latest CLI (`agy`) | Current Antigravity runtime note supplied for this framework | `GEMINI.md`, `.agents/skills`; `.agent/rules` and `.agents/AGENTS.md` only as portable/legacy fallback |

## Current Structure Assessment

- `.ai/registry/` is the source of truth for skills, workflows, triggers, adapters, and tool bootstrap.
- `.ai/rules/` contains durable framework rules and should stay canonical.
- `.ai/skills/<skill>/SKILL.md` already matches the Agent Skills directory pattern for most skills.
- `bin/ai-agent-sync` handles the one-command bootstrap flow and agent shortcuts.
- `bin/ai-agent-adapter-sync` generates compact native pointer instructions, checksum manifests, and native Agent Skills.

## Standardization Rules

- Keep `.ai/` as the only hand-maintained source.
- Keep always-on native files compact because they consume prompt context.
- Keep pointer adapters under 250 lines and 12000 bytes; do not copy registry/rule sources into default outputs.
- Reserve full materialization for explicit `--materialized` compatibility mode.
- Detect drift with generated manifests and `--check`.
- Generate native skill directories from `.ai/skills/*/SKILL.md` only for verified native skill surfaces in the default `isolated` profile.
- Mark generated files with `generated-by: ai-agent-adapter-sync`.
- Skip existing user-authored native files unless `--force` is provided.
- Treat `.agents/skills` as portable fallback for Cursor but native project skills for Antigravity and Codex/generic Agent Skills.
- Use `--adapter-profile portable` or `--adapter-profile legacy-all` only when the target repo intentionally supports fallback/multi-host loading.

## Native Output Matrix

| Agent | Command | Generated instructions | Generated skills |
|---|---|---|---|
| Codex | `ai-agent-sync codex` | `AGENTS.md` | `.agents/skills/<skill>/SKILL.md` |
| Cline | `ai-agent-sync cline` | `.clinerules/00-ai-framework.md` | `.cline/skills/<skill>/SKILL.md` |
| Copilot | `ai-agent-sync copilot` | `.github/copilot-instructions.md`, `.github/instructions/ai-framework.instructions.md` | `.github/skills/<skill>/SKILL.md` |
| Claude | `ai-agent-sync claude` | `CLAUDE.md`, `.claude/00-ai-framework.manifest.json` | `.claude/skills/<skill>/SKILL.md` |
| Cursor | `ai-agent-sync cursor` | `.cursor/rules/00-ai-framework.mdc`, `.cursor/rules/00-ai-framework.manifest.json` | None by default |
| Antigravity | `ai-agent-sync agy` | `GEMINI.md`, `GEMINI.ai-framework.manifest.json` | `.agents/skills/<skill>/SKILL.md` |

## Maintenance Flow

1. Update `.ai` source files, never generated native files.
2. Run `python3 -m py_compile bin/ai-agent-sync bin/ai-agent-adapter-sync`.
3. Validate registries and skill frontmatter.
4. Test `ai-agent-sync <agent> --no-tools` in a temporary repository.
5. Commit `.ai`, `bin/`, and `docs/` changes together.

## Known Fallbacks

- Cursor portable skills require `--adapter-profile portable` or `legacy-all`; default isolated sync does not generate `.agents/skills` for Cursor.
- Antigravity project skills are generated under `.agents/skills` by default. `.agent/rules` and `.agents/AGENTS.md` remain opt-in fallback rule surfaces.
