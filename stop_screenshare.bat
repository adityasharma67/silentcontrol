@echo off
setlocal
set "PID_FILE=%~dp0screenshare.pid"

if not exist "%PID_FILE%" (
    echo No running Silent Screenshare instance was found.
    endlocal
    exit /b 0
)

for /f "usebackq delims=" %%P in ("%PID_FILE%") do (
    taskkill /PID %%P /T /F >nul 2>&1
    if errorlevel 1 (
        echo Process %%P was not found or could not be stopped.
    ) else (
        echo Silent Screenshare stopped.
    )
)
del /q "%PID_FILE%"
endlocal