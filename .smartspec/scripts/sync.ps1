# SmartSpec Sync (Project-first)

$WorkflowsDir = ".smartspec\workflows"

if (-not (Test-Path $WorkflowsDir)) {
  Write-Host "❌ Master workflows not found at $WorkflowsDir"
  exit 1
}

function Sync-Dir($Name, $Target) {
  New-Item -ItemType Directory -Force -Path $Target | Out-Null

  # clear target
  Get-ChildItem -Path $Target -Force -ErrorAction SilentlyContinue | Remove-Item -Recurse -Force -ErrorAction SilentlyContinue

  # copy
  Copy-Item -Path (Join-Path $WorkflowsDir "*") -Destination $Target -Recurse -Force

  Write-Host "✅ $Name synced → $Target"
}

$ProjectTargets = @(
  @{ Name = "Antigravity"; Target = ".agent\workflows" },
  @{ Name = "Claude";      Target = ".claude\commands" },
  @{ Name = "Gemini";      Target = ".gemini\commands" }
)

Write-Host "🔄 Syncing SmartSpec workflows (project-first)..."

foreach ($t in $ProjectTargets) {
  Sync-Dir $t.Name $t.Target
}

Write-Host "✅ Sync complete (project targets)"
