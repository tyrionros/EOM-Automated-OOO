import subprocess
import time
import sys
from ooo_logic import set_user_ooo_message

def run_powershell(command):
    """
    Executes a PowerShell command using 'pwsh' (PowerShell Core) which is standard for Mac/Linux.
    Falls back to 'powershell' if 'pwsh' is not found (for Windows).
    """
    executable = "pwsh"
    try:
        subprocess.run([executable, "-version"], capture_output=True)
    except FileNotFoundError:
        executable = "powershell"

    try:
        process = subprocess.run(
            [executable, "-Command", command],
            capture_output=True,
            text=True,
            check=True
        )
        return process.stdout
    except subprocess.CalledProcessError as e:
        print(f"PowerShell Error: {e.stderr}", file=sys.stderr)
        return None
    except FileNotFoundError:
        print(f"Error: PowerShell ({executable}) not found. Please ensure PowerShell is installed.", file=sys.stderr)
        return None

def connect_exchange(admin_upn):
    """
    Connects to Exchange Online. 
    """
    print(f"Connecting to Exchange Online as {admin_upn}...")
    command = f"Connect-ExchangeOnline -UserPrincipalName {admin_upn} -ShowBanner:$false"
    return run_powershell(command)

def disconnect_exchange():
    """
    Disconnects from Exchange Online session.
    """
    print("Disconnecting from Exchange Online...")
    return run_powershell("Disconnect-ExchangeOnline -Confirm:$false")

def add_full_access(target_mailbox, delegate_user):
    """
    Grants Full Access permission to the delegate_user for the target_mailbox.
    """
    print(f"Adding Full Access for {delegate_user} on {target_mailbox}...")
    command = (
        f"Add-MailboxPermission -Identity '{target_mailbox}' "
        f"-User '{delegate_user}' -AccessRights FullAccess "
        f"-InheritanceType All -Confirm:$false"
    )
    return run_powershell(command)

def remove_full_access(target_mailbox, delegate_user):
    """
    Removes Full Access permission.
    """
    print(f"Removing Full Access for {delegate_user} on {target_mailbox}...")
    command = (
        f"Remove-MailboxPermission -Identity '{target_mailbox}' "
        f"-User '{delegate_user}' -AccessRights FullAccess "
        f"-Confirm:$false"
    )
    return run_powershell(command)

def update_ooo_with_delegation(token, admin_upn, target_mailbox, html_message, marker, wait_seconds=5):
    """
    Orchestrates the process: Add delegation -> Update OOO -> Remove delegation.
    """
    if add_full_access(target_mailbox, admin_upn) is None:
        print(f"Skipping {target_mailbox} due to delegation error.")
        return False
    
    if wait_seconds > 0:
        print(f"Waiting {wait_seconds}s for permission propagation...")
        time.sleep(wait_seconds)
    
    success = set_user_ooo_message(token, target_mailbox, html_message, marker)
    
    if not success:
        print(f"Failed to update OOO for {target_mailbox} even with delegation.")

    remove_full_access(target_mailbox, admin_upn)
    
    return success
