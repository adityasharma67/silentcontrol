@echo off
setlocal
set "APP_DIR=%~dp0"
set "PID_FILE=%APP_DIR%screenshare.pid"
set "PYTHONW_EXE=%APP_DIR%.venv\Scripts\pythonw.exe"

if not exist "%PYTHONW_EXE%" (
	echo Python environment not found. Run setup.bat first.
	endlocal
	exit /b 1
)

if exist "%PID_FILE%" (
	for /f "usebackq delims=" %%P in ("%PID_FILE%") do (
		tasklist /FI "PID eq %%P" /NH | findstr /R /C:"%%P" >nul && (
			echo Silent Screenshare is already running with PID %%P.
			endlocal
			exit /b 0
		)
	)
	del /q "%PID_FILE%"
)

if exist "%SystemRoot%\System32\WindowsPowerShell\v1.0\powershell.exe" (
	set "PS_EXE=%SystemRoot%\System32\WindowsPowerShell\v1.0\powershell.exe"
) else (
	set "PS_EXE=pwsh.exe"
)

"%PS_EXE%" -NoProfile -Command "$p = Start-Process -FilePath '%PYTHONW_EXE%' -ArgumentList ('\"' + '%APP_DIR%main.py' + '\"') -WorkingDirectory '%APP_DIR%' -WindowStyle Hidden -PassThru; Set-Content -Path '%PID_FILE%' -Value $p.Id"
if not exist "%PID_FILE%" (
	echo Failed to start Silent Screenshare. Check that Python is installed and on PATH.
	endlocal
	exit /b 1
)
echo Silent Screenshare started in the background.
echo Use stop_screenshare.bat to stop it.
endlocal
