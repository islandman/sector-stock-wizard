@echo off
echo Fixing GitHub remote URL...

REM Remove existing remote
git remote remove origin 2>nul

REM Get correct username
set /p githubUser="Enter your correct GitHub username: "

REM Create correct URL
set remoteUrl=https://github.com/%githubUser%/sector-stock-wizard.git

REM Add the correct remote
git remote add origin %remoteUrl%

echo Remote origin set to: %remoteUrl%

REM Test the connection
echo Testing connection...
git remote -v

REM Push to GitHub
echo Pushing to GitHub...
git push -u origin main

echo Done!
pause
