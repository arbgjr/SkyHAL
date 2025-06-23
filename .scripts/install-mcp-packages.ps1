# Script para instalação global dos pacotes MCP necessários
# Criado em: 05/06/2025

$ErrorActionPreference = "Stop"

Write-Host "📦 Instalando pacotes MCP globalmente..." -ForegroundColor Cyan

# Verificar instalação do Node.js e NPM
try {
    $nodeVersion = node -v
    $npmVersion = npm -v
    
    Write-Host "✅ Node.js $nodeVersion está instalado" -ForegroundColor Green
    Write-Host "✅ NPM $npmVersion está instalado" -ForegroundColor Green
} catch {
    Write-Host "❌ Node.js ou NPM não está instalado ou não está no PATH!" -ForegroundColor Red
    Write-Host "Por favor, instale o Node.js da página oficial: https://nodejs.org/" -ForegroundColor Yellow
    exit 1
}

# Lista de pacotes MCP para instalar
$mcpPackages = @(
    "@modelcontextprotocol/server-github",
    "@modelcontextprotocol/server-filesystem",
    "@modelcontextprotocol/server-memory",
    "@modelcontextprotocol/server-sequential-thinking",
    "@modelcontextprotocol/server-everything"
)

# Tentar instalar os pacotes MCP
foreach ($pkg in $mcpPackages) {
    Write-Host "`nInstalando $pkg..." -ForegroundColor Cyan
    try {
        & npm install -g $pkg
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✅ $pkg instalado globalmente com sucesso!" -ForegroundColor Green
        } else {
            Write-Host "❌ Falha ao instalar $pkg. Código de saída: $LASTEXITCODE" -ForegroundColor Red
        }
    } catch {
        Write-Host ("❌ Erro ao instalar " + $pkg + ":") -ForegroundColor Red
        Write-Host "   $($_.Exception.Message)" -ForegroundColor Red
    }
}

# Verificar se uvicorn também está instalado (para uvx)
Write-Host "`nVerificando uvicorn (necessário para uvx)..." -ForegroundColor Cyan
try {
    & pip show uvicorn | Out-Null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ uvicorn está instalado" -ForegroundColor Green
    } else {
        Write-Host "Instalando uvicorn..." -ForegroundColor Yellow
        & pip install uvicorn
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✅ uvicorn instalado com sucesso!" -ForegroundColor Green
        } else {
            Write-Host "❌ Falha ao instalar uvicorn" -ForegroundColor Red
        }
    }
} catch {
    Write-Host "❌ Erro ao verificar/instalar uvicorn:" -ForegroundColor Red
    Write-Host "   $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host "`n✅ Instalação concluída!" -ForegroundColor Green
Write-Host "`nPara verificar o ambiente MCP, execute: .\.scripts\diagnose-mcp-environment.ps1" -ForegroundColor Cyan
Write-Host "Para iniciar os servidores MCP com correções, execute: .\.scripts\start-mcp-servers-fix.ps1" -ForegroundColor Cyan
