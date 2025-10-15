# Fix remote URL script

$repoName = "sector-stock-wizard"

Write-Host "Fixing GitHub remote URL..."

# Remove existing remote if it exists
git remote remove origin 2>$null

# Get correct username
$githubUser = Read-Host "Enter your correct GitHub username"

# Create correct URL
$remoteUrl = "https://github.com/$githubUser/$repoName.git"

# Add the correct remote
git remote add origin $remoteUrl

Write-Host "Remote origin set to: $remoteUrl"

# Test the connection
Write-Host "Testing connection..."
git remote -v

# Push to GitHub
Write-Host "Pushing to GitHub..."
git push -u origin main

Write-Host "Done!"
