# SmartSpec Multi-Platform Installer (Windows)
# Version: 5.0
# Supports: Kilo Code, Roo Code, Claude Code

$ErrorActionPreference = "Stop"

# Configuration
$SMARTSPEC_REPO = "https://github.com/naibarn/SmartSpec.git"
$SMARTSPEC_VERSION = "v5.0"
$SMARTSPEC_DIR = ".smartspec"
$WORKFLOWS_DIR = "$SMARTSPEC_DIR\workflows"

Write-Host "🚀 SmartSpec Multi-Platform Installer" -ForegroundColor Cyan
Write-Host "======================================" -ForegroundColor Cyan
Write-Host ""

# Check if already installed
$UPDATE_MODE = $false
if (Test-Path $SMARTSPEC_DIR) {
    $UPDATE_MODE = $true
    Write-Host "🔄 SmartSpec is already installed" -ForegroundColor Cyan
    Write-Host "📦 Updating to latest version..." -ForegroundColor Cyan
    Write-Host ""
    
    # Backup custom workflows (if any)
    if (Test-Path $WORKFLOWS_DIR) {
        Write-Host "💾 Backing up existing workflows..."
        Copy-Item -Recurse $WORKFLOWS_DIR "${WORKFLOWS_DIR}.backup"
        Write-Host "  ✅ Backup created" -ForegroundColor Green
    }
    
    # Remove old installation (but keep backup)
    Write-Host "🗑️  Removing old installation..."
    Remove-Item -Recurse -Force $SMARTSPEC_DIR
    Write-Host "  ✅ Old installation removed" -ForegroundColor Green
    Write-Host ""
}

# Step 1: Download workflows and knowledge base
Write-Host "📥 Downloading SmartSpec workflows and knowledge base..."

if (Get-Command git -ErrorAction SilentlyContinue) {
    # Use git sparse checkout
    New-Item -ItemType Directory -Force -Path $SMARTSPEC_DIR | Out-Null
    Push-Location $SMARTSPEC_DIR
    git init -q
    git remote add origin $SMARTSPEC_REPO
    git config core.sparseCheckout true
    ".kilocode/workflows/" | Out-File -Encoding ASCII .git\info\sparse-checkout
    ".smartspec/" | Out-File -Encoding ASCII -Append .git\info\sparse-checkout
    git pull -q origin main 2>&1 | Out-Null
    Move-Item .kilocode\workflows .\workflows
    if (Test-Path ".smartspec") {
        Copy-Item -Recurse .smartspec\* .
    }
    Remove-Item -Recurse -Force .kilocode, .smartspec, .git -ErrorAction SilentlyContinue
    Pop-Location
    Write-Host "✅ Downloaded workflows and knowledge base via git" -ForegroundColor Green
} else {
    # Download as zip
    $zipPath = "smartspec.zip"
    try {
        Invoke-WebRequest -Uri "$SMARTSPEC_REPO/archive/refs/heads/main.zip" -OutFile $zipPath -UseBasicParsing
    } catch {
        Write-Host "❌ Error downloading SmartSpec" -ForegroundColor Red
        Write-Host $_.Exception.Message -ForegroundColor Red
        exit 1
    }
    
    Expand-Archive -Path $zipPath -DestinationPath . -Force
    New-Item -ItemType Directory -Force -Path $WORKFLOWS_DIR | Out-Null
    Copy-Item -Recurse "SmartSpec-main\.kilocode\workflows\*" $WORKFLOWS_DIR\
    if (Test-Path "SmartSpec-main\.smartspec") {
        Copy-Item -Recurse "SmartSpec-main\.smartspec\*" $SMARTSPEC_DIR\
    }
    Remove-Item -Recurse -Force SmartSpec-main, $zipPath
    Write-Host "✅ Downloaded workflows and knowledge base via zip" -ForegroundColor Green
}

