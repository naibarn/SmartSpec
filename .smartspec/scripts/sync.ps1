# SmartSpec Sync Script (Standalone) - PowerShell
# Version: 5.2 (centralization-compatible)
# Master source of workflows: .smartspec/workflows/

$ErrorActionPreference = "Stop"

$SmartSpecDir = ".smartspec"
$WorkflowsDir = Join-Path $SmartSpecDir "workflows"
$configPath = Join-Path $SmartSpecDir "config.json"

Write-Host "🔄 SmartSpec Sync Tool" -ForegroundColor Cyan
Write-Host "=====================" -ForegroundColor Cyan
Write-Host ""

if (-not (Test-Path $SmartSpecDir)) {
    throw "SmartSpec is not installed in this project. Run install.ps1 first."
}

if (-not (Test-Path $WorkflowsDir)) {
    throw "Master workflows directory not found: $WorkflowsDir"
}

if (-not (Test-Path $configPath)) {
    throw "SmartSpec configuration not found: $configPath"
}

$config = Get-Content $configPath -Raw | ConvertFrom-Json

if ($config.PSObject.Properties.Name -contains "use_symlinks" -and [bool]$config.use_symlinks) {
    Write-Host "You're using symlinks - manual sync is not required." -ForegroundColor Yellow
    return
}

$platforms = @()
if ($config.PSObject.Properties.Name -contains "platforms") {
    $platforms = $config.platforms
}

if (-not $platforms -or $platforms.Count -eq 0) {
    Write-Host "⚠️  No platforms configured in config.json." -ForegroundColor Yellow
    return
}

# Platform directories (home-based defaults)
$KiloDir = Join-Path $HOME ".kilocode\workflows"
$RooDir = Join-Path $HOME ".roo\commands"
$ClaudeDir = Join-Path $HOME ".claude\commands"
$AgentDir = Join-Path $HOME ".agent\workflows"
$GeminiDir = Join-Path $HOME ".gemini\commands"

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

Write-Host "Syncing workflows to platforms..." -ForegroundColor Cyan
Write-Host ""

$syncCount = 0

foreach ($p in $platforms) {
    switch ($p) {
        "kilocode" { $target = $KiloDir; $name = "Kilo Code" }
        "roo" { $target = $RooDir; $name = "Roo Code" }
        "claude" { $target = $ClaudeDir; $name = "Claude Code" }
        "antigravity" { $target = $AgentDir; $name = "Google Antigravity" }
        "gemini-cli" { $target = $GeminiDir; $name = "Gemini CLI" }
        default { 
            Write-Host "⚠️  Unknown platform: $p - skipping" -ForegroundColor Yellow
            continue 
        }
    }

    New-Item -ItemType Directory -Path $target -Force | Out-Null

    if ($p -eq "gemini-cli") {
        foreach ($md in $mdFiles) {
            $base = [IO.Path]::GetFileNameWithoutExtension($md.Name)
            $tomlPath = Join-Path $target ($base + ".toml")
            Convert-MdToToml $md.FullName $tomlPath
        }
        Write-Host "  ✅ $name synced (TOML)" -ForegroundColor Green
        $syncCount++
        continue
    }

    # Replace only SmartSpec files
    Get-ChildItem -Path $target -Filter "smartspec_*.md" -File -ErrorAction SilentlyContinue | Remove-Item -Force -ErrorAction SilentlyContinue
    foreach ($md in $mdFiles) { Copy-Item $md.FullName $target -Force }

    Write-Host "  ✅ $name synced" -ForegroundColor Green
    $syncCount++
}

Write-Host ""
if ($syncCount -gt 0) {
    Write-Host "✅ Sync complete - $syncCount platform(s) updated" -ForegroundColor Green
} else {
    Write-Host "⚠️  No platforms synced" -ForegroundColor Yellow
}
