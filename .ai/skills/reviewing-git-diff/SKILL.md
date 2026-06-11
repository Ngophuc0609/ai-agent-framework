---
name: reviewing-git-diff
description: Use when reviewing existing git changes, staged or unstaged diffs, before commit or before finalizing implementation
---

# Reviewing Git Diff

## Vietnamese User Summary

Skill này review diff hiện tại, ưu tiên chỉ đọc file đã thay đổi và dependency trực tiếp.

## Workflow

1. Use git diff first.
2. Read only changed files.
3. Read direct dependencies only when needed.
4. Review logic, security, validation, auth, performance, tests, docs, and backward compatibility.
5. If the diff adds a new endpoint or feature without tests or an executable test plan, raise a finding.
6. Respond in Vietnamese with findings ordered by severity.

## TDD Review Gate

If a diff contains a new endpoint, new service behavior, new database-backed flow, new job, webhook, or integration flow:

- Warn when brainstorm/contract/test plan is missing.
- Warn when no automated tests or manual regression checks exist.
- Warn when docs/API examples are missing for public API changes.
