<#!
.SYNOPSIS
  SmartSpec Installer (Project-Local) for Windows (PowerShell)

.DESCRIPTION
  - Downloads the SmartSpec distribution repo
  - Copies `.smartspec/` and `.smartspec-docs/` into the current project
  - Ensures stable filenames:
      .smartspec/system_prompt_smartspec.md
      .smartspec/knowledge_base_smartspec.md
  - Copies .smartspec/workflows into tool-specific folders if present:
      .kilocode/workflows
      .roo/commands
      .claude/commands
      .agent/workflows
      .gemini/commands

  Configure `$env:SMARTSPEC_REPO_URL` and `$env:SMARTSPEC_REPO_BRANCH`
  as needed, or edit defaults below.

.NOTES
  Version: 5.6
#>

param()

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

################################
# Configuration
################################

$SmartSpecRepoUrl    = $env:SMARTSPEC_REPO_URL
if (-not $SmartSpecRepoUrl) { $SmartSpecRepoUrl = 'https://github.com/your-org/SmartSpec.git' }

$SmartSpecRepoBranch = $env:SMARTSPEC_REPO_BRANCH
if (-not $SmartSpecRepoBranch) { $SmartSpecRepoBranch = 'main' }

$SmartSpecDir       = '.smartspec'
$SmartSpecDocsDir   = '.smartspec-docs'
$WorkflowsDir       = Join-Path $SmartSpecDir 'workflows'
$WorkflowDocsDir    = Join-Path $SmartSpecDocsDir 'workflows'

$KiloDir            = '.kilocode/workflows'
$RooDir             = '.roo/commands'
$ClaudeDir          = '.claude/commands'
$AntigravityDir     = '.agent/workflows'
$GeminiDir          = '.gemini/commands'

################################
# Helpers
################################

function Write-Log {
  param([string]$Message)
  Write-Host $Message
}

function New-TempDir {
  $base = Join-Path ([System.IO.Path]::GetTempPath()) "smartspec_$([System.Guid]::NewGuid().ToString('N'))"
  New-Item -ItemType Directory -Path $base | Out-Null
  return $base
}

function Backup-DirIfExists {
  param([string]$Path)
  if (Test-Path $Path -PathType Container) {
    $stamp = Get-Date -Format 'yyyyMMdd_HHmmss'
    $backup = "$Path.backup.$stamp"
    Write-Log "  • Backing up '$Path' -> '$backup'"
    Copy-Item -Recurse -Force $Path $backup
  }
}

function Copy-Dir {
  param(
    [string]$Source,
    [string]$Destination
  )
  if (-not (Test-Path $Source -PathType Container)) {
    return
  }
  if (-not (Test-Path $Destination -PathType Container)) {
    New-Item -ItemType Directory -Path $Destination | Out-Null
  }
  Copy-Item -Recurse -Force (Join-Path $Source '*') $Destination
}

function Sync-ToDir {
  param(
    [string]$Source,
    [string]$Destination
  )
  if (-not (Test-Path $Destination -PathType Container)) {
    New-Item -ItemType Directory -Path $Destination | Out-Null
  }
  Copy-Dir -Source $Source -Destination $Destination
  Write-Log "  • Synced workflows -> $Destination"
}

################################
# Banner
################################

Write-Log "============================================="
Write-Log "🚀 SmartSpec Installer (Windows) v5.6"
Write-Log "============================================="
Write-Log ("Project root: {0}" -f (Get-Location))
Write-Log ("Repo:         {0} ({1})" -f $SmartSpecRepoUrl, $SmartSpecRepoBranch)
Write-Log ""

################################
# Step 1: Download SmartSpec repo
################################

$TmpDir = New-TempDir
Write-Log "📥 Downloading SmartSpec into temp dir: $TmpDir"

