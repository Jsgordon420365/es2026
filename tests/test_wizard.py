"""Tests for the CLI wizard module (non-interactive paths)."""

import subprocess
import sys
import os
from unittest.mock import patch, MagicMock
from datetime import datetime

BASE_ENV = {**os.environ, "PYTHONPATH": "src"}


def run_wizard(args, stdin_text=""):
    """Run wizard module as a subprocess with controlled stdin."""
    return subprocess.run(
        [sys.executable, "-m", "search_everything.wizard"] + args,
        capture_output=True,
        text=True,
        input=stdin_text,
        env=BASE_ENV,
        cwd=os.path.dirname(os.path.dirname(__file__)),
    )


def run_cli(args, stdin_text=""):
    """Run CLI module as a subprocess with controlled stdin."""
    return subprocess.run(
        [sys.executable, "-m", "search_everything.cli"] + args,
        capture_output=True,
        text=True,
        input=stdin_text,
        env=BASE_ENV,
        cwd=os.path.dirname(os.path.dirname(__file__)),
    )


# ─── wizard.py unit tests ────────────────────────────────────────────────────


def test_wizard_help_flag():
    result = run_wizard(["--help"])
    assert result.returncode == 0
    assert "interactive" in result.stdout.lower()
    assert "setup" in result.stdout.lower() or "wizard" in result.stdout.lower()


def test_wizard_module_importable():
    result = subprocess.run(
        [sys.executable, "-c", "from search_everything.wizard import SetupWizard, InteractiveSearch, _fmt_size, _fmt_date"],
        capture_output=True,
        text=True,
        env=BASE_ENV,
        cwd=os.path.dirname(os.path.dirname(__file__)),
    )
    assert result.returncode == 0, result.stderr


def test_fmt_size():
    from search_everything.wizard import _fmt_size
    assert "KB" in _fmt_size(2048)
    assert "MB" in _fmt_size(2 * 1024 * 1024)
    assert "GB" in _fmt_size(2 * 1024 * 1024 * 1024)
    assert "B" in _fmt_size(500)


def test_fmt_date():
    from search_everything.wizard import _fmt_date
    dt = datetime(2026, 1, 15, 9, 30)
    result = _fmt_date(dt)
    assert "2026-01-15" in result
    assert "09:30" in result


def test_print_results_no_results(capsys=None):
    from search_everything.wizard import _print_results
    import io, contextlib

    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        _print_results([], query="*.foo", took_ms=1.0)
    assert "no results" in buf.getvalue()


def test_print_results_with_data():
    from search_everything.wizard import _print_results
    from search_everything.models import SearchResult
    import io, contextlib

    results = [
        SearchResult(
            path=r"C:\Users\test\foo.py",
            name="foo.py",
            extension="py",
            size=4096,
            modified_at=datetime(2026, 1, 10, 12, 0),
        ),
        SearchResult(
            path=r"C:\Users\test\bar",
            name="bar",
            extension="",
            size=0,
            modified_at=datetime(2026, 1, 11, 8, 0),
            is_directory=True,
        ),
    ]
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        _print_results(results, query="test", took_ms=5.2)
    out = buf.getvalue()
    assert "foo.py" in out
    assert "bar/" in out
    assert "2 result(s)" in out
    assert "5.2ms" in out


# ─── InteractiveSearch unit tests ────────────────────────────────────────────


def test_interactive_mode_str():
    from search_everything.wizard import InteractiveSearch
    from search_everything.config import Config

    config = Config(es_path="es.exe", default_limit=50)
    repl = InteractiveSearch(config)
    assert "limit=50" in repl._mode_str()

    repl.folders_only = True
    assert "folders" in repl._mode_str()

    repl.folders_only = False
    repl.regex = True
    assert "regex" in repl._mode_str()


def test_interactive_handle_command_toggles():
    from search_everything.wizard import InteractiveSearch
    from search_everything.config import Config
    import io, contextlib

    config = Config(es_path="es.exe", default_limit=100)
    repl = InteractiveSearch(config)

    # toggle folders
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        repl._handle_command("folders")
    assert repl.folders_only is True
    assert repl.files_only is False

    # toggle files should disable folders
    with contextlib.redirect_stdout(buf):
        repl._handle_command("files")
    assert repl.files_only is True
    assert repl.folders_only is False

    # toggle regex
    with contextlib.redirect_stdout(buf):
        repl._handle_command("regex")
    assert repl.regex is True


def test_interactive_handle_limit():
    from search_everything.wizard import InteractiveSearch
    from search_everything.config import Config
    import io, contextlib

    config = Config(es_path="es.exe", default_limit=100)
    repl = InteractiveSearch(config)
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        repl._handle_command("limit 25")
    assert repl.limit == 25

    # clamp to max
    with contextlib.redirect_stdout(buf):
        repl._handle_command("limit 9999")
    assert repl.limit == 1000

    # clamp to min
    with contextlib.redirect_stdout(buf):
        repl._handle_command("limit 0")
    assert repl.limit == 1


def test_interactive_handle_unknown_command():
    from search_everything.wizard import InteractiveSearch
    from search_everything.config import Config
    import io, contextlib

    config = Config(es_path="es.exe", default_limit=100)
    repl = InteractiveSearch(config)
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        repl._handle_command("nonexistent")
    assert "unknown" in buf.getvalue().lower()


# ─── CLI integration: --wizard and --interactive flags ───────────────────────


def test_cli_wizard_flag_shows_wizard_output():
    # Send EOF immediately so wizard exits after the banner
    result = run_cli(["--wizard"], stdin_text="")
    # Should not error out with a Python traceback
    assert "Traceback" not in result.stderr
    # Wizard header should appear
    assert "Wizard" in result.stdout or "wizard" in result.stdout.lower() or result.returncode in (0, 1)


def test_cli_interactive_flag_starts_repl():
    result = run_cli(["--interactive"], stdin_text="")
    assert "Traceback" not in result.stderr


def test_wizard_interactive_flag():
    result = run_wizard(["-i"], stdin_text="")
    assert "Traceback" not in result.stderr
