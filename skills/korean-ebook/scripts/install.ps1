$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$Python = if (Get-Command py -ErrorAction SilentlyContinue) { "py" } else { "python" }
if ($Python -eq "py") {
    & py -3.11 -m venv "$Root\.venv"
} else {
    & python -m venv "$Root\.venv"
}
& "$Root\.venv\Scripts\python.exe" -m pip install --upgrade pip
& "$Root\.venv\Scripts\python.exe" -m pip install -r "$Root\scripts\requirements.txt"
Write-Host "Installed. Activate with: $Root\.venv\Scripts\Activate.ps1"
