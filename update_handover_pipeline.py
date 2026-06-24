import os
import re

def write_file(path, content):
    with open(path, "w") as f:
        f.write(content.strip() + "\n")

# 1. scan-source-code-handover-provenance.sh
provenance_sh = """
#!/usr/bin/env bash
# scan-source-code-handover-provenance.sh
# Scans for template contamination, placeholder secrets, and generic content in final docs.

TARGET_DIR="${1:-.ai/runs/source-code-handover/*/final}"

if [ ! -d "$TARGET_DIR" ] && ! ls $TARGET_DIR >/dev/null 2>&1; then
  echo "Target directory not found: $TARGET_DIR"
  exit 0
fi

echo "Scanning provenance in $TARGET_DIR..."

CRITICAL_PATTERNS=(
  "dotnet new"
  "github.com/skoruba"
  "skoruba.local"
  "example.com"
  "Password123"
  "Pa\\$\\$word123"
  "Secret123"
  "your-api-key"
  "your-client-secret"
  "PayPal"
  "Patreon"
  "Gitter"
  "Hangfire hoặc Quartz"
  "NotificationHub"
  "ReceiveMessage"
  "sample only"
  "example only"
)

EXIT_CODE=0

for pattern in "${CRITICAL_PATTERNS[@]}"; do
  # Search for the pattern, ignoring lines with [UPSTREAM_REFERENCE]
  MATCHES=$(grep -Hn -E "$pattern" $(find $TARGET_DIR -name "*.md") 2>/dev/null | grep -v "\\[UPSTREAM_REFERENCE\\]")
  if [ -n "$MATCHES" ]; then
    echo "CRITICAL WARNING: Found template contamination for pattern: $pattern"
    echo "$MATCHES"
    EXIT_CODE=1
  fi
done

if [ $EXIT_CODE -eq 0 ]; then
  echo "Provenance scan passed. No unredacted secret detected. No template contamination."
else
  echo "Provenance scan failed. Found generic upstream/template content without [UPSTREAM_REFERENCE] or missing code evidence."
fi

exit $EXIT_CODE
"""

# 2. validate-source-code-handover-run.sh
validate_sh = """
#!/usr/bin/env bash
# validate-source-code-handover-run.sh

RUN_ID="${1}"
if [ -z "$RUN_ID" ]; then
  echo "Usage: $0 <run_id>"
  exit 1
fi

RUN_DIR=".ai/runs/source-code-handover/$RUN_ID"

if [ ! -d "$RUN_DIR" ]; then
  echo "BLOCKED: Run directory not found: $RUN_DIR"
  exit 1
fi

# canonical artifact/run ID validation
echo "Validating canonical artifacts..."
REQUIRED_FINAL_COUNT=20
FINAL_COUNT=$(find "$RUN_DIR/final" -name "*.md" 2>/dev/null | wc -l)

if [ "$FINAL_COUNT" -ne "$REQUIRED_FINAL_COUNT" ]; then
  echo "FAIL: Expected $REQUIRED_FINAL_COUNT final documents, found $FINAL_COUNT"
  exit 1
fi

echo "Validating STATUS.md consistency..."
if [ ! -f "$RUN_DIR/STATUS.md" ]; then
  echo "FAIL: STATUS.md not found"
  exit 1
fi

echo "Running provenance/template contamination scan..."
./.ai/scripts/scan-source-code-handover-provenance.sh "$RUN_DIR/final"
if [ $? -ne 0 ]; then
  echo "FAIL: template contamination detected."
  exit 1
fi

echo "Validating Agent 8 verdict..."
if [ ! -f "$RUN_DIR/validation/final-verdict.md" ]; then
  echo "FAIL: Agent 8 verdict not found. Agent 8 must run."
  exit 1
fi

VERDICT=$(cat "$RUN_DIR/validation/final-verdict.md" | grep -o "PASS\|REJECT_REQUIRES_REVISION\|BLOCKED" | head -n 1)
if [ "$VERDICT" != "PASS" ]; then
  echo "FAIL: Agent 8 verdict is $VERDICT"
  exit 1
fi

echo "Validation passed."
exit 0
"""

