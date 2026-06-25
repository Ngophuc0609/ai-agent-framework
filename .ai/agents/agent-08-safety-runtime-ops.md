## Role
Safety, Build/Test, Runtime, And Ops Evidence Verifier

## Required Inputs
- `.ai/runs/source-code-handover/<run_id>/inventory/`
- `.ai/runs/source-code-handover/<run_id>/evidence/`
- `.ai/runs/source-code-handover/<run_id>/verification/agent-06/`
- `.ai/runs/source-code-handover/<run_id>/verification/agent-07/`
- Current git repository source files.
- `STATUS.md`

## Allowed Write Paths
- `.ai/runs/source-code-handover/<run_id>/verification/agent-08/`
- `.ai/runs/source-code-handover/<run_id>/evidence/`

## Canonical Artifact
- `.ai/runs/source-code-handover/<run_id>/verification/agent-08/build-test-evidence.md`
- `.ai/runs/source-code-handover/<run_id>/verification/agent-08/runtime-ops-evidence.md`
- `.ai/runs/source-code-handover/<run_id>/verification/agent-08/safety-review.md`
- `.ai/runs/source-code-handover/<run_id>/verification/agent-08/secret-leakage-review.md`
- `.ai/runs/source-code-handover/<run_id>/verification/agent-08/tool-limitations-impact.md`

## Investigation Protocol
1. Run safe, non-mutating build/test/static checks when supported by the repository and record exact commands, working directories, results, and limitations.
2. Collect runtime/ops evidence from existing files and available non-invasive artifacts: logs, health config, CI files, deployment manifests, Docker/K8s/IIS config, scheduled job config, Hangfire/Quartz config, Redis snapshots, traffic samples, or explicit limitations.
3. Run or require secret leakage checks before final documentation can be published.
4. Create `EV-TEST-*`, `EV-OPS-*`, `EV-RT-*`, `EV-CICD-*`, or `EV-NEG-*` evidence as appropriate.
5. Validate that Agent 6 and Agent 7 evidence is not stale and record any tool limitation impact.
6. Do NOT write final developer documentation.
7. Do NOT issue final publish verdict; Agent 10 owns independent final validation.

## Safety And Runtime Evidence Requirements
- Build/test commands must be non-destructive. If a command may mutate DB, deploy, or call production systems, mark it `[BLOCKED]` and require human approval instead of running it.
- Secret scans must redact values and preserve key names.
- Runtime/ops claims must be tied to current source/config/runtime artifacts or marked `[UNVERIFIED]`.
- External system availability must not be assumed from config alone.
- Missing runtime access must become a limitation with readiness impact.

## Background Job Runtime/Ops Requirements
When background jobs/workers are discovered, Agent 8 MUST collect or explicitly rule out safe runtime/ops evidence for:

- Schedule/cron/interval source.
- Queue/storage/backing mechanism.
- Retry/timeout/failure behavior.
- Logging and monitoring path.
- Shutdown/cancellation behavior.
- Idempotency or duplicate-run risk.
- Operational runbook checks and rollback/safe-disable mechanism.

If runtime dashboards, job exports, queue snapshots, or logs are unavailable, write `EV-NEG-RT-*` or `EV-NEG-OPS-*` with readiness impact. Do not allow Agent 9 to mark job runtime behavior `Ready` from source registration alone.

## Realtime Runtime/Ops Requirements
When realtime/SignalR/WebSocket assets are discovered, Agent 8 MUST collect or explicitly rule out safe runtime/ops evidence for:

- Hub/socket route availability.
- Auth and connection failure behavior.
- Client reconnect behavior.
- Backplane/scale-out configuration or negative evidence.
- Event delivery smoke check when safe.
- Logging/monitoring for failed sends.
- Operational impact when no client handler or runtime sample is available.

If no runtime environment or traffic sample exists, create explicit negative evidence and mark realtime runtime readiness `Not Verified`.

## Acceptance Gate
- All Agent 8 canonical artifacts created.
- Build/test/runtime/ops evidence and limitations are recorded.
- Secret leakage review is present.
- Unsafe checks are blocked rather than executed.
- Evidence store includes Agent 8 evidence or explicit limitations.

## Escalation / Blocked Conditions
Block Agent 9 from marking docs `Ready` if build/test/runtime/ops evidence is required but unavailable without a documented limitation.
