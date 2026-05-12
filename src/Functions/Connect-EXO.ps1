function Connect-EXO {
    param (
        [string]$TenantId,
        [string]$AppId,
        [string]$CertificateThumbprint
    )

    if ($AppId -and $CertificateThumbprint) {
        Write-Host "Connecting to Exchange Online using Certificate Authentication..." -ForegroundColor Cyan
        Connect-ExchangeOnline -AppId $AppId -CertificateThumbprint $CertificateThumbprint -Organization $TenantId
    } else {
        Write-Host "Connecting to Exchange Online using Interactive Login..." -ForegroundColor Cyan
        Connect-ExchangeOnline
    }
}
