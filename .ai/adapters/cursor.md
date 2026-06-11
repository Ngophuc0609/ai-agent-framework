# Cursor Adapter

## Vietnamese User Summary

Adapter này mô tả cách dùng framework `.ai/` khi chạy bằng Cursor.

## Runtime Instructions

- Load `.ai/README.md`, `.ai/registry/`, and the selected skill/workflow.
- Keep Cursor rules thin; delegate workflow behavior to `.ai/rules/`.
- Use the current workspace as the filesystem boundary.
- Prefer source evidence from files, CodeGraph, tests, and git history.
- Write user-facing chat responses in Vietnamese.
