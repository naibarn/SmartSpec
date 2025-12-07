# SmartSpec Multi-Platform Installer (PowerShell)
# Version: 5.2 (centralization-compatible)
# Supports: Kilo Code, Roo Code, Claude Code, Google Antigravity, Gemini CLI
#
# Master source of workflows: .smartspec/workflows/
# This script installs/updates SmartSpec into the current project
# and syncs workflows to platform-specific command folders in your home directory.

$ErrorActionPreference = "Stop"

$SmartSpecRepoZip = "https://github.com/naibarn/SmartSpec/archive/refs/heads/main.zip"
$SmartSpecVersion = "v5.2"
$SmartSpecDir = ".smartspec"
$WorkflowsDir = Join-Path $SmartSpecDir "workflows"

# Platform directories (home-based defaults)
$KiloDir = Join-Path $HOME ".kilocode\workflows"
$RooDir = Join-Path $HOME ".roo\commands"
$ClaudeDir = Join-Path $HOME ".claude\commands"
$AgentDir = Join-Path $HOME ".agent\workflows"
$GeminiDir = Join-Path $HOME ".gemini\commands"

Write-Host "🚀 SmartSpec Multi-Platform Installer" -ForegroundColor Cyan
Write-Host "======================================" -ForegroundColor Cyan
Write-Host ""

# Backup & remove old install if exists
if (Test-Path $SmartSpecDir) {
    Write-Host "🔄 SmartSpec is already installed. Updating..." -ForegroundColor Cyan

    if (Test-Path $WorkflowsDir) {
        Write-Host "💾 Backing up existing workflows..."
        Copy-Item $WorkflowsDir "$WorkflowsDir.backup" -Recurse -Force
        Write-Host "  ✅ Backup created" -ForegroundColor Green
    }

    Write-Host "🗑️  Removing old installation..."
    Remove-Item $SmartSpecDir -Recurse -Force
    Write-Host "  ✅ Old installation removed" -ForegroundColor Green
    Write-Host ""
}

# Step 1: Download SmartSpec zip
Write-Host "📥 Downloading SmartSpec workflows and knowledge base..."
$tempRoot = Join-Path $env:TEMP ("smartspec_install_" + [guid]::NewGuid().ToString("N"))
New-Item -ItemType Directory -Path $tempRoot | Out-Null

$zipPath = Join-Path $tempRoot "smartspec.zip"
Invoke-WebRequest -Uri $SmartSpecRepoZip -OutFile $zipPath

Expand-Archive -Path $zipPath -DestinationPath $tempRoot -Force

$repoExtract = Join-Path $tempRoot "SmartSpec-main"
$sourceSpec = Join-Path $repoExtract ".smartspec"

if (-not (Test-Path $sourceSpec)) {
    throw "'.smartspec' folder not found in the downloaded archive."
}

New-Item -ItemType Directory -Path $SmartSpecDir | Out-Null
Copy-Item (Join-Path $sourceSpec "*") $SmartSpecDir -Recurse -Force

Remove-Item $tempRoot -Recurse -Force

if (-not (Test-Path $WorkflowsDir)) {
    throw "Master workflows directory not found: $WorkflowsDir"
}

Write-Host "  ✅ Downloaded SmartSpec" -ForegroundColor Green
Write-Host ""

# Step 2: Select platforms
Write-Host "Which platforms do you want to install/update?"
Write-Host "  1) Kilo Code"
Write-Host "  2) Roo Code"
Write-Host "  3) Claude Code"
Write-Host "  4) Google Antigravity"
Write-Host "  5) Gemini CLI"
Write-Host "  6) All of the above"

$choice = Read-Host "Enter choice [1-6] (default: 1)"
if ([string]::IsNullOrWhiteSpace($choice)) { $choice = "1" }

switch ($choice) {
    "1" { $platforms = @("kilocode") }
    "2" { $platforms = @("roo") }
    "3" { $platforms = @("claude") }
    "4" { $platforms = @("antigravity") }
    "5" { $platforms = @("gemini-cli") }
    "6" { $platforms = @("kilocode","roo","claude","antigravity","gemini-cli") }
    default { throw "Invalid choice: $choice" }
}

# Step 3: Save configuration
Write-Host ""
Write-Host "💾 Saving configuration..."

$config = @{
    version = $SmartSpecVersion
    installed_at = (Get-Date).ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ssZ")
    platforms = $platforms
    use_symlinks = $false
    repo = "https://github.com/naibarn/SmartSpec.git"
}

$config | ConvertTo-Json -Depth 4 | Set-Content -Path (Join-Path $SmartSpecDir "config.json") -Encoding UTF8
$SmartSpecVersion | Set-Content -Path (Join-Path $SmartSpecDir "version.txt") -Encoding UTF8

