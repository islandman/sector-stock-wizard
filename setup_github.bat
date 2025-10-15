@echo off
echo Setting up GitHub repository for sector-stock-wizard
echo.

echo STEP 1: Create the repository on GitHub first!
echo 1. Go to https://github.com/new
echo 2. Repository name: sector-stock-wizard
echo 3. Description: Sector-Aware Stock Buy/Sell Wizard
echo 4. Make it Public or Private (your choice)
echo 5. DO NOT initialize with README, .gitignore, or license
echo 6. Click 'Create repository'
echo.

pause

echo.
echo STEP 2: Setting up local repository...

REM Remove existing remote if it exists
git remote remove origin 2>nul

REM Add the correct remote
set remoteUrl=https://github.com/islandman/sector-stock-wizard.git
git remote add origin %remoteUrl%

echo Remote origin set to: %remoteUrl%

REM Test the connection
echo Testing connection...
git remote -v

echo.
echo STEP 3: Pushing to GitHub...
git push -u origin main

echo.
echo Done! Your repository should now be available at:
echo https://github.com/islandman/sector-stock-wizard
pause
