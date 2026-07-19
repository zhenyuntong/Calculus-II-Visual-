@echo off
setlocal
cd /d "%~dp0"

where py >nul 2>nul
if not errorlevel 1 goto :use_py
where python >nul 2>nul
if errorlevel 1 goto :no_python
set "PYTHON=python"
goto :python_ready

:use_py
set "PYTHON=py -3"

:python_ready

if not exist ".venv\Scripts\python.exe" (
  echo Preparing Calculus Visualizer for first use...
  %PYTHON% -m venv .venv
  if errorlevel 1 goto :error
)

.venv\Scripts\python.exe -c "import flask, sympy" >nul 2>nul
if errorlevel 1 (
  echo Installing required packages...
  .venv\Scripts\python.exe -m pip install --disable-pip-version-check -r requirements.txt
  if errorlevel 1 goto :error
)

echo Starting Calculus Visualizer...
start "" /b cmd /c "timeout /t 2 >nul & start "" http://127.0.0.1:5050/"
.venv\Scripts\python.exe app.py
exit /b 0

:no_python
echo Python 3 is required. Install it from https://www.python.org/downloads/
pause
exit /b 1

:error
echo The app could not start. Review the message above and try again.
pause
exit /b 1
