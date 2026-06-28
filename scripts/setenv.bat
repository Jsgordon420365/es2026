@echo off
REM Shared environment for Search Everything Class-0.
REM Called by other scripts via "call setenv.bat".
REM Edit EVERYTHING_ES_PATH here, or set it in a gitignored
REM search_everything.env / .env file (see search_everything.env.example),
REM or run: python -m search_everything.wizard

set "EVERYTHING_ES_PATH=es.exe"
set "EVERYTHING_DEFAULT_LIMIT=100"
set "EVERYTHING_LOG_LEVEL=INFO"
set "PYTHONPATH=src"
