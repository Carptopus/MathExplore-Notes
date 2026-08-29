param(
    [string]$Python
)

$ErrorActionPreference = 'Stop'
$here = Split-Path -Parent $MyInvocation.MyCommand.Path

if (-not $Python) {
    $projectPython = Join-Path $here '..\..\..\.venv\Scripts\python.exe'
    if (Test-Path -LiteralPath $projectPython) {
        $Python = (Resolve-Path -LiteralPath $projectPython).Path
    } elseif (Get-Command py -ErrorAction SilentlyContinue) {
        $Python = 'py'
    } elseif (Get-Command python -ErrorAction SilentlyContinue) {
        $Python = 'python'
    } else {
        throw 'Python 3 was not found. Pass its path with -Python.'
    }
}

$oldHashSeed = $env:PYTHONHASHSEED
try {
    $env:PYTHONHASHSEED = '0'
    & $Python -X utf8 -c "import sys; assert sys.version_info >= (3, 10); assert sys.flags.optimize == 0; assert __debug__; print(sys.version)"
    if ($LASTEXITCODE -ne 0) {
        throw 'Python must run with assertions enabled and optimization disabled.'
    }

    $checks = @(
        'verify_slice_orbits.py',
        'verify_rank_exclusions.py',
        'verify_three_signed_dyadic_sum_13.py',
        'verify_walsh_zero_low_rank_boundary.py',
        'verify_kdr_arbitrary_length_formulas.py',
        'verify_hit_singular_kronecker_transfer.py',
        'verify_hit_degenerate_regular_transfer.py',
        'verify_hit_regular_nondegenerate_transfer.py',
        'verify_rank2_full_core_recursion.py',
        'verify_rank4_stratum_recursion.py',
        'verify_rank4_full_core_recursion.py',
        'verify_rank2_or_rank4_dichotomy_19_8.py',
        'verify_rank4_obstruction_19_8_all_n.py',
        'verify_rank4_obstruction_152_complete.py'
    )

    foreach ($check in $checks) {
        Write-Host "==> $check"
        & $Python -X utf8 (Join-Path $here $check)
        if ($LASTEXITCODE -ne 0) {
            throw "$check failed with exit code $LASTEXITCODE"
        }
    }

    Write-Host 'PASS: all RM2 third-support-region checks completed'
} finally {
    $env:PYTHONHASHSEED = $oldHashSeed
}
