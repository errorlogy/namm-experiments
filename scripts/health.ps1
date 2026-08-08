# NAMM health loop: pytest + smoke experiment
$ErrorActionPreference = "Stop"
$py = "C:\Users\lawye\AppData\Local\Programs\Python\Python312\python.exe"
Set-Location "c:\Users\Public\NAMM"

& $py -m pytest tests/ -q
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

& $py -m namm.cli run-experiment --id NAMM-2026-001
exit $LASTEXITCODE
