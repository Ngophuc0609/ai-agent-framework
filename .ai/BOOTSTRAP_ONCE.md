# AI Framework Bootstrap Once

## Vietnamese User Summary

File này chỉ dùng cho lần thiết lập đầu tiên, smoke test agent mới, hoặc khi người dùng yêu cầu bootstrap. Không đọc file này trong startup của task thông thường.

## Scope

Use this document only when onboarding a repository or runtime, validating native adapter discovery, configuring optional integrations, or responding to an explicit bootstrap request.

Normal tasks must follow the generated pointer adapter and load `.ai` files progressively. They must not read this document automatically.

## One-Time Setup

1. Verify `.ai/README.md`, `.ai/registry/triggers.yml`, `.ai/rules/00-global-rules.md`, and `.ai/rules/15-agent-runtime-tool-policy.md` are readable.
2. Select the matching `.ai/adapters/<agent>.md` file.
3. Generate pointer-only native instructions:

   ```bash
   ai-agent-adapter-sync --agent <agent>
   ```

4. Verify generated sources and checksums:

   ```bash
   ai-agent-adapter-sync --agent <agent> --check
   ```

5. Inspect runtime state with safe local checks. Do not install missing tools during this step.
6. If optional tools are required, explain the install/network effects and obtain runtime-appropriate approval before running `ai-agent-sync --install-tools --yes`.
7. If Memory remains unavailable, use `docs/PROJECT_CONTEXT.md`, `docs/FINDINGS.md`, and `docs/DECISIONS.md`, and record the limitation.
8. Smoke-test routing with a localized task and a workflow-specific task.

## Materialized Compatibility Mode

Use this only for a restricted runtime that cannot read repository files:

```bash
ai-agent-adapter-sync --agent <agent> --materialized
```

Filesystem-capable agents should use pointer-only mode to avoid duplicated policy, stale context, and cross-runtime rules.

## Completion Record

Record the selected adapter, generated manifest path, runtime tools available, optional installations approved, fallbacks activated, and smoke-test result.
