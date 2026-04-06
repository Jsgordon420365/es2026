# Antigravity IDE Build Instructions

You are working inside the repository for a local-first Search Everything Class-0 project.

Your job is to continue from the existing scaffold and build this repository forward in small, deterministic, testable steps.

## Core mission

Build a Windows-first local search service around Voidtools Everything using `es.exe` as the first implementation backend.

The system must avoid pay-per-use APIs in the core flow.
The search layer must be local-first, read-first, structured, and deterministic.

## Repository intent

This repository should evolve toward one canonical search backend with multiple adapters.

The target adapters are:

1. CLI wrapper
2. MCP server
3. Optional local HTTP server
4. Thin environment notes and wrappers for external tools

The build order matters.
Do not start with advanced features.
Do not start with semantic ranking.
Do not start with file mutation.
Do not start with a UI.

## First required action

Create a `todo.md` file in the repository root if it does not already exist.

That file must be used as the primary project planning and progress tracking document.
It must include:

1. A short project summary
2. Phases
3. Concrete tasks
4. Status markers for each task
5. Notes on blockers
6. A section called `Next Smallest Step`
7. A section called `Decisions Made`
8. A section called `Open Questions`

Keep `todo.md` current as you work.

## Implementation priorities

Work in the following order unless a local blocker makes a nearby reorder necessary:

1. Define models and the JSON output contract
2. Implement configuration loading
3. Implement logging utilities
4. Implement `es.exe` discovery and invocation
5. Implement query building
6. Implement result parsing
7. Implement service orchestration
8. Implement health checks
9. Implement CLI entrypoint
10. Implement tests
11. Implement MCP server
12. Implement optional HTTP adapter

## Required implementation constraints

- Use Python for the initial implementation
- Keep write actions out of v1
- Prefer explicit errors over silent failure
- Prefer structured JSON over ad hoc text output
- Keep functions small and testable
- Avoid unnecessary dependencies
- Make Windows paths first-class
- Preserve compatibility with running from PowerShell

## Expected source files

You should build toward these Python modules under `src/search_everything/`:

- `__init__.py`
- `config.py`
- `logging_utils.py`
- `models.py`
- `es_client.py`
- `query_builder.py`
- `result_parser.py`
- `service.py`
- `health.py`
- `cli.py`
- `mcp_server.py`
- `http_server.py`

You should also build tests under `tests/`.

## Required documentation behavior

As you build, update the relevant docs in `docs/`.
Do not leave the repository with code that has no explanation.
Prefer concise, concrete documentation.

## Safety and behavior constraints

- Assume `Everything` may not be running and detect that cleanly
- Assume `es.exe` may not be on PATH and detect that cleanly
- Never fabricate paths
- Never fabricate result counts
- Never claim success without validating it
- Always create or update tests when behavior changes materially

## Definition of done for the first milestone

The first milestone is complete when:

1. A user can run a PowerShell command that invokes the Python CLI
2. The tool can confirm health status
3. The tool can execute a basic search through `es.exe`
4. The tool returns structured JSON
5. At least a minimal smoke test suite passes

## Development style

Work incrementally.
Use the `todo.md` file actively.
Before large changes, state the specific small step being taken.
After changes, update `todo.md` with what changed and what remains.

## Important note

This repository exists to reduce the amount of manual file hunting required from the human.
That purpose should guide design decisions whenever there is doubt.