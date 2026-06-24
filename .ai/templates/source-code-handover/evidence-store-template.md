# Source Code Handover Evidence Store Template

Use this template for the machine-readable evidence store:

```text
.ai/runs/source-code-handover/<run_id>/evidence/
```

All files are AI-facing and MUST be written in English. Secret values MUST be redacted while preserving key names.

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
      "producing_agent": "agent-XX",
      "final_documents": ["09_api_catalog.md"],
      "status": "[CONFIRMED]"
    }
  ]
}
```

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

## `symbol-reference-map.json`

Records definitions, references, implementations, callers, and call chains used for claims.

## `data-flow-map.json`

Records request-to-controller-to-service-to-repository-to-SQL/Redis/job/external paths for high-risk flows.

## `sql-metadata.json`

Records table, column, key, index, procedure, function, trigger, constraint, view, and relationship metadata. If no database exists, record `status: "not_applicable"` with negative evidence.

## `api-contract-sources.json`

Records Swagger/OpenAPI, Postman, integration tests, API traffic samples, or limitations used for API contract evidence.

## `runtime-artifacts.json`

Records logs, Hangfire export, Redis snapshot, API traffic sample, database query logs, or limitations.

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
