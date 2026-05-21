import json
import os
from datetime import datetime
from graph_auth import get_access_token
from ooo_logic import get_users_with_ooo, get_manager, set_user_ooo_message
from exchange import connect_exchange, disconnect_exchange, update_ooo_with_delegation

def main():
    config_path = "src/Config/settings.json"
    if not os.path.exists(config_path):
        print(f"Error: Configuration file not found at {config_path}")
        return

    with open(config_path, 'r') as f:
        config = json.load(f)

    # Delegation settings
    use_delegation = config.get("UseDelegation", False)
    admin_upn = config.get("AdminUPN")

    if use_delegation and not admin_upn:
        print("Error: 'AdminUPN' must be provided in settings.json when 'UseDelegation' is enabled.")
        return

    # Acquire access token
    token = get_access_token(config)
    if not token:
        print("Authentication failed.")
        return

    # Fetch users with active OOO
    users = get_users_with_ooo(token)
    print(f"Found {len(users)} users with active/scheduled OOO.")

    # Load template
    template_path = config.get("TemplatePath", "src/Templates/OOO-Template.html")
    with open(template_path, 'r') as f:
        template_content = f.read()

    marker = "OOO-AUTOMATED-TEMPLATE-V1"

    # Connect to Exchange if delegation is needed
    if use_delegation:
        connect_exchange(admin_upn)

    try:
        for user in users:
            user_id = user['id']
            display_name = user['displayName']
            upn = user['userPrincipalName']
            
            # Get Return Date from mailbox settings
            mailbox_settings = user.get('mailboxSettings', {})
            end_time_dict = mailbox_settings.get('automaticRepliesSetting', {}).get('scheduledEndDateTime', {})
            end_time_str = end_time_dict.get('dateTime')
            
            formatted_date = "TBD"
            if end_time_str:
                try:
                    # Microsoft Graph date format: 2026-05-30T08:00:00.0000000
                    dt = datetime.fromisoformat(end_time_str.split('.')[0])
                    formatted_date = dt.strftime("%B %d, %y")
                except Exception:
                    formatted_date = end_time_str

            # Fetch Manager
            manager = get_manager(token, user_id)
            manager_name = manager['displayName'] if manager else "your supervisor"
            manager_email = manager.get('mail') or manager.get('userPrincipalName') if manager else "N/A"

            # Fill Template
            final_message = template_content.replace("{{DisplayName}}", display_name) \
                                           .replace("{{Date}}", formatted_date) \
                                           .replace("{{ManagerName}}", manager_name) \
                                           .replace("{{ManagerEmail}}", manager_email)

            # Apply Template
            print(f"Processing OOO for {upn}...")
            
            if use_delegation:
                # Use the delegation flow: Add FullAccess -> Update -> Remove FullAccess
                success = update_ooo_with_delegation(token, admin_upn, upn, final_message, marker)
            else:
                # Direct update via Graph (requires Application permissions or self-update)
                success = set_user_ooo_message(token, user_id, final_message, marker)
                
            if success:
                print(f"Successfully applied template for {upn}")
    finally:
        # Always disconnect from Exchange Online if we connected
        if use_delegation:
            disconnect_exchange()

if __name__ == "__main__":
    main()
