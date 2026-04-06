from typing import List

class QueryBuilder:
    """Helper for constructing Everything search queries."""
    
    @staticmethod
    def build_query(query: str, folders_only: bool = False, files_only: bool = False) -> str:
        """Apply Everything filters to a query string."""
        parts: List[str] = []
        
        if folders_only:
            parts.append("folder:")
        elif files_only:
            parts.append("file:")
            
        parts.append(query)
        return " ".join(parts).strip()