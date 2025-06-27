#!/usr/bin/env pwsh

# Remover ambiente virtual existente
if (Test-Path ".venv") {
    Write-Host "Removendo ambiente virtual existente..."
    Remove-Item -Path ".venv" -Recurse -Force
}

# Criar novo ambiente virtual
Write-Host "Criando novo ambiente virtual..."
python -m venv .venv --clear

# Ativar ambiente virtual
Write-Host "Ativando ambiente virtual..."
.venv\Scripts\Activate

# Atualizar pip
Write-Host "Atualizando pip..."
python -m pip install --upgrade pip

# Instalar dependências
Write-Host "Instalando dependências..."
pip install -r requirements.txt

# Configurar variáveis de ambiente
Write-Host "Configurando variáveis de ambiente..."
$env:PYTHONPATH = (Get-Location).Path

Write-Host "Ambiente configurado com sucesso!"
