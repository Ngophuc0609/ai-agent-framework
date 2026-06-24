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
