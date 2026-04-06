import logging
import sys
from pathlib import Path
from typing import Optional

from typing import Optional, Union

def setup_logging(level: Union[str, int] = logging.INFO, log_file: Optional[Path] = None):
    """Set up logging to console and optionally to a file."""
    if isinstance(level, str):
        level = getattr(logging, level.upper(), logging.INFO)
        
    format_str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    handlers = [logging.StreamHandler(sys.stderr)]
    
    if log_file:
        log_file.parent.mkdir(parents=True, exist_ok=True)
        handlers.append(logging.FileHandler(log_file, encoding='utf-8'))
        
    logging.basicConfig(
        level=level,
        format=format_str,
        handlers=handlers,
        force=True
    )

def get_logger(name: str) -> logging.Logger:
    """Get a named logger."""
    return logging.getLogger(name)