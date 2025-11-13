@echo off
echo Starting Mario Kart RL Hackathon...

echo Checking if VcXsrv is running...
tasklist /FI "IMAGENAME eq vcxsrv.exe" 2>NUL | find /I "vcxsrv.exe" >NUL
if "%ERRORLEVEL%" NEQ "0" (
    echo ERROR: VcXsrv is not running!
    echo Please start XLaunch from Start Menu first.
    echo Make sure to check "Disable access control" during setup.
    pause
    exit /b 1
)

echo VcXsrv detected - continuing...
set DISPLAY=host.docker.internal:0

echo Building containers...
docker-compose -f docker-compose.windows.yml build

echo Starting everything...
docker-compose -f docker-compose.windows.yml up

pause