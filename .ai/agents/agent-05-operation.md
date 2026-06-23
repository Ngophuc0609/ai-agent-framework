# Agent 5: Operations, Jobs & Realtime

## Vietnamese User Summary

Agent này đảm nhiệm Sổ tay Vận hành, SignalR/Sockets, và Background Jobs. Viết hoàn toàn bằng tiếng Việt.

## Allowed Write Paths

- `.ai/runs/source-code-handover/<run_id>/findings/agent-05/findings.md`
- `draft-docs/agent-05-findings.md`

## Required Output Details & Definition of Done

1. **Background Jobs Inventory & Cards**:
   - Quét toàn bộ IHostedService, BackgroundService, Hangfire, Quartz, Timer, v.v.
   - Job Card: `ID | Tên | Cơ chế | Trigger | Lịch chạy | Input | Output/Side effect | Dependency | Retry | Failure behavior | Monitoring`. Sequence diagram cho job quan trọng.
2. **Realtime / SignalR / Sockets**:
   - Hub inventory: `Hub ID | Class | Route | Auth policy | Evidence`.
   - Connection contract: URL, protocol, CORS, transport, reconnect policy, scale-out (Redis backplane).
   - Event contract (Client->Server & Server->Client): `Event | Payload DTO | Trigger | Receiver`.
   - Realtime Smoke test.
3. **Operations Runbook (Docker/Nginx/Redis/Logs)**:
   - Compose file topology, volume, port map, env sources. Nginx routing, TLS cert paths.
   - Serilog sinks, log retention, PII masking.
   - Redis role (Cache vs DataProtection vs SignalR).
4. **Incident & Disaster Recovery**:
   - Backup/restore ops, Rollback steps, Secret rotation. Incident runbooks cho lỗi Login/Redis/DB/Mail.
