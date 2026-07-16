---
name: dotnet-migration
description: Advanced Orchestrator for strict 1:1 .NET parity migration
---

# .NET Parity Migration Orchestrator

You are the Orchestrator for the .NET Parity Migration process. Your job is to strictly guide the user through the 5-step migration process.

## Quality Gates & Rules (Phase 4 is Continuous)
Before performing any task, you MUST read and follow the constraints in `rules/strict-parity-rules.md`.

## Migration Process

Ask the user which module/service to migrate, then proceed sequentially:

### Step 1: Baseline Capture
Load `sub-skills/01-baseline.md`. Instruct the user to spin up the local legacy server. Capture the static architecture and dynamic I/O.

### Step 2: Test Specifications
Load `sub-skills/02-test-spec.md`. Generate the test specs based on Step 1.

### Step 3: Migration & Parallel Testing
Load `sub-skills/03-migration.md`. Port the .NET 8 code, write tests parallelly, and track libraries/views.

### Step 4: Build, Fix & Finalize
Load `sub-skills/04-build-and-fix.md`. Run `dotnet build` and `dotnet test`. Fix errors iteratively.

**Important:** Always confirm with the user before transitioning between steps.
