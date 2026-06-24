#!/usr/bin/env bash
# validate-source-code-handover-language.sh
# Validates the Source Code Handover language matrix for an existing run.

set -u

RUN_ID="${1:-}"
if [ -z "$RUN_ID" ]; then
  echo "Usage: $0 <run_id>"
  exit 2
fi

RUN_DIR=".ai/runs/source-code-handover/$RUN_ID"
if [ ! -d "$RUN_DIR" ]; then
  echo "BLOCKED: Run directory not found: $RUN_DIR"
  exit 1
fi

FAILURES=0

fail() {
  echo "FAIL: $1"
  FAILURES=$((FAILURES + 1))
}

require_file() {
  if [ ! -f "$1" ]; then
    fail "required artifact not found: $1"
    return 1
  fi
  return 0
}

require_pattern() {
  file="$1"
  pattern="$2"
  if ! grep -qE "$pattern" "$file"; then
    fail "required pattern not found in $file: $pattern"
  fi
}

forbidden_vietnamese_internal_heading() {
  file="$1"
  if grep -qE '^## (Phạm vi|Trạng thái|Nguồn dữ liệu|Nội dung chính|Hạn chế|Câu hỏi mở|Rủi ro|Inputs bắt buộc)' "$file"; then
    fail "intermediate artifact contains Vietnamese final-doc heading: $file"
  fi
}

final_docs_dir="$RUN_DIR/final"
if [ ! -d "$final_docs_dir" ]; then
  fail "final directory not found: $final_docs_dir"
else
  echo "Validating Vietnamese final-document language..."
  while IFS= read -r -d '' file; do
    require_pattern "$file" '^## Phạm vi$'
    require_pattern "$file" '^## Trạng thái$'
    require_pattern "$file" '^## Nguồn dữ liệu / Evidence$'
    require_pattern "$file" '^## Nội dung chính$'
    require_pattern "$file" '^## Hạn chế$'
    require_pattern "$file" '^## Câu hỏi mở$'
    require_pattern "$file" '^## Rủi ro$'

    if ! grep -qE '[ăâđêôơưĂÂĐÊÔƠƯáàảãạắằẳẵặấầẩẫậéèẻẽẹếềểễệíìỉĩịóòỏõọốồổỗộớờởỡợúùủũụứừửữựýỳỷỹỵ]' "$file"; then
      fail "final document has no obvious Vietnamese prose markers: $file"
    fi

    vi_marker_count=$(grep -oE '[ăâđêôơưĂÂĐÊÔƠƯáàảãạắằẳẵặấầẩẫậéèẻẽẹếềểễệíìỉĩịóòỏõọốồổỗộớờởỡợúùủũụứừửữựýỳỷỹỵ]' "$file" | wc -l)
    english_common_count=$(grep -oiE '\b(the|and|or|with|without|must|should|working directory|prerequisites|expected result|impact|risk|question|limitation|troubleshooting|operation|deployment|configuration|architecture)\b' "$file" | wc -l)
    if [ "$english_common_count" -gt 40 ] && [ "$vi_marker_count" -lt 20 ]; then
      fail "final document appears primarily English instead of Vietnamese: $file"
    fi

    if grep -qE '^## (Commands Executed|Discovery Reconciliation|Domain Findings|Required Domain Tables|Final-Doc Handoff)$' "$file"; then
      fail "final document copied internal English artifact heading: $file"
    fi
  done < <(find "$final_docs_dir" -maxdepth 1 -name "*.md" -print0)
fi

echo "Validating English intermediate artifact language..."
require_file "$RUN_DIR/STATUS.md" && forbidden_vietnamese_internal_heading "$RUN_DIR/STATUS.md"

for agent in 01 02 03 04 05; do
  findings="$RUN_DIR/findings/agent-$agent/findings.md"
  if require_file "$findings"; then
    require_pattern "$findings" '^## Scope$'
    require_pattern "$findings" '^## Commands Executed$'
    require_pattern "$findings" '^## Evidence List$'
    require_pattern "$findings" '^## Discovery Reconciliation$'
    require_pattern "$findings" '^## Domain Findings$'
    require_pattern "$findings" '^## Required Domain Tables$'
    require_pattern "$findings" '^## Negative Evidence$'
    require_pattern "$findings" '^## Final-Doc Handoff$'
    forbidden_vietnamese_internal_heading "$findings"
  fi
done

if [ -d "$RUN_DIR/review" ]; then
  while IFS= read -r -d '' file; do
    forbidden_vietnamese_internal_heading "$file"
  done < <(find "$RUN_DIR/review" -name "*.md" -print0)
fi

if [ -d "$RUN_DIR/validation" ]; then
  while IFS= read -r -d '' file; do
    forbidden_vietnamese_internal_heading "$file"
  done < <(find "$RUN_DIR/validation" -name "*.md" -print0)
fi

if [ "$FAILURES" -ne 0 ]; then
  echo "Language validation failed with $FAILURES issue(s)."
  exit 1
fi

echo "Language validation passed."
exit 0
