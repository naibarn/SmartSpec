# SmartSpec Multi-Platform Installer (Windows)
# Version: 5.2
# Supports: Kilo Code, Roo Code, Claude Code

$ErrorActionPreference = "Stop"

# Configuration
$SMARTSPEC_REPO_GIT_GIT = "https://github.com/naibarn/SmartSpec.git"
$SMARTSPEC_REPO_GIT_URL = "https://github.com/naibarn/SmartSpec"
$SMARTSPEC_VERSION = "v5.2"
$SMARTSPEC_DIR = ".smartspec"
$WORKFLOWS_DIR = "$SMARTSPEC_DIR\workflows"

# Platform directories (home-based)
$KILOCODE_DIR = "$env:USERPROFILE\.kilocode\workflows"
$ROO_DIR = "$env:USERPROFILE\.roo\commands"
$CLAUDE_DIR = "$env:USERPROFILE\.claude\commands"
$ANTIGRAVITY_DIR = "$env:USERPROFILE\.agent\workflows"
$GEMINI_CLI_DIR = "$env:USERPROFILE\.gemini\commands"

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
    git remote add origin $SMARTSPEC_REPO_GIT
    git config core.sparseCheckout true
    ".smartspec/" | Out-File -Encoding ASCII .git\info\sparse-checkout
    git pull -q origin main 2>&1 | Out-Null
    # Move all files and directories from .smartspec/ to current directory
    if (Test-Path ".smartspec") {
        Get-ChildItem -Path ".smartspec" -Force | Move-Item -Destination . -Force
    }
    Remove-Item -Recurse -Force .smartspec, .git -ErrorAction SilentlyContinue
    Pop-Location
    Write-Host "✅ Downloaded workflows and knowledge base via git" -ForegroundColor Green
} else {
    # Download as zip
    $zipPath = "smartspec.zip"
    try {
        Invoke-WebRequest -Uri "$SMARTSPEC_REPO_URL/archive/refs/heads/main.zip" -OutFile $zipPath -UseBasicParsing
    } catch {
        Write-Host "❌ Error downloading SmartSpec" -ForegroundColor Red
        Write-Host $_.Exception.Message -ForegroundColor Red
        exit 1
    }
    
    Expand-Archive -Path $zipPath -DestinationPath . -Force
    New-Item -ItemType Directory -Force -Path $WORKFLOWS_DIR | Out-Null
    # Workflows are stored under .smartspec\workflows in the SmartSpec repo
    # Copy the full .smartspec package into the project
    Copy-Item -Recurse "SmartSpec-main\.smartspec\*" $SMARTSPEC_DIR\ -Force
    if (Test-Path "SmartSpec-main\.smartspec") {
        Copy-Item -Recurse "SmartSpec-main\.smartspec\*" $SMARTSPEC_DIR\
    }
    Remove-Item -Recurse -Force SmartSpec-main, $zipPath
    Write-Host "✅ Downloaded workflows and knowledge base via zip" -ForegroundColor Green
}

# Step 2: Detect platforms and ask user
Write-Host ""
Write-Host "🔍 Detecting platforms..."

$DETECTED_PLATFORMS = @()
if ($false) { # deprecated legacy block removed
    $DETECTED_PLATFORMS += "kilocode"
    Write-Host "  ✅ Kilo Code detected" -ForegroundColor Green
}

if (Test-Path ".roo") {
    $DETECTED_PLATFORMS += "roo"
    Write-Host "  ✅ Roo Code detected" -ForegroundColor Green
}

if (Test-Path ".claude") {
    $DETECTED_PLATFORMS += "claude"
    Write-Host "  ✅ Claude Code detected" -ForegroundColor Green
}

if ($DETECTED_PLATFORMS.Count -eq 0) {
    Write-Host "  ⚠️  No platforms detected" -ForegroundColor Yellow
}

