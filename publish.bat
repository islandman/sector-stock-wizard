@echo off
REM publish.bat — One-click GitHub deployment for Sector Stock Wizard

set projectName=stock-wizard
set repoName=sector-stock-wizard
set zipName=%repoName%.zip

echo 🚀 Starting GitHub deployment...

REM Step 1: Navigate to project folder
cd %projectName%

REM Step 2: Initialize Git if needed
if not exist ".git" (
    git init
    echo ✅ Git initialized.
)

REM Step 3: Add all files
git add .

REM Step 4: Commit changes
git commit -m "Initial commit: full scaffold with Streamlit, CLI, rules, tests, and CI"

REM Step 5: Check if remote exists and add if needed
git remote | findstr "origin" >nul
if errorlevel 1 (
    set /p githubUser="Enter your GitHub username: "
    set remoteUrl=https://github.com/%githubUser%/%repoName%.git
    git remote add origin %remoteUrl%
    echo 🔗 Remote origin set to %remoteUrl%
) else (
    echo ✅ Remote origin already exists
)

REM Step 6: Push to GitHub
git branch -M main
git push -u origin main
echo 🚀 Pushed to GitHub: %repoName%

REM Step 7: Optional zip archive
cd ..
powershell Compress-Archive -Path %projectName% -DestinationPath %zipName% -Force
echo 📦 Project zipped as %zipName%

echo ✅ Deployment complete!
pause
