REM Play completion chime
powershell -c "[console]::beep(800,300); [console]::beep(1000,300); [console]::beep(1200,500)"

REM Auto-exit after 3 seconds (comment out if you want manual pause)
timeout /t 3 /nobreak > nul