# .NET Parity Migration Skill Package (Advanced V2)

## Overview
This is a comprehensive, 5-step Antigravity CLI skill package for 1:1 parity migration from legacy .NET to modern .NET 8+. It combines static analysis, dynamic API capturing (Co-pilot mode), and parallel unit test generation to guarantee exact behavior retention.

## Workflow Phases

### Phase 1: Baseline Capture (`01-baseline`)
*   **Static Analysis:** Scans legacy projects, generates Sequence Diagrams (Mermaid), and documents business logic for services, background jobs, and real-time components.
*   **Dynamic Capture:** In Co-pilot mode, the Human Dev runs the legacy server locally. The Agent invokes the local endpoints with mock data to capture exact input/output payloads (casing, headers, exact types).

### Phase 2: Test Spec Generation (`02-test-spec`)
*   Generates comprehensive Test Specifications for each service, background job, and real-time logic based on Phase 1 baselines.

### Phase 3: Parity Migration (`03-migration`)
*   Ports code to .NET 8+.
*   Writes Unit Tests in parallel with the code based on the Test Spec.
*   Tracks library upgrades (logs unsupported/custom libraries to `library-report.md`).
*   Documents hidden bugs in `deferred-issues.md` without fixing them.
*   Migrates unaffected frontend views (e.g., React) as-is; flags affected views for update.

### Phase 4: Rules Enforcement (Continuous)
*   Enforces strict formatting: exact casing, exact error shapes, and 1:1 logical parity. See `rules/strict-parity-rules.md`.

### Phase 5: Build & Fix (`04-build-and-fix`)
*   Builds the .NET 8+ project, fixes compilation errors, upgrades necessary Nuget packages, runs the unit tests, and finalizes all reports.

## How to Use
Type `/skill dotnet-migration` in your Antigravity CLI to start the Orchestrator.
