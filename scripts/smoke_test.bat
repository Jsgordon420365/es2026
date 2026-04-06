@echo off
setlocal
set PYTHONPATH=src
pytest tests/test_cli.py tests/test_models.py
endlocal