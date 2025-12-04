# SmartSpec Sync Script (Standalone - Windows)
# Use this to manually sync workflows to all platforms

$SMARTSPEC_DIR = ".smartspec"
$WORKFLOWS_DIR = "$SMARTSPEC_DIR\workflows"

Write-Host "🔄 SmartSpec Sync Tool" -ForegroundColor Cyan
Write-Host "=====================" -ForegroundColor Cyan
Write-Host ""

# Check if SmartSpec is installed
if (-not (Test-Path $SMARTSPEC_DIR)) {
    Write-Host "❌ Error: SmartSpec is not installed" -ForegroundColor Red
    Write-Host "Run 'install.ps1' first"
    exit 1
}

# Check if config exists
if (-not (Test-Path "$SMARTSPEC_DIR\config.json")) {
    Write-Host "❌ Error: SmartSpec configuration not found" -ForegroundColor Red
    exit 1
}

# Read config
try {
    $config = Get-Content "$SMARTSPEC_DIR\config.json" | ConvertFrom-Json
    $PLATFORMS = $config.platforms
    $USE_SYMLINKS = $config.use_symlinks
} catch {
    Write-Host "❌ Error reading configuration" -ForegroundColor Red
    exit 1
}

# Check if using symlinks
if ($USE_SYMLINKS) {
    Write-Host "⚠️  You're using symlinks - sync is automatic" -ForegroundColor Yellow
    Write-Host "No manual sync needed!"
    exit 0
}

# Sync to each platform
Write-Host "Syncing workflows to platforms..."
Write-Host ""

$SYNCED = 0
$FAILED = 0

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
    
    # Check if parent directory exists
    $parentDir = Split-Path -Parent $TARGET_DIR
    if (-not (Test-Path $parentDir)) {
        Write-Host "  ⚠️  $PLATFORM_NAME directory not found - skipping" -ForegroundColor Yellow
        continue
    }
    
    # Sync
    try {
        if (Test-Path $TARGET_DIR) {
            Remove-Item -Recurse -Force $TARGET_DIR
        }
        Copy-Item -Recurse $WORKFLOWS_DIR $TARGET_DIR
        Write-Host "  ✅ $PLATFORM_NAME synced" -ForegroundColor Green
        $SYNCED++
    } catch {
        Write-Host "  ❌ Failed to sync $PLATFORM_NAME" -ForegroundColor Red
        Write-Host "     $($_.Exception.Message)" -ForegroundColor Gray
        $FAILED++
    }
}

Write-Host ""
if ($SYNCED -gt 0) {
    Write-Host "✅ Sync complete - $SYNCED platform(s) updated" -ForegroundColor Green
} else {
    Write-Host "⚠️  No platforms synced" -ForegroundColor Yellow
}

if ($FAILED -gt 0) {
    Write-Host "⚠️  $FAILED platform(s) failed" -ForegroundColor Yellow
}
