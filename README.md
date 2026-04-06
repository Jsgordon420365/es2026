# Search Everything Class-0 Project

This repository is the local-first build space for a Search Everything Class-0 toolchain centered on Voidtools Everything and `es.exe`.

The purpose of this repository is to create one canonical backend that can expose fast local file and folder discovery to agent environments without relying on pay-per-use APIs.

## Primary goals

1. Build a deterministic, local-first search layer around `es.exe`.
2. Expose that search layer through clean interfaces such as CLI, MCP, and optional local HTTP.
3. Make the tool usable from Antigravity IDE, Codex CLI, Gemini CLI, Perplexity computer-use workflows, and sparingly Claude Code or Cowork when necessary.
4. Keep the search layer read-first, safe, transparent, and structured.

## Repository shape

- `docs/` contains plans, architecture, integration notes, safety notes, and tracking files.
- `src/` contains the implementation.
- `tests/` contains validation and smoke tests.
- `scripts/` contains bootstrap and launch scripts.
- `examples/` contains environment-specific examples and notes.
- `logs/` contains local logs and generated diagnostics.
- `artifacts/` contains generated outputs or temporary project artifacts.

## Usage

### CLI
Search using the provided script:
```powershell
.\scripts\run_cli.bat "your query"
```

### Health Check
```powershell
.\scripts\run_cli.bat --health
```

### MCP
Register the server in your MCP config (see `docs/agent-integration-notes.md` for details).
```powershell
.\scripts\run_mcp.bat
```

## Project Status

- [x] **Phase 0**: Protocol and Pydantic Models.
- [x] **Phase 1**: `es.exe` Wrapper with version detection.
- [x] **Phase 2**: CLI and Smoke Test Suite.
- [x] **Phase 3**: MCP Server (FastMCP).
- [ ] **Phase 4**: Optional HTTP adapter (Planned).
- [x] **Phase 5**: Environment integration notes.

## Build sequence

1. Define the contract and JSON output shape.
2. Build the `es.exe` wrapper.
3. Add health checks and smoke tests.
4. Add MCP server support.
5. Add environment-specific integration notes and launch flows.
6. Expand only after the deterministic core is stable.