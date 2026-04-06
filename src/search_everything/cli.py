import argparse
import json
import sys
from .config import load_config
from .service import SearchService
from .models import SearchRequest
from .logging_utils import setup_logging

def main():
    parser = argparse.ArgumentParser(description="Search Everything Class-0 CLI")
    parser.add_argument("query", nargs='?', default=None, help="The search query string")
    parser.add_argument("--limit", type=int, default=100, help="Max results to return")
    parser.add_argument("--folders", action="store_true", help="Search folders only")
    parser.add_argument("--files", action="store_true", help="Search files only")
    parser.add_argument("--regex", action="store_true", help="Enable regex search")
    parser.add_argument("--health", action="store_true", help="Perform a health check and exit")
    parser.add_argument("--debug", action="store_true", help="Enable debug logging")
    
    args = parser.parse_args()
    
    config = load_config()
    if args.debug:
        config.log_level = "DEBUG"
        
    setup_logging(level=config.log_level, log_file=config.log_file)
    
    service = SearchService(config)
    
    if args.health:
        health = service.check_health()
        print(health.model_dump_json(indent=2))
        sys.exit(0 if health.everything_running else 1)
        
    if not args.query:
        if not args.health:
            parser.print_help(sys.stderr)
            sys.exit(1)
        return

    request = SearchRequest(
        query=args.query,
        limit=args.limit,
        folders_only=args.folders,
        files_only=args.files,
        regex=args.regex
    )
    
    try:
        response = service.search(request)
        print(response.model_dump_json(indent=2))
    except Exception as e:
        print(json.dumps({"error": "RUNTIME_ERROR", "message": str(e), "code": 500}, indent=2))
        sys.exit(1)

if __name__ == "__main__":
    main()