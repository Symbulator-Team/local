@echo off
rem Double-click this file to run Symbulator 9 locally and open it in
rem your browser.
cd /d "%~dp0"
set PORT=8000

where python >nul 2>nul
if %errorlevel%==0 (
  set PYCMD=python
) else (
  where py >nul 2>nul
  if %errorlevel%==0 (
    set PYCMD=py
  ) else (
    echo Python was not found. Install it from https://python.org and try again.
    echo Tip: tick "Add python.exe to PATH" during setup.
    pause
    exit /b 1
  )
)

start "" "http://localhost:%PORT%/"
echo Starting Symbulator 9 at http://localhost:%PORT%/
echo Leave this window open while you use it. Close it to stop.
%PYCMD% -m http.server %PORT%
