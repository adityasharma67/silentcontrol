@echo off
setlocal
set "APP_DIR=%~dp0"
set "VENV_DIR=%APP_DIR%.venv"
set "PYTHON_EXE=%VENV_DIR%\Scripts\python.exe"

where py >nul 2>&1
if not errorlevel 1 (
	set "PYTHON_CMD=py -3"
) else (
	where python >nul 2>&1
	if errorlevel 1 (
		echo Python 3.10 or newer is required.
		echo Install it from https://www.python.org/downloads/windows/
		echo Make sure ^"Add python.exe to PATH^" is enabled, then run setup.bat again.
		endlocal
		exit /b 1
	)
	set "PYTHON_CMD=python"
)

if not exist "%PYTHON_EXE%" (
	echo Creating a local Python environment...
	%PYTHON_CMD% -m venv "%VENV_DIR%"
	if errorlevel 1 (
		echo Could not create the Python environment.
		endlocal
		exit /b 1
	)
)

echo Installing dependencies...
"%PYTHON_EXE%" -m pip install --upgrade pip
if errorlevel 1 (
	echo Could not upgrade pip.
	endlocal
	exit /b 1
)
"%PYTHON_EXE%" -m pip install -r "%APP_DIR%requirements.txt"
if errorlevel 1 (
	echo Dependency installation failed.
	endlocal
	exit /b 1
)

echo.
echo Setup complete. Run start_screenshare.bat to start the app.
endlocal