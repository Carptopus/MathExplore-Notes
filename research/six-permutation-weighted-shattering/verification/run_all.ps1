$ErrorActionPreference = 'Stop'

$verificationDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$python = Get-Command python -ErrorAction Stop

& $python.Source -X utf8 (Join-Path $verificationDir 'verify_weighted_eurocomb26_bound.py')
if ($LASTEXITCODE -ne 0) { throw 'Weighted shattering certificate verification failed' }

Write-Output 'PASS: weighted six-permutation shattering certificate verified'

