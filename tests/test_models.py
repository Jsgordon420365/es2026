import pytest
from datetime import datetime
from search_everything.models import SearchResult, SearchResponse, SearchRequest

def test_search_result_validation():
    data = {
        "path": "C:\\test.txt",
        "name": "test.txt",
        "extension": "txt",
        "size": 1024,
        "modified_at": "2024-03-06T10:00:00Z",
        "is_directory": False
    }
    result = SearchResult(**data)
    assert result.path == "C:\\test.txt"
    assert result.size == 1024
    assert isinstance(result.modified_at, datetime)

def test_search_response_validation():
    result_data = {
        "path": "C:\\test.txt",
        "name": "test.txt",
        "extension": "txt",
        "size": 1024,
        "modified_at": datetime.now(),
        "is_directory": False
    }
    response = SearchResponse(
        results=[SearchResult(**result_data)],
        count=1,
        total=1,
        query="test",
        took_ms=0.5
    )
    assert len(response.results) == 1
    assert response.count == 1

def test_search_request_defaults():
    req = SearchRequest(query="hello")
    assert req.limit == 100
    assert req.offset == 0
    assert req.folders_only is False
