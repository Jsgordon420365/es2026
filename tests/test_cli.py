import subprocess
import json
import os

def run_cli(args):
    """Helper to run the CLI and return stdout, stderr, and returncode."""
    env = os.environ.copy()
    env["PYTHONPATH"] = "src"
    result = subprocess.run(
        ["python", "-m", "search_everything.cli"] + args,
        capture_output=True,
        text=True,
        env=env
    )
    return result

def test_cli_health():
    result = run_cli(["--health"])
    assert result.returncode == 0
    data = json.loads(result.stdout)
    assert data["status"] == "ok"
    assert "everything_running" in data

def test_cli_search_basic():
    # Use a common file that should exist in the workspace
    result = run_cli(["Antigravity.md", "--limit", "1"])
    assert result.returncode == 0
    data = json.loads(result.stdout)
    assert "results" in data
    assert "count" in data
    assert data["query"] == "Antigravity.md"

def test_cli_no_query_error():
    # Running without query or flags should show help and exit 1
    result = run_cli([])
    assert result.returncode == 1
    assert "usage:" in result.stderr.lower()

def test_cli_debug_mode():
    result = run_cli(["--health", "--debug"])
    assert result.returncode == 0
    # Debug output goes to stdout/stderr depending on config, 
    # but the JSON should still be there.
    assert "ok" in result.stdout
