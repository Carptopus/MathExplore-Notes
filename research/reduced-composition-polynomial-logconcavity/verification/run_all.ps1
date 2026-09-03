param(
    [string]$Python = "python"
)

$ErrorActionPreference = "Stop"
$verificationDir = Split-Path -Parent $MyInvocation.MyCommand.Path

& $Python (Join-Path $verificationDir "test_truncation_pencil.py")
if ($LASTEXITCODE -ne 0) {
    throw "test_truncation_pencil.py failed with exit code $LASTEXITCODE"
}

& $Python (Join-Path $verificationDir "verify_composition_unimodality.py")
if ($LASTEXITCODE -ne 0) {
    throw "verify_composition_unimodality.py failed with exit code $LASTEXITCODE"
}

Write-Output "ALL VERIFICATION CHECKS PASSED"
