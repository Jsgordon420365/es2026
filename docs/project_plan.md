# Search Everything Class-0 Project Plan

(Imported from C:\Users\jsgor\Downloads\search_everything_class_0_project_plan.md)

## Mission

Provide one canonical local search service that exposes Everything's indexed file discovery to multiple agent environments:

- Antigravity IDE / Gemini
- Codex CLI
- Gemini CLI
- Perplexity computer-use workflows
- Claude Code only when explicitly needed
- Cowork where applicable

The service should reduce human copy-paste and manual file hunting by giving models a safe, fast, structured way to find files, folders, and likely working roots.

## Core principles

1. Local-first
2. Subscription-first, not usage-priced APIs
3. One backend, many adapters
4. Read-first and minimally dangerous by default
5. Deterministic outputs before cleverness
6. Fast enough to feel instant
7. Usable from CLI, MCP, HTTP, and skill wrappers

## Phase 0: protocol and scope lock

Define the exact contract before code:

- search files
- search folders
- search full paths
- regex search
- extension filter
- date modified filter
- size filter
- limit / offset
- JSON output
- health check
- index-ready check
- open-containing-folder action descriptor only, not execution by default
- file-preview metadata only

## Phase 1: core wrapper around `es.exe`

Create a local executable service that:

- finds `es.exe`
- validates that Everything is running
- executes safe searches
- normalizes raw output
- returns structured JSON
- logs operations
- handles timeouts and empty results cleanly
