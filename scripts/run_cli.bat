@echo off
setlocal
set PYTHONPATH=src
python -m search_everything.cli %*
endlocal