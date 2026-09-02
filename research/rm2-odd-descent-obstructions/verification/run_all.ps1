param(
    [string]$Python = "python"
)

$ErrorActionPreference = "Stop"
$here = $PSScriptRoot
$results = Join-Path $here "results"
$log = Join-Path $results "verification-summary.txt"

if ($null -eq (Get-Command $Python -ErrorAction SilentlyContinue)) {
    throw "Python interpreter not found: $Python"
}

New-Item -ItemType Directory -Force -Path $results | Out-Null
$lines = [System.Collections.Generic.List[string]]::new()

foreach ($script in @(
    "verify_odd_descent_counterexample_family.py",
    "verify_six_endpoint_families.py",
    "verify_local_slope_three_band.py"
)) {
    $output = & $Python (Join-Path $here $script) 2>&1
    if ($LASTEXITCODE -ne 0) {
        $output | ForEach-Object { Write-Output $_ }
        throw "Verification command failed with exit code ${LASTEXITCODE}: $script"
    }
    $lines.Add("[$script]")
    $output | ForEach-Object {
        $lines.Add([string]$_)
        Write-Output $_
    }
}

$lines.Add("[summary]")
$lines.Add("PASS: all released RM2 odd-descent and local-band regression checks passed")
[IO.File]::WriteAllLines($log, $lines, [Text.UTF8Encoding]::new($false))
Write-Output "Wrote $log"
