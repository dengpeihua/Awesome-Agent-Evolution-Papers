param(
    [string]$AstrBotPath = "C:\Users\16332\Projects\AstrBot",
    [string]$ProjectPath = (Split-Path -Parent $PSScriptRoot)
)

$ErrorActionPreference = "Stop"
$source = (Resolve-Path -LiteralPath $ProjectPath).Path
$plugins = Join-Path $AstrBotPath "data\plugins"
$target = Join-Path $plugins "astrbot_plugin_agent_paper_digest"

New-Item -ItemType Directory -Path $plugins -Force | Out-Null
if (Test-Path -LiteralPath $target) {
    Write-Output "Plugin path already exists: $target"
    exit 0
}

New-Item -ItemType Junction -Path $target -Target $source | Out-Null
Write-Output "Installed AstrBot plugin junction: $target -> $source"

