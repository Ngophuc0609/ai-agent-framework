# Claude Adapter

## Vietnamese User Summary

Adapter này mô tả cách dùng framework `.ai/` khi chạy bằng Claude.

## Runtime Instructions

- Treat `.ai/registry/` as the source of truth for skill/workflow resolution.
- Load only the selected skill, workflow, and directly referenced rules.
- Apply `.ai/rules/15-agent-runtime-tool-policy.md` before Bash, file edit, MCP, or sub-agent tool use.
- Use memory only for durable, verified, reusable project facts.
- Keep raw source-code snippets out of memory unless summarized.
- Record evidence paths for every important claim.
- Use Vietnamese for chat responses to the user.

## Optimization Profile

- Best fit: deep reasoning, cross-file synthesis, architecture review, security review, and final documentation critique.
- Use deterministic tools first; keep Claude reasoning on narrowed source slices and evidence manifests.
- Use Task/sub-agent style delegation only when the active Claude runtime exposes it and the workflow requires isolated agents.
- Do not let long reasoning replace build/test/source evidence; claims must point back to files, commands, or evidence IDs.
- For `source-code-handover`, Claude is well-suited for Agent 7 cross-layer conflict analysis and Agent 10 independent critique, but must not rewrite weak evidence as final certainty.
- Avoid storing raw source in memory; store only verified summaries, decisions, and reusable findings.
