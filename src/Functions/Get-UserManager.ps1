function Get-UserManager {
    param (
        [string]$UserEmail
    )

    try {
        $user = Get-User -Identity $UserEmail -ErrorAction Stop
        if ($null -eq $user.Manager) {
            return $null
        }

        $manager = Get-User -Identity $user.Manager -ErrorAction Stop
        return [PSCustomObject]@{
            DisplayName        = $manager.DisplayName
            PrimarySmtpAddress = $manager.PrimarySmtpAddress
        }
    } catch {
        Write-Warning "Could not fetch manager for $UserEmail: $($_.Exception.Message)"
        return $null
    }
}
