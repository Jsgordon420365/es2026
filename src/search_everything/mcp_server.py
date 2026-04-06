import logging
from mcp.server.fastmcp import FastMCP
from .config import load_config
from .service import SearchService
from .models import SearchRequest
from .logging_utils import setup_logging

# Load config and service
config = load_config()
service = SearchService(config)

# Create FastMCP server
mcp = FastMCP("Everything")

@mcp.tool()
def everything_search(query: str, limit: int = 100, regex: bool = False) -> str:
    """
    Search Everything for files and folders.
    
    Args:
        query: Search string (e.g., 'Antigravity.md', 'ext:py', 'C:\\Projects').
        limit: Maximum results (default 100).
        regex: Enable regex search.
    """
    request = SearchRequest(query=query, limit=limit, regex=regex)
    return service.search(request).model_dump_json(indent=2)

@mcp.tool()
def everything_search_folders(query: str, limit: int = 100) -> str:
    """Search for directories only matching the query."""
    request = SearchRequest(query=query, limit=limit, folders_only=True)
    return service.search(request).model_dump_json(indent=2)

@mcp.tool()
def everything_locate_exact(path: str) -> str:
    """Locate a file or folder by its exact absolute path."""
    # We wrap the path in quotes for exact match in Everything
    request = SearchRequest(query=f'"{path}"', limit=1)
    return service.search(request).model_dump_json(indent=2)

@mcp.tool()
def everything_recent_files(limit: int = 10) -> str:
    """List the most recently modified files across all indexed volumes."""
    # 'dm:today' or just sorting by dm
    # es.exe uses sort:dm-desc usually if we add it to the query
    request = SearchRequest(query="sort:dm-desc", limit=limit)
    return service.search(request).model_dump_json(indent=2)

@mcp.tool()
def everything_health() -> str:
    """Check the connection to the Everything service and es.exe path."""
    return service.check_health().model_dump_json(indent=2)

if __name__ == "__main__":
    # Ensure logs don't interfere with MCP protocol (stdio)
    setup_logging(level=logging.ERROR, log_file=config.log_file)
    mcp.run()