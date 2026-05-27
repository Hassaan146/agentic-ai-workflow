$ErrorActionPreference = "Stop"

$Root = Split-Path -Parent $PSScriptRoot
$Python = Join-Path $Root ".venv\Scripts\python.exe"

Set-Location $Root
& $Python -m compileall backend\app

Set-Location (Join-Path $Root "backend")
& $Python -m pytest tests -q

Set-Location (Join-Path $Root "frontend")
npm run build
npm audit --audit-level=high