# Step 2: Detect platforms
Write-Host ""
Write-Host "🔍 Detecting platforms..."
$PLATFORMS = @()

if (Test-Path ".kilocode") {
    $PLATFORMS += "kilocode"
    Write-Host "  ✅ Kilo Code detected" -ForegroundColor Green
}

if (Test-Path ".roo") {
    $PLATFORMS += "roo"
    Write-Host "  ✅ Roo Code detected" -ForegroundColor Green
}

if (Test-Path ".claude") {
    $PLATFORMS += "claude"
    Write-Host "  ✅ Claude Code detected" -ForegroundColor Green
}

if ($PLATFORMS.Count -eq 0) {
    Write-Host "⚠️  No platforms detected" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Which platforms do you want to install?"
    Write-Host "  1) Kilo Code"
    Write-Host "  2) Roo Code"
    Write-Host "  3) Claude Code"
    Write-Host "  4) All of the above"
    $choice = Read-Host "Enter choice [1-4]"
    
    switch ($choice) {
        1 { $PLATFORMS = @("kilocode") }
        2 { $PLATFORMS = @("roo") }
        3 { $PLATFORMS = @("claude") }
        4 { $PLATFORMS = @("kilocode", "roo", "claude") }
        default { 
            Write-Host "Invalid choice" -ForegroundColor Red
            exit 1
        }
    }
}

# Step 3: Try symlinks first (Windows 10+ with Developer Mode)
Write-Host ""
Write-Host "🔗 Setting up platform integrations..."

$USE_SYMLINKS = $false

# Test if symlinks work
try {
    $testDir = ".smartspec_test"
    New-Item -ItemType Directory -Force -Path $testDir | Out-Null
    New-Item -ItemType SymbolicLink -Path "$testDir\link" -Target $testDir -ErrorAction Stop | Out-Null
    Remove-Item -Recurse -Force $testDir
    $USE_SYMLINKS = $true
    Write-Host "  ✅ Symlinks supported - using symlinks" -ForegroundColor Green
} catch {
    if (Test-Path ".smartspec_test") {
        Remove-Item -Recurse -Force .smartspec_test -ErrorAction SilentlyContinue
    }
    Write-Host "  ⚠️  Symlinks not supported - using copies" -ForegroundColor Yellow
    Write-Host "     (Enable Developer Mode in Windows Settings for symlinks)" -ForegroundColor Gray
    $USE_SYMLINKS = $false
}

# Step 4: Install for each platform
foreach ($platform in $PLATFORMS) {
    switch ($platform) {
        "kilocode" { 
            $TARGET_DIR = ".kilocode\workflows"
            $PLATFORM_NAME = "Kilo Code"
        }
        "roo" { 
            $TARGET_DIR = ".roo\commands"
            $PLATFORM_NAME = "Roo Code"
        }
        "claude" { 
            $TARGET_DIR = ".claude\commands"
            $PLATFORM_NAME = "Claude Code"
        }
    }
    
    # Create parent directory
    $parentDir = Split-Path -Parent $TARGET_DIR
    New-Item -ItemType Directory -Force -Path $parentDir | Out-Null
    
    # Remove existing
    if (Test-Path $TARGET_DIR) {
        Remove-Item -Recurse -Force $TARGET_DIR
    }
    
    # Install
    if ($USE_SYMLINKS) {
        # Create symlink (relative path)
        $sourcePath = "..\..\$WORKFLOWS_DIR"
        New-Item -ItemType SymbolicLink -Path $TARGET_DIR -Target $sourcePath | Out-Null
        Write-Host "  ✅ $PLATFORM_NAME`: Symlink created" -ForegroundColor Green
    } else {
        # Copy files
        Copy-Item -Recurse $WORKFLOWS_DIR $TARGET_DIR
        Write-Host "  ✅ $PLATFORM_NAME`: Files copied" -ForegroundColor Green
    }
}

# Step 5: Save configuration
Write-Host ""
Write-Host "💾 Saving configuration..."

