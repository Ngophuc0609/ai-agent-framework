# Cline Adapter

## Vietnamese User Summary

Adapter này mô tả cách dùng framework `.ai/` khi chạy bằng Cline.

## Runtime Instructions

- Resolve user intent through `.ai/registry/triggers.yml`.
- Read the selected `SKILL.md` before executing the workflow.
- Run CodeGraph preflight before source-code review.
- Keep all tool access scoped to the project folder.
- If an MCP server or tool is missing, record the limitation and ask the user before continuing with a weaker fallback.
- Respond to the user in Vietnamese.

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
