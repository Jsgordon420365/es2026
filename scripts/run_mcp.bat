@echo off
setlocal
set PYTHONPATH=src
python -m search_everything.mcp_server %*
endlocal