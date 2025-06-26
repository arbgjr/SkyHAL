# Test script para Windows (PowerShell)
param()
Write-Host "Executando testes com pytest e cobertura..."

# Ativar ambiente virtual se necessário (ajuste conforme seu setup)
# $env:VIRTUAL_ENV = "<CAMINHO_VENV>"
# . <CAMINHO_VENV>\Scripts\Activate.ps1

# Executa pytest com cobertura
poetry run pytest --cov=src --cov=tests --cov-report=term-missing
$LASTEXITCODE = $?
if ($LASTEXITCODE -eq $true) {
    exit 0
}
else {
    exit 1
}
