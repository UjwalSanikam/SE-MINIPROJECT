# Runs style, security and test checks. Run from the repo root with the venv active.
$failed = $false

Write-Host "== flake8 (style) =="
flake8 src
if ($LASTEXITCODE -ne 0) { $failed = $true }

Write-Host "== bandit (security) =="
bandit -r src -x "*/tests/*" -q
if ($LASTEXITCODE -ne 0) { $failed = $true }

Write-Host "== pytest (tests) =="
python -m pytest -q
if ($LASTEXITCODE -eq 5) { Write-Host "No tests found (ok for now)" }
elseif ($LASTEXITCODE -ne 0) { $failed = $true }

if ($failed) { Write-Host "CHECKS FAILED"; exit 1 }
Write-Host "ALL CHECKS PASSED"