# 3. Agent 8 validator
agent_08 = """
# Agent 8 - Final Documentation Quality Validator

**Role**: Independent reviewer checking the final assembled handover documents. Agent 8 DOES NOT write or modify the documentation. It only validates the output of Agent 7 against the repository source and the Definition of Done.

## Input
- `.ai/runs/source-code-handover/<run_id>/inventory/`
- `.ai/runs/source-code-handover/<run_id>/review/`
- `.ai/runs/source-code-handover/<run_id>/final/`
- Current git repository source files.

## Output Canonical Artifacts
Create the following files in `.ai/runs/source-code-handover/<run_id>/validation/`:
1. `final-quality-report.md`
2. `provenance-scan.md`
3. `evidence-validation.md`
4. `coverage-validation.md`
5. `links-validation.md`
6. `secret-scan.md`
7. `final-verdict.md`

## Validation Rules

1. **Provenance & Template Guard**: 
   - Check for `dotnet new`, generic Docker images, placeholder domains, or sample passwords. 
   - Ensure they are tagged `[UPSTREAM_REFERENCE]` if unavoidable.
2. **Evidence Policy**:
   - Check every `[CONFIRMED]` claim has a valid `EV-xxx-###` Evidence ID.
   - Verify `19_evidence_index.md` contains valid source paths.
3. **Coverage Math**:
   - Ensure `accounted = documented + unresolved + not applicable with negative evidence + excluded with explicit reason`.
4. **Safety**:
   - Secret scan executed and passed. No credential-like literal copied from source unless redacted and explicitly documented.
5. **Verdict**:
   - In `final-verdict.md`, strictly output ONLY ONE of: `PASS`, `REJECT_REQUIRES_REVISION`, or `BLOCKED`.
"""

# 4. SKILL.md
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
"""

# 5. Workflow make-new-dev-docs.md
workflow_md = """
# Source Code Handover Workflow

## Execution Isolation Policy
1. `subagent-isolated-worktrees`
2. `isolated-sequential-sessions`
3. `blocked-no-isolation-capability`

Forbidden: `single-runtime-sequential-fallback`, `single-session-multi-role-execution`, `memory-only-agent-handoff`, `implicit-agent-output`, `direct-final-handbook-without-artifacts`

## Phase 0: Preflight + Deterministic Discovery
Before Agent 1-5 runs, the coordinator MUST create:
`.ai/runs/source-code-handover/<run_id>/inventory/` containing JSON files (projects, entry-points, dbcontexts, controllers, etc.) scanned from AST/CodeGraph/CLI. If a component is missing, create the inventory JSON with `0` count.

## Phase 1 to Phase 6 Pipeline
- Agent 1-5: Domain Analysis (Read Phase 0 inventory, match with source evidence).
- Agent 6: Evidence & Coverage Review (Must produce coverage-reconciliation.md).
- Agent 7: Final Documentation Assembly (Reads canonical artifacts, produces 20 files in `.ai/runs/.../final/`).
- Agent 8: Independent Final Validation (Runs `scan-source-code-handover-provenance.sh` and semantic checks, issues verdict).

## Final Validation
Must execute:
- git diff --check
- required output existence check
- canonical artifact/run ID validation
- STATUS.md consistency validation
- provenance/template contamination scan
- secret scan executed and passed
- Markdown/internal link validation
- evidence ID validation
- coverage reconciliation validation
- final docs content-contract validation
- no unresolved critical conflict omitted
- stack-appropriate build/test commands when environment permits
"""

# 6. Model Routing
routing_md = """
# Model Routing for Dev Docs

If the repository involves authentication, payment, SignalR, PII, Kubernetes, Background Jobs, or DB Migrations, FAST_CHEAP is forbidden for Agents 2, 3, 5, 6, and 8.

Default routing for auth-heavy projects:
- Agent 1: BALANCED
- Agent 2: REASONING_STRONG
- Agent 3: REASONING_STRONG
- Agent 4: BALANCED
- Agent 5: REASONING_STRONG
- Agent 6: REASONING_STRONG
- Agent 7: LONG_CONTEXT_STRONG
- Agent 8: REASONING_STRONG

If runner lacks routing:
- Log limitation in STATUS.md.
- Max readiness is `Partial` if critical review cannot be reliable.
"""

# 7. DoD Rules update
dod_md = """
# Documentation Definition of Done (DoD)

Mọi agent tham gia quá trình Handover phải tuân thủ nghiêm ngặt chuẩn này.

## 1. Quy tắc chung: mỗi claim phải có Evidence
- Status: Confirmed | Inferred | Unverified | Conflict | Not Applicable
- Every `[CONFIRMED]` claim requires an Evidence ID (e.g., EV-DB-001).

