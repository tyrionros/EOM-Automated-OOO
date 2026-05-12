# Main execution script for OOO Automation
param (
    [string]$ConfigPath = "src/Config/settings.json"
)

# Import functions
Get-ChildItem "$PSScriptRoot/Functions/*.ps1" | ForEach-Object { . $_.FullName }

# Load configuration
if (-not (Test-Path $ConfigPath)) {
    Write-Error "Configuration file not found at $ConfigPath"
    exit 1
}
$config = Get-Content -Path $ConfigPath | ConvertFrom-Json

# Ensure logs directory exists
if ($config.LoggingEnabled -and $config.LogPath) {
    $logDir = Split-Path -Path $config.LogPath -Parent
    if (-not (Test-Path $logDir)) {
        New-Item -ItemType Directory -Path $logDir -Force | Out-Null
    }
}

# Connect to Exchange Online
Connect-EXO -TenantId $config.TenantId -AppId $config.AppId -CertificateThumbprint $config.CertificateThumbprint

# Process users
$usersOOO = Get-UsersWithOOO -ActiveOnly

foreach ($user in $usersOOO) {
    Set-UserOOOTemplate -UserEmail $user.UserPrincipalName `
                        -DisplayName $user.DisplayName `
                        -TemplatePath $config.TemplatePath `
                        -CurrentInternalMessage $user.InternalMessage
}

Write-Host "OOO Automation completed." -ForegroundColor Green
