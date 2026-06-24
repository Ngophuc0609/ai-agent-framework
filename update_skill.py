import os

def write_file(path, content):
    with open(path, "w") as f:
        f.write(content.strip() + "\n")

skill_md = """
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

## Execution Isolation Policy & Fallbacks
Isolation is MANDATORY. Valid modes:
1. `subagent-isolated-worktrees`
2. `isolated-sequential-sessions`
3. `blocked-no-isolation-capability`

Forbidden Legacy Modes: `single-runtime-sequential-fallback`, `single-session-multi-role-execution`, `memory-only-agent-handoff`, `implicit-agent-output`, `direct-final-handbook-without-artifacts`

If runner lacks isolation capability, STOP before Agent 1, log `blocked-no-isolation-capability` in `STATUS.md`, generate block report, DO NOT run Agent 7, DO NOT publish.

## Artifact-First Handoff Policy & Coordinator Restrictions
- Physical files on disk are the ONLY official handoff mechanism. 
- Coordinator CANNOT bypass Agents 1-6 to generate docs directly.
- `draft-docs/` shared path is NEVER the source of truth. Canonical artifacts are ONLY in `.ai/runs/source-code-handover/<run_id>/...`

## Disk Validation Gate
- Next agent must not start until previous agent artifact passes.
- Artifact must have YAML front matter (`run_id`, `source_commit`, `created_at`, `status`).

## Current Repository Provenance & Template Guard
- Final docs ONLY describe the currently checked-out repository.
- NO generic framework knowledge, template docs, upstream READMEs, generic passwords (Password123), or sample domains (example.com).
- Upstream references must be isolated in `docs/02_project_context.md` with `[UPSTREAM_REFERENCE]`.

## Evidence & Negative Evidence Policy
- Valid Labels: `[CONFIRMED]`, `[INFERRED]`, `[UNVERIFIED]`, `[CONFLICT]`, `[NOT_APPLICABLE]`, `[BLOCKED]`
- `[NOT_APPLICABLE]` is strictly for `not_found_after_scan` and MUST include negative evidence IDs (`EV-NEG-###`).

## Secret Safety
Secret scan MUST be executed and passed. No unredacted secrets or credential-like literals are permitted.

## Pipeline Phases
Phase 0: Preflight + Deterministic Discovery (create JSON inventories).
Phase 1: Agent 1–5 Domain Analysis (match findings against Phase 0 inventory).
Phase 2: Agent 6 Evidence/Coverage/Conflict Review.
Phase 3: Agent 7 Final Documentation Assembly.
Phase 4: Agent 8 Independent Quality Validation.
Phase 5: Agent 7 Revision (only if Agent 8 REJECTS).
Phase 6: Final Publish.

## Readiness Policy
- **Ready**: Execution isolation passed. Phase 0 valid. Agents 1-6 passed. Agent 7 created 20 canonical docs. Agent 8 passed. No critical conflicts. No unresolved cores. No template contamination. Secret scan passed. Coverage math passed.
- **Partial**: Isolation passed. Inventory & coverage exist. Runtime/prod limitations noted. Local dev possible. Agent 8 finds no critical failure. No `Ready` claims for unverified areas.
- **Blocked**: No isolation. No reliable inventory. Stale/missing artifacts. Coverage fails. Template contamination. Agent 8 rejects without revision. Critical evidence conflict.

## Publish Policy
Documents in `.ai/runs/.../final/` MUST NOT be copied to `docs/` until Agent 8 validation is complete and yields a `PASS` verdict.
"""

write_file(".ai/skills/source-code-handover/SKILL.md", skill_md)
print("Updated SKILL.md")
