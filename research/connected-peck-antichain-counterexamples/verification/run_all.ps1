param(
    [string]$Python = "python"
)

$ErrorActionPreference = "Stop"
$scriptPath = Join-Path $PSScriptRoot "verify_counterexample.py"
$pythonCommand = Get-Command $Python -ErrorAction SilentlyContinue
if ($null -eq $pythonCommand) {
    throw "Python interpreter not found: $Python"
}

& $Python $scriptPath
if ($LASTEXITCODE -ne 0) {
    throw "Verification failed with exit code $LASTEXITCODE"
}
