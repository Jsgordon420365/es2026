"""Interactive CLI wizard for Search Everything es.exe.

Two modes:
  python -m search_everything.wizard            # setup/config wizard
  python -m search_everything.wizard -i         # interactive search REPL
"""

import os
import sys
import shutil
from datetime import datetime
from pathlib import Path
from typing import List

from .config import Config, load_config
from .es_client import ESClient
from .logging_utils import setup_logging
from .models import SearchRequest, SearchResult
from .service import SearchService


# ─── terminal helpers ────────────────────────────────────────────────────────

def _term_width() -> int:
    return shutil.get_terminal_size((80, 24)).columns


def _hr(char: str = "-", label: str = "") -> None:
    w = _term_width()
    if label:
        side = max(2, (w - len(label) - 2) // 2)
        print(f"{'─' * side} {label} {'─' * side}")
    else:
        print(char * w)


def _fmt_size(size_bytes: int) -> str:
    for unit, threshold in [("GB", 1 << 30), ("MB", 1 << 20), ("KB", 1 << 10)]:
        if size_bytes >= threshold:
            return f"{size_bytes / threshold:.1f}{unit}"
    return f"{size_bytes}B"


def _fmt_date(dt: datetime) -> str:
    return dt.strftime("%Y-%m-%d %H:%M")


def _prompt(msg: str, default: str = "") -> str:
    hint = f" [{default}]" if default else ""
    try:
        val = input(f"  {msg}{hint}: ").strip()
    except (EOFError, KeyboardInterrupt):
        print()
        sys.exit(0)
    return val if val else default


def _yn(msg: str, default: bool = True) -> bool:
    hint = "Y/n" if default else "y/N"
    try:
        raw = input(f"  {msg} [{hint}]: ").strip().lower()
    except (EOFError, KeyboardInterrupt):
        print()
        sys.exit(0)
    if not raw:
        return default
    return raw in ("y", "yes")


def _print_results(results: List[SearchResult], query: str, took_ms: float) -> None:
    if not results:
        print("  (no results)")
        return

    w = _term_width()
    name_col = min(32, max((len(r.name) for r in results), default=4) + 2)
    size_col = 9
    date_col = 17
    path_col = max(w - name_col - size_col - date_col - 6, 15)

    header = f"  {'Name':<{name_col}} {'Size':>{size_col}} {'Modified':<{date_col}} Path"
    print(header)
    print("  " + "─" * min(w - 2, name_col + size_col + date_col + path_col + 4))

    for r in results:
        name = r.name + ("/" if r.is_directory else "")
        if len(name) > name_col:
            name = name[: name_col - 1] + "…"
        size_str = "—" if r.is_directory else _fmt_size(r.size)
        date_str = _fmt_date(r.modified_at)
        parent = str(Path(r.path).parent)
        if len(parent) > path_col:
            parent = "…" + parent[-(path_col - 1) :]
        print(
            f"  {name:<{name_col}} {size_str:>{size_col}} {date_str:<{date_col}} {parent}"
        )

    print(f"\n  {len(results)} result(s)  ·  {took_ms:.1f}ms  ·  query: {query}")


# ─── setup wizard ────────────────────────────────────────────────────────────


class SetupWizard:
    """Walk the user through first-run configuration and write a .env file."""

    def run(self) -> None:
        _hr("=", "Search Everything  ·  Setup Wizard")
        print()
        print("  Configure es.exe path and defaults, then optionally save")
        print("  settings to search_everything.env for later use.")
        print()

        # Step 1: locate es.exe
        _hr(label="Step 1: Locate es.exe")
        client = ESClient()
        detected = client._find_path()
        path_exists = Path(detected).exists()

        if path_exists:
            print(f"  Detected: {detected}")
            use_detected = _yn("Use this path?")
            es_path = detected if use_detected else _prompt("Path to es.exe", detected)
        else:
            print("  es.exe not found on PATH or in default install locations.")
            es_path = _prompt(
                "Path to es.exe", r"C:\Program Files\Everything\es.exe"
            )
        print()

        # Step 2: verify service
        _hr(label="Step 2: Verify Everything Service")
        probe = ESClient(es_path=es_path)
        running = probe.is_everything_running()
        if running:
            print("  Everything service is running.")
        else:
            print("  WARNING: Everything service does not appear to be running.")
            print(
                "  Start the Everything desktop app and retry, or continue anyway."
            )
        print()

        # Step 3: defaults
        _hr(label="Step 3: Default Settings")
        raw_limit = _prompt("Default result limit (1-1000)", "100")
        try:
            default_limit = max(1, min(1000, int(raw_limit)))
        except ValueError:
            default_limit = 100

        log_levels = ("DEBUG", "INFO", "WARNING", "ERROR")
        print(f"  Log levels: {', '.join(log_levels)}")
        log_level = _prompt("Log level", "INFO").upper()
        if log_level not in log_levels:
            log_level = "INFO"
        print()

        # Step 4: write .env
        _hr(label="Step 4: Save Configuration")
        env_lines = [
            f"EVERYTHING_ES_PATH={es_path}",
            f"EVERYTHING_DEFAULT_LIMIT={default_limit}",
            f"EVERYTHING_LOG_LEVEL={log_level}",
        ]
        env_path = Path("search_everything.env")
        print(f"  Target file: {env_path.resolve()}")
        print()
        for line in env_lines:
            print(f"    {line}")
        print()

        if _yn("Save these settings?"):
            env_path.write_text("\n".join(env_lines) + "\n", encoding="utf-8")
            print(f"  Saved: {env_path.resolve()}")
        else:
            print("  Skipped (settings not saved).")
        print()

        # Step 5: test search
        _hr(label="Step 5: Test Search")
        if running and _yn("Run a quick test search?"):
            test_query = _prompt("Test query", "*.py")
            config = Config(
                es_path=es_path,
                default_limit=default_limit,
                log_level=log_level,
            )
            svc = SearchService(config)
            req = SearchRequest(query=test_query, limit=10)
            try:
                resp = svc.search(req)
                print()
                _print_results(resp.results, resp.query, resp.took_ms)
            except Exception as exc:
                print(f"  Search failed: {exc}")
        print()

        # Done
        _hr("=")
        print()
        print("  Setup complete.")
        print("  Non-interactive search: python -m search_everything.cli \"<query>\"")
        print("  Interactive search:     python -m search_everything.wizard -i")
        print()


# ─── interactive search REPL ─────────────────────────────────────────────────

_HELP = """\
Commands:
  <query>          search for files and folders
  :folders         toggle folders-only mode  (current: {folders})
  :files           toggle files-only mode    (current: {files})
  :regex           toggle regex mode         (current: {regex})
  :limit [N]       show or set result limit  (current: {limit})
  :health          show Everything service status
  :clear           clear the screen
  :help            show this help
  :quit            exit
"""


class InteractiveSearch:
    """REPL-style interactive search session against es.exe."""

    def __init__(self, config: Config) -> None:
        self.config = config
        self.service = SearchService(config)
        self.limit: int = config.default_limit
        self.folders_only: bool = False
        self.files_only: bool = False
        self.regex: bool = False

    def _mode_str(self) -> str:
        flags = []
        if self.folders_only:
            flags.append("folders")
        if self.files_only:
            flags.append("files")
        if self.regex:
            flags.append("regex")
        flag_str = f"  [{', '.join(flags)}]" if flags else ""
        return f"limit={self.limit}{flag_str}"

    def _show_help(self) -> None:
        print(
            _HELP.format(
                folders=self.folders_only,
                files=self.files_only,
                regex=self.regex,
                limit=self.limit,
            )
        )

    def run(self) -> None:
        _hr("=", "Search Everything  ·  Interactive Search")
        print()
        print("  Type a search query or a :command (:help for list, :quit to exit).")
        print(f"  {self._mode_str()}")
        print()

        while True:
            try:
                raw = input("es> ").strip()
            except (EOFError, KeyboardInterrupt):
                print()
                break

            if not raw:
                continue

            if raw.startswith(":"):
                self._handle_command(raw[1:].strip())
                continue

            self._do_search(raw)
            print()

    def _handle_command(self, cmd: str) -> None:
        lower = cmd.lower()

        if lower in ("quit", "q", "exit"):
            sys.exit(0)

        elif lower == "help":
            self._show_help()

        elif lower == "folders":
            self.folders_only = not self.folders_only
            self.files_only = False
            print(f"  folders-only: {'on' if self.folders_only else 'off'}")

        elif lower == "files":
            self.files_only = not self.files_only
            self.folders_only = False
            print(f"  files-only: {'on' if self.files_only else 'off'}")

        elif lower == "regex":
            self.regex = not self.regex
            print(f"  regex: {'on' if self.regex else 'off'}")

        elif lower.startswith("limit"):
            parts = lower.split(maxsplit=1)
            if len(parts) == 2:
                try:
                    self.limit = max(1, min(1000, int(parts[1])))
                    print(f"  limit set to {self.limit}")
                except ValueError:
                    print("  Usage: :limit <N>  (1–1000)")
            else:
                print(f"  Current limit: {self.limit}")

        elif lower == "health":
            h = self.service.check_health()
            print(f"  Everything running : {h.everything_running}")
            print(f"  es.exe found       : {h.es_found}")
            print(f"  es.exe path        : {h.es_path}")

        elif lower == "clear":
            os.system("cls" if os.name == "nt" else "clear")

        else:
            print(f"  Unknown command: :{cmd}  (type :help for commands)")

    def _do_search(self, query: str) -> None:
        req = SearchRequest(
            query=query,
            limit=self.limit,
            folders_only=self.folders_only,
            files_only=self.files_only,
            regex=self.regex,
        )
        try:
            resp = self.service.search(req)
            _print_results(resp.results, resp.query, resp.took_ms)
        except Exception as exc:
            print(f"  Error: {exc}")


# ─── entry point ─────────────────────────────────────────────────────────────


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(
        description="Search Everything CLI Wizard",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
            "  python -m search_everything.wizard           # setup wizard\n"
            "  python -m search_everything.wizard -i        # interactive REPL\n"
            "  python -m search_everything.wizard -i --debug"
        ),
    )
    parser.add_argument(
        "--interactive", "-i",
        action="store_true",
        help="launch interactive search REPL instead of setup wizard",
    )
    parser.add_argument("--debug", action="store_true", help="enable debug logging")
    args = parser.parse_args()

    config = load_config()
    if args.debug:
        config.log_level = "DEBUG"
    setup_logging(level=config.log_level, log_file=config.log_file)

    if args.interactive:
        InteractiveSearch(config).run()
    else:
        SetupWizard().run()


if __name__ == "__main__":
    main()
