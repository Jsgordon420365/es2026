@echo off
setlocal
call "%~dp0setenv.bat"
python -m search_everything.mcp_server %*
endlocal
