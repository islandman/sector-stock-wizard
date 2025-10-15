# publish.ps1 — One-click GitHub deployment for Sector Stock Wizard

$projectName = "stock-wizard"
$repoName = "sector-stock-wizard"
$zipName = "$repoName.zip"

# Step 1: Navigate to project folder
Set-Location -Path $projectName

# Step 2: Initialize Git if needed
if (-not (Test-Path ".git")) {
    git init
    Write-Host "Git initialized."
}

# Step 3: Add all files
git add .

# Step 4: Commit changes
git commit -m "Initial commit: full scaffold with Streamlit, CLI, rules, tests, and CI"

# Step 5: Set remote if missing
try {
    $remotes = git remote
    $originExists = $false
    foreach ($remote in $remotes) {
        if ($remote -eq "origin") {
            $originExists = $true
            break
        }
    }
    
    if (-not $originExists) {
        $githubUser = Read-Host "Enter your GitHub username"
        $remoteUrl = "https://github.com/$githubUser/$repoName.git"
        git remote add origin $remoteUrl
        Write-Host "Remote origin set to $remoteUrl"
    } else {
        Write-Host "Remote origin already exists"
    }
} catch {
    Write-Host "Warning: Could not check existing remotes. Adding origin anyway."
    $githubUser = Read-Host "Enter your GitHub username"
    $remoteUrl = "https://github.com/$githubUser/$repoName.git"
    git remote add origin $remoteUrl
    Write-Host "Remote origin set to $remoteUrl"
}

# Step 6: Push to GitHub
git branch -M main
git push -u origin main
Write-Host "Pushed to GitHub: $repoName"

# Step 7: Optional zip archive
Set-Location ..
Compress-Archive -Path $projectName -DestinationPath $zipName -Force
Write-Host "Project zipped as $zipName"