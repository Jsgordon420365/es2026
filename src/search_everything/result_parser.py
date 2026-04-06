import os
from datetime import datetime
from typing import List, Dict, Any, Optional
from .models import SearchResult
from .logging_utils import get_logger

logger = get_logger(__name__)

def parse_size(size_str: Optional[str]) -> int:
    """Safely parse size string from es.exe."""
    if not size_str:
        return 0
    try:
        return int(size_str.replace(",", ""))
    except (ValueError, TypeError):
        return 0

def is_directory_from_attrib(attrib_str: Optional[str]) -> bool:
    """Check if 'D' (Directory/Folder) is present in the attributes."""
    if not attrib_str:
        return False
    return "D" in attrib_str.upper()

def parse_es_result(raw_result: Dict[str, Any]) -> SearchResult:
    """Map a single es.exe CSV dictionary to a SearchResult model."""
    path = raw_result.get("Filename", "")
    if not path:
        # If 'Filename' is missing, try lowercase 'filename' or first key
        path = raw_result.get("filename", next(iter(raw_result.values()), ""))
        
    name = os.path.basename(path)
    if not name and path:
        name = path 
        
    # Attempt to infer extension if missing
    extension = raw_result.get("Extension", "")
    if not extension and "." in name:
        extension = name.split(".")[-1]

    # Handle missing date with a fallback to now
    modified_at_raw = raw_result.get("Date Modified")
    if not modified_at_raw:
        modified_at = datetime.now()
    else:
        modified_at = modified_at_raw

    return SearchResult(
        path=path,
        name=name,
        extension=extension,
        size=parse_size(raw_result.get("Size")),
        modified_at=modified_at,
        is_directory=is_directory_from_attrib(raw_result.get("Attributes"))
    )

def parse_all_results(raw_results: List[Dict[str, Any]]) -> List[SearchResult]:
    """Parse a list of results, skipping those that fail validation."""
    parsed = []
    for raw in raw_results:
        try:
            res = parse_es_result(raw)
            parsed.append(res)
        except Exception as e:
            logger.debug(f"Validation failed for result '{raw.get('Filename', 'unknown')}': {e}")
    return parsed