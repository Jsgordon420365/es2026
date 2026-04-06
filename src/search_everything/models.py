from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field

class SearchResult(BaseModel):
    """A single search result entry from Everything."""
    path: str
    name: str
    extension: str
    size: int
    modified_at: datetime
    is_directory: bool = False

class SearchResponse(BaseModel):
    """Standard search response structure."""
    results: List[SearchResult]
    count: int
    total: int
    query: str
    took_ms: float

class SearchRequest(BaseModel):
    """Configuration for an Everything search request."""
    query: str
    limit: int = 100
    offset: int = 0
    folders_only: bool = False
    files_only: bool = False
    regex: bool = False

class EverythingHealth(BaseModel):
    """Status of the local Everything environment."""
    status: str = "ok"
    everything_running: bool
    es_found: bool
    es_path: Optional[str] = None
    version: str = "0.1.0"

class ErrorResponse(BaseModel):
    """A standard error container."""
    error: str
    message: str
    code: int