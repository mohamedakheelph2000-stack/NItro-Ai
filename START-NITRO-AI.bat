@echo off
echo ======================================
echo  Starting Nitro AI Local Server
echo ======================================
echo.

REM Set up environment
set PYTHONIOENCODING=utf-8

REM Start backend
echo [1/2] Starting Backend Server...
cd /d "%~dp0backend"
start "Nitro AI Backend" python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
timeout /t 3 /nobreak >nul

REM Start frontend
echo [2/2] Starting Frontend Server...
cd /d "%~dp0frontend"
start "Nitro AI Frontend" python -m http.server 3000
timeout /t 2 /nobreak >nul

REM Open browser
echo.
echo ======================================
echo  Nitro AI is Ready!
echo ======================================
echo.
echo  Frontend: http://localhost:3000
echo  Backend:  http://localhost:8000
echo.
echo  For network access, find your IP:
echo  ipconfig ^| findstr IPv4
echo.
echo  Press Ctrl+C in the terminal windows to stop
echo ======================================
echo.

start http://localhost:3000

echo Servers are running in separate windows.
echo Close this window to keep them running.
pause
