<#
SmartSpec Multi-Platform Installer (Project-Local)
Version: 5.2
Supports: Kilo Code, Roo Code, Claude Code, Google Antigravity, Gemini CLI

Master source of workflows: .smartspec/workflows/
This script installs/updates SmartSpec into the current repository and
syncs workflows into project-local tool folders:
  .kilocode/workflows
  .roo/commands
  .claude/commands
  .agent/workflows
  .gemini/commands

Run from your repo root:
  powershell -ExecutionPolicy Bypass -File .smartspec/scripts/install.ps1
or pipe from remote if you prefer.
#>

$ErrorActionPreference = "Stop"

# =============================
# Configuration
# =============================
$SmartSpecVersion = "v5.2"
$SmartSpecDir = ".smartspec"
$WorkflowsDir = Join-Path $SmartSpecDir "workflows"

$RepoZipUrl = "https://github.com/naibarn/SmartSpec/archive/refs/heads/main.zip"
$RepoGitUrl = "https://github.com/naibarn/SmartSpec.git"

# Project-local platform directories
$KiloCodeDir     = ".kilocode\workflows"
$RooDir          = ".roo\commands"
$ClaudeDir       = ".claude\commands"
$AntigravityDir  = ".agent\workflows"
$GeminiDir       = ".gemini\commands"

function Write-Info($msg)  { Write-Host $msg -ForegroundColor Cyan }
function Write-Ok($msg)    { Write-Host $msg -ForegroundColor Green }
function Write-Warn($msg)  { Write-Host $msg -ForegroundColor Yellow }
function Write-Err($msg)   { Write-Host $msg -ForegroundColor Red }

function New-TempDir {
    $base = [System.IO.Path]::GetTempPath()
    $name = "smartspec_" + ([System.Guid]::NewGuid().ToString("N"))
    $path = Join-Path $base $name
    New-Item -ItemType Directory -Path $path | Out-Null
    return $path
}

function Backup-IfExists($path) {
    if (Test-Path $path) {
        $ts = Get-Date -Format "yyyyMMdd_HHmmss"
        $backup = "$path.backup.$ts"
        Copy-Item -Recurse -Force $path $backup
        Write-Ok "Backup created: $backup"
    }
}

# =============================
# Header
# =============================
Write-Info "🚀 SmartSpec Multi-Platform Installer (Project-Local)"
Write-Info "====================================================="
Write-Host ""

$updateMode = Test-Path $SmartSpecDir
if ($updateMode) {
    Write-Info "🔄 Existing SmartSpec detected — updating"
    Backup-IfExists $WorkflowsDir
}

# =============================
# Step 1: Download SmartSpec .smartspec
# =============================
Write-Info "📥 Downloading SmartSpec framework (.smartspec)..."

$tmp = New-TempDir
try {
    $repoPath = Join-Path $tmp "repo"
    $zipPath  = Join-Path $tmp "smartspec.zip"

    $git = Get-Command git -ErrorAction SilentlyContinue
    if ($git) {
        Write-Info "  • Using git"
        git clone --depth 1 $RepoGitUrl $repoPath | Out-Null
        $sourceSpec = Join-Path $repoPath ".smartspec"
        if (-not (Test-Path $sourceSpec)) { throw ".smartspec folder not found in git repo" }

        if ($updateMode -and (Test-Path $WorkflowsDir)) {
            # Replace non-workflow assets, keep workflows
            $items = Get-ChildItem $sourceSpec -Force
            foreach ($item in $items) {
                if ($item.Name -eq "workflows") { continue }
                $dest = Join-Path $SmartSpecDir $item.Name
                if (Test-Path $dest) { Remove-Item -Recurse -Force $dest }
                Copy-Item -Recurse -Force $item.FullName $dest
            }
        }
        else {
            if (Test-Path $SmartSpecDir) { Remove-Item -Recurse -Force $SmartSpecDir }
            Copy-Item -Recurse -Force $sourceSpec $SmartSpecDir
        }
    }
    else {
        Write-Info "  • Using zip download"
        Invoke-WebRequest -Uri $RepoZipUrl -OutFile $zipPath
        Expand-Archive -Path $zipPath -DestinationPath $tmp -Force

        $root = Get-ChildItem $tmp -Directory | Where-Object { $_.Name -like "SmartSpec-*" } | Select-Object -First 1
        if (-not $root) { throw "SmartSpec-* folder not found in zip" }
        $sourceSpec = Join-Path $root.FullName ".smartspec"
        if (-not (Test-Path $sourceSpec)) { throw ".smartspec folder not found in zip" }

        if ($updateMode -and (Test-Path $WorkflowsDir)) {
            $items = Get-ChildItem $sourceSpec -Force
            foreach ($item in $items) {
                if ($item.Name -eq "workflows") { continue }
                $dest = Join-Path $SmartSpecDir $item.Name
                if (Test-Path $dest) { Remove-Item -Recurse -Force $dest }
                Copy-Item -Recurse -Force $item.FullName $dest
            }
        }
        else {
            if (Test-Path $SmartSpecDir) { Remove-Item -Recurse -Force $SmartSpecDir }
            Copy-Item -Recurse -Force $sourceSpec $SmartSpecDir
        }
    }

    if (-not (Test-Path $WorkflowsDir)) {
        throw "Master workflows directory not found: $WorkflowsDir"
    }

    Write-Ok "SmartSpec framework ready"
}
finally {
    if (Test-Path $tmp) { Remove-Item -Recurse -Force $tmp }
}

