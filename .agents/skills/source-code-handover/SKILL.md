---
name: source-code-handover
description: Use when creating source-code handover documentation, onboarding documentation for new developers, architecture summaries, repository maps, setup guides, API/database/auth documentation, or final project handbooks from source code
---

<!-- generated-by: ai-agent-adapter-sync -->


# Source Code Handover

## Vietnamese User Summary

Skill này dùng để tạo tài liệu bàn giao source code cho developer mới, bắt buộc sử dụng các session độc lập cho từng agent và kiểm tra file vật lý.

## REQUIRED BACKGROUND

Read `.ai/skills/using-superpowers/SKILL.md` before using this skill.

## Required Rules

- `.ai/rules/00-global-rules.md`
- `.ai/rules/01-documentation-skill.md`
- `.ai/rules/10-codegraph-first-rules.md`
- `.ai/rules/12-memory-policy-rules.md`
- `.ai/rules/06-quality-gates.md`
- `.ai/rules/07-handover-documentation-dod.md`

## Main Workflow

Use `.ai/workflows/make-new-dev-docs.md`.
Use `.ai/workflows/make-new-dev-docs-model-routing.md` when the request includes cost, balanced, high-accuracy, or model-routing intent.

## Execution Isolation Policy

Isolation là yêu cầu workflow, không phải khuyến nghị. Các execution mode hợp lệ theo thứ tự ưu tiên:
1. `subagent-isolated-worktrees`
2. `isolated-sequential-sessions`
3. `blocked-no-isolation-capability`

Forbidden legacy modes: `single-runtime-sequential-fallback`, `single-session-multi-role-execution`, `memory-only-agent-handoff`, `implicit-agent-output`, `direct-final-handbook-without-artifacts`.

Không được coi một session đổi role là nhiều agent độc lập.

## Artifact-First Handoff Policy

Artifact trên disk là nguồn trao đổi chính thức giữa agents. Memory/chats/context chỉ là hỗ trợ, không phải artifact chính thức.
Mỗi agent (1-7) phải sinh ra file vật lý Markdown đúng đường dẫn quy định trong workflow. File phải chứa các section chuẩn yếu: `Status`, `Evidence`, `Open Questions`, `Risks`, `Files Inspected`/`Commands Executed`. Không chứa secret thực tế.

## Sequential Session Fallback Policy

Nếu sử dụng `isolated-sequential-sessions`:
Mỗi Agent 1–7 phải chạy trong một session mới, độc lập. Session coordinator chỉ điều phối việc tạo namespace, kích hoạt agent, và kiểm tra artifact gate, nhưng không được tự làm thay nội dung cho agent.

## Coordinator Restrictions

Session coordinator không được tự thực hiện nội dung khảo sát thay Agent 1–6. Không được bypass Agent 1–6 để tạo handbook trực tiếp.

## Disk Validation Gate

CRITICAL: Intermediate findings must never exist only in model context, temporary memory, chat history, or coordinator state.
CRITICAL: The next agent must not start until the previous agent artifact gate passes (file exists, size > 0, required headings, status file updated).
CRITICAL: Agent 7 must read Agent 1–6 artifacts from disk. It must not aggregate from hidden session context or remembered summaries.

## Memory Policy & Source of Truth

Current repository source, configuration, migrations, CI/CD, and verified runtime output are authoritative. Project memory and existing documentation are supplementary context only. Any memory-derived claim that is not verified against current source must be marked `[UNVERIFIED]`.

## Secret Safety

Never copy secret values (connection strings, JWT signing keys, OAuth secrets, API keys, passwords) into documentation, findings, memory, logs, status files, or chat output. Redact sensitive values while preserving variable names and setup requirements.

## Evidence Policy

All technical claims must be labeled as one of: `[CONFIRMED]`, `[INFERRED]`, `[UNVERIFIED]`, `[CONFLICT]`, `[NOT_APPLICABLE]`, or `[BLOCKED]`.

## Final Validation

Before publishing final docs or committing changes, run required-output validation, STATUS.md consistency validation, git diff --check, secret scan, markdown/link validation, and stack-appropriate build or test commands when environment permits.
