import requests

GRAPH_URL = "https://graph.microsoft.com/v1.0"

def get_users_with_ooo(access_token):
    """
    Fetches users who have an active or scheduled Out-of-Office status.
    Requires MailboxSettings.Read permission.
    """
    headers = {"Authorization": f"Bearer {access_token}"}
    # We fetch all users and their mailbox settings. 
    # Note: In large tenants, you would use $filter or pagination.
    url = f"{GRAPH_URL}/users?$select=id,displayName,userPrincipalName,mailboxSettings"
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        print(f"Error fetching users: {response.text}")
        return []

    users = response.json().get("value", [])
    active_ooo_users = []

    for user in users:
        mailbox_settings = user.get("mailboxSettings")
        if mailbox_settings and mailbox_settings.get("automaticRepliesSetting", {}).get("status") != "disabled":
            active_ooo_users.append(user)
            
    return active_ooo_users

def get_manager(access_token, user_id):
    """
    Fetches the manager details for a specific user.
    """
    headers = {"Authorization": f"Bearer {access_token}"}
    url = f"{GRAPH_URL}/users/{user_id}/manager?$select=displayName,mail,userPrincipalName"
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    elif response.status_code == 404:
        return None  # No manager found
    else:
        print(f"Error fetching manager for {user_id}: {response.text}")
        return None

def set_user_ooo_message(access_token, user_id, html_message, marker):
    """
    Updates the internal and external OOO messages for a user.
    """
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    # First, check if the marker is already present
    url = f"{GRAPH_URL}/users/{user_id}/mailboxSettings"
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        current_settings = response.json()
        internal_msg = current_settings.get("automaticRepliesSetting", {}).get("internalReplyMessage", "")
        if marker in internal_msg:
            print(f"Template already applied for {user_id}. Skipping.")
            return True

    # Patch the mailbox settings
    payload = {
        "automaticRepliesSetting": {
            "internalReplyMessage": html_message,
            "externalReplyMessage": html_message
        }
    }
    
    patch_response = requests.patch(url, headers=headers, json=payload)
    if patch_response.status_code == 200:
        return True
    else:
        print(f"Failed to set OOO for {user_id}: {patch_response.text}")
        return False
