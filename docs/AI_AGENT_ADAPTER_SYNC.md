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

Check generated files and manifest checksums without writing:

```bash
ai-agent-adapter-sync --check
```

Generate a full embedded bundle only for a restricted runtime that cannot read repository files:

```bash
ai-agent-adapter-sync --materialized
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
| Cross-tool / Codex | `.agents/00-ai-framework.manifest.json` |
| Cross-tool / Codex | `.agents/skills/<skill>/SKILL.md` |
| Cursor | `.cursor/rules/00-ai-framework.mdc` |
| Cursor | `.cursor/rules/00-ai-framework.manifest.json` |
| Cursor | `.agents/skills/<skill>/SKILL.md` |
| GitHub Copilot | `.github/copilot-instructions.md` |
| GitHub Copilot | `.github/instructions/ai-framework.instructions.md` |
| GitHub Copilot | `.github/instructions/00-ai-framework.manifest.json` |
| GitHub Copilot | `.github/skills/<skill>/SKILL.md` |
| Claude Code | `CLAUDE.md` |
| Claude Code | `.claude/rules/00-ai-framework.md` |
| Claude Code | `.claude/rules/00-ai-framework.manifest.json` |
| Claude Code | `.claude/skills/<skill>/SKILL.md` |
| Cline | `.clinerules/00-ai-framework.md` |
| Cline | `.clinerules/00-ai-framework.manifest.json` |
| Cline | `.cline/skills/<skill>/SKILL.md` |
| Google Antigravity | `GEMINI.md` |
| Google Antigravity | `.agent/rules/00-ai-framework.md` |
| Google Antigravity | `.agent/rules/00-ai-framework.manifest.json` |
| Google Antigravity / managed agent | `.agents/AGENTS.md` |
| Google Antigravity / portable skills | `.agents/skills/<skill>/SKILL.md` |

## Design

- `.ai/` remains the source of truth.
- Native files are generated, not hand-maintained.
- Pointer files define non-negotiable rules, progressive routing, a rule-loading matrix, runtime fallbacks, and the completion contract without copying framework sources.
- Default pointer output is guarded at 250 lines and 12000 bytes and must not contain `Materialized .ai Rule Bundle`.
- Each adapter manifest records framework version, generator version, mode, source commit, source paths, and SHA-256 checksums.
- `--check` reports missing, stale, or obsolete generated outputs without writing.
- `--materialized` embeds framework sources only for restricted runtimes that cannot read repository files.
- Native Agent Skills are generated from `.ai/skills/*/SKILL.md` into the target agent's skill directory.
- Existing user-authored files are not overwritten unless `--force` is passed.

## Runtime Tool Policy

Generated native instructions point to `.ai/rules/15-agent-runtime-tool-policy.md` instead of embedding it. The current source rule remains authoritative.

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

## Cline Source-Handover Failure Mode

If Cline reports that `.ai/workflows/make-new-dev-docs.md` is missing while file listing shows it exists, or if Cline times out on `.ai/scripts/init-source-code-handover-run.sh`, treat the run as blocked. Do not let Cline write generic fallback files such as `docs/onboarding.md`.

Common causes:

- The target repository has not synced the latest `.ai` framework and generated `.clinerules`.
- Cline workspace permissions or file filters prevent reliable access to hidden `.ai/` paths.
- The active model is too weak for tool-following and workflow execution, such as `nvidia/nemotron-3-nano-30b-a3b:free`.
- The model ignored fatal preflight gates after a tool timeout.

Recommended recovery in the target repository:

```bash
/home/pc1503/Desktop/Workspace/work/ai-agent-framework/bin/ai-agent-sync --source /home/pc1503/Desktop/Workspace/work/ai-agent-framework/.ai --generate-adapters --adapter-agent cline --no-tools .
```

Then run a Cline preflight:

```bash
pwd; test -f .ai/workflows/make-new-dev-docs.md; test -x .ai/scripts/init-source-code-handover-run.sh; rg --files .ai/workflows .ai/skills/source-code-handover .ai/rules | rg 'make-new-dev-docs|source-code-handover/SKILL|15-agent-runtime-tool-policy'
```

Use a BALANCED-equivalent or stronger model for the actual source-handover workflow. Free/nano models may summarize existing artifacts but must stop with `model-capability-blocked` for full documentation generation.

If a free OpenRouter/provider model returns `429`, respect `Retry-After`, retry once, then switch through the approved free fallback ladder in `.ai/rules/08-model-routing-rules.md`. If no approved model is available, stop as `BLOCKED_MODEL_RATE_LIMIT` and resume later from the existing `.ai/runs/source-code-handover/<run_id>/` artifacts.

## Recommended Sync Flow

From the target repository, generate adapters without installing tools:

```bash
ai-agent-adapter-sync
ai-agent-adapter-sync --check
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

Agent shortcuts sync `.ai` and generate pointer adapters. Tool installation is a separate explicit bootstrap/maintenance action and must follow runtime approval policy.

For Cline, the shortcut creates the officially discovered workspace locations:

- Rules: `.clinerules/00-ai-framework.md`
- Skills: `.cline/skills/<skill>/SKILL.md`

Cline discovers these files automatically. Because Skills is currently experimental, enable `Settings > Features > Enable Skills` in Cline when the Skills panel does not list them.

Skip native skills only when you intentionally want rule/instruction files without Agent Skills:

```bash
ai-agent-adapter-sync --no-skills
```

## Maintenance Rule

When `.ai/` rules, registry, bootstrap, or adapters change, rerun:

```bash
ai-agent-adapter-sync
ai-agent-adapter-sync --check
```

Do not edit generated native files by hand unless you intend to stop regenerating them.