if (Get-Command git -ErrorAction SilentlyContinue) {
  git clone --depth 1 --branch $SmartSpecRepoBranch $SmartSpecRepoUrl $TmpDir | Out-Null
}
else {
  Write-Log "⚠️ git not found, using ZIP download..."
  $zipUrl  = $SmartSpecRepoUrl.TrimEnd('.git') + "/archive/refs/heads/$SmartSpecRepoBranch.zip"
  $zipFile = Join-Path $TmpDir 'smartspec.zip'

  if (-not (Get-Command Invoke-WebRequest -ErrorAction SilentlyContinue)) {
    Write-Log "❌ Invoke-WebRequest is not available. Please install git or enable web cmdlets."
    exit 1
  }

  Invoke-WebRequest -Uri $zipUrl -OutFile $zipFile

  if (-not (Get-Command Expand-Archive -ErrorAction SilentlyContinue)) {
    Write-Log "❌ Expand-Archive is required when git is not installed."
    exit 1
  }

  Expand-Archive -Path $zipFile -DestinationPath $TmpDir -Force
  # assume single top-level folder from zip
  $dirs = Get-ChildItem -Path $TmpDir -Directory | Where-Object { $_.FullName -ne $TmpDir }
  if ($dirs.Count -gt 0) {
    $TmpDir = $dirs[0].FullName
  }
}

################################
# Step 2: Copy .smartspec and .smartspec-docs
################################

$SrcSmartSpec      = Join-Path $TmpDir '.smartspec'
$SrcSmartSpecDocs  = Join-Path $TmpDir '.smartspec-docs'

if (-not (Test-Path $SrcSmartSpec -PathType Container)) {
  Write-Log "❌ Source repo does not contain .smartspec/. Please ensure the distribution repo layout is correct."
  exit 1
}

Write-Log "📂 Installing/Updating .smartspec/"
Backup-DirIfExists -Path $SmartSpecDir
if (-not (Test-Path $SmartSpecDir -PathType Container)) {
  New-Item -ItemType Directory -Path $SmartSpecDir | Out-Null
}
Copy-Dir -Source $SrcSmartSpec -Destination $SmartSpecDir

if (Test-Path $SrcSmartSpecDocs -PathType Container) {
  Write-Log "📂 Installing/Updating .smartspec-docs/"
  Backup-DirIfExists -Path $SmartSpecDocsDir
  if (-not (Test-Path $SmartSpecDocsDir -PathType Container)) {
    New-Item -ItemType Directory -Path $SmartSpecDocsDir | Out-Null
  }
  Copy-Dir -Source $SrcSmartSpecDocs -Destination $SmartSpecDocsDir
}
else {
  Write-Log "ℹ️ No .smartspec-docs/ directory found in repo; skipping docs copy."
}

################################
# Step 3: Sanity check core files
################################

$SystemPromptPath = Join-Path $SmartSpecDir 'system_prompt_smartspec.md'
$KbPath           = Join-Path $SmartSpecDir 'knowledge_base_smartspec.md'

if (-not (Test-Path $SystemPromptPath -PathType Leaf)) {
  Write-Log "⚠️ Warning: .smartspec/system_prompt_smartspec.md not found."
}

if (-not (Test-Path $KbPath -PathType Leaf)) {
  Write-Log "⚠️ Warning: .smartspec/knowledge_base_smartspec.md not found."
}

################################
# Step 4: Sync workflows to local tool directories
################################

if (-not (Test-Path $WorkflowsDir -PathType Container)) {
  Write-Log "⚠️ No workflows directory found at $WorkflowsDir. Nothing to sync to tools."
}
else {
  Write-Log "🔁 Syncing workflows to tool-specific directories (if they exist or will be used)..."
  Sync-ToDir -Source $WorkflowsDir -Destination $KiloDir
  Sync-ToDir -Source $WorkflowsDir -Destination $RooDir
  Sync-ToDir -Source $WorkflowsDir -Destination $ClaudeDir
  Sync-ToDir -Source $WorkflowsDir -Destination $AntigravityDir
  Sync-ToDir -Source $WorkflowsDir -Destination $GeminiDir
}

################################
# Step 5: Done
################################

Write-Log ""
Write-Log "✅ SmartSpec installation/update complete."
Write-Log ("   - Core:   {0}" -f $SmartSpecDir)
Write-Log ("   - Docs:   {0}" -f $SmartSpecDocsDir)
Write-Log ("   - Tools:  {0}, {1}, {2}, {3}, {4}" -f $KiloDir, $RooDir, $ClaudeDir, $AntigravityDir, $GeminiDir)
Write-Log ""
Write-Log "You can now run SmartSpec workflows (e.g. /smartspec_project_copilot) via your"
Write-Log "preferred tool (Kilo/Roo/Claude/Antigravity/Gemini) using the synced commands"
Write-Log "from .smartspec/workflows."
