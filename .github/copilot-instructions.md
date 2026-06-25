<!-- generated-by: ai-agent-adapter-sync -->
# .ai Framework Instructions for copilot

Generated on: `2026-06-25`
Source of truth: `.ai/`

## Required Startup

Before any coding, documentation, debugging, review, refactor, commit, or analysis task:

1. Verify `.ai/` exists in this repository.
2. Initialize runtime tools when `.ai/runtime/memory/memory.jsonl` or `.ai/runtime/mcp-servers.json` is missing:

   ```bash
   ai-agent-sync --install-tools --yes
   ```

   If `ai-agent-sync` is not in `PATH`, run:

   ```bash
   bin/ai-agent-sync --install-tools --yes
   ```

3. Follow `.ai/registry/triggers.yml` before choosing a skill or workflow.
4. Read the selected `SKILL.md` and workflow before acting.
5. Apply CodeGraph-first, MCP Memory-first, safety, quality gates, and TDD-first rules from `.ai/rules/`.
6. For new backend APIs/features/jobs/webhooks/integration flows, route to `developing-backend-feature-tdd` and define brainstorm, contract, acceptance criteria, and tests before production code.
7. For workflows listing required agents, create every required agent output or mark it not applicable with evidence before final synthesis.
8. Keep chat responses to the Vietnamese-speaking user in Vietnamese unless another language is requested.

## Canonical Files To Read

- `.ai/README.md`
- `.ai/BOOTSTRAP_ONCE.md`
- `.ai/registry/triggers.yml`
- `.ai/registry/skills.yml`
- `.ai/registry/workflows.yml`
- `.ai/registry/tool-bootstrap.json`
- `.ai/rules/00-global-rules.md`
- `.ai/rules/05-workflow-execution-rules.md`
- `.ai/rules/06-quality-gates.md`
- `.ai/rules/10-codegraph-first-rules.md`
- `.ai/rules/12-memory-policy-rules.md`
- `.ai/rules/13-efficiency-cost-policy-rules.md`
- `.ai/rules/14-tdd-first-feature-rules.md`