Write-Host ""

# =============================
# Step 2: Choose platforms
# =============================
Write-Info "Which platforms do you want to install/update in this repo?"
Write-Host "  1) Kilo Code (.kilocode)"
Write-Host "  2) Roo Code (.roo)"
Write-Host "  3) Claude Code (.claude)"
Write-Host "  4) Google Antigravity (.agent)"
Write-Host "  5) Gemini CLI (.gemini)"
Write-Host "  6) All of the above"
Write-Host ""

$choice = Read-Host "Enter choice [1-6] (default: 6)"
if ([string]::IsNullOrWhiteSpace($choice)) { $choice = "6" }

$platforms = switch ($choice) {
    "1" { @("kilocode") }
    "2" { @("roo") }
    "3" { @("claude") }
    "4" { @("antigravity") }
    "5" { @("gemini-cli") }
    default { @("kilocode","roo","claude","antigravity","gemini-cli") }
}

# =============================
# Step 3: Write config.json
# =============================
$platformJson = ($platforms | ForEach-Object { '"' + $_ + '"' }) -join ", "
$cfg = @"
{
  "version": "$SmartSpecVersion",
  "platforms": [$platformJson],
  "use_symlinks": false,
  "install_scope": "project-local"
}
"@

New-Item -ItemType Directory -Path $SmartSpecDir -Force | Out-Null
Set-Content -Path (Join-Path $SmartSpecDir "config.json") -Value $cfg -Encoding UTF8
Write-Ok "Config written: .smartspec\config.json"

# =============================
# Step 4: Create/update sync.ps1
# =============================
$syncPath = Join-Path $SmartSpecDir "sync.ps1"

$syncContent = @'
<#
SmartSpec Sync Script (Project-Local)
Copies master workflows from .smartspec/workflows to tool folders in this repo.
#>

$ErrorActionPreference = "Stop"

$SmartSpecDir = ".smartspec"
$WorkflowsDir = Join-Path $SmartSpecDir "workflows"
$ConfigPath   = Join-Path $SmartSpecDir "config.json"

$KiloCodeDir     = ".kilocode\workflows"
$RooDir          = ".roo\commands"
$ClaudeDir       = ".claude\commands"
$AntigravityDir  = ".agent\workflows"
$GeminiDir       = ".gemini\commands"

function Write-Info($msg)  { Write-Host $msg -ForegroundColor Cyan }
function Write-Ok($msg)    { Write-Host $msg -ForegroundColor Green }
function Write-Warn($msg)  { Write-Host $msg -ForegroundColor Yellow }
function Write-Err($msg)   { Write-Host $msg -ForegroundColor Red }

if (-not (Test-Path $WorkflowsDir)) {
    Write-Err "Master workflows directory not found: $WorkflowsDir"
    exit 1
}

$platforms = @("kilocode","roo","claude","antigravity","gemini-cli")
if (Test-Path $ConfigPath) {
    try {
        $cfg = Get-Content $ConfigPath -Raw | ConvertFrom-Json
        if ($cfg.platforms) { $platforms = $cfg.platforms }
    } catch {
        # ignore
    }
}

Write-Info "🔄 SmartSpec Sync (project-local)"
Write-Info "=============================="
Write-Host ""

