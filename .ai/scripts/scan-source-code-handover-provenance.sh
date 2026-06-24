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
  "Pa\$\$word123"
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
  MATCHES=$(grep -Hn -E "$pattern" $(find $TARGET_DIR -name "*.md") 2>/dev/null | grep -v "\[UPSTREAM_REFERENCE\]")
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
