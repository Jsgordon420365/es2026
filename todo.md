# TODO

## Project Summary

Build a local-first Search Everything Class-0 backend around Voidtools Everything and `es.exe`, then expose it through practical adapters such as CLI and MCP.

## Phases

### Phase 0: Scope and Contract
- [x] Confirm repository structure
- [x] Define JSON output contract
- [x] Define error contract
- [x] Define health check behavior
- [x] Implement initial Pydantic models in models.py

### Phase 1: Core `es.exe` Wrapper
- [x] Implement config loading
- [x] Implement logging utilities
- [x] Implement `es.exe` discovery
- [x] Implement `es.exe` invocation
- [x] Implement query builder
- [x] Implement result parsing
- [x] Implement core service orchestration

### Phase 2: CLI and Tests
- [x] Implement CLI entrypoint
- [x] Add smoke tests
- [x] Add unit tests for query builder
- [x] Add unit tests for parser
- [x] Add unit tests for service behavior

### Phase 3: MCP
- [x] Implement MCP server
- [x] Define MCP tools
- [x] Test MCP integration locally

### Phase 4: Optional HTTP
- [ ] Implement local HTTP adapter
- [ ] Add local-only binding safeguards
- [ ] Test loopback-only operation

### Phase 5: Environment Notes
- [ ] Add Codex notes
- [ ] Add Gemini CLI notes
- [ ] Add Antigravity notes
- [ ] Add Perplexity notes
- [ ] Add Claude Code notes
- [ ] Add Cowork notes

## Next Smallest Step

Implement the MCP server using mcp-sdk-python to expose everything_search and everything_health tools.

## Decisions Made

- Python is the initial implementation language
- `es.exe` is the first backend
- The system is read-first in v1
- The project avoids pay-per-use APIs in the core flow

## Open Questions

- Will MCP be built directly in Python or through an auxiliary wrapper?
- Should the initial parser support CSV, tab-delimited output, or both?
- What is the exact minimal health check contract?
- How should exact-path lookup differ from normal search behavior?

## Blockers

- None yet