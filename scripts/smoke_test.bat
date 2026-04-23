@echo off
setlocal
call "%~dp0setenv.bat"
pytest tests/test_cli.py tests/test_models.py tests/test_wizard.py
endlocal
