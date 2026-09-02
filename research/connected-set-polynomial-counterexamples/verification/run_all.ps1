param(
    [Parameter(Mandatory = $true)]
    [string]$Graph8Catalog,

    [string]$Python = "python"
)

$ErrorActionPreference = "Stop"
$scriptPath = Join-Path $PSScriptRoot "verify_families.py"

if (-not (Test-Path -LiteralPath $Graph8Catalog -PathType Leaf)) {
    throw "graph8c.g6 not found: $Graph8Catalog"
}
$pythonCommand = Get-Command $Python -ErrorAction SilentlyContinue
if ($null -eq $pythonCommand) {
    throw "Python interpreter not found: $Python"
}

& $Python $scriptPath --graph8c $Graph8Catalog
if ($LASTEXITCODE -ne 0) {
    throw "Verification failed with exit code $LASTEXITCODE"
}
