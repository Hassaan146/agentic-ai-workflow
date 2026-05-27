$ErrorActionPreference = "Stop"

$Root = Split-Path -Parent $PSScriptRoot
$Python = Join-Path $Root ".venv\Scripts\python.exe"
$Backend = Join-Path $Root "backend"

Set-Location $Backend
& $Python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000

