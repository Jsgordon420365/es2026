import subprocess
import shutil
import csv
import io
import logging
from typing import List, Optional, Dict
from pathlib import Path
from .logging_utils import get_logger

logger = get_logger(__name__)

class ESClient:
    """Low-level wrapper around the Everything CLI (es.exe)."""
    
    def __init__(self, es_path: str = "es.exe"):
        self.es_path = es_path
        self._resolved_path = None
        self._version = None
        self._flags_supported = True # Assume supported initially

    def resolve_path(self) -> str:
        """Find the absolute path to es.exe if not already cached and detect version."""
        if self._resolved_path:
            return self._resolved_path
        
        path = self._find_path()
        self._resolved_path = path
        
        # Check version to see if modern flags are supported
        try:
            # es.exe with no args usually returns help/version info
            proc = subprocess.run([path], capture_output=True, text=True, timeout=5)
            version_line = proc.stdout.splitlines()[0] if proc.stdout else ""
            self._version = version_line
            # If -get-column-names fails, it's definitely old.
            check_proc = subprocess.run([path, "-get-column-names"], capture_output=True, timeout=2)
            if check_proc.returncode != 0:
                logger.warning(f"Older es.exe version detected ({version_line}). Disabling advanced flags.")
                self._flags_supported = False
        except Exception:
            self._flags_supported = False
            
        return self._resolved_path

    def _find_path(self) -> str:
        """Internal helper for resolve_path."""
        if Path(self.es_path).is_absolute() and Path(self.es_path).exists():
            return self.es_path
        path_on_system = shutil.which(self.es_path)
        if path_on_system:
            return str(path_on_system)
        common_paths = [
            r"C:\Program Files\Everything\es.exe",
            r"C:\Program Files (x86)\Everything\es.exe"
        ]
        for p in common_paths:
            if Path(p).exists():
                return p
        return self.es_path

    def is_everything_running(self) -> bool:
        """Check if Everything desktop/service is running."""
        try:
            # -get-result-count works in older 1.1.0.27 too
            cmd = [self.resolve_path(), "-get-result-count", "."]
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=5,
                check=False
            )
            return result.returncode == 0
        except Exception as e:
            logger.error(f"Everything status check failed: {e}")
            return False

    def run_query(self, query: str, limit: int = 100, regex: bool = False, folders_only: bool = False) -> List[Dict]:
        """Execute a search query and return raw dictionaries."""
        base_cmd = [self.resolve_path(), "-n", str(limit), "-csv"]
        
        # If modern flags are available, we use them to get rich metadata
        if self._flags_supported:
            base_cmd.extend(["-dm", "-sz", "-ext", "-attrib"])
        
        if regex:
            base_cmd.append("-r")
        if folders_only:
            base_cmd.append("-d")
        
        base_cmd.append(query)
        
        try:
            result = subprocess.run(
                base_cmd, 
                capture_output=True, 
                text=True, 
                timeout=15, 
                check=True
            )
            # DEBUG
            logger.debug(f"RAW STDOUT: {result.stdout[:200]!r}")
            
            if not result.stdout or not result.stdout.strip():
                return []
                
            f = io.StringIO(result.stdout.strip())
            # Header will vary based on _flags_supported
            reader = csv.DictReader(f)
            data = list(reader)
            logger.debug(f"Parsed {len(data)} raw rows")
            return data
        except subprocess.CalledProcessError as e:
            if e.returncode == 1 and not e.stderr:
                return []
            logger.warning(f"es.exe query failed (code {e.returncode}): {e.stderr}")
            return []
        except Exception as e:
            logger.error(f"Error running query: {e}")
            return []