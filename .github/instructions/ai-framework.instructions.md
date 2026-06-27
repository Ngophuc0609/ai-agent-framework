---
applyTo: ".ai/**,bin/ai-agent-*"
---

<!-- generated-by: ai-agent-adapter-sync -->
# .ai Framework Instructions for copilot

Source of truth: `.ai/`
Mode: pointer-only; do not treat this generated file as a policy copy.

## Progressive Startup

Before any coding, documentation, debugging, review, refactor, commit, or analysis task:

1. Verify `.ai/` exists in this repository.
2. Read `.ai/README.md`, `.ai/rules/00-global-rules.md`, and `.ai/rules/15-agent-runtime-tool-policy.md`.
3. Inspect runtime state using safe local checks. Do not install tools or packages automatically.
4. Read `.ai/adapters/copilot.md` when native tool constraints are relevant and the file exists.
5. Read `.ai/registry/triggers.yml` and match the user intent.
6. Read only the selected `SKILL.md`, selected workflow, and their directly referenced rules.
7. Execute with bounded source scope and validate only applicable quality gates.
8. Record tool fallbacks, confidence/readiness impact, and evidence paths.

The one-time bootstrap document is setup-only. Do not load it during normal tasks.

## Non-Negotiable Rules

- `.ai/` is canonical; this file only points to current policy.
- Keep filesystem access within the active repository.
- Never expose secrets or store unverified/raw source in memory.
- Package/tool installation and other high-risk actions require runtime-appropriate approval.
- Current source and executable evidence override memory and generated documentation.
- New backend features/APIs/jobs/webhooks/integrations require brainstorm, contract, acceptance criteria, and tests before production code.
- Respond to the Vietnamese-speaking user in Vietnamese unless another language is requested.

## Rule Loading Matrix

- Every task: `00-global-rules.md`, `03-safety-rules.md`, `15-agent-runtime-tool-policy.md`.
- Skill/workflow routing: `triggers.yml`, then only the selected skill and workflow. Read `skills.yml` or `workflows.yml` only when metadata resolution requires them.
- Localized source work: apply `10-codegraph-first-rules.md` and `12-memory-policy-rules.md` as preferred, non-blocking preflight with documented fallback.
- Architecture, source handover, cross-module analysis, broad refactor, dependency tracing: attempt CodeGraph first; block only when the selected workflow requires graph evidence.
- New backend behavior: `14-tdd-first-feature-rules.md` and `developing-backend-feature-tdd`.
- Source handover: load its selected skill/workflow and required agent/evidence rules exactly.
- Model routing: load `08-model-routing-rules.md` and `09-model-trigger-rules.md` only for model selection/routing tasks.

## Runtime Fallbacks

- Missing Memory: use `docs/PROJECT_CONTEXT.md`, `docs/FINDINGS.md`, and `docs/DECISIONS.md`; record the limitation and do not claim a memory write.
- Missing CodeGraph on localized work: use `rg`, IDE/LSP references, and narrow source slices; downgrade confidence/readiness.
- Missing required workflow evidence: stop that workflow rather than fabricate output.

## Completion Contract

Before completion, report changed files, validations run, fallbacks/limitations, and readiness. Run `ai-agent-adapter-sync --check` when framework or adapter sources changed.