# Always ask user which platforms to install
Write-Host ""
Write-Host "Which platforms do you want to install/update?"
Write-Host "  1) Kilo Code"
Write-Host "  2) Roo Code"
Write-Host "  3) Claude Code"
Write-Host "  4) All of the above"
$choice = Read-Host "Enter choice [1-4] (default: 1)"

# Default to 1 if empty
if ([string]::IsNullOrWhiteSpace($choice)) {
    $choice = "1"
}

switch ($choice) {
    "1" { $PLATFORMS = @("kilocode") }
    "2" { $PLATFORMS = @("roo") }
    "3" { $PLATFORMS = @("claude") }
    "4" { $PLATFORMS = @("kilocode", "roo", "claude") }
    default { 
        Write-Host "Invalid choice: $choice" -ForegroundColor Red
        exit 1
    }
}

# Step 3: Install workflows
Write-Host ""
Write-Host "📦 Installing SmartSpec workflows..."

# Step 4: Install for each platform
foreach ($platform in $PLATFORMS) {
    switch ($platform) {
        "kilocode" { 
            $TARGET_DIR = $KILOCODE_DIR
            $PLATFORM_NAME = "Kilo Code"
        }
        "roo" { 
            $TARGET_DIR = $ROO_DIR
            $PLATFORM_NAME = "Roo Code"
        }
        "claude" { 
            $TARGET_DIR = $CLAUDE_DIR
            $PLATFORM_NAME = "Claude Code"
        }
    }
    
    # Create parent directory
    $parentDir = Split-Path -Parent $TARGET_DIR
    New-Item -ItemType Directory -Force -Path $parentDir | Out-Null
    
    # Verify source directory exists
    if (-not (Test-Path $WORKFLOWS_DIR)) {
        Write-Host "  ❌ Error: Workflows directory not found: $WORKFLOWS_DIR" -ForegroundColor Red
        exit 1
    }
    
    # Handle existing workflows directory
    if (Test-Path $TARGET_DIR) {
        $item = Get-Item $TARGET_DIR
        if ($item.LinkType -eq "SymbolicLink") {
            # Remove old symlink and convert to directory
            Write-Host "  🔗 Converting symlink to directory" -ForegroundColor Cyan
            Remove-Item $TARGET_DIR -Force
            New-Item -ItemType Directory -Force -Path $TARGET_DIR | Out-Null
            Copy-Item "$WORKFLOWS_DIR\smartspec_*.md" $TARGET_DIR -ErrorAction SilentlyContinue
            Write-Host "  ✅ $PLATFORM_NAME`: Workflows installed" -ForegroundColor Green
        } else {
            # Directory exists - merge workflows
            Write-Host "  🔍 Checking for existing SmartSpec workflows..." -ForegroundColor Cyan
            
            # Find existing SmartSpec workflows
            $existingSmartSpec = @(Get-ChildItem -Path $TARGET_DIR -Filter "smartspec_*.md" -ErrorAction SilentlyContinue)
            
            if ($existingSmartSpec.Count -gt 0) {
                Write-Host "  ⚠️  Found $($existingSmartSpec.Count) existing SmartSpec workflow(s)" -ForegroundColor Yellow
                Write-Host ""
                Write-Host "  How do you want to proceed?"
                Write-Host "    1) Overwrite all (recommended for updates)"
                Write-Host "    2) Skip all (keep existing versions)"
                Write-Host "    3) Cancel installation"
                $overwriteChoice = Read-Host "  Enter choice [1-3] (default: 1)"
                
                # Default to 1 if empty
                if ([string]::IsNullOrWhiteSpace($overwriteChoice)) {
                    $overwriteChoice = "1"
                }
                
                switch ($overwriteChoice) {
                    "1" {
                        # Backup existing SmartSpec workflows
                        $timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
                        $BACKUP_DIR = "${TARGET_DIR}.smartspec.backup.$timestamp"
                        New-Item -ItemType Directory -Force -Path $BACKUP_DIR | Out-Null
                        foreach ($file in $existingSmartSpec) {
                            Copy-Item $file.FullName $BACKUP_DIR -ErrorAction SilentlyContinue
                        }
                        Write-Host "  💾 Backed up existing SmartSpec workflows to $(Split-Path -Leaf $BACKUP_DIR)" -ForegroundColor Green
                        
                        # Copy new workflows
                        Copy-Item "$WORKFLOWS_DIR\smartspec_*.md" $TARGET_DIR -Force -ErrorAction SilentlyContinue
                        Write-Host "  ✅ $PLATFORM_NAME`: Workflows merged ($($existingSmartSpec.Count) updated)" -ForegroundColor Green
                    }
                    "2" {
                        # Copy only new workflows (skip existing)
                        $copied = 0
                        $newWorkflows = Get-ChildItem -Path $WORKFLOWS_DIR -Filter "smartspec_*.md"
                        foreach ($file in $newWorkflows) {
                            $targetFile = Join-Path $TARGET_DIR $file.Name
                            if (-not (Test-Path $targetFile)) {
                                Copy-Item $file.FullName $targetFile
                                $copied++
                            }
                        }
                        Write-Host "  ✅ $PLATFORM_NAME`: $copied new workflow(s) added" -ForegroundColor Green
                    }
                    "3" {
                        Write-Host "  ❌ Installation cancelled for $PLATFORM_NAME" -ForegroundColor Yellow
                        continue
                    }
                    default {
                        Write-Host "  Invalid choice, skipping $PLATFORM_NAME" -ForegroundColor Red
                        continue
                    }
                }
            } else {
                # No existing SmartSpec workflows, just copy
                Copy-Item "$WORKFLOWS_DIR\smartspec_*.md" $TARGET_DIR -ErrorAction SilentlyContinue
                Write-Host "  ✅ $PLATFORM_NAME`: Workflows installed" -ForegroundColor Green
            }
        }
    } else {
        # Directory doesn't exist - create and copy
        New-Item -ItemType Directory -Force -Path $TARGET_DIR | Out-Null
        Copy-Item "$WORKFLOWS_DIR\smartspec_*.md" $TARGET_DIR -ErrorAction SilentlyContinue
        Write-Host "  ✅ $PLATFORM_NAME`: Workflows installed" -ForegroundColor Green
    }
}

