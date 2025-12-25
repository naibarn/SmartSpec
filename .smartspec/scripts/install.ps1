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

# Determine installation directory
$InstallDir = "$env:USERPROFILE\.smartspec"

# Clone or update repository
if (Test-Path $InstallDir) {
    Write-Host "📥 Updating existing SmartSpec installation..." -ForegroundColor Cyan
    Set-Location $InstallDir
    git pull origin main
} else {
    Write-Host "📥 Cloning SmartSpec repository..." -ForegroundColor Cyan
    git clone https://github.com/naibarn/SmartSpec.git $InstallDir
    Set-Location $InstallDir
}

# Verify workflows directory exists
if (-not (Test-Path "$InstallDir\.smartspec\workflows")) {
    Write-Host "❌ Error: Workflows directory not found after clone." -ForegroundColor Red
    exit 1
}

# Verify scripts directory exists
if (-not (Test-Path "$InstallDir\.smartspec\scripts")) {
    Write-Host "❌ Error: Scripts directory not found after clone." -ForegroundColor Red
    exit 1
}

# Install Python dependencies if requirements.txt exists
if (Test-Path "requirements.txt") {
    Write-Host "📦 Installing Python dependencies..." -ForegroundColor Cyan
    python -m pip install --user -r requirements.txt
}

# Add to PATH
$CurrentPath = [Environment]::GetEnvironmentVariable("Path", "User")
$SmartSpecPath = "$InstallDir\.smartspec\scripts"

if ($CurrentPath -notlike "*$SmartSpecPath*") {
    [Environment]::SetEnvironmentVariable(
        "Path",
        "$CurrentPath;$SmartSpecPath",
        "User"
    )
    Write-Host "✅ Added SmartSpec to PATH" -ForegroundColor Green
}

# Set SMARTSPEC_HOME
[Environment]::SetEnvironmentVariable("SMARTSPEC_HOME", $InstallDir, "User")

Write-Host ""
Write-Host "✅ SmartSpec installed successfully!" -ForegroundColor Green
Write-Host ""
Write-Host "📍 Installation directory: $InstallDir" -ForegroundColor Cyan
Write-Host "📁 Workflows: $InstallDir\.smartspec\workflows\" -ForegroundColor Cyan
Write-Host "📁 Scripts: $InstallDir\.smartspec\scripts\" -ForegroundColor Cyan
Write-Host ""
Write-Host "🎯 Next steps:" -ForegroundColor Yellow
Write-Host "   1. Restart your terminal to reload PATH"
Write-Host "   2. Verify installation: python `$env:SMARTSPEC_HOME\.smartspec\scripts\verify_evidence_strict.py --help"
Write-Host "   3. Check workflows: dir `$env:SMARTSPEC_HOME\.smartspec\workflows\"
Write-Host ""
