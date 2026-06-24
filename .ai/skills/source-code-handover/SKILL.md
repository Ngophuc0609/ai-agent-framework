---
name: source-code-handover
description: Use when creating source-code handover documentation, onboarding documentation for new developers, architecture summaries, repository maps, setup guides, API/database/auth documentation, or final project handbooks from source code
---

# Source Code Handover (Evidence-First Documentation Pipeline)

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
Use `.ai/workflows/make-new-dev-docs-model-routing.md` when model-routing is required.

## Current Repository Provenance Guard
Final documentation ONLY describes the currently checked-out repository. 
- You MUST NOT use generic framework knowledge, template generator docs, upstream READMEs, or chat memory as primary evidence.
- Upstream content MUST be placed in `docs/02_project_context.md` under "Nguồn gốc upstream / template" with `[UPSTREAM_REFERENCE]`.

## Canonical Artifact Policy
- Draft docs shared path (`draft-docs/`) is NEVER the source of truth.
- Canonical path: `.ai/runs/source-code-handover/<run_id>/...`
- Every canonical artifact MUST contain a YAML front matter with `run_id`, `agent_id`, `source_commit`, `created_at`, `status`.

## Pipeline Phases
Phase 0: Preflight + Deterministic Discovery
Phase 1: Agent 1–5 isolated domain analysis
Phase 2: Agent 6 evidence/coverage/conflict review
Phase 3: Agent 7 creates final documentation
Phase 4: Agent 8 independently validates final documentation
Phase 5: Agent 7 revision in a new isolated session if Agent 8 rejects
Phase 6: Agent 8 final pass
