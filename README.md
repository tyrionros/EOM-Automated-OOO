# OOO Automated Template Enforcement (Python)

This project automates the application of a standardized Out-of-Office (OOO) template for Microsoft 365 users using the Microsoft Graph API.

## Features
- **Automatic Detection**: Identifies users with active or scheduled auto-replies via Graph API.
- **Template Enforcement**: Replaces user-defined messages with a standardized HTML template.
- **Manager Details**: Dynamically fetches the user's manager's name and email.
- **Smart Skipping**: Uses a hidden marker in the HTML to avoid redundant updates.

## Project Structure
- `src/main.py`: The entry point for the automation.
- `src/graph_auth.py`: Authentication logic using MSAL.
- `src/ooo_logic.py`: Functions for interacting with Microsoft Graph.
- `src/Templates/`: HTML templates for the OOO messages.
- `src/Config/settings.json`: Configuration for Tenant ID, App ID, and paths.

## Prerequisites
- **Python**: 3.8 or higher.
- **Azure App Registration**:
  - **Platform**: Add 'Mobile and desktop applications' with redirect URI `http://localhost`.
  - **Permissions (Delegated)**: `User.Read.All`, `MailboxSettings.ReadWrite`, `Directory.Read.All`.
  - **Type**: Public Client (No Client Secret required).

## Setup
1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
2. **Configuration**: Update `src/Config/settings.json`.
   ```json
   {
       "TenantId": "YOUR_TENANT_ID",
       "AppId": "YOUR_APP_ID",
       "TemplatePath": "src/Templates/OOO-Template.html"
   }
   ```
   *Note: No `ClientSecret` is needed for interactive login.*
3. **Template**: Customize `src/Templates/OOO-Template.html`.

## Usage
You can run the automation using the provided `run.py` wrapper, which automatically checks and installs dependencies:
```bash
python run.py
```

Alternatively, run the main script directly (ensure dependencies are installed):
```bash
python src/main.py
```

## Scheduling
It is recommended to run this script as a Cron Job or an Azure Function every 15 minutes.
