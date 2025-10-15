# Setup GitHub repository script

$repoName = "sector-stock-wizard"
$githubUser = "islandman"  # Your GitHub username

Write-Host "Setting up GitHub repository for $repoName"
Write-Host ""

Write-Host "STEP 1: Create the repository on GitHub first!"
Write-Host "1. Go to https://github.com/new"
Write-Host "2. Repository name: $repoName"
Write-Host "3. Description: Sector-Aware Stock Buy/Sell Wizard"
Write-Host "4. Make it Public or Private (your choice)"
Write-Host "5. DO NOT initialize with README, .gitignore, or license"
Write-Host "6. Click 'Create repository'"
Write-Host ""

$continue = Read-Host "Press Enter when you've created the repository on GitHub"

Write-Host ""
Write-Host "STEP 2: Setting up local repository..."

# Remove existing remote if it exists
git remote remove origin 2>$null

# Add the correct remote
$remoteUrl = "https://github.com/$githubUser/$repoName.git"
git remote add origin $remoteUrl

Write-Host "Remote origin set to: $remoteUrl"

# Test the connection
Write-Host "Testing connection..."
git remote -v

Write-Host ""
Write-Host "STEP 3: Pushing to GitHub..."
git push -u origin main

Write-Host ""
Write-Host "Done! Your repository should now be available at:"
Write-Host "https://github.com/$githubUser/$repoName"
