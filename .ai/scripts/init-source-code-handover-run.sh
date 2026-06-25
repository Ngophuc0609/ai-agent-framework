#!/usr/bin/env bash
# init-source-code-handover-run.sh

set -eu

RUN_ID="${1:-}"
if [ -z "$RUN_ID" ]; then
  RUN_ID="run-$(date +%Y%m%d-%H%M%S)"
fi

case "$RUN_ID" in
  *[!A-Za-z0-9._-]*)
    echo "FAIL: run_id contains unsupported characters: $RUN_ID"
    exit 2
    ;;
esac

RUN_DIR=".ai/runs/source-code-handover/$RUN_ID"

if [ -e "$RUN_DIR" ]; then
  echo "FAIL: run directory already exists: $RUN_DIR"
  exit 1
fi

SOURCE_COMMIT="$(git rev-parse HEAD 2>/dev/null || echo unknown)"
SOURCE_BRANCH="$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo unknown)"
GIT_REMOTE="$(git remote get-url origin 2>/dev/null || echo unknown)"
CREATED_AT="$(date -Iseconds)"

mkdir -p \
  "$RUN_DIR/metadata" \
  "$RUN_DIR/inventory" \
  "$RUN_DIR/evidence" \
  "$RUN_DIR/findings/agent-01" \
  "$RUN_DIR/findings/agent-02" \
  "$RUN_DIR/findings/agent-03" \
  "$RUN_DIR/findings/agent-04" \
  "$RUN_DIR/findings/agent-05" \
  "$RUN_DIR/verification/agent-06" \
  "$RUN_DIR/verification/agent-07" \
  "$RUN_DIR/verification/agent-08" \
  "$RUN_DIR/drafting" \
  "$RUN_DIR/final" \
  "$RUN_DIR/validation" \
  "$RUN_DIR/publish"

cat > "$RUN_DIR/STATUS.md" <<EOF
---
run_id: "$RUN_ID"
source_commit: "$SOURCE_COMMIT"
source_branch: "$SOURCE_BRANCH"
git_remote: "$GIT_REMOTE"
created_at: "$CREATED_AT"
status: "Initialized"
---

# Source Code Handover Run Status

| Field | Value |
|---|---|
| Run ID | \`$RUN_ID\` |
| Source Commit | \`$SOURCE_COMMIT\` |
| Source Branch | \`$SOURCE_BRANCH\` |
| Git Remote | \`$GIT_REMOTE\` |
| Execution Mode | \`unverified\` |
| Current Phase | Phase 0 - Preflight + Deterministic Discovery |
| Isolation Verified | no |

## Agent Execution Map

| Agent | Session ID/Subagent ID | Worktree | Canonical Artifact | Status | Gate |
|---|---|---|---|---|---|
| agent-01 | TBD | TBD | \`findings/agent-01/findings.md\` | Pending | Required |
| agent-02 | TBD | TBD | \`findings/agent-02/findings.md\` | Pending | Required |
| agent-03 | TBD | TBD | \`findings/agent-03/findings.md\` | Pending | Required |
| agent-04 | TBD | TBD | \`findings/agent-04/findings.md\` | Pending | Required |
| agent-05 | TBD | TBD | \`findings/agent-05/findings.md\` | Pending | Required |
| agent-06 | TBD | TBD | \`verification/agent-06/source-symbol-verification.md\` | Pending | Required |
| agent-07 | TBD | TBD | \`verification/agent-07/cross-layer-flow-map.md\` | Pending | Required |
| agent-08 | TBD | TBD | \`verification/agent-08/build-test-evidence.md\` | Pending | Required |
| agent-09 | TBD | TBD | \`final/01_project_handover_full.md\` to \`final/20_documentation_coverage.md\` | Pending | Required |
| agent-10 | TBD | TBD | \`validation/final-verdict.md\` | Pending | Required |

## Notes

- This run was initialized by \`.ai/scripts/init-source-code-handover-run.sh\`.
- Do not publish to \`docs/\` until Agent 10 writes \`PASS\` in \`validation/final-verdict.md\`.
EOF

cat > "$RUN_DIR/metadata/run.json" <<EOF
{
  "run_id": "$RUN_ID",
  "source_commit": "$SOURCE_COMMIT",
  "source_branch": "$SOURCE_BRANCH",
  "git_remote": "$GIT_REMOTE",
  "created_at": "$CREATED_AT",
  "status": "initialized"
}
EOF

printf "Initialized source-code handover run: %s\n" "$RUN_DIR"