## 2. Bộ tài liệu mục tiêu
- `01_project_handover_full.md`
- `02_project_context.md`
- `03_repository_guide.md`
- `04_local_setup.md`
- `05_configuration_reference.md`
- `06_architecture.md`
- `07_database_reference.md`
- `08_auth_and_security.md`
- `09_api_catalog.md`
- `10_background_jobs.md`
- `11_realtime_signalr_socket.md`
- `12_external_integrations.md`
- `13_frontend_guide.md`
- `14_operations_runbook.md`
- `15_deployment_and_cicd.md`
- `16_testing_guide.md`
- `17_known_risks.md`
- `18_open_questions.md`
- `19_evidence_index.md`
- `20_documentation_coverage.md`

## 3. Mandatory Coverage Rule
`accounted = documented + unresolved + not applicable with negative evidence + excluded with explicit reason`

## 4. Documentation Coverage Manifest (20_documentation_coverage.md)
Must use structural tables calculating `accounted` components versus `discovered` components from Phase 0 Inventory.

## 5. Negative Evidence Rule
`[NOT_APPLICABLE]` must include search roots, commands executed, results, and negative evidence IDs.
"""

# Agents 1-7 (Adding Investigation Protocol)
investigation_protocol = """
## Mandatory Investigation Protocol
1. Read Phase 0 Preflight & Inventory before analyzing source.
2. Log all executed commands.
3. List inspected source roots.
4. Record discovery count from inventory.
5. Reconcile `discovered / documented / unresolved / not applicable`.
6. Assign Evidence IDs (EV-xxx-###) for claims.
7. ONLY use current source as implementation evidence.
8. Do NOT copy generic examples or upstream template docs.
9. Generate negative evidence reports if components are missing.
10. Note limitations if tools/runtime fail.
"""

agent_1 = investigation_protocol + "\nAgent 1: Source, Local Setup, Configuration, CI/CD. Verify git remote. List executable projects. Do not use dotnet new unless repo is a template. CI/CD: no guessing, confirmed missing if not found."
agent_2 = investigation_protocol + "\nAgent 2: Database & Auth. Create DB reconciliation table. Do not guess DB types from class names. Auth clients require code evidence."
agent_3 = investigation_protocol + "\nAgent 3: API. Sequence diagram mandatory for important APIs. DTO source mandatory. No JSON hallucination. Routes discovered from controllers, not just Swagger."
agent_4 = investigation_protocol + "\nAgent 4: Business, Frontend, Integration. Business flows rely on source call chain. Do not assert 3rd party APIs without registration/config evidence."
agent_5 = investigation_protocol + "\nAgent 5: Operations, Jobs, Realtime. Sequence diagram mandatory for jobs and Realtime. Do NOT say 'Hangfire or Quartz', specify exact engine or [NOT_APPLICABLE]. Incident runbook must distinguish confirmed vs recommended."
agent_6 = investigation_protocol + "\nAgent 6: Reviewer. Compare findings vs Phase 0 Inventory. Verify coverage math. Reject missing evidence or generic samples. Output to `review/`."
agent_7 = investigation_protocol + "\nAgent 7: Aggregator. Creates 20 final markdown files in Vietnamese. Reads only from Phase 1-6 canonical artifacts. No new technical claims. Write YAML front matter on all final docs."

# Write files
write_file(".ai/scripts/scan-source-code-handover-provenance.sh", provenance_sh)
write_file(".ai/scripts/validate-source-code-handover-run.sh", validate_sh)
os.chmod(".ai/scripts/scan-source-code-handover-provenance.sh", 0o755)
os.chmod(".ai/scripts/validate-source-code-handover-run.sh", 0o755)

write_file(".ai/agents/agent-08-final-documentation-validator.md", agent_08)
write_file(".ai/workflows/make-new-dev-docs.md", workflow_md)
write_file(".ai/workflows/make-new-dev-docs-model-routing.md", routing_md)
write_file(".ai/rules/07-handover-documentation-dod.md", dod_md)
write_file(".ai/skills/source-code-handover/SKILL.md", skill_md)

write_file(".ai/agents/agent-01-source-local.md", agent_1)
write_file(".ai/agents/agent-02-database-auth.md", agent_2)
write_file(".ai/agents/agent-03-api-postman.md", agent_3)
write_file(".ai/agents/agent-04-business-frontend.md", agent_4)
write_file(".ai/agents/agent-05-operation.md", agent_5)
write_file(".ai/agents/agent-06-coordinator-reviewer.md", agent_6)
write_file(".ai/agents/agent-07-single-handbook-aggregator.md", agent_7)

print("Update completed successfully.")
