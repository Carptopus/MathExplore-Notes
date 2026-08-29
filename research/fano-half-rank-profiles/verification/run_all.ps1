param(
    [string]$Python = 'python'
)

$ErrorActionPreference = 'Stop'

$BuildDir = Join-Path ([IO.Path]::GetTempPath()) 'fano-half-rank-profiles'

if (-not (Get-Command $Python -ErrorAction SilentlyContinue)) {
    throw "Python command not found: $Python"
}

& $Python -X utf8 -c 'import sys, sympy; raise SystemExit(0 if (__debug__ and sys.flags.optimize == 0) else 1)'
if ($LASTEXITCODE -ne 0) {
    throw 'Python with SymPy is required, and optimization must be disabled because the exact certificates use assertions'
}

$Compiler = (Get-Command g++ -ErrorAction Stop).Source
New-Item -ItemType Directory -Path $BuildDir -Force | Out-Null

function Invoke-Python([string]$Name) {
    & $Python -X utf8 (Join-Path $PSScriptRoot $Name)
    if ($LASTEXITCODE -ne 0) {
        throw "$Name failed with exit code $LASTEXITCODE"
    }
}

function Invoke-Certificate(
    [string]$SourceName,
    [string]$BinaryName,
    [string[]]$Arguments = @()
) {
    $Source = Join-Path $PSScriptRoot $SourceName
    $Binary = Join-Path $BuildDir $BinaryName
    & $Compiler -std=c++17 -O2 $Source -o $Binary
    if ($LASTEXITCODE -ne 0) {
        throw "Compilation failed: $SourceName"
    }
    & $Binary @Arguments
    if ($LASTEXITCODE -ne 0) {
        throw "$SourceName failed with exit code $LASTEXITCODE"
    }
}

Invoke-Certificate 'verify_fano_triangle_extreme_rays.cpp' 'verify_fano_triangle_extreme_rays.exe'
Invoke-Python 'verify_fano_triangle_hilbert_basis.py'
Invoke-Python 'verify_fano_43_counterexample.py'
Invoke-Python 'verify_realized_strengthened_fano_atoms.py'
Invoke-Python 'verify_fano_profile_two_saturation.py'
Invoke-Python 'probe_fano_profile_semigroup_holes.py'
Invoke-Certificate 'verify_fano_anchor_cone_extreme_rays.cpp' 'verify_fano_anchor_cone_extreme_rays.exe'
Invoke-Python 'verify_scaled_chamber_ray_witnesses.py'
Invoke-Certificate 'probe_n5_profile_saturation.cpp' 'probe_n5_profile_saturation.exe'
Invoke-Certificate 'probe_n6_profile_saturation.cpp' 'probe_n6_profile_saturation.exe'
Invoke-Certificate 'probe_n7_noncollinear_full_exception.cpp' 'probe_n7_noncollinear_full_exception.exe'
Invoke-Certificate 'probe_n8_line_full_rank2_coset.cpp' 'probe_n8_line_full_rank2_coset.exe'
Invoke-Certificate 'probe_n10_second_boundary_orbit.cpp' 'probe_n10_second_boundary_orbit.exe'
Invoke-Python 'verify_fano_graded_conductor.py'
Invoke-Python 'verify_fano_graded_required_bases.py'
$RequiredBases = Join-Path $PSScriptRoot 'results\required_sharp_bases.tsv'
Invoke-Certificate 'verify_fano_graded_excess_bound.cpp' 'verify_fano_graded_excess_bound.exe' @($RequiredBases)
Invoke-Python 'verify_constant_height_five_field_net.py'

Write-Output 'PASS: all core Fano half-rank profile checks completed'
