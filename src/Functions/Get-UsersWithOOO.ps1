function Get-UsersWithOOO {
    param (
        [switch]$ActiveOnly
    )

    Write-Host "Fetching mailbox auto-reply configurations..." -ForegroundColor Cyan
    
    # Getting all user mailboxes first might be slow in large environments.
    # We filter for 'UserMailbox' types.
    $mailboxes = Get-Mailbox -RecipientTypeDetails UserMailbox -ResultSize Unlimited

    $results = foreach ($mb in $mailboxes) {
        $config = Get-MailboxAutoReplyConfiguration -Identity $mb.UserPrincipalName
        
        if ($ActiveOnly) {
            if ($config.AutoReplyState -ne "Disabled") {
                [PSCustomObject]@{
                    UserPrincipalName = $mb.UserPrincipalName
                    DisplayName       = $mb.DisplayName
                    AutoReplyState    = $config.AutoReplyState
                    InternalMessage   = $config.InternalMessage
                    ExternalMessage   = $config.ExternalMessage
                    EndTime           = $config.EndTime
                }
            }
        } else {
            [PSCustomObject]@{
                UserPrincipalName = $mb.UserPrincipalName
                DisplayName       = $mb.DisplayName
                AutoReplyState    = $config.AutoReplyState
                InternalMessage   = $config.InternalMessage
                ExternalMessage   = $config.ExternalMessage
                EndTime           = $config.EndTime
            }
        }
    }

    return $results
}
