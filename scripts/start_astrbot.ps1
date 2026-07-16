param(
    [string]$AstrBotPath = "C:\Users\16332\Projects\AstrBot"
)

$ErrorActionPreference = "Stop"
$python = Join-Path $AstrBotPath ".venv\Scripts\python.exe"
$main = Join-Path $AstrBotPath "main.py"
$pidFile = Join-Path $AstrBotPath ".astrbot.pid"
$stdout = Join-Path $AstrBotPath "astrbot.stdout.log"
$stderr = Join-Path $AstrBotPath "astrbot.stderr.log"

if (-not (Test-Path -LiteralPath $python)) {
    throw "AstrBot virtual environment not found: $python"
}

$listener = Get-NetTCPConnection -LocalPort 6185 -State Listen -ErrorAction SilentlyContinue
if ($listener) {
    Write-Output "AstrBot is already listening at http://localhost:6185 (PID $($listener.OwningProcess))."
    exit 0
}

$env:PYTHONUTF8 = "1"
$process = Start-Process -FilePath $python -ArgumentList $main -WorkingDirectory $AstrBotPath `
    -RedirectStandardOutput $stdout -RedirectStandardError $stderr -WindowStyle Hidden -PassThru
Set-Content -LiteralPath $pidFile -Value $process.Id
Write-Output "AstrBot started (PID $($process.Id)); dashboard: http://localhost:6185"

