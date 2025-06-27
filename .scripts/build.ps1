# Build script para Windows (PowerShell)
param()
Write-Host "Iniciando build com Poetry..."

# Build do pacote Python
poetry build
if ($LASTEXITCODE -ne 0) {
    Write-Host "Build falhou." -ForegroundColor Red
    exit 1
}

Write-Host "Build finalizado com sucesso."
exit 0
