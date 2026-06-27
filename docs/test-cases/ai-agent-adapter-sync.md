# AI Agent Adapter Sync Test Cases

## Codex `AGENTS.md` ownership

| ID | Scenario | Expected result | Status |
|---|---|---|---|
| ADAPTER-CODEX-001 | Run adapter sync with no `--agent` filter | `AGENTS.md` is generated once with the Codex header | Implemented |
| ADAPTER-CODEX-002 | Run adapter sync with `--agent codex` | `AGENTS.md` uses the Codex header | Implemented |
| ADAPTER-AGENTS-001 | Run adapter sync with `--agent agents` | The portable alias remains available and uses the agents header | Implemented |

The default run must not schedule both `agents` and `codex`, because both targets own
the same `AGENTS.md` path and the first writer suppresses the second as a duplicate.

## Native rule scope

| ID | Scenario | Expected result | Status |
|---|---|---|---|
| ADAPTER-CURSOR-001 | Generate Cursor rules | Always-on rule uses `alwaysApply: true` without a glob; deep bundle is agent-selected by description | Implemented |
| ADAPTER-CLAUDE-001 | Generate Claude instructions | `CLAUDE.md` stays compact and the secondary pointer is scoped to framework files with `paths` | Implemented |
| ADAPTER-COPILOT-001 | Generate Copilot instructions | Repository instructions stay compact and the secondary pointer has a framework-only `applyTo` glob | Implemented |
| ADAPTER-SKILLS-001 | Generate Cursor, Claude, and Copilot skills | Skill is written to each native directory and retains valid `name` and `description` frontmatter | Implemented |

## Pointer-only adapters and drift detection

| ID | Scenario | Expected result | Status |
|---|---|---|---|
| ADAPTER-POINTER-001 | Generate any adapter in default mode | Every instruction is pointer-only, at most 250 lines and 12000 bytes, without a materialized bundle heading | Implemented |
| ADAPTER-POINTER-002 | Generate Cursor after a legacy generated bundle exists | The generated legacy `99-ai-framework-bundle.mdc` is removed safely | Implemented |
| ADAPTER-MANIFEST-001 | Generate an adapter | A colocated manifest records agent, pointer mode, framework/generator versions, source paths, source commit, and SHA-256 checksums | Implemented |
| ADAPTER-CHECK-001 | Run `--check` immediately after generation | Exit successfully without writing files | Implemented |
| ADAPTER-CHECK-002 | Change a checksummed `.ai` source after generation | Exit non-zero and report source/output drift | Implemented |
| ADAPTER-MATERIALIZED-001 | Generate with `--materialized` | Full source bundle remains available as an explicit compatibility mode | Implemented |

## Cline shortcut integration

| ID | Scenario | Expected result | Status |
|---|---|---|---|
| SYNC-CLINE-001 | Run `ai-agent-sync cline` in a repository | Sync `.ai`, generate `.clinerules/00-ai-framework.md`, manifest, and `.cline/skills/*/SKILL.md` without automatic tool installation | Implemented |
| SYNC-CLINE-002 | Complete Cline adapter generation | Print a concise discovery summary for the rule and skills directories | Implemented |