# Step 5: Save configuration
Write-Host ""
Write-Host "💾 Saving configuration..."

$config = @{
    version = $SMARTSPEC_VERSION
    installed_at = (Get-Date).ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ssZ")
    platforms = $PLATFORMS
    use_symlinks = $false
    repo = $SMARTSPEC_REPO_URL
}

$config | ConvertTo-Json | Out-File -Encoding UTF8 "$SMARTSPEC_DIR\config.json"
$SMARTSPEC_VERSION | Out-File -Encoding UTF8 "$SMARTSPEC_DIR\version.txt"

Write-Host "✅ Configuration saved" -ForegroundColor Green

# Step 6: Create sync script
# Always create sync script for manual updates
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
        "kilocode" { $TARGET_DIR = $KILOCODE_DIR }
        "roo" { $TARGET_DIR = $ROO_DIR }
        "claude" { $TARGET_DIR = $CLAUDE_DIR }
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

# Step 7: Success message
Write-Host ""
Write-Host "╔════════════════════════════════════════╗" -ForegroundColor Green
Write-Host "║  ✅ SmartSpec installed successfully!  ║" -ForegroundColor Green
Write-Host "╚════════════════════════════════════════╝" -ForegroundColor Green
Write-Host ""
Write-Host "📍 Installation details:"
Write-Host "  - Version: $SMARTSPEC_VERSION"
Write-Host "  - Location: $SMARTSPEC_DIR"
Write-Host "  - Method: Merged installation (preserves existing workflows)"
Write-Host "  - Platforms: $($PLATFORMS -join ', ')"
Write-Host ""

Write-Host "📝 Note: SmartSpec workflows are merged with your existing workflows" -ForegroundColor Yellow
Write-Host "   Run '.smartspec\sync.ps1' to update SmartSpec workflows from repository"
Write-Host ""

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