param(
    [string]$Python = "python"
)

$ErrorActionPreference = "Stop"
$pythonCommand = Get-Command $Python -ErrorAction SilentlyContinue
if ($null -eq $pythonCommand) {
    throw "Python interpreter not found: $Python"
}

$resultsPath = Join-Path $PSScriptRoot "results"
$backupPath = Join-Path ([System.IO.Path]::GetTempPath()) ("thue-morse-verification-" + [guid]::NewGuid())
New-Item -ItemType Directory -Path $backupPath | Out-Null

try {
    Copy-Item -LiteralPath (Join-Path $resultsPath "candidate_checks.json") -Destination $backupPath
    Copy-Item -LiteralPath (Join-Path $resultsPath "scale_and_minimizer_checks.json") -Destination $backupPath

    & $Python (Join-Path $PSScriptRoot "verify_candidate.py") | Out-Null
    if ($LASTEXITCODE -ne 0) {
        throw "verify_candidate.py failed with exit code $LASTEXITCODE"
    }

    & $Python (Join-Path $PSScriptRoot "verify_scale_and_minimizer.py") | Out-Null
    if ($LASTEXITCODE -ne 0) {
        throw "verify_scale_and_minimizer.py failed with exit code $LASTEXITCODE"
    }

    foreach ($name in @("candidate_checks.json", "scale_and_minimizer_checks.json")) {
        $expected = (Get-FileHash -Algorithm SHA256 -LiteralPath (Join-Path $backupPath $name)).Hash
        $actual = (Get-FileHash -Algorithm SHA256 -LiteralPath (Join-Path $resultsPath $name)).Hash
        if ($actual -ne $expected) {
            throw "$name differs from the released evidence"
        }
    }

    Write-Output "All Thue--Morse verification checks passed."
}
finally {
    Remove-Item -LiteralPath $backupPath -Recurse -Force -ErrorAction SilentlyContinue
}
