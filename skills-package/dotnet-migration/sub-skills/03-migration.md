# Sub-skill: 03 Migration & Parallel Testing

## Purpose
Port the code and write tests strictly following the Test Spec and Rules.

## Code & Test Generation
1. Create the .NET 8 base structure for the module.
2. Implement the functions and write the corresponding Unit Tests in parallel.

## Library Management
1. Note all required legacy libraries.
2. Attempt to map them to .NET 8 equivalents.
3. If a library has no replacement or is custom, log it into `templates/library-report.md`.

## Views & Frontend
1. If the legacy app has frontend views (e.g., React) that are unaffected by the API update, copy them over EXACTLY as-is and configure them to pack/run on .NET 8.
2. If views are affected, explicitly flag them for the human developer.

## Hidden Bugs
If you discover hidden logical bugs during migration, DO NOT FIX THEM. Keep the legacy logic, and log the bug into `templates/deferred-issues.template.md`.
