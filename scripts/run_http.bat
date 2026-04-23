@echo off
setlocal
call "%~dp0setenv.bat"
python -m search_everything.http_server %*
endlocal
