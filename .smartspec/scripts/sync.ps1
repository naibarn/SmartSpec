# SmartSpec Sync Script (Standalone) - PowerShell
# Use this to manually sync workflows to all platforms.

$ErrorActionPreference = "Stop"

$SmartSpecDir = ".smartspec"
$WorkflowsDir = Join-Path $SmartSpecDir "workflows"

if (-not (Test-Path $SmartSpecDir)) {
    throw "SmartSpec is not installed. Run install.ps1 first."
}

if (-not (Test-Path (Join-Path $SmartSpecDir "config.json"))) {
    throw "SmartSpec configuration not found."
}

$config = Get-Content (Join-Path $SmartSpecDir "config.json") -Raw | ConvertFrom-Json
$platforms = $config.platforms
$useSymlinks = $false
if ($config.PSObject.Properties.Name -contains "use_symlinks") {
    $useSymlinks = [bool]$config.use_symlinks
}

if ($useSymlinks) {
    Write-Host "⚠️  You're using symlinks - sync is automatic" -ForegroundColor Yellow
    return
}

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
    if ($descLine) { $description = ($descLine -replace "^\s*description\s*:\s*", "").Trim() }
    if ([string]::IsNullOrWhiteSpace($description)) {
        $titleLine = $lines | Where-Object { $_ -match "^\s*#\s+" } | Select-Object -First 1
        if ($titleLine) { $description = ($titleLine -replace "^\s*#\s+", "").Trim() }
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

Write-Host "🔄 Syncing SmartSpec workflows..." -ForegroundColor Cyan

$syncCount = 0

foreach ($p in $platforms) {
    switch ($p) {
        "kilocode" { $parent = Join-Path $HOME ".kilocode"; $target = $KiloDir; $name = "Kilo Code" }
        "roo" { $parent = Join-Path $HOME ".roo"; $target = $RooDir; $name = "Roo Code" }
        "claude" { $parent = Join-Path $HOME ".claude"; $target = $ClaudeDir; $name = "Claude Code" }
        "antigravity" { $parent = Join-Path $HOME ".agent"; $target = $AgentDir; $name = "Google Antigravity" }
        "gemini-cli" { $parent = Join-Path $HOME ".gemini"; $target = $GeminiDir; $name = "Gemini CLI" }
        default { continue }
    }

    if (-not (Test-Path $parent)) {
        Write-Host "  ⚠️  $name not detected at $parent - skipping" -ForegroundColor Yellow
        continue
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
