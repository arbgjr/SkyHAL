# Memory Bank status script para Windows (PowerShell)
param()
Write-Host "Status do Memory Bank (Windows):"
Get-ChildItem -Path "memory-bank" -Filter "*.md" | ForEach-Object {
    Write-Host ("$($_.Name):") -ForegroundColor Yellow
    Get-Content $_.FullName | Select-Object -First 3
    Write-Host ""
}
exit 0
