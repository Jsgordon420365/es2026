# Search Everything Class-0 Project

This project turns Voidtools Everything into a dependable local retrieval layer for coding agents and orchestration tools, with zero pay-per-use API dependency.

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

## Recommended architecture

### Canonical backend

Build a single Windows-native backend service called `search-everything-core`.

It should support multiple transport or adapter layers:

- ES adapter using `es.exe`
- Optional DLL adapter for higher-performance later
- MCP server adapter
- Local HTTP adapter
- Thin CLI wrapper
- Agent-specific prompt/skill wrappers

### Why this shape

If you build five integrations first, you will own five brittle little kingdoms. If you build one core with adapters, you own a train station.

## Phase order

### Phase 0: protocol and scope lock

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

### Phase 1: core wrapper around `es.exe`

Create a local executable service that:

- finds `es.exe`
- validates that Everything is running
- executes safe searches
- normalizes raw output
- returns structured JSON
- logs operations
- handles timeouts and empty results cleanly

### Phase 2: MCP server

Expose the same contract as MCP tools so agent environments that support MCP can use it directly.

Candidate tool set:

- `everything_search`
- `everything_search_folders`
- `everything_locate_exact`
- `everything_recent_files`
- `everything_health`
- `everything_explain_query`

### Phase 3: agent wrappers

Add environment-specific wrappers:

- Codex helper docs and launcher
- Gemini CLI MCP config
- Antigravity integration notes and prompts
- Perplexity computer-use helper scripts
- Claude Code adapter only if needed
- Cowork workflow notes if it supports external tools or bridge scripts

### Phase 4: advanced connectors

After the stable path works:

- HTTP local service for tools that prefer REST
- direct DLL adapter
- ETP / FTP bridge when useful
- optional reranking using local or subscription-included frontier models only when a deterministic search returns too much

## Initial repo shape

```text
search-everything-class0/
  README.md
  docs/
    vision.md
    architecture.md
    mcp-tools.md
    agent-integration-notes.md
    safety-model.md
    test-plan.md
  src/
    search_everything/
      __init__.py
      config.py
      logging_utils.py
      models.py
      es_client.py
      query_builder.py
      result_parser.py
      service.py
      health.py
      mcp_server.py
      http_server.py
      cli.py
  tests/
    test_query_builder.py
    test_result_parser.py
    test_service.py
    test_health.py
  scripts/
    run_cli.bat
    run_mcp.bat
    run_http.bat
    smoke_test.bat
  examples/
    codex/
    gemini-cli/
    antigravity/
    perplexity/
    claude-code/
    cowork/
```

## Success criteria

The project is successful when:

- a model can ask for likely project roots and get them in seconds
- a model can search by name, path, extension, recency, or regex without human translation
- the same backend works across at least Codex CLI and Gemini CLI
- all output is structured and copy-safe
- the tool fails loudly and clearly instead of hallucinating paths

## Guardrails

- No pay-per-use APIs in core flow
- No cloud dependency for search
- No write actions in v1 except optional explicit opt-in wrappers
- No autonomous file opening or execution unless separately authorized
- Prefer loopback-only local services
- Treat local web-fetch capable agents carefully because localhost access can widen the blast radius

## Best implementation bet

Python is the strongest v1 choice because it is fast to build, easy to wrap for MCP and HTTP, and straightforward for subprocess control around `es.exe`.

If performance or packaging becomes annoying later, a Rust rewrite can come in after the interface stabilizes.

## Recommended near-term deliverables

1. Contract spec
2. `es.exe` wrapper with JSON output
3. MCP server
4. Gemini CLI example config
5. Codex usage notes
6. Smoke tests
7. Windows packaging notes

## What not to overbuild yet

Do not begin with:

- direct DLL bindings
- multi-host distributed search
- semantic embeddings
- automatic file mutation
- cross-machine sync logic
- fancy UI

Those are dessert. Right now you need a spoon.

## Product framing

This is not merely a search tool.

It is a Class-0 agent primitive.

It answers the question: “Before an agent can act, how does it know where reality is on disk?”

That makes it foundational infrastructure for local-first orchestration.

