param(
    [string]$Python = 'python',
    [int]$MemoryLimitMB = 1024,
    [int]$TimeoutSeconds = 120
)

$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest

$pythonCommand = Get-Command $Python -ErrorAction Stop
$pythonPath = $pythonCommand.Source
$scripts = @(
    'torus_rank4_probe.py',
    'independent_schreier_verifier.py'
)
$memoryLimitBytes = [int64]$MemoryLimitMB * 1MB

function Get-ProcessTreeIds {
    param([int]$RootProcessId)

    $rows = @(Get-CimInstance Win32_Process -Property ProcessId, ParentProcessId)
    $ids = [Collections.Generic.HashSet[int]]::new()
    [void]$ids.Add($RootProcessId)
    $changed = $true
    while ($changed) {
        $changed = $false
        foreach ($row in $rows) {
            if ($ids.Contains([int]$row.ParentProcessId) -and $ids.Add([int]$row.ProcessId)) {
                $changed = $true
            }
        }
    }
    return @($ids)
}

function Stop-ProcessTree {
    param([int[]]$ProcessIds)

    foreach ($processId in $ProcessIds) {
        Stop-Process -Id $processId -Force -ErrorAction SilentlyContinue
    }
}

foreach ($scriptName in $scripts) {
    $scriptPath = Join-Path $PSScriptRoot $scriptName
    $process = $null
    $stdoutTask = $null
    $stderrTask = $null
    $stopwatch = [Diagnostics.Stopwatch]::StartNew()
    $peakPrivateBytes = [int64]0

    try {
        $startInfo = [Diagnostics.ProcessStartInfo]::new()
        $startInfo.FileName = $pythonPath
        $startInfo.WorkingDirectory = $PSScriptRoot
        $startInfo.UseShellExecute = $false
        $startInfo.CreateNoWindow = $true
        $startInfo.RedirectStandardOutput = $true
        $startInfo.RedirectStandardError = $true
        $startInfo.ArgumentList.Add('-B')
        $startInfo.ArgumentList.Add('-u')
        $startInfo.ArgumentList.Add($scriptPath)

        $process = [Diagnostics.Process]::new()
        $process.StartInfo = $startInfo
        if (-not $process.Start()) {
            throw "failed to start $scriptName"
        }
        $stdoutTask = $process.StandardOutput.ReadToEndAsync()
        $stderrTask = $process.StandardError.ReadToEndAsync()

        while (-not $process.HasExited -or -not $stdoutTask.IsCompleted -or -not $stderrTask.IsCompleted) {
            $process.Refresh()
            $processIds = @(Get-ProcessTreeIds -RootProcessId $process.Id)
            $privateBytes = [int64]0
            foreach ($trackedId in $processIds) {
                $trackedProcess = Get-Process -Id $trackedId -ErrorAction SilentlyContinue
                if ($null -ne $trackedProcess) {
                    $privateBytes += [int64]$trackedProcess.PrivateMemorySize64
                }
            }
            if ($privateBytes -gt $peakPrivateBytes) {
                $peakPrivateBytes = $privateBytes
            }
            if ($privateBytes -gt $memoryLimitBytes) {
                Stop-ProcessTree -ProcessIds $processIds
                throw "$scriptName exceeded the ${MemoryLimitMB} MiB private-memory limit"
            }
            if ($stopwatch.Elapsed.TotalSeconds -gt $TimeoutSeconds) {
                Stop-ProcessTree -ProcessIds $processIds
                throw "$scriptName exceeded the ${TimeoutSeconds} second timeout"
            }
            Start-Sleep -Milliseconds 200
        }

        $process.WaitForExit()
        $stopwatch.Stop()
        $stdoutText = $stdoutTask.GetAwaiter().GetResult()
        $stderrText = $stderrTask.GetAwaiter().GetResult()
        if ($stdoutText) {
            [Console]::Out.Write($stdoutText)
        }
        if ($stderrText) {
            [Console]::Error.Write($stderrText)
        }
        if ($process.ExitCode -ne 0) {
            throw "$scriptName exited with code $($process.ExitCode)"
        }
        Write-Output (
            'SAFE_RUN script={0} exit=0 elapsed_seconds={1:N2} peak_private_mib={2:N1}' -f `
                $scriptName,
                $stopwatch.Elapsed.TotalSeconds,
                ($peakPrivateBytes / 1MB)
        )
    }
    finally {
        if ($null -ne $process -and -not $process.HasExited) {
            try {
                Stop-ProcessTree -ProcessIds @(Get-ProcessTreeIds -RootProcessId $process.Id)
            }
            catch {
                # 运行失败或被外部终止后的兜底清理。
            }
        }
        if ($null -ne $process) {
            $process.Dispose()
        }
    }
}
