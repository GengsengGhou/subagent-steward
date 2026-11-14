param(
    [Parameter(Position = 0)]
    [string] $PythonPath
)

$ErrorActionPreference = 'SilentlyContinue'
$Fallback = '{"status":"fallback","model":null,"effort":null,"routing_policy":"sol","source":"sol_policy","reason":"runtime_unavailable"}'
$Probe = "import json, os, re, sqlite3, sys; from pathlib import Path; from typing import Mapping; sys.exit(0 if sys.version_info >= (3, 9) else 1)"
$ReaderPath = Join-Path $PSScriptRoot 'read_primary_model.py'
$Candidates = @()

if (-not [string]::IsNullOrWhiteSpace($PythonPath)) {
    if (-not [System.IO.Path]::IsPathRooted($PythonPath) -or -not (Test-Path -LiteralPath $PythonPath -PathType Leaf)) {
        [Console]::Out.WriteLine($Fallback)
        exit 0
    }
    $Candidates = @($PythonPath)
} else {
    foreach ($Name in @('python3', 'python')) {
        foreach ($Command in @(Get-Command -Name $Name -CommandType Application -All -ErrorAction SilentlyContinue)) {
            $Path = $Command.Source
            if ($Path -and $Path -notmatch '[\\/]WindowsApps[\\/]') {
                $Candidates += $Path
            }
        }
    }
    $Candidates = @($Candidates | Select-Object -Unique)
}

$SelectedPython = $null
foreach ($Candidate in $Candidates) {
    if (-not (Test-Path -LiteralPath $Candidate -PathType Leaf)) {
        if (-not [string]::IsNullOrWhiteSpace($PythonPath)) {
            [Console]::Out.WriteLine($Fallback)
            exit 0
        }
        continue
    }
    try {
        & $Candidate -B -c $Probe *> $null
        if ($LASTEXITCODE -eq 0) {
            $SelectedPython = $Candidate
            break
        }
    } catch {
        if (-not [string]::IsNullOrWhiteSpace($PythonPath)) {
            [Console]::Out.WriteLine($Fallback)
            exit 0
        }
    }
}

if (-not $SelectedPython) {
    [Console]::Out.WriteLine($Fallback)
    exit 0
}

try {
    $Output = @(& $SelectedPython -B $ReaderPath 2>$null)
    if ($LASTEXITCODE -ne 0 -or $Output.Count -eq 0) {
        [Console]::Out.WriteLine($Fallback)
        exit 0
    }
    $Result = ($Output -join "`n") | ConvertFrom-Json -ErrorAction Stop
    if ($Result.status -notin @('ok', 'fallback')) {
        [Console]::Out.WriteLine($Fallback)
        exit 0
    }
    [Console]::Out.WriteLine(($Result | ConvertTo-Json -Compress -Depth 4))
} catch {
    [Console]::Out.WriteLine($Fallback)
}
exit 0
