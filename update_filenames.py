import re

files_to_update = [
    ".ai/workflows/make-new-dev-docs.md",
    ".ai/agents/agent-07-single-handbook-aggregator.md",
    ".ai/rules/07-handover-documentation-dod.md"
]

replacements = [
    ("PROJECT_HANDOVER_FULL.md", "01_PROJECT_HANDOVER_FULL.md"),
    ("PROJECT_CONTEXT.md", "02_PROJECT_CONTEXT.md"),
    ("REPOSITORY_GUIDE.md", "03_REPOSITORY_GUIDE.md"),
    ("LOCAL_SETUP.md", "04_LOCAL_SETUP.md"),
    ("CONFIGURATION_REFERENCE.md", "05_CONFIGURATION_REFERENCE.md"),
    ("ARCHITECTURE.md", "06_ARCHITECTURE.md"),
    ("DATABASE_REFERENCE.md", "07_DATABASE_REFERENCE.md"),
    ("AUTH_AND_SECURITY.md", "08_AUTH_AND_SECURITY.md"),
    ("API_CATALOG.md", "09_API_CATALOG.md"),
    ("BACKGROUND_JOBS.md", "10_BACKGROUND_JOBS.md"),
    ("REALTIME_SIGNALR_SOCKET.md", "11_REALTIME_SIGNALR_SOCKET.md"),
    ("EXTERNAL_INTEGRATIONS.md", "12_EXTERNAL_INTEGRATIONS.md"),
    ("FRONTEND_GUIDE.md", "13_FRONTEND_GUIDE.md"),
    ("OPERATIONS_RUNBOOK.md", "14_OPERATIONS_RUNBOOK.md"),
    ("DEPLOYMENT_AND_CICD.md", "15_DEPLOYMENT_AND_CICD.md"),
    ("TESTING_GUIDE.md", "16_TESTING_GUIDE.md"),
    ("KNOWN_RISKS.md", "17_KNOWN_RISKS.md"),
    ("OPEN_QUESTIONS.md", "18_OPEN_QUESTIONS.md"),
    ("EVIDENCE_INDEX.md", "19_EVIDENCE_INDEX.md"),
    ("DOCUMENTATION_COVERAGE.md", "20_DOCUMENTATION_COVERAGE.md")
]

for filepath in files_to_update:
    with open(filepath, "r") as f:
        content = f.read()
    
    for old, new in replacements:
        # Be careful to only replace when preceded by `docs/`, `final/`, or `1. ` etc.
        # But wait, replacing them globally is mostly safe for these exact filenames.
        # Let's ensure we don't double replace (if it already has 01_)
        if old in content and new not in content:
            # We only replace exact filename matches
            content = re.sub(r'(?<![A-Z0-9_])' + re.escape(old), new, content)
            
    with open(filepath, "w") as f:
        f.write(content)

print("Updated filenames successfully.")
