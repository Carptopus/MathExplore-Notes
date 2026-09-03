param(
    [string]$Python = 'python'
)

$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest

$pythonCommand = Get-Command $Python -ErrorAction Stop
$scriptPath = Join-Path $PSScriptRoot 'verify_general_lower_model.py'
$expectedPath = Join-Path $PSScriptRoot 'results\general-lower-model-t2-t8.txt'

$actual = @(& $pythonCommand.Source -B $scriptPath)
if ($LASTEXITCODE -ne 0) {
    throw "verification exited with code $LASTEXITCODE"
}
$expected = @(Get-Content -LiteralPath $expectedPath -Encoding UTF8)
$difference = @(Compare-Object -ReferenceObject $expected -DifferenceObject $actual -SyncWindow 0)
if ($difference.Count -ne 0) {
    $difference | Format-Table -AutoSize | Out-String | Write-Error
    throw 'verification output differs from the frozen result'
}

$actual | Write-Output
Write-Output 'VERIFICATION_OUTPUT_MATCH=PASS'
