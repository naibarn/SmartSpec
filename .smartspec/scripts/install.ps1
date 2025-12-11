<#
  SmartSpec Installer (Project-Local)
  Platform : Windows (PowerShell)
  Version  : 5.6.1

  This script:
    - Downloads the SmartSpec distribution repo
    - Copies `.smartspec/` and `.smartspec-docs/` into the current project
    - Ensures stable filenames:
        .smartspec/system_prompt_smartspec.md
        .smartspec/knowledge_base_smart_spec.md
    - Copies .smartspec/workflows into platform-specific folders if present:
        .kilocode/workflows
        .roo/commands
        .claude/commands
        .agent/workflows
        .gemini/commands

  NOTE:
    - The distribution repo is fixed to https://github.com/naibarn/SmartSpec
    - You may override the branch with the SMARTSPEC_REPO_BRANCH environment
      variable if really needed (default: main).
#>

[CmdletBinding()]
param()

$ErrorActionPreference = 'Stop'

###############################
# Configuration
###############################

# Fixed distribution repository (do NOT override)
$SmartSpecRepoUrl    = 'https://github.com/naibarn/SmartSpec.git'
# Branch can be overridden via environment variable SMARTSPEC_REPO_BRANCH
$SmartSpecRepoBranch = if ($env:SMARTSPEC_REPO_BRANCH) { $env:SMARTSPEC_REPO_BRANCH } else { 'main' }

$SmartSpecDir       = '.smartspec'
$SmartSpecDocsDir   = '.smartspec-docs'
$WorkflowsDir       = Join-Path $SmartSpecDir 'workflows'
$WorkflowDocsDir    = Join-Path $SmartSpecDocsDir 'workflows'

# Project-local platform directories
$KiloCodeDir        = '.kilocode/workflows'
$RooDir             = '.roo/commands'
$ClaudeDir          = '.claude/commands'
$AntigravityDir     = '.agent/workflows'
$GeminiDir          = '.gemini/commands'

###############################
# Helpers
###############################

function Write-Log {
  param([string]$Message)
  Write-Host $Message
}

function New-TempDir {
  $base = Join-Path ([System.IO.Path]::GetTempPath()) "smartspec-$(Get-Random)"
  New-Item -ItemType Directory -Path $base -Force | Out-Null
  return $base
}

function Backup-DirIfExists {
  param([string]$Path)
  if (Test-Path $Path -PathType Container) {
    $ts = Get-Date -Format 'yyyyMMdd_HHmmss'
    $backup = "$Path.backup.$ts"
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
    New-Item -ItemType Directory -Path $Destination -Force | Out-Null
  }
  Copy-Item -Recurse -Force (Join-Path $Source '*') $Destination
}

###############################
# Banner
###############################

Write-Log '============================================='
Write-Log '🚀 SmartSpec Installer (Windows PowerShell) v5.6.1'
Write-Log '============================================='
Write-Log ("Project root: {0}" -f (Get-Location))
Write-Log ("Repo:         {0} (branch: {1})" -f $SmartSpecRepoUrl, $SmartSpecRepoBranch)
Write-Log ''

###############################
# Step 1: Download SmartSpec repo
###############################

$TmpDir = New-TempDir
Write-Log ("📥 Downloading SmartSpec into temp dir: {0}" -f $TmpDir)

if (Get-Command git -ErrorAction SilentlyContinue) {
  git clone --depth 1 --branch $SmartSpecRepoBranch $SmartSpecRepoUrl $TmpDir | Out-Null
}
else {
  Write-Log '⚠️ git not found, trying Invoke-WebRequest + Expand-Archive...'
  if (-not (Get-Command Invoke-WebRequest -ErrorAction SilentlyContinue)) {
    Write-Log '❌ Neither git nor Invoke-WebRequest is available. Please install git (recommended).'
    exit 1
  }
  $zipUrl  = ($SmartSpecRepoUrl -replace '\.git$','') + "/archive/refs/heads/$SmartSpecRepoBranch.zip"
  $zipFile = Join-Path $TmpDir 'smartspec.zip'
  Invoke-WebRequest -Uri $zipUrl -OutFile $zipFile
  if (-not (Get-Command Expand-Archive -ErrorAction SilentlyContinue)) {
    Write-Log '❌ Expand-Archive is required when git is not installed.'
    exit 1
  }
  Expand-Archive -Path $zipFile -DestinationPath $TmpDir -Force
  $root = Get-ChildItem -Path $TmpDir -Directory | Where-Object { $_.FullName -ne $TmpDir } | Select-Object -First 1
  if ($null -ne $root) {
    $TmpDir = $root.FullName
  }
}

