$ErrorActionPreference = 'Stop'

$verificationDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$python = Get-Command python -ErrorAction Stop

& $python.Source -X utf8 (Join-Path $verificationDir 'verify_k6_cographic_counterexample.py')
if ($LASTEXITCODE -ne 0) { throw 'K6 cographic counterexample verification failed' }

& $python.Source -X utf8 (Join-Path $verificationDir 'verify_k6_projective_plane_mechanism.py')
if ($LASTEXITCODE -ne 0) { throw 'K6 projective-plane mechanism verification failed' }

& $python.Source -X utf8 (Join-Path $verificationDir 'verify_rp2_stellar_family.py')
if ($LASTEXITCODE -ne 0) { throw 'RP2 stellar-family verification failed' }

Write-Output 'PASS: all orderable-cographic projective-plane checks completed'

