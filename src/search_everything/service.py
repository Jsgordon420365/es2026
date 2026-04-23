import time
from pathlib import Path
from .models import SearchRequest, SearchResponse, EverythingHealth
from .config import Config
from .es_client import ESClient
from .query_builder import QueryBuilder
from .result_parser import parse_all_results
from .logging_utils import get_logger

logger = get_logger(__name__)

class SearchService:
    """Orchestrates search operations using the Everything CLI backend."""
    
    def __init__(self, config: Config):
        self.config = config
        self.client = ESClient(es_path=config.es_path)
        self.query_builder = QueryBuilder()

    def check_health(self) -> EverythingHealth:
        """Check if Everything and es.exe are ready to use."""
        resolved_path = self.client.resolve_path()
        is_running = self.client.is_everything_running()
        return EverythingHealth(
            everything_running=is_running,
            es_found=resolved_path is not None and Path(resolved_path).exists(),
            es_path=resolved_path
        )

    def search(self, request: SearchRequest) -> SearchResponse:
        """Perform a search and return a validated response."""
        start_time = time.perf_counter()
        
        # Build Everything-specific syntax
        effective_query = self.query_builder.build_query(
            request.query,
            folders_only=request.folders_only,
            files_only=request.files_only
        )
        
        # Fetch raw data
        raw_data = self.client.run_query(
            effective_query,
            limit=request.limit,
            regex=request.regex
        )
        
        # Transform to internal models
        results = parse_all_results(raw_data)
        
        took_ms = (time.perf_counter() - start_time) * 1000
        logger.info(f"Searched '{effective_query}' - Found {len(results)} results in {took_ms:.2f}ms")
        
        return SearchResponse(
            results=results,
            count=len(results),
            total=len(results), # Placeholder for total without limit
            query=effective_query,
            took_ms=took_ms
        )