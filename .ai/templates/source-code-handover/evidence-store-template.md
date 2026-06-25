# Source Code Handover Evidence Store Template

Use this template for the machine-readable evidence store:

```text
.ai/runs/source-code-handover/<run_id>/evidence/
```

All files are AI-facing and MUST be written in English. Secret values MUST be redacted while preserving key names.

Agent 1-5 findings may contain `DISC-*` discovery IDs. The evidence store is the verified evidence layer. Final documentation may only cite `EV-*` IDs that Agents 6-8 have promoted or verified.

## `tool-runs.jsonl`

One JSON object per tool attempt:

```json
{"run_id":"<run_id>","agent_id":"agent-XX","tool_category":"fast_search|build|symbol|semantic|pattern_scan|sql_metadata|api_contract|runtime_artifact|git_history|manual_slice","tool":"rg","query":"<query or command>","working_directory":"<path>","target":"<route/symbol/table/key/job/config>","status":"complete|partial|failed|tool_unavailable|not_applicable|blocked","output_artifact":"evidence/<artifact>.json","started_at":"<ISO-8601>","completed_at":"<ISO-8601>","limitation":"<none or reason>"}
```

## `evidence-manifest.json`

Top-level shape:

```json
{
  "run_id": "<run_id>",
  "source_commit": "<git_sha>",
  "generated_at": "<ISO-8601>",
  "evidence": [
    {
      "evidence_id": "EV-API-001",
      "claim": "<claim>",
      "source_type": "source|sql|api_contract|runtime|git_history|negative",
      "source_path": "<path-or-object>",
      "range_or_symbol": "<line-range-or-symbol>",
      "verification_type": "Source|CodeGraph|Roslyn|CodeQL|Semgrep|SQL metadata|OpenAPI|Postman|Runtime|Negative evidence",
      "producing_agent": "agent-06|agent-07|agent-08",
      "promoted_from": ["DISC-API-001"],
      "final_documents": ["09_api_catalog.md"],
      "status": "[CONFIRMED]"
    }
  ]
}
```

Rules:

- `EV-*` IDs used by final docs MUST appear here.
- Final-doc `EV-*` IDs MUST NOT be produced directly by Agent 1-5. Agent 1-5 findings are discovery inputs; Agents 6-8 perform promotion after source/symbol, flow/conflict, and safety/runtime verification.
- `source_type=source` evidence MUST include a repository file path in `source_path` and an exact line range or symbol in `range_or_symbol`.
- Runtime, SQL, API contract, and git-history evidence MUST point to a concrete object, artifact, query, or exported source.

## `focused-slices.json`

Records exact slices admitted into model context:

```json
{
  "slices": [
    {
      "slice_id": "SLICE-API-001",
      "evidence_id": "EV-API-001",
      "source_type": "source",
      "source_path": "src/Api/Controllers/AccountsController.cs",
      "range_or_symbol": "AccountsController.Create lines 42-97",
      "reason": "Supports account creation route, channel_id fallback, and response contract."
    }
  ]
}
```

Final-doc `EV-*` IDs MUST have focused slices unless they are pure negative evidence with an explicit negative-evidence search record.

## `symbol-reference-map.json`

Records definitions, references, implementations, callers, and call chains used for claims.

## `data-flow-map.json`

Records request-to-controller-to-service-to-repository-to-SQL/Redis/job/external paths for high-risk flows.

## `sql-metadata.json`

Records table, column, key, index, procedure, function, trigger, constraint, view, and relationship metadata. If no database exists, record `status: "not_applicable"` with negative evidence.

Minimum shape when a database exists:

