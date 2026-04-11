@echo off
setlocal

cd /d "%~dp0"

echo Checking Python environment...

where python >nul 2>nul
if %ERRORLEVEL% equ 0 (
    set PY_CMD=python
    goto found
)

where py >nul 2>nul
if %ERRORLEVEL% equ 0 (
    set PY_CMD=py
    goto found
)

echo [ERROR] Python not found!
pause
exit /b 1

:found
echo Using command: %PY_CMD%

if not exist "backend" (
    echo [ERROR] Folder 'backend' not found!
    pause
    exit /b 1
)

cd backend

if not exist "requirements.txt" (
    echo [ERROR] requirements.txt not found in 'backend' folder!
    pause
    exit /b 1
)

%PY_CMD% -m pip install -r requirements.txt

echo Service starting...
%PY_CMD% -m uvicorn app.main:app --host 0.0.0.0 --port 8000

pause
