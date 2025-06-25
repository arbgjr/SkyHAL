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

# Instalação dinâmica dos pacotes MCP a partir de .vscode/mcp.json
$mcpConfigFile = Join-Path $PSScriptRoot "..\.vscode\mcp.json"
if (-Not (Test-Path $mcpConfigFile)) {
    Write-Host "❌ Arquivo de configuração MCP não encontrado: $mcpConfigFile" -ForegroundColor Red
    exit 1
}

try {
    $mcpJson = Get-Content $mcpConfigFile -Raw | ConvertFrom-Json
    if (-not $mcpJson.servers) {
        Write-Host "❌ Nenhum servidor MCP encontrado em $mcpConfigFile" -ForegroundColor Red
        exit 1
    }
    $mcpPackages = @()
    foreach ($srv in $mcpJson.servers.PSObject.Properties) {
        $cmd = $srv.Value.command
        $srvArgs = $srv.Value.args
        # Detecta pacotes npm do comando npx
        if ($cmd -eq "npx" -and $srvArgs.Count -ge 2) {
            $pkg = $srvArgs[1]
            if ($pkg -like "@modelcontextprotocol/*") {
                $mcpPackages += $pkg
            }
        }
    }
    $mcpPackages = $mcpPackages | Select-Object -Unique
    if ($mcpPackages.Count -eq 0) {
        Write-Host "[WARN] Nenhum pacote MCP detectado para instalação." -ForegroundColor Yellow
        exit 0
    }
    foreach ($pkg in $mcpPackages) {
        Write-Host ("[INFO] Instalando pacote MCP: {0}" -f $pkg) -ForegroundColor Cyan
        try {
            & npm install -g $pkg
            if ($LASTEXITCODE -eq 0) {
                Write-Host ("[OK] {0} instalado globalmente." -f $pkg) -ForegroundColor Green
            } else {
                Write-Host ("[ERRO] Falha ao instalar {0}. Código de saída: {1}" -f $pkg, $LASTEXITCODE) -ForegroundColor Red
            }
        } catch {
            Write-Host ("[ERRO] Exceção ao instalar {0}: {1}" -f $pkg, $_.Exception.Message) -ForegroundColor Red
        }
    }
} catch {
    Write-Host ("[ERRO] Falha ao processar {0}: {1}" -f $mcpConfigFile, $_.Exception.Message) -ForegroundColor Red
    exit 1
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
