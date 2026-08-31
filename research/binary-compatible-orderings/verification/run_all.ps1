$ErrorActionPreference = 'Stop'

$verificationDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$python = Get-Command python -ErrorAction Stop

foreach ($script in @(
    'classify_n4.py',
    'verify_n4_independent.py',
    'probe_binary_compatible.py'
)) {
    & $python.Source -X utf8 (Join-Path $verificationDir $script)
    if ($LASTEXITCODE -ne 0) { throw "Verification failed: $script" }
}

$expected = @{
    'binary-compatible-n4-classification.json' = '32b5a7c748270696372f57e5df890c963a4aef09cf583bd9c5e95cc2a642663a'
    'binary-compatible-n4-independent.json' = 'cb682eb6e88009f7cda3b8c127f7fc323ac30c6a7910a0c0886e6ae328c3753f'
    'binary-compatible-n4-local-probe.json' = 'ea4ed9d933e1fa909b3f933783bdca06f4a656dc14e7a92aa85ff6daf6a40c30'
}

foreach ($entry in $expected.GetEnumerator()) {
    $path = Join-Path (Join-Path $verificationDir 'results') $entry.Key
    $actual = (Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash.ToLowerInvariant()
    if ($actual -ne $entry.Value) {
        throw "Certificate hash mismatch: $($entry.Key)"
    }
}

Write-Output 'PASS: binary compatible-order certificates verified'