foreach ($p in $platforms) {
    switch ($p) {
        "kilocode"     { $target = $KiloCodeDir;    $name = "Kilo Code" }
        "roo"          { $target = $RooDir;         $name = "Roo Code" }
        "claude"       { $target = $ClaudeDir;      $name = "Claude Code" }
        "antigravity"  { $target = $AntigravityDir; $name = "Google Antigravity" }
        "gemini-cli"   { $target = $GeminiDir;      $name = "Gemini CLI" }
        default        { Write-Warn "Unknown platform '$p' - skipping"; continue }
    }

    New-Item -ItemType Directory -Path $target -Force | Out-Null

    if ($p -eq "gemini-cli") {
        $mdFiles = Get-ChildItem $WorkflowsDir -Filter "smartspec_*.md" -File -ErrorAction SilentlyContinue
        $count = 0
        foreach ($md in $mdFiles) {
            $filename = [System.IO.Path]::GetFileNameWithoutExtension($md.Name)
            $toml = Join-Path $target ("$filename.toml")

            $lines = Get-Content $md.FullName
            # Description priority: YAML frontmatter line, then first heading
            $desc = ($lines | Where-Object { $_ -match '^description:' } | Select-Object -First 1)
            if ($desc) { $desc = $desc -replace '^description:\s*','' }
            else {
                $h1 = ($lines | Where-Object { $_ -match '^#\s+' } | Select-Object -First 1)
                if ($h1) { $desc = $h1 -replace '^#\s+','' }
            }
            if ([string]::IsNullOrWhiteSpace($desc)) { $desc = "SmartSpec workflow: $filename" }

            # Find end of frontmatter (second ---)
            $dashIdx = @()
            for ($i=0; $i -lt $lines.Count; $i++) {
                if ($lines[$i].Trim() -eq "---") { $dashIdx += $i }
            }
            if ($dashIdx.Count -ge 2) {
                $promptLines = $lines[($dashIdx[1]+1)..($lines.Count-1)]
            } else {
                $promptLines = $lines[1..($lines.Count-1)]
            }
            $prompt = ($promptLines -join "`n")

            $tomlContent = @(
                "description = \"$desc\"",
                "",
                "prompt = \"\"\"",
                $prompt,
                "\"\"\""
            ) -join "`n"

            Set-Content -Path $toml -Value $tomlContent -Encoding UTF8
            $count++
        }
        Write-Ok "$name synced ($count TOML files generated)"
        continue
    }

    Copy-Item -Force (Join-Path $WorkflowsDir "smartspec_*.md") $target -ErrorAction SilentlyContinue
    Write-Ok "$name synced"
}

Write-Host ""
Write-Ok "Sync complete"
'@

Set-Content -Path $syncPath -Value $syncContent -Encoding UTF8
Write-Ok "Sync script ready: .smartspec\sync.ps1"

# =============================
# Step 5: Run initial sync
# =============================
Write-Host ""
Write-Info "🔄 Syncing workflows to project tool folders..."
& $syncPath

# =============================
# Step 6: Optional git hook
# =============================
if (Test-Path ".git") {
    $hookDir = ".git\hooks"
    New-Item -ItemType Directory -Path $hookDir -Force | Out-Null
    $hookPath = Join-Path $hookDir "post-merge"
    $hook = @"
#!/usr/bin/env bash
# Auto-sync SmartSpec after git pull/merge (project-local)

if [ -f ".smartspec/sync.sh" ]; then
  .smartspec/sync.sh
elif [ -f ".smartspec/sync.ps1" ]; then
  powershell -ExecutionPolicy Bypass -File .smartspec/sync.ps1
fi
"@
    Set-Content -Path $hookPath -Value $hook -Encoding UTF8
    try { git update-index --add --chmod=+x $hookPath | Out-Null } catch {}
    Write-Ok "Git hook installed (auto-sync on pull)"
}

# =============================
# Done
# =============================
Write-Host ""
Write-Ok "✅ SmartSpec installed successfully!"
Write-Host "Version: $SmartSpecVersion"
Write-Host "Scope: project-local"
Write-Host "Location: $SmartSpecDir"
Write-Host "Platforms: $($platforms -join ', ')"
Write-Host ""
Write-Warn "Always edit master workflows in .smartspec\workflows"
Write-Warn "Run .smartspec\sync.ps1 to re-sync anytime"
