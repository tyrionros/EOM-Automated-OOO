function Set-UserOOOTemplate {
    param (
        [string]$UserEmail,
        [string]$DisplayName,
        [string]$ManagerName,
        [string]$ManagerEmail,
        [string]$TemplatePath,
        [string]$CurrentInternalMessage,
        [datetime]$ReturnDate,
        [string]$Marker = "OOO-AUTOMATED-TEMPLATE-V1"
    )

    try {
        if ($CurrentInternalMessage -like "*$Marker*") {
            Write-Host "Template already applied for $UserEmail. Skipping." -ForegroundColor Gray
            return $true
        }

        if (-not (Test-Path $TemplatePath)) {
            throw "Template file not found at $TemplatePath"
        }

        $formattedDate = $ReturnDate.ToString("MMMM dd, yyyy")
        $templateContent = Get-Content -Path $TemplatePath -Raw
        $finalMessage = $templateContent.Replace("{{DisplayName}}", $DisplayName) `
                                        .Replace("{{Date}}", $formattedDate) `
                                        .Replace("{{ManagerName}}", $ManagerName) `
                                        .Replace("{{ManagerEmail}}", $ManagerEmail)

        Write-Host "Applying OOO template for $UserEmail with return date $formattedDate..." -ForegroundColor Green
        
        # Set both Internal and External messages
        Set-MailboxAutoReplyConfiguration -Identity $UserEmail `
            -InternalMessage $finalMessage `
            -ExternalMessage $finalMessage `
            -ErrorAction Stop

        return $true
    } catch {
        Write-Error "Failed to set OOO template for $UserEmail: $($_.Exception.Message)"
        return $false
    }
}
