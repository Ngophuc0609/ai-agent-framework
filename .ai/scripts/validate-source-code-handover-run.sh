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

require_file() {
  if [ ! -f "$1" ]; then
    echo "FAIL: required artifact not found: $1"
    exit 1
  fi
}

require_pattern() {
  file="$1"
  pattern="$2"
  if ! grep -q "$pattern" "$file"; then
    echo "FAIL: required pattern not found in $file: $pattern"
    exit 1
  fi
}

# canonical artifact/run ID validation
echo "Validating canonical artifacts..."
REQUIRED_FINAL_COUNT=20
FINAL_COUNT=$(find "$RUN_DIR/final" -name "*.md" 2>/dev/null | wc -l)

if [ "$FINAL_COUNT" -ne "$REQUIRED_FINAL_COUNT" ]; then
  echo "FAIL: Expected $REQUIRED_FINAL_COUNT final documents, found $FINAL_COUNT"
  exit 1
fi

echo "Validating STATUS.md consistency..."
require_file "$RUN_DIR/STATUS.md"
require_file ".ai/templates/source-code-handover/agent-findings-template.md"
require_file ".ai/templates/source-code-handover/final-document-template.md"
require_file ".ai/templates/source-code-handover/evidence-store-template.md"

echo "Validating Phase 0 inventory artifacts..."
for inventory in \
  projects.json entry-points.json configuration-files.json dependencies.json dbcontexts.json dbsets.json \
  entities.json entity-configurations.json migrations.json seed-data.json raw-sql.json sql-metadata.json \
  controllers.json routes.json api-contract-sources.json hubs.json realtime-events.json background-jobs.json \
  redis-cache.json queues.json integrations.json docker-services.json ci-cd-files.json tests.json runtime-artifacts.json
do
  require_file "$RUN_DIR/inventory/$inventory"
done

echo "Validating evidence store artifacts..."
for evidence in \
  tool-runs.jsonl evidence-manifest.json focused-slices.json symbol-reference-map.json data-flow-map.json \
  sql-metadata.json api-contract-sources.json runtime-artifacts.json tool-limitations.json
do
  require_file "$RUN_DIR/evidence/$evidence"
done

python3 ./.ai/scripts/validate-source-code-handover-evidence-store.py "$RUN_DIR/evidence"
if [ $? -ne 0 ]; then
  echo "FAIL: evidence store validation failed."
  exit 1
fi

echo "Validating Agent 1-6 canonical artifacts..."
for agent in 01 02 03 04 05; do
  findings="$RUN_DIR/findings/agent-$agent/findings.md"
  require_file "$findings"
  require_pattern "$findings" "^## Scope"
  require_pattern "$findings" "^## Commands Executed"
  require_pattern "$findings" "^## Tool Orchestration"
  require_pattern "$findings" "^## Focused Evidence Slices"
  require_pattern "$findings" "^## Evidence List"
  require_pattern "$findings" "^## Discovery Reconciliation"
  require_pattern "$findings" "^## Domain Findings"
  require_pattern "$findings" "^## Required Domain Tables"
  require_pattern "$findings" "^## Negative Evidence"
  require_pattern "$findings" "^## Final-Doc Handoff"
done
for review in review.md coverage-reconciliation.md conflicts.md evidence-store-review.md tool-orchestration-review.md template-contamination-report.md readiness-decision.md; do
  require_file "$RUN_DIR/review/$review"
done

echo "Running provenance/template contamination scan..."
./.ai/scripts/scan-source-code-handover-provenance.sh "$RUN_DIR/final"
if [ $? -ne 0 ]; then
  echo "FAIL: template contamination detected."
  exit 1
fi

echo "Running source-code handover quality checklist..."
python3 ./.ai/scripts/validate-source-code-handover-quality.py "$RUN_DIR/final"
if [ $? -ne 0 ]; then
  echo "FAIL: quality checklist failed."
  exit 1
fi

echo "Running source-code handover language validation..."
./.ai/scripts/validate-source-code-handover-language.sh "$RUN_ID"
if [ $? -ne 0 ]; then
  echo "FAIL: language validation failed."
  exit 1
fi

echo "Validating Agent 8 verdict..."
for validation in final-quality-report.md provenance-scan.md evidence-validation.md coverage-validation.md links-validation.md secret-scan.md language-validation.md evidence-store-validation.md tool-orchestration-validation.md final-verdict.md; do
  require_file "$RUN_DIR/validation/$validation"
done

VERDICT=$(cat "$RUN_DIR/validation/final-verdict.md" | grep -o "PASS\|REJECT_REQUIRES_REVISION\|BLOCKED" | head -n 1)
if [ "$VERDICT" != "PASS" ]; then
  echo "FAIL: Agent 8 verdict is $VERDICT"
  exit 1
fi

echo "Validation passed."
exit 0
