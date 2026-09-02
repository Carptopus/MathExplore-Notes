param(
    [string]$Python = "python",
    [switch]$SkipExactEnumeration
)

$ErrorActionPreference = "Stop"
$here = $PSScriptRoot
$results = Join-Path $here "results"

function Invoke-CheckedPython {
    param([Parameter(ValueFromRemainingArguments = $true)][string[]]$Arguments)
    & $Python @Arguments
    if ($LASTEXITCODE -ne 0) {
        throw "Verification command failed with exit code ${LASTEXITCODE}: $Arguments"
    }
}

if ($null -eq (Get-Command $Python -ErrorAction SilentlyContinue)) {
    throw "Python interpreter not found: $Python"
}

Invoke-CheckedPython (Join-Path $here "audit_normalisation_and_connectivity.py")

if (-not $SkipExactEnumeration) {
    Invoke-CheckedPython (Join-Path $here "exact_first_cube_enumeration.py") --n 8 --maximum-edges 15
    Invoke-CheckedPython (Join-Path $here "exact_first_cube_enumeration.py") --n 9 --maximum-edges 16
    Invoke-CheckedPython (Join-Path $here "exact_first_cube_enumeration.py") --n 10 --maximum-edges 17 --structural-filter
}

Invoke-CheckedPython (Join-Path $here "verify_small_order_witnesses.py")

Invoke-CheckedPython (Join-Path $here "build_activation_certificate.py") `
    --input (Join-Path $results "exact-first-cube-n9.json") `
    --output (Join-Path $results "q3-k9-16-edge-certificate.json")
Invoke-CheckedPython (Join-Path $here "build_activation_certificate.py") `
    --input (Join-Path $results "small-order-upper-witnesses.json") `
    --n 10 `
    --output (Join-Path $results "q3-k10-18-edge-certificate.json")
Invoke-CheckedPython (Join-Path $here "build_activation_certificate.py") `
    --input (Join-Path $results "small-order-upper-witnesses.json") `
    --n 12 `
    --output (Join-Path $results "q3-k12-21-edge-certificate.json")

foreach ($certificate in @(
    "q3-k9-16-edge-certificate.json",
    "q3-k10-18-edge-certificate.json",
    "q3-k11-k7-anchor-certificate.json",
    "q3-k12-21-edge-certificate.json"
)) {
    Invoke-CheckedPython (Join-Path $here "audit_activation_certificate.py") `
        (Join-Path $results $certificate)
}

Invoke-CheckedPython (Join-Path $here "compute_q3_combinatorial_lower_bound.py")
Invoke-CheckedPython (Join-Path $here "verify_dense_anchor_extension.py")

Write-Output "All requested Q3 weak-saturation checks passed."
