import os
from pathlib import Path
from typing import Optional
from pydantic import BaseModel, Field

_ENV_FILE_NAMES = ("search_everything.env", ".env")


def _load_env_file() -> dict:
    """Read key=value pairs from a local env file, skipping comments and blanks.

    Checks the current working directory and the project root (two levels up
    from this file) so the file is found whether you run from the repo root
    or from scripts/.
    """
    search_dirs = [
        Path.cwd(),
        Path(__file__).parent.parent.parent,  # project root
    ]
    for directory in search_dirs:
        for name in _ENV_FILE_NAMES:
            env_path = directory / name
            if env_path.exists():
                pairs: dict = {}
                for line in env_path.read_text(encoding="utf-8").splitlines():
                    line = line.strip()
                    if not line or line.startswith("#"):
                        continue
                    if "=" in line:
                        key, _, value = line.partition("=")
                        pairs[key.strip()] = value.strip()
                return pairs
    return {}


class Config(BaseModel):
    """Configuration settings for Search Everything Class-0."""
    es_path: str = Field(default="es.exe", description="Path to es.exe (defaults to PATH)")
    default_limit: int = Field(default=100, ge=1, le=1000)
    log_file: Optional[Path] = Field(default=None)
    log_level: str = Field(default="INFO")


def load_config() -> Config:
    """Load configuration from environment variables, falling back to env file."""
    file_vals = _load_env_file()

    def _get(key: str, default: str) -> str:
        return os.getenv(key) or file_vals.get(key, default)

    log_file_str = _get("EVERYTHING_LOG_FILE", "")
    try:
        default_limit = int(_get("EVERYTHING_DEFAULT_LIMIT", "100"))
    except ValueError:
        default_limit = 100
    return Config(
        es_path=_get("EVERYTHING_ES_PATH", "es.exe"),
        default_limit=default_limit,
        log_file=Path(log_file_str) if log_file_str else None,
        log_level=_get("EVERYTHING_LOG_LEVEL", "INFO"),
    )
