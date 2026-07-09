<!-- generated-by: ai-agent-adapter-sync -->
# .ai Framework Instructions for antigravity

Native entrypoints: `GEMINI.md` and `.agents/skills/<skill>/SKILL.md`.
Canonical source/resources: `.ai/`.
Mode: Antigravity isolated native mode; do not eagerly load `.ai/`.

## Progressive Startup

Before coding, documentation, debugging, review, refactor, commit, or analysis:

1. Use Antigravity native skill discovery from `.agents/skills/`.
2. Select skills by slash command or by matching the `description` in each `SKILL.md`.
3. Read only the selected `SKILL.md` and its directly referenced files.
4. Do not read `.ai/README.md`, `.ai/registry/*`, or all `.ai/rules/*` during normal startup.
5. Read `.ai/` files only when the selected skill or this file directly references them.
6. Inspect runtime state using safe local checks. Do not install tools or packages automatically.
7. Execute with bounded source scope and validate only applicable quality gates.
8. Record tool fallbacks, confidence/readiness impact, and evidence paths.

The one-time bootstrap document is setup-only. Do not load it during normal tasks.

## Non-Negotiable Rules

- `.agents/skills/` is the native Antigravity project skill surface.
- `.ai/` is canonical source/reference material, not an always-on policy bundle.
- Keep filesystem access within the active repository.
- Never expose secrets or store unverified/raw source in memory.
- Package/tool installation and other high-risk actions require runtime-appropriate approval.
- Current source and executable evidence override memory and generated documentation.
- New backend features/APIs/jobs/webhooks/integrations require brainstorm, contract, acceptance criteria, and tests before production code.
- Respond to the Vietnamese-speaking user in Vietnamese unless another language is requested.

## .NET Parity Migration Guardrails

When the task is .NET Framework or legacy .NET migration to .NET 8+:

- Treat the work as 1:1 parity migration, not modernization.
- Baseline legacy behavior before production code conversion.
- Generate unit/contract tests from the legacy baseline before using migrated output.
- Convert one endpoint, view, job, integration, or business flow at a time.
- Do not change request/response contracts, status codes, content types, JSON casing, data types, object structure, cookies, session, redirects, views, static assets, side effects, or business rules.
- Do not fix latent legacy bugs during the parity phase; record them in `15_DEFERRED_ISSUES_REPORT.md`.
- Do not mechanically map `Request.Params` by HTTP method or mechanically convert `Json(responseString)` to `Content(responseString, "application/json")`.
- Use `PASS`, `FAIL`, `BLOCKED`, `PARTIAL`, and `DEFERRED`; missing baseline/evidence means `BLOCKED`, not guessed output.

## Runtime Fallbacks

- Missing native skill: inspect `.ai/registry/triggers.yml` only as a routing fallback.
- Missing Memory: use `docs/PROJECT_CONTEXT.md`, `docs/FINDINGS.md`, and `docs/DECISIONS.md`; record the limitation and do not claim a memory write.
- Missing CodeGraph on localized work: use `rg`, IDE/LSP references, and narrow source slices; downgrade confidence/readiness.
- Missing required workflow evidence: stop that workflow rather than fabricate output.

## Completion Contract

Before completion, report changed files, validations run, fallbacks/limitations, and readiness. Run `ai-agent-adapter-sync --check` when framework or adapter sources changed.
