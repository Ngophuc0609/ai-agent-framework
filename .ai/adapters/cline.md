# Cline Adapter

## Vietnamese User Summary

Adapter này mô tả cách dùng framework `.ai/` khi chạy bằng Cline.

## Runtime Instructions

- Resolve user intent through `.ai/registry/triggers.yml`.
- Read the selected `SKILL.md` before executing the workflow.
- Apply `.ai/rules/15-agent-runtime-tool-policy.md` before `execute_command`, file edits, browser actions, MCP calls, or delegated tool actions.
- Apply the risk-based CodeGraph matrix from `.ai/rules/10-codegraph-first-rules.md`; localized work may continue with a documented fallback.
- Keep all tool access scoped to the project folder.
- If an MCP server or tool is missing, record the limitation and use the selected workflow's approved fallback; block only when required evidence cannot be produced.
- Respond to the user in Vietnamese.

## Cline Model Capability Gate

For `source-code-handover` or `make-new-dev-docs`, do not run the full workflow with low-capability, nano, random-router, non-generative, safety-only, embedding-only, rerank-only, or unproven instruction-following models. Do not hard-code exact free model names as required or forbidden in Cline rules; route by observed capability and phase risk.

Free pricing alone is not a blocker. Any free or paid model may be used when it meets the required capability class and Cline can reliably read `.ai/`, run required tools, and preserve evidence.

If Cline receives an OpenRouter/provider `429` for a free model, it MUST follow `.ai/rules/08-model-routing-rules.md` rate-limit fallback:

- wait for `Retry-After` when short,
- retry once,
- switch to another model in the same or stronger capability class,
- record the limitation,
- stop as `BLOCKED_MODEL_RATE_LIMIT` if no approved model is available.

Cline MUST NOT recover from a free-model rate limit by switching to `OpenRouter Free Models Router`, embedding/rerank/safety models, nano models, or by writing generic docs.

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

If Cline is using a blocked low-capability or tool-unreliable model/runtime and the user asks to create onboarding/source-handover docs, stop with `BLOCKED_MODEL_CAPABILITY` and ask the user to switch to a stronger model or run the workflow with Codex/Claude/Gemini High-equivalent tooling.

Cline MUST NOT respond with a humorous refusal, non-technical excuse, or suggestion that the user should write the docs manually. If blocked, use this exact shape:

```text
BLOCKED_MODEL_CAPABILITY
Workflow: source-code-handover / make-new-dev-docs
Requested model: <model name>
Reason: <capability/routing/tool limitation>
Required action: switch to an approved BALANCED/REASONING_STRONG/LONG_CONTEXT_STRONG model or run with Codex/Claude/Gemini High-equivalent tooling
Artifacts preserved: <run dir or none>
```

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