###############################
# Step 2: Copy .smartspec and .smartspec-docs
###############################

$SrcSmartSpec      = Join-Path $TmpDir '.smartspec'
$SrcSmartSpecDocs  = Join-Path $TmpDir '.smartspec-docs'

if (-not (Test-Path $SrcSmartSpec -PathType Container)) {
  Write-Log '❌ Source repo does not contain .smartspec/. Please ensure the distribution repo layout is correct.'
  exit 1
}

Write-Log '📂 Installing/Updating .smartspec/'
Backup-DirIfExists -Path $SmartSpecDir
New-Item -ItemType Directory -Path $SmartSpecDir -Force | Out-Null
Copy-Dir -Source $SrcSmartSpec -Destination $SmartSpecDir

if (Test-Path $SrcSmartSpecDocs -PathType Container) {
  Write-Log '📂 Installing/Updating .smartspec-docs/'
  Backup-DirIfExists -Path $SmartSpecDocsDir
  New-Item -ItemType Directory -Path $SmartSpecDocsDir -Force | Out-Null
  Copy-Dir -Source $SrcSmartSpecDocs -Destination $SmartSpecDocsDir
}
else {
  Write-Log 'ℹ️ No .smartspec-docs/ directory found in repo; skipping docs copy.'
}

###############################
# Step 3: Sanity check core files
###############################

if (-not (Test-Path (Join-Path $SmartSpecDir 'system_prompt_smartspec.md'))) {
  Write-Log '⚠️ Warning: .smartspec/system_prompt_smartspec.md not found.'
}

if (-not (Test-Path (Join-Path $SmartSpecDir 'knowledge_base_smart_spec.md'))) {
  Write-Log '⚠️ Warning: .smartspec/knowledge_base_smart_spec.md not found.'
}

###############################
# Step 4: Sync workflows to local tool directories
###############################

if (-not (Test-Path $WorkflowsDir -PathType Container)) {
  Write-Log ("⚠️ No workflows directory found at {0}. Nothing to sync to tools." -f $WorkflowsDir)
}
else {
  Write-Log '🔁 Syncing workflows to tool-specific directories (if they exist)...'

  function Sync-To {
    param([string]$Destination)
    if (-not (Test-Path $Destination -PathType Container)) {
      New-Item -ItemType Directory -Path $Destination -Force | Out-Null
    }
    Copy-Dir -Source $WorkflowsDir -Destination $Destination
    Write-Log ("  • Synced workflows -> {0}" -f $Destination)
  }

  Sync-To -Destination $KiloCodeDir
  Sync-To -Destination $RooDir
  Sync-To -Destination $ClaudeDir
  Sync-To -Destination $AntigravityDir
  Sync-To -Destination $GeminiDir
}

###############################
# Step 5: Done
###############################

Write-Log ''
Write-Log '✅ SmartSpec installation/update complete.'
Write-Log ("   - Core:   {0}" -f $SmartSpecDir)
Write-Log ("   - Docs:   {0} (if present in repo)" -f $SmartSpecDocsDir)
Write-Log ("   - Tools:  {0}, {1}, {2}, {3}, {4}" -f $KiloCodeDir, $RooDir, $ClaudeDir, $AntigravityDir, $GeminiDir)
Write-Log ''
Write-Log 'You can now run SmartSpec workflows (e.g. /smartspec_project_copilot) via your preferred tool (Kilo/Roo/Claude/Antigravity/Gemini) using the synced commands from .smartspec/workflows.'
