param(
    [string]$Python = 'python'
)

$ErrorActionPreference = 'Stop'
$folder = Split-Path -Parent $MyInvocation.MyCommand.Path
$scripts = Get-ChildItem -LiteralPath $folder -Filter 'verify_*.py' -File | Sort-Object Name

if ($scripts.Count -ne 17) {
    throw "Expected 17 verification scripts, found $($scripts.Count)."
}

foreach ($script in $scripts) {
    Write-Host "Running $($script.Name)"
    & $Python -X utf8 $script.FullName
    if ($LASTEXITCODE -ne 0) {
        throw "$($script.Name) failed with exit code $LASTEXITCODE."
    }
}

Write-Host 'All 17 finite verification checks passed.'
