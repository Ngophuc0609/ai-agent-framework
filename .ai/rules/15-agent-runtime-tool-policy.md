# 15 Agent Runtime Tool Policy

## Vietnamese User Summary

Rule này khóa cách agent dùng tool/runtime để tránh lỗi gọi tool sai schema, scan quá rộng, tự retry vô hạn, hoặc tạo tài liệu từ context thay vì source vật lý.

## Universal Tool-Call Contract

Before calling any tool, the agent MUST know the exact schema required by the active runtime.

If the runtime exposes a shell/command tool, the agent MUST provide every required field in one valid call. Do not emit partial, empty, or placeholder tool calls.

If a tool call fails because of malformed arguments:

1. Retry at most once with the complete required schema.
2. If the retry fails, stop that action.
3. Record the limitation in the workflow artifact.
4. Continue only with a documented fallback that does not pretend the failed tool succeeded.

Do not loop on the same malformed tool call.

## Command Safety Defaults

Safe local read/setup commands may run without user approval when the runtime permits it:

- `pwd`
- `ls`
- `rg`
- `rg --files`
- `git status`
- `git rev-parse`
- bounded `find <path> -maxdepth N`
- validation scripts under `.ai/scripts/`
- run initialization under `.ai/runs/`

High-risk commands require explicit user approval or an approved workflow gate:

- destructive git commands
- deploy/release commands
- database migration or data mutation commands
- production credentials or secret access
- external network operations that upload code or data
- package install commands when the environment policy requires approval

## Search And Scan Limits

Do not start with unbounded repository scans such as `find .` without exclusions or max depth.

Prefer:

```bash
rg --files
rg --files .ai/workflows
find .ai/workflows -maxdepth 1 -type f -name "*.md"
```

For large repositories, exclude generated/vendor/build folders before broad discovery:

```bash
rg --files -g '!bin/' -g '!obj/' -g '!node_modules/' -g '!dist/' -g '!build/'
```

## Source-Code Handover Minimum Tool Behavior

When running `source-code-handover` or `make-new-dev-docs`:

1. Read `.ai/registry/triggers.yml`, the selected `SKILL.md`, `.ai/workflows/make-new-dev-docs.md`, and this runtime tool policy.
2. Initialize the run with `.ai/scripts/init-source-code-handover-run.sh`.
3. Agents 1-5 MUST discover from physical files and write inventory/findings artifacts.
4. Agents 6-8 MUST re-open physical source slices and tool outputs before verifying claims.
5. Agent 9 MUST write final docs from frozen evidence, not from vague model memory.
6. Agent 10 MUST audit evidence coverage and mark weak sections `REJECT`, `PARTIAL`, or `NOT_VERIFIED`.
7. Agent 10 MUST produce a structured `final-verdict.md` with gate-by-gate PASS/FAIL lines. A one-line `PASS` is invalid.
8. Final publish MUST run `.ai/scripts/validate-source-code-handover-run.sh <run_id>` and stop on any failure.

If the selected skill/workflow cannot be read, if the run cannot be initialized, or if the runtime cannot access `.ai/`, the workflow MUST stop before writing deliverable docs.

Forbidden fallback outputs:

- `docs/onboarding.md`
- `docs/NEW-DEVELOPER-ONBOARDING.md`
- any direct `docs/*.md` handover file written without Agent 10 `PASS`
- any direct `docs/*.md` handover file written when `STATUS.md` still has `Execution Mode: unverified`, `Isolation Verified: no`, `TBD`, or pending required agents
- any generic setup guide based on model assumptions instead of current-repository evidence

## Runtime Limitation Recording

Every workflow that depends on tools MUST record missing or failed tools in a limitation artifact such as:

- `.ai/runs/<skillflow_id>/<run_id>/evidence/tool-limitations.json`
- `.ai/runs/<skillflow_id>/<run_id>/validation/tool-orchestration-validation.md`
- `.ai/runs/<skillflow_id>/<run_id>/STATUS.md`

The limitation record MUST include:

- tool name
- expected role
- attempted command or tool action
- error/failure mode
- impact on evidence quality
- fallback used

## Do Not

- Do not claim a tool was used when it was skipped or failed.
- Do not treat model context as evidence.
- Do not mark generated docs `Ready` when build/test/runtime evidence is missing.
- Do not use repeated prose, repeated paragraphs, or extremely long generated lines to satisfy documentation length checks.
- Do not publish final docs when required agent artifacts are absent.
- Do not publish final docs when the deterministic validation script fails, even if a model-generated verdict says `PASS`.
- Do not create generic onboarding documents as a fallback when `.ai` files, tools, or source scans fail.
- Do not broaden filesystem or network access to compensate for poor prompt routing.
