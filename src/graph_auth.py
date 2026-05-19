import msal
import sys

def get_access_token(config):
    """
    Acquires an access token from Microsoft Entra ID (formerly Azure AD) using interactive login.
    This method opens a browser for the user to authenticate.
    """
    # Use 'common' if TenantId is not provided, allowing any tenant (Multi-tenant)
    tenant_id = config.get("TenantId", "common")
    authority = f"https://login.microsoftonline.com/{tenant_id}"
    
    # Required scopes for the Graph API calls we make
    # Note: These must be granted as 'Delegated' permissions in the App Registration
    scopes = [
        "User.Read.All", 
        "MailboxSettings.ReadWrite", 
        "Directory.Read.All"
    ]

    app = msal.PublicClientApplication(
        config["AppId"], 
        authority=authority
    )

    # First, try to get a token from the cache
    accounts = app.get_accounts()
    result = None
    if accounts:
        result = app.acquire_token_silent(scopes, account=accounts[0])

    if not result:
        print("No cached token found. Opening browser for interactive login...")
        # This will open the default system browser
        result = app.acquire_token_interactive(scopes=scopes)

    if "access_token" in result:
        return result["access_token"]
    else:
        print(f"Error acquiring token: {result.get('error')}")
        print(f"Description: {result.get('error_description')}")
        return None