$config = @{
    version = $SMARTSPEC_VERSION
    installed_at = (Get-Date).ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ssZ")
    platforms = $PLATFORMS
    use_symlinks = $USE_SYMLINKS
    repo = $SMARTSPEC_REPO
}

$config | ConvertTo-Json | Out-File -Encoding UTF8 "$SMARTSPEC_DIR\config.json"
$SMARTSPEC_VERSION | Out-File -Encoding UTF8 "$SMARTSPEC_DIR\version.txt"

Write-Host "✅ Configuration saved" -ForegroundColor Green

# Step 6: Create sync script (if using copies)
if (-not $USE_SYMLINKS) {
    $syncScript = @'
# SmartSpec Sync Script (Windows)

$SMARTSPEC_DIR = ".smartspec"
$WORKFLOWS_DIR = "$SMARTSPEC_DIR\workflows"

# Read config
if (-not (Test-Path "$SMARTSPEC_DIR\config.json")) {
    Write-Host "Error: SmartSpec not installed" -ForegroundColor Red
    exit 1
}

$config = Get-Content "$SMARTSPEC_DIR\config.json" | ConvertFrom-Json
$PLATFORMS = $config.platforms

Write-Host "🔄 Syncing SmartSpec workflows..." -ForegroundColor Cyan

foreach ($platform in $PLATFORMS) {
    switch ($platform) {
        "kilocode" { $TARGET_DIR = ".kilocode\workflows" }
        "roo" { $TARGET_DIR = ".roo\commands" }
        "claude" { $TARGET_DIR = ".claude\commands" }
    }
    
    # Sync
    if (Test-Path $TARGET_DIR) {
        Remove-Item -Recurse -Force $TARGET_DIR
    }
    Copy-Item -Recurse $WORKFLOWS_DIR $TARGET_DIR
    Write-Host "  ✅ $platform synced" -ForegroundColor Green
}

Write-Host "✅ Sync complete" -ForegroundColor Green
'@
    
    $syncScript | Out-File -Encoding UTF8 "$SMARTSPEC_DIR\sync.ps1"
    Write-Host "✅ Sync script created" -ForegroundColor Green
}

# Step 7: Success message
Write-Host ""
Write-Host "╔════════════════════════════════════════╗" -ForegroundColor Green
Write-Host "║  ✅ SmartSpec installed successfully!  ║" -ForegroundColor Green
Write-Host "╚════════════════════════════════════════╝" -ForegroundColor Green
Write-Host ""
Write-Host "📍 Installation details:"
Write-Host "  - Version: $SMARTSPEC_VERSION"
Write-Host "  - Location: $SMARTSPEC_DIR"
Write-Host "  - Method: $(if ($USE_SYMLINKS) { 'Symlinks (auto-sync)' } else { 'Copies (manual sync)' })"
Write-Host "  - Platforms: $($PLATFORMS -join ', ')"
Write-Host ""

if (-not $USE_SYMLINKS) {
    Write-Host "📝 Note: You're using copies (not symlinks)" -ForegroundColor Yellow
    Write-Host "   Run '.smartspec\sync.ps1' after updating workflows"
    Write-Host ""
}

Write-Host "🎉 You can now use SmartSpec workflows in:"
foreach ($platform in $PLATFORMS) {
    switch ($platform) {
        "kilocode" { Write-Host "  - Kilo Code: /smartspec_generate_spec, /smartspec_generate_tasks, etc." }
        "roo" { Write-Host "  - Roo Code: /smartspec_generate_spec, /smartspec_generate_tasks, etc." }
        "claude" { Write-Host "  - Claude Code: /smartspec_generate_spec, /smartspec_generate_tasks, etc." }
    }
}

Write-Host ""
Write-Host "📚 Documentation: https://github.com/naibarn/SmartSpec"
Write-Host "💡 Quick start: /smartspec_generate_spec <your-spec-file>"
