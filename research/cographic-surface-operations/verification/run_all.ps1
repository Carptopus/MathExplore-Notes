param(
    [string]$Python = 'python'
)

$ErrorActionPreference = 'Stop'

$scripts = @(
    'verify_rp2_stellar_family.py',
    'verify_nonorientable_triangle_sum_family.py',
    'check_vertex_split_nonclosure.py',
    'probe_two_step_seam_persistence.py'
)

foreach ($script in $scripts) {
    & $Python -X utf8 (Join-Path $PSScriptRoot $script)
    if ($LASTEXITCODE -ne 0) {
        throw "Verification failed: $script"
    }
}

Write-Output 'PASS all cographic surface-operation verification checks'
