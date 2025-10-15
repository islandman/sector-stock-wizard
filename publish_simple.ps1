# Simple PowerShell script for GitHub deployment

$projectName = "stock-wizard"
$repoName = "sector-stock-wizard"
$zipName = "$repoName.zip"

Write-Host "Starting deployment..."

# Navigate to project folder
Set-Location -Path $projectName

# Initialize Git if needed
if (-not (Test-Path ".git")) {
    git init
    Write-Host "Git initialized."
}

# Add all files
git add .

# Commit changes
git commit -m "Initial commit: full scaffold with Streamlit, CLI, rules, tests, and CI"

# Check for existing remote
$remotes = git remote
$hasOrigin = $false
foreach ($remote in $remotes) {
    if ($remote -eq "origin") {
        $hasOrigin = $true
        break
    }
}

# Add remote if missing
if (-not $hasOrigin) {
    $githubUser = Read-Host "Enter your GitHub username"
    $remoteUrl = "https://github.com/$githubUser/$repoName.git"
    git remote add origin $remoteUrl
    Write-Host "Remote origin set to $remoteUrl"
} else {
    Write-Host "Remote origin already exists"
}

# Push to GitHub
git branch -M main
git push -u origin main
Write-Host "Pushed to GitHub: $repoName"

# Create zip archive
Set-Location ..
Compress-Archive -Path $projectName -DestinationPath $zipName -Force
Write-Host "Project zipped as $zipName"

Write-Host "Deployment complete!"
