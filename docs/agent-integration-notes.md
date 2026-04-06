# Agent Integration Notes

This search service is a Class-0 primitive designed to be used by various agents.

## Codex CLI
Add a custom skill or run the CLI wrapper directly:
```powershell
.\scripts\run_cli.bat "Antigravity.md"
```

## Gemini CLI / Claude Desktop (MCP)
Add the following to your MCP configuration:

```json
{
  "mcpServers": {
    "everything": {
      "command": "python",
      "args": ["-m", "search_everything.mcp_server"],
      "env": {
        "PYTHONPATH": "c:\\Users\\jsgor\\Projects\\es2026\\src"
      }
    }
  }
}
```

## Antigravity IDE
The `everything_search` tool should be automatically available once the MCP server is configured in your environment.
Use it to find project roots and specific library files before you start coding to ensure you have the correct local context.

This project is intended to support:

- Antigravity IDE
- Codex CLI
- Gemini CLI
- Perplexity computer-use workflows
- Claude Code when necessary
- Cowork when necessary

The local search core should remain independent of any one agent environment.
Environment-specific wrappers should stay thin.