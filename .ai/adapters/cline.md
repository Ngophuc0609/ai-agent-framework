# Cline Adapter

## Vietnamese User Summary

Adapter này mô tả cách dùng framework `.ai/` khi chạy bằng Cline.

## Runtime Instructions

- Resolve user intent through `.ai/registry/triggers.yml`.
- Read the selected `SKILL.md` before executing the workflow.
- Apply `.ai/rules/15-agent-runtime-tool-policy.md` before `execute_command`, file edits, browser actions, MCP calls, or delegated tool actions.
- Run CodeGraph preflight before source-code review.
- Keep all tool access scoped to the project folder.
- If an MCP server or tool is missing, record the limitation and ask the user before continuing with a weaker fallback.
- Respond to the user in Vietnamese.

## Cline Model Capability Gate

For `source-code-handover` or `make-new-dev-docs`, do not run the full workflow with low-capability, nano, free, or unknown instruction-following models. This includes `nvidia/nemotron-3-nano-30b-a3b:free`.

Those models may only run:

- framework preflight checks,
- file existence checks,
- run status summaries,
- summaries of already-created evidence.

They MUST NOT:

- create or publish `docs/` handover files,
- write `docs/onboarding.md` as a fallback,
- synthesize final documentation,
- mark any documentation `Ready`,
- bypass `.ai` because a file read or shell command failed.

If Cline is using a low-capability/free model and the user asks to create onboarding/source-handover docs, stop with `model-capability-blocked` and ask the user to switch to a stronger model or run the workflow with Codex/Claude/Gemini High-equivalent tooling.

## Cline Fatal Preflight Gate

Before creating any source-handover artifact, Cline MUST successfully read all of:

- `.ai/registry/triggers.yml`
- `.ai/skills/source-code-handover/SKILL.md`
- `.ai/workflows/make-new-dev-docs.md`
- `.ai/rules/15-agent-runtime-tool-policy.md`

If any required file cannot be read, Cline MUST STOP. It may report the blocked state in chat. If `.ai/runs/` is writable, it may write only a blocked report under `.ai/runs/source-code-handover/<run_id>/validation/blocked-report.md`. It MUST NOT write to `docs/`.

## Cline Tool-Call Safety

Cline's `execute_command` tool requires BOTH fields every time:

- `command`: the exact shell command string.
- `requires_approval`: `false` for safe local read/setup commands, `true` for destructive, network, deploy, install, or credential-sensitive commands.

When using Cline, never emit an `execute_command` call with an empty/missing `command` or missing `requires_approval`. If Cline reports a malformed tool-call error, stop retrying the same step after one retry, write the limitation in the run artifact, and ask the user for confirmation or switch to a file-write/manual artifact fallback.

Safe local commands that may use `requires_approval: false`:

```text
ls
pwd
rg
find with bounded paths and -maxdepth
git status
git rev-parse
mkdir -p inside .ai/runs
python3 .ai/scripts/*.py validation commands
```

Avoid unbounded commands that may hang in Cline, such as `find .` without `-maxdepth` or broad recursive scans over vendor/build folders. Prefer `rg --files`, bounded `find <path> -maxdepth N`, or project-specific source roots.

## Source-Code Handover Run Init

For `source-code-handover` or `make-new-dev-docs`, Cline should initialize the run with one safe script command instead of manually composing multiple `mkdir` commands:

```bash
RUN_ID="run-$(date +%Y%m%d-%H%M%S)"; ./.ai/scripts/init-source-code-handover-run.sh "$RUN_ID"
```

Cline `execute_command` shape:

```xml
<execute_command>
  <command>RUN_ID="run-$(date +%Y%m%d-%H%M%S)"; ./.ai/scripts/init-source-code-handover-run.sh "$RUN_ID"</command>
  <requires_approval>false</requires_approval>
</execute_command>
```

After this command, continue by filling the created Phase 0 inventory, evidence, findings, verification, drafting, final, validation, and publish artifacts. Do not create `.ai/runs/source-code-handover/` through repeated ad hoc shell commands.

If Cline command execution is unreliable, first run a bounded preflight command:

```bash
pwd; test -f .ai/workflows/make-new-dev-docs.md; test -x .ai/scripts/init-source-code-handover-run.sh; rg --files .ai/workflows .ai/skills/source-code-handover .ai/rules | rg 'make-new-dev-docs|source-code-handover/SKILL|15-agent-runtime-tool-policy'
```

If this command times out or fails, stop and report the Cline tool limitation. Do not create fallback docs.
