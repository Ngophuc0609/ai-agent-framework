import re
import os

files_to_update = [
    ".ai/workflows/make-new-dev-docs.md",
    ".ai/agents/agent-07-single-handbook-aggregator.md",
    ".ai/rules/07-handover-documentation-dod.md"
]

replacements = {
    "01_PROJECT_HANDOVER_FULL.md": "01_project_handover_full.md",
    "02_PROJECT_CONTEXT.md": "02_project_context.md",
    "03_REPOSITORY_GUIDE.md": "03_repository_guide.md",
    "04_LOCAL_SETUP.md": "04_local_setup.md",
    "05_CONFIGURATION_REFERENCE.md": "05_configuration_reference.md",
    "06_ARCHITECTURE.md": "06_architecture.md",
    "07_DATABASE_REFERENCE.md": "07_database_reference.md",
    "08_AUTH_AND_SECURITY.md": "08_auth_and_security.md",
    "09_API_CATALOG.md": "09_api_catalog.md",
    "10_BACKGROUND_JOBS.md": "10_background_jobs.md",
    "11_REALTIME_SIGNALR_SOCKET.md": "11_realtime_signalr_socket.md",
    "12_EXTERNAL_INTEGRATIONS.md": "12_external_integrations.md",
    "13_FRONTEND_GUIDE.md": "13_frontend_guide.md",
    "14_OPERATIONS_RUNBOOK.md": "14_operations_runbook.md",
    "15_DEPLOYMENT_AND_CICD.md": "15_deployment_and_cicd.md",
    "16_TESTING_GUIDE.md": "16_testing_guide.md",
    "17_KNOWN_RISKS.md": "17_known_risks.md",
    "18_OPEN_QUESTIONS.md": "18_open_questions.md",
    "19_EVIDENCE_INDEX.md": "19_evidence_index.md",
    "20_DOCUMENTATION_COVERAGE.md": "20_documentation_coverage.md"
}

for filepath in files_to_update:
    with open(filepath, "r") as f:
        content = f.read()
    
    for old, new in replacements.items():
        content = content.replace(old, new)
            
    with open(filepath, "w") as f:
        f.write(content)

# Update agent-03
agent_03_path = ".ai/agents/agent-03-api-postman.md"
with open(agent_03_path, "r") as f:
    content = f.read()
content = content.replace("Flow diagram cho endpoint quan trọng.", "Flow diagram (Sequence Logic Diagram) bắt buộc cho các hàm phức tạp và endpoint quan trọng.")
content = content.replace("KHÔNG ĐƯỢC TỰ BỊA", "KHÔNG ĐƯỢC TỰ BỊA NỘI DUNG (NO HALLUCINATION) - BẮT BUỘC CÓ CODE EVIDENCE CHỨNG MINH")
with open(agent_03_path, "w") as f:
    f.write(content)

# Update agent-05
agent_05_path = ".ai/agents/agent-05-operation.md"
with open(agent_05_path, "r") as f:
    content = f.read()
content = content.replace("Sequence diagram cho job quan trọng.", "BẮT BUỘC vẽ Sequence diagram đầy đủ cho các Background Job phức tạp/quan trọng.")
content = content.replace("Realtime Smoke test.", "Realtime Smoke test. BẮT BUỘC vẽ Sequence diagram logic cho các flow realtime (Socket/SignalR) quan trọng.")
with open(agent_05_path, "w") as f:
    f.write(content)

# Update agent-01
agent_01_path = ".ai/agents/agent-01-source-local.md"
with open(agent_01_path, "r") as f:
    content = f.read()
content = content.replace("You MUST provide verifiable evidence for all of the following:", "CRITICAL: You MUST provide exact code evidence (file/line/commit) for EVERYTHING. ABSOLUTELY NO HALLUCINATING.")
with open(agent_01_path, "w") as f:
    f.write(content)

print("Updated filenames and added strict sequence diagram & evidence requirements.")
