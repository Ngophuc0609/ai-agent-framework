# Cline Rollout And Smoke Test Plan

## Vietnamese User Summary

Plan này hướng dẫn chạy thử bộ `.ai` trên Cline để kiểm tra router, TDD-first gate, memory policy, cost policy và workflow tạo tài liệu.

## Goal

Validate that Cline can use the `.ai` framework without reading the whole repository, without jumping directly into implementation for new features, and while keeping user-facing chat in Vietnamese.

## Preconditions

- Open Cline in the project root.
- Allow filesystem access only to the current project folder.
- Configure MCP Git, MCP Filesystem, and MCP Memory when available.
- Configure CodeGraph or confirm the fallback decision with the user.
- Do not grant whole-drive filesystem access.

## Files Cline Should Read First

1. `.ai/README.md`
2. `.ai/adapters/cline.md`
3. `.ai/registry/triggers.yml`
4. `.ai/registry/skills.yml`
5. `.ai/registry/workflows.yml`
6. `.ai/rules/00-global-rules.md`
7. `.ai/rules/13-efficiency-cost-policy-rules.md`
8. `.ai/rules/14-tdd-first-feature-rules.md`

## Smoke Test 1: Routing New Endpoint

Prompt:

```text
tạo endpoint mới GET /api/v1/health/details, trước hết chỉ brainstorm và lập test plan, chưa implement
```

Expected behavior:

- Cline routes to `routing-ai-task`.
- Cline selects `developing-backend-feature-tdd`.
- Cline does not edit production code.
- Cline returns Vietnamese chat response.
- Response includes Brainstorm, API Contract, Acceptance Criteria, Test Plan, Implementation Plan, Files to Change, Risks, Done Criteria.

Pass criteria:

- No production file changed.
- No broad repository scan.
- TDD gate is explicitly applied.

## Smoke Test 2: Prevent Direct API Implementation

Prompt:

```text
tạo api mới để lấy danh sách quiz game
```

Expected behavior:

- Cline does not route to `creating-apis`.
- Cline routes to `developing-backend-feature-tdd`.
- Cline asks at most one concise Vietnamese clarification question if the contract is missing.
- Cline does not implement until brainstorm, contract, and test plan exist.

## Smoke Test 3: Existing API Analysis

Prompt:

```text
phân tích endpoint hiện có /api/v1/health
```

Expected behavior:

- Cline routes to `analyzing-api-endpoint` or `creating-apis` for existing API work.
- Cline uses memory and `docs/PROJECT_CONTEXT.md` first.
- Cline reads only route/controller/service files relevant to that endpoint.

## Smoke Test 4: Diff Review TDD Gate

Prompt:

```text
review diff hiện tại trước commit
```

Expected behavior:

- Cline uses `reviewing-git-diff`.
- Cline starts with git diff.
- If the diff contains a new endpoint/feature without tests or test plan, Cline raises a warning.
- Review findings are returned in Vietnamese.

## Smoke Test 5: Documentation Workflow

Prompt:

```text
tạo tài liệu cho người mới bản cân bằng
```

Expected behavior:

- Cline routes to `source-code-handover`.
- Cline applies CodeGraph-first and Memory Policy.
- Cline uses model routing if the runner supports it.
- Cline writes docs to approved paths only.

## Expected Failure Handling

If CodeGraph is unavailable and automatic setup fails:

- Stop.
- Explain the limitation in Vietnamese.
- Ask whether to continue without CodeGraph or use another tool.

If MCP Memory is unavailable:

- Record the limitation.
- Use repo-local docs as fallback.
- Do not pretend memory was written.

## Evaluation Checklist

- [ ] Cline reads registry before choosing a workflow.
- [ ] New endpoint requests route to TDD-first skill.
- [ ] Existing endpoint analysis does not route to TDD-first unnecessarily.
- [ ] No production code is edited before brainstorm, contract, and test plan.
- [ ] Memory/project docs are checked before deep code reads.
- [ ] File reads are narrow.
- [ ] Git diff is used for review/commit tasks.
- [ ] Responses to the user are Vietnamese.
- [ ] Internal operational instructions remain English.
- [ ] Secret and filesystem scope rules are respected.
