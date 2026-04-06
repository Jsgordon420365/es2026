# Architecture

## Canonical backend

The first backend uses Voidtools Everything through `es.exe`.

## Adapters

- CLI
- MCP
- Optional local HTTP

## Core modules

- Configuration
- Logging
- Models
- Query builder
- `es.exe` client
- Result parser
- Service orchestration
- Health checks

## Rule

One backend, many adapters.
Do not fork logic by agent environment unless truly necessary.