Write-Host "  ✅ Configuration saved" -ForegroundColor Green

# Step 4: Create project helper sync.ps1 (wrapper)
$syncHelperPath = Join-Path $SmartSpecDir "sync.ps1"

$syncHelper = @'
# SmartSpec Sync Script (Project Helper) - PowerShell
$ErrorActionPreference = "Stop"

$root = Resolve-Path (Join-Path (Split-Path -Parent $MyInvocation.MyCommand.Path) "..")
$standalone = Join-Path $root "sync.ps1"

if (Test-Path $standalone) {
    & $standalone @args
    exit $LASTEXITCODE
}

throw "Root-level sync.ps1 not found. Please run the standalone sync.ps1 from your SmartSpec distribution."
'@

Set-Content -Path $syncHelperPath -Value $syncHelper -Encoding UTF8

Write-Host "  ✅ Sync helper created at .smartspec/sync.ps1" -ForegroundColor Green

# Step 5: Initial sync (inline)
Write-Host ""
Write-Host "📦 Installing SmartSpec workflows..."

function Get-FrontmatterEndIndex([string[]]$lines) {
    $indexes = @()
    for ($i=0; $i -lt $lines.Length; $i++) {
        if ($lines[$i].Trim() -eq "---") { $indexes += $i }
        if ($indexes.Count -ge 2) { break }
    }
    if ($indexes.Count -ge 2) { return $indexes[1] }
    return $null
}

function Convert-MdToToml([string]$mdPath, [string]$tomlPath) {
    $lines = Get-Content $mdPath

    $descLine = $lines | Where-Object { $_ -match "^\s*description\s*:" } | Select-Object -First 1
    $description = ""
    if ($descLine) {
        $description = ($descLine -replace "^\s*description\s*:\s*", "").Trim()
    }
    if ([string]::IsNullOrWhiteSpace($description)) {
        $titleLine = $lines | Where-Object { $_ -match "^\s*#\s+" } | Select-Object -First 1
        if ($titleLine) {
            $description = ($titleLine -replace "^\s*#\s+", "").Trim()
        }
    }
    if ([string]::IsNullOrWhiteSpace($description)) {
        $base = [IO.Path]::GetFileNameWithoutExtension($mdPath)
        $description = "SmartSpec workflow: " + ($base -replace "_", " ")
    }

    $frontEnd = Get-FrontmatterEndIndex $lines
    if ($frontEnd -ne $null) {
        $promptLines = $lines[($frontEnd+1)..($lines.Length-1)]
    } else {
        if ($lines.Length -gt 1) { $promptLines = $lines[1..($lines.Length-1)] } else { $promptLines = @() }
    }

    $prompt = ($promptLines -join "`n")

    $toml = @()
    $toml += "description = `"$description`""
    $toml += ""
    $toml += "prompt = `"`"`"`""
    $toml += $prompt
    $toml += "`"`"`"`""

    Set-Content -Path $tomlPath -Value $toml -Encoding UTF8
}

$mdFiles = Get-ChildItem -Path $WorkflowsDir -Filter "smartspec_*.md" -File

foreach ($p in $platforms) {
    switch ($p) {
        "kilocode" { $target = $KiloDir; $name = "Kilo Code" }
        "roo" { $target = $RooDir; $name = "Roo Code" }
        "claude" { $target = $ClaudeDir; $name = "Claude Code" }
        "antigravity" { $target = $AgentDir; $name = "Google Antigravity" }
        "gemini-cli" { $target = $GeminiDir; $name = "Gemini CLI" }
        default { continue }
    }

    New-Item -ItemType Directory -Path $target -Force | Out-Null

    if ($p -eq "gemini-cli") {
        foreach ($md in $mdFiles) {
            $base = [IO.Path]::GetFileNameWithoutExtension($md.Name)
            $tomlPath = Join-Path $target ($base + ".toml")
            Convert-MdToToml $md.FullName $tomlPath
        }
        Write-Host "  ✅ $name installed (TOML)" -ForegroundColor Green
        continue
    }

    Get-ChildItem -Path $target -Filter "smartspec_*.md" -File -ErrorAction SilentlyContinue | Remove-Item -Force -ErrorAction SilentlyContinue
    foreach ($md in $mdFiles) { Copy-Item $md.FullName $target -Force }

    Write-Host "  ✅ $name installed" -ForegroundColor Green
}

Write-Host ""
Write-Host "✅ SmartSpec installed successfully!" -ForegroundColor Green
Write-Host "Edit workflows in .smartspec/workflows/ and run .smartspec\sync.ps1 to re-sync."
