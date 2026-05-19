import msal
import sys

def get_access_token(config):
    """
    Acquires an access token from Microsoft Entra ID.
    Prioritizes Client Secret (Application Permissions) for bulk operations.
    Falls back to interactive if ClientSecret is missing.
    """
    tenant_id = config.get("TenantId", "common")
    authority = f"https://login.microsoftonline.com/{tenant_id}"
    app_id = config.get("AppId")
    client_secret = config.get("ClientSecret")

    if app_id and client_secret:
        # Application Permissions (Service-to-Service)
        # Required for managing OTHER users' mailbox settings
        print("Using Application Permissions (Client Secret)...")
        app = msal.ConfidentialClientApplication(
            app_id, 
            authority=authority,
            client_credential=client_secret
        )
        result = app.acquire_token_for_client(scopes=["https://graph.microsoft.com/.default"])
    else:
        # Fallback to Interactive (Delegated Permissions)
        # WARNING: This will only allow access to the signed-in user's mailbox
        print("ClientSecret missing. Falling back to Interactive Login...")
        print("NOTE: Interactive login only allows managing your OWN mailbox.")
        app = msal.PublicClientApplication(app_id, authority=authority)
        scopes = ["User.Read.All", "MailboxSettings.ReadWrite", "Directory.Read.All"]
        
        accounts = app.get_accounts()
        result = app.acquire_token_silent(scopes, account=accounts[0]) if accounts else None
        if not result:
            result = app.acquire_token_interactive(scopes=scopes)

    if "access_token" in result:
        return result["access_token"]
    else:
        print(f"Error acquiring token: {result.get('error')}")
        print(f"Description: {result.get('error_description')}")
        return None
