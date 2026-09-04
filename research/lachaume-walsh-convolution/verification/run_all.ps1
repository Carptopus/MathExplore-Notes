param(
    [string]$Python = 'python'
)

$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest

$scriptPath = Join-Path $PSScriptRoot 'verify_identity.py'
$expectedPath = Join-Path $PSScriptRoot 'results\expected-output.txt'
$expected = (Get-Content -LiteralPath $expectedPath -Raw).Trim()

$ordinaryLines = @(& $Python -B -X utf8 $scriptPath 2>&1)
if ($LASTEXITCODE -ne 0) {
    throw "ordinary verifier exited with code $LASTEXITCODE"
}
$ordinary = ($ordinaryLines -join "`n").Trim()

$optimizedLines = @(& $Python -O -B -X utf8 $scriptPath 2>&1)
if ($LASTEXITCODE -ne 0) {
    throw "optimized verifier exited with code $LASTEXITCODE"
}
$optimized = ($optimizedLines -join "`n").Trim()

if ($ordinary -ne $optimized) {
    throw 'ordinary and optimized verifier outputs differ'
}
if ($ordinary -ne $expected) {
    throw 'verifier output differs from the frozen expected result'
}

Write-Output $ordinary
Write-Output 'ORDINARY_AND_OPTIMIZED_OUTPUT_MATCH=PASS'
