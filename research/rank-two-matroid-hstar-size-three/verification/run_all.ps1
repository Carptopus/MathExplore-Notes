param(
    [string]$Python = 'python'
)

$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest

$pythonCommand = Get-Command $Python -ErrorAction Stop
$scriptPath = Join-Path $PSScriptRoot 'verify_a3_bound.py'
$expectedPath = Join-Path $PSScriptRoot 'results\expected-output.txt'

$ordinary = @(& $pythonCommand.Source -B -X utf8 $scriptPath)
if ($LASTEXITCODE -ne 0) {
    throw "ordinary verification exited with code $LASTEXITCODE"
}

$optimized = @(& $pythonCommand.Source -B -O -X utf8 $scriptPath)
if ($LASTEXITCODE -ne 0) {
    throw "optimized verification exited with code $LASTEXITCODE"
}

$expected = @(Get-Content -LiteralPath $expectedPath -Encoding UTF8)
$ordinaryDifference = @(Compare-Object -ReferenceObject $expected -DifferenceObject $ordinary -SyncWindow 0)
$optimizedDifference = @(Compare-Object -ReferenceObject $expected -DifferenceObject $optimized -SyncWindow 0)

if ($ordinaryDifference.Count -ne 0) {
    $ordinaryDifference | Format-Table -AutoSize | Out-String | Write-Error
    throw 'ordinary verification output differs from the frozen result'
}
if ($optimizedDifference.Count -ne 0) {
    $optimizedDifference | Format-Table -AutoSize | Out-String | Write-Error
    throw 'optimized verification output differs from the frozen result'
}

$ordinary | Write-Output
Write-Output 'ORDINARY_AND_OPTIMIZED_OUTPUT_MATCH=PASS'

