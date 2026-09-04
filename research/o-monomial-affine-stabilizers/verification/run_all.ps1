param(
    [string]$Python = 'python'
)

$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest

$pythonCommand = Get-Command $Python -ErrorAction Stop

$checks = @(
    @{
        Name = 'overline-Segre'
        Script = Join-Path $PSScriptRoot 'verify_bar_segre_value_polynomial.py'
        Expected = Join-Path $PSScriptRoot 'results\bar-segre-output.txt'
    },
    @{
        Name = 'Glynn-I'
        Script = Join-Path $PSScriptRoot 'verify_glynn_cycle_cover_arithmetic.py'
        Expected = Join-Path $PSScriptRoot 'results\glynn-output.txt'
    }
)

foreach ($check in $checks) {
    $ordinary = @(& $pythonCommand.Source -B $check.Script)
    if ($LASTEXITCODE -ne 0) {
        throw "$($check.Name) ordinary verification exited with code $LASTEXITCODE"
    }

    $optimized = @(& $pythonCommand.Source -B -O $check.Script)
    if ($LASTEXITCODE -ne 0) {
        throw "$($check.Name) optimized verification exited with code $LASTEXITCODE"
    }

    $expected = @(Get-Content -LiteralPath $check.Expected -Encoding UTF8)
    $ordinaryDifference = @(Compare-Object -ReferenceObject $expected -DifferenceObject $ordinary -SyncWindow 0)
    $optimizedDifference = @(Compare-Object -ReferenceObject $expected -DifferenceObject $optimized -SyncWindow 0)

    if ($ordinaryDifference.Count -ne 0) {
        $ordinaryDifference | Format-Table -AutoSize | Out-String | Write-Error
        throw "$($check.Name) ordinary output differs from the frozen result"
    }
    if ($optimizedDifference.Count -ne 0) {
        $optimizedDifference | Format-Table -AutoSize | Out-String | Write-Error
        throw "$($check.Name) optimized output differs from the frozen result"
    }

    $ordinary | Write-Output
    Write-Output "$($check.Name): ORDINARY_AND_OPTIMIZED_OUTPUT_MATCH=PASS"
}