```json
{
  "dbcontexts": [
    {
      "name": "ConfigurationDbContext",
      "source_path": "src/Data/ConfigurationDbContext.cs",
      "registration": "Startup.ConfigureServices",
      "connection_string_key": "ConfigurationDbConnection",
      "migration_assembly": "Project.EntityFramework",
      "status": "[CONFIRMED]"
    }
  ],
  "tables": [
    {
      "table": "Clients",
      "schema": "dbo",
      "entity": "Client",
      "mapping_source": "Fluent API + migration",
      "columns": [
        {
          "name": "ClientId",
          "clr_type": "string",
          "db_type": "nvarchar(200)",
          "nullable": false,
          "key_or_index": "unique index",
          "meaning": "OAuth client identifier",
          "evidence_id": "EV-DB-022"
        }
      ]
    }
  ]
}
```

## `api-contract-sources.json`

Records Swagger/OpenAPI, Postman, integration tests, API traffic samples, or limitations used for API contract evidence.

Minimum shape when APIs exist:

```json
{
  "endpoints": [
    {
      "api_id": "API-CLIENT-001",
      "route": "/Clients/Create",
      "method": "POST",
      "action": "ClientsController.Create",
      "source_path": "src/Admin/Controllers/ClientsController.cs",
      "request_fields": [
        {"name": "ClientId", "type": "string", "required": true, "validation": "required"}
      ],
      "response_fields": [
        {"name": "ModelState", "type": "validation errors", "condition": "invalid request"}
      ],
      "status_codes": ["200", "302", "400"],
      "evidence_ids": ["EV-API-041"]
    }
  ]
}
```

## `runtime-artifacts.json`

Records logs, Hangfire export, Redis snapshot, API traffic sample, database query logs, or limitations.

Background job and realtime runtime evidence MUST include flow/runtime coverage or explicit limitations:

```json
{
  "background_jobs": [
    {
      "job": "TokenCleanupJob",
      "registration": "Startup.ConfigureServices",
      "trigger": "recurring schedule",
      "handler": "TokenCleanupJob.Execute",
      "retry_or_failure_behavior": "Hangfire retry/logging source",
      "runtime_status": "verified|not_verified|blocked",
      "evidence_ids": ["EV-JOB-001", "EV-OPS-012"]
    }
  ],
  "realtime": [
    {
      "event": "newDeviceLogin",
      "hub": "AccountHub",
      "producer": "SignalController.SendNewDeviceLogin",
      "consumer": "web client handler",
      "payload_fields": ["userId", "device", "time"],
      "runtime_status": "verified|not_verified|blocked",
      "evidence_ids": ["EV-RT-011", "EV-API-066"]
    }
  ]
}
```

## `tool-limitations.json`

Records unavailable tools and readiness impact:

```json
{
  "limitations": [
    {
      "tool_category": "semantic",
      "tool": "CodeQL",
      "status": "tool_unavailable",
      "impact": "High-risk data-flow claims must remain [UNVERIFIED] or be validated with Roslyn/call graph alternative.",
      "readiness_impact": "Partial"
    }
  ]
}
```

## Mini Examples

Good promoted evidence:

```json
{
  "evidence_id": "EV-API-014",
  "claim": "POST /quiz-submit is implemented by QuizSubmitController.Submit.",
  "source_type": "source",
  "source_path": "src/WebApi/Controllers/QuizSubmitController.cs",
  "range_or_symbol": "QuizSubmitController.Submit",
  "verification_type": "Source + Symbol",
  "producing_agent": "agent-06",
  "promoted_from": ["DISC-API-014"],
  "final_documents": ["09_api_catalog.md"],
  "status": "[CONFIRMED]"
}
```

Bad evidence:

```json
{
  "evidence_id": "EV-BIZ-001",
  "claim": "Accounts module manages accounts.",
  "source_type": "source",
  "source_path": "unknown",
  "range_or_symbol": "unknown",
  "verification_type": "Model context",
  "producing_agent": "agent-01",
  "status": "[CONFIRMED]"
}
```

Reject the bad evidence because Agent 1-5 cannot produce final proof, the claim is generic, and the source cannot be physically verified.
