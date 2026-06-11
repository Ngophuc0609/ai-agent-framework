# Claude Adapter

## Vietnamese User Summary

Adapter này mô tả cách dùng framework `.ai/` khi chạy bằng Claude.

## Runtime Instructions

- Treat `.ai/registry/` as the source of truth for skill/workflow resolution.
- Load only the selected skill, workflow, and directly referenced rules.
- Use memory only for durable, verified, reusable project facts.
- Keep raw source-code snippets out of memory unless summarized.
- Record evidence paths for every important claim.
- Use Vietnamese for chat responses to the user.
