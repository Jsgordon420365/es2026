import os
from pathlib import Path
from typing import Optional
from pydantic import BaseModel, Field

class Config(BaseModel):
    """Configuration settings for Search Everything Class-0."""
    es_path: str = Field(default="es.exe", description="Path to es.exe (defaults to PATH)")
    default_limit: int = Field(default=100, ge=1, le=1000)
    log_file: Optional[Path] = Field(default=None)
    log_level: str = Field(default="INFO")

def load_config() -> Config:
    """Load configuration from environment variables."""
    log_file_str = os.getenv("EVERYTHING_LOG_FILE", "logs/search_everything.log")
    return Config(
        es_path=os.getenv("EVERYTHING_ES_PATH", "es.exe"),
        default_limit=int(os.getenv("EVERYTHING_DEFAULT_LIMIT", "100")),
        log_file=Path(log_file_str) if log_file_str else None,
        log_level=os.getenv("EVERYTHING_LOG_LEVEL", "INFO")
    )