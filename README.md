# OOO Automated Template Enforcement

This project automates the application of a standardized Out-of-Office (OOO) template for Exchange Online users. When a user enables their auto-reply, this script detects it and applies a corporate-branded HTML template.

## Features
- **Automatic Detection**: Identifies users with active or scheduled auto-replies.
- **Template Enforcement**: Replaces user-defined messages with a standardized HTML template.
- **Smart Skipping**: Uses a hidden marker in the HTML to avoid redundant updates.
- **Flexible Authentication**: Supports both interactive login and Certificate-based authentication (unattended).

## Project Structure
- `src/Main.ps1`: The entry point for the automation.
- `src/Functions/`: Modular PowerShell functions for EXO connection, status checking, and template setting.
- `src/Templates/`: HTML templates for the OOO messages.
- `src/Config/settings.json`: Configuration for Tenant ID, App ID, and paths.

## Setup
1. **Exchange Online PowerShell**: Ensure you have the `ExchangeOnlineManagement` module installed.
   ```powershell
   Install-Module -Name ExchangeOnlineManagement
   ```
2. **Configuration**: Update `src/Config/settings.json` with your Tenant ID. If running unattended, provide `AppId` and `CertificateThumbprint`.
3. **Template**: Customize `src/Templates/OOO-Template.html` to match your corporate branding. Use `{{DisplayName}}` as a placeholder for the user's name.

## Usage
Run the main script:
```powershell
pwsh src/Main.ps1
```

## Scheduling
To apply the template "the moment they set themselves as out of office," it is recommended to run this script as a Scheduled Task (Windows) or a Cron Job (Linux/macOS) every 5-15 minutes.

Alternatively, consider using an Azure Automation Runbook for a cloud-native scheduled execution.
