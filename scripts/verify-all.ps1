$ErrorActionPreference = "Stop"

$Root = Split-Path -Parent $PSScriptRoot
$Python = Join-Path $Root ".venv\Scripts\python.exe"

Write-Host "== Backend compile =="
Set-Location $Root
& $Python -m compileall backend\app

Write-Host "== Backend tests =="
Set-Location (Join-Path $Root "backend")
& $Python -m pytest tests -q

Write-Host "== Frontend build =="
Set-Location (Join-Path $Root "frontend")
npm run build

Write-Host "== Frontend high-severity audit =="
npm audit --audit-level=high

Write-Host "All verification checks completed."

