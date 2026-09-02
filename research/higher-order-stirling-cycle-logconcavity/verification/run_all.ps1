param(
    [string]$Python = 'python'
)

$ErrorActionPreference = 'Stop'
$env:PYTHONUTF8 = '1'
$scriptRoot = Split-Path -Parent $MyInvocation.MyCommand.Path

$programs = @(
    'verify_normalized_logconcavity.py',
    'verify_r4_weighted_cone.py',
    'verify_two_step_lc_preserver.py',
    'verify_small_excess_strips.py',
    'verify_sparse_cycle_k2.py',
    'verify_saddle_curvature.py',
    'verify_bulk_edgeworth_margin.py',
    'verify_bulk_second_order_margin.py',
    'verify_bulk_third_order_margin.py',
    'verify_bulk_fourth_order_margin.py',
    'verify_bulk_fifth_order_margin.py',
    'verify_renewal_reformulation.py',
    'verify_low_cumulant_envelope.py',
    'verify_characteristic_tail_constants.py',
    'verify_effective_fourier_remainder.py',
    'verify_bulk_finite_prefix.py'
)

Push-Location -LiteralPath $scriptRoot
try {
    foreach ($program in $programs) {
        Write-Host "RUN: $program"
        & $Python $program
        if ($LASTEXITCODE -ne 0) {
            throw "$program failed with exit code $LASTEXITCODE"
        }
    }
}
finally {
    Pop-Location
}

Write-Host 'PASS: all higher-order Stirling cycle log-concavity certificates verified'
