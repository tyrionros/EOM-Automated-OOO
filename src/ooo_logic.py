import requests

GRAPH_URL = "https://graph.microsoft.com/v1.0"

def get_users_with_ooo(access_token):
    """
    Fetches users who have an active or scheduled Out-of-Office status.
    Handles pagination to fetch all users and checks settings individually.
    """
    headers = {"Authorization": f"Bearer {access_token}"}
    all_users = []
    
    # Fetch first page of users (Filtering for 'Member' to focus on User Mailboxes)
    url = f"{GRAPH_URL}/users?$filter=userType eq 'Member'&$select=id,displayName,userPrincipalName"
    
    while url:
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            print(f"Error fetching users: {response.text}")
            break
            
        data = response.json()
        all_users.extend(data.get("value", []))
        
        # Check if there's a next page
        url = data.get("@odata.nextLink")

    active_ooo_users = []
    print(f"Checking OOO status for {len(all_users)} users...")

    for user in all_users:
        user_id = user['id']
        # Fetch mailbox settings individually for this user
        settings_url = f"{GRAPH_URL}/users/{user_id}/mailboxSettings"
        settings_resp = requests.get(settings_url, headers=headers)
        
        if settings_resp.status_code == 200:
            mailbox_settings = settings_resp.json()
            status = mailbox_settings.get("automaticRepliesSetting", {}).get("status")
            if status and status != "disabled":
                # Attach settings to the user object for main.py to use
                user['mailboxSettings'] = mailbox_settings
                active_ooo_users.append(user)
        elif settings_resp.status_code == 404 or settings_resp.status_code == 400:
            # Likely no mailbox or invalid ID for mailbox purposes (e.g. Guest)
            continue
        else:
            # Log other errors but keep going
            print(f"Warning: Could not check settings for {user.get('userPrincipalName')}: {settings_resp.status_code}")
            
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
