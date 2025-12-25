# SmartSpec Installation Script for Windows
# Usage: iwr -useb https://raw.githubusercontent.com/naibarn/SmartSpec/main/.smartspec/scripts/install.ps1 | iex

Write-Host "🚀 Installing SmartSpec..." -ForegroundColor Green

# Check prerequisites
if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    Write-Host "❌ Error: git is not installed. Please install git first." -ForegroundColor Red
    Write-Host "   Download from: https://git-scm.com/download/win" -ForegroundColor Yellow
    exit 1
}

if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Host "❌ Error: python is not installed. Please install Python 3.8+ first." -ForegroundColor Red
    Write-Host "   Download from: https://www.python.org/downloads/" -ForegroundColor Yellow
    exit 1
}

# Determine installation directories
$RepoDir = "$env:USERPROFILE\.smartspec-repo"
$SmartSpecHome = "$env:USERPROFILE\.smartspec"

# Clone or update repository
if (Test-Path $RepoDir) {
    Write-Host "📥 Updating existing SmartSpec installation..." -ForegroundColor Cyan
    Set-Location $RepoDir
    git pull origin main
} else {
    Write-Host "📥 Cloning SmartSpec repository..." -ForegroundColor Cyan
    git clone https://github.com/naibarn/SmartSpec.git $RepoDir
    Set-Location $RepoDir
}

# Verify .smartspec directory exists in repo
if (-not (Test-Path "$RepoDir\.smartspec")) {
    Write-Host "❌ Error: .smartspec directory not found in repository." -ForegroundColor Red
    exit 1
}

# Verify workflows directory exists
if (-not (Test-Path "$RepoDir\.smartspec\workflows")) {
    Write-Host "❌ Error: Workflows directory not found after clone." -ForegroundColor Red
    exit 1
}

# Verify scripts directory exists
if (-not (Test-Path "$RepoDir\.smartspec\scripts")) {
    Write-Host "❌ Error: Scripts directory not found after clone." -ForegroundColor Red
    exit 1
}

# Create symbolic link to .smartspec directory
if (Test-Path $SmartSpecHome) {
    # Check if it's a symbolic link
    $item = Get-Item $SmartSpecHome -Force
    if ($item.Attributes -band [System.IO.FileAttributes]::ReparsePoint) {
        # It's a symlink, remove and recreate
        Remove-Item $SmartSpecHome -Force
    } else {
        # It's a directory, backup
        $timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
        Move-Item $SmartSpecHome "$SmartSpecHome.backup.$timestamp"
    }
}

# Create new symbolic link (requires admin or Developer Mode on Windows 10+)
try {
    New-Item -ItemType SymbolicLink -Path $SmartSpecHome -Target "$RepoDir\.smartspec" -Force | Out-Null
    Write-Host "✅ Created symbolic link: $SmartSpecHome -> $RepoDir\.smartspec" -ForegroundColor Green
} catch {
    Write-Host "⚠️  Warning: Could not create symbolic link. Copying directory instead..." -ForegroundColor Yellow
    Copy-Item -Path "$RepoDir\.smartspec" -Destination $SmartSpecHome -Recurse -Force
}

# Install Python dependencies if requirements.txt exists
if (Test-Path "$RepoDir\requirements.txt") {
    Write-Host "📦 Installing Python dependencies..." -ForegroundColor Cyan
    python -m pip install --user -r "$RepoDir\requirements.txt"
}

# Add to PATH
$CurrentPath = [Environment]::GetEnvironmentVariable("Path", "User")
$SmartSpecScripts = "$SmartSpecHome\scripts"

if ($CurrentPath -notlike "*$SmartSpecScripts*") {
    [Environment]::SetEnvironmentVariable(
        "Path",
        "$CurrentPath;$SmartSpecScripts",
        "User"
    )
    Write-Host "✅ Added SmartSpec to PATH" -ForegroundColor Green
}

# Set SMARTSPEC_HOME
[Environment]::SetEnvironmentVariable("SMARTSPEC_HOME", $SmartSpecHome, "User")

Write-Host ""
Write-Host "✅ SmartSpec installed successfully!" -ForegroundColor Green
Write-Host ""
Write-Host "📍 Repository: $RepoDir" -ForegroundColor Cyan
Write-Host "📍 SmartSpec Home: $SmartSpecHome (symlink)" -ForegroundColor Cyan
Write-Host "📁 Workflows: $SmartSpecHome\workflows\" -ForegroundColor Cyan
Write-Host "📁 Scripts: $SmartSpecHome\scripts\" -ForegroundColor Cyan
Write-Host ""
Write-Host "🎯 Next steps:" -ForegroundColor Yellow
Write-Host "   1. Restart your terminal to reload PATH"
Write-Host "   2. Verify installation: python `$env:SMARTSPEC_HOME\scripts\verify_evidence_strict.py --help"
Write-Host "   3. Check workflows: dir `$env:SMARTSPEC_HOME\workflows\"
Write-Host ""
