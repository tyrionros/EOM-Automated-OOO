import msal
import sys

def get_access_token(config):
    """
    Acquires an access token from Microsoft Entra ID (formerly Azure AD).
    Supports both Client Secret and Certificate-based authentication.
    """
    authority = f"https://login.microsoftonline.com/{config['TenantId']}"
    scopes = ["https://graph.microsoft.com/.default"]

    # Try Certificate-based auth first if thumbprint is provided
    if config.get("CertificateThumbprint"):
        # Note: In a real scenario, you'd need to load the private key from a file or store.
        # This is a placeholder for the logic.
        print("Certificate-based authentication detected (Logic placeholder).")
        # app = msal.ConfidentialClientApplication(
        #     config["AppId"], authority=authority,
        #     client_credential={"thumbprint": config["CertificateThumbprint"], "private_key": open("path_to_key.pem").read()}
        # )
        # return app.acquire_token_for_client(scopes=scopes)
        pass

    # Fallback to Client Secret if provided
    if config.get("ClientSecret"):
        app = msal.ConfidentialClientApplication(
            config["AppId"], authority=authority,
            client_credential=config["ClientSecret"]
        )
        result = app.acquire_token_for_client(scopes=scopes)
        if "access_token" in result:
            return result["access_token"]
        else:
            print(f"Error acquiring token: {result.get('error_description')}")
            return None

    print("Error: No valid authentication method (ClientSecret or Certificate) found in config.")
    return None
