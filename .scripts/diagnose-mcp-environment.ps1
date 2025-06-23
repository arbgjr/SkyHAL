# Script de diagnóstico para ambiente MCP
# Este script verifica a instalação e configuração do Node.js, NPX e outros requisitos
# Criado em: 05/06/2025

$ErrorActionPreference = "Continue"
$diagnosticoPath = Join-Path -Path $PSScriptRoot -ChildPath ".." -AdditionalChildPath "logs", "mcp-diagnostico.json"

# Função para exibir cabeçalho
function Write-Header {
    param (
        [Parameter(Mandatory = $true)]
        [string]$Text
    )
    
    Write-Host "`n===== $Text =====" -ForegroundColor Cyan
}

Write-Header "MCP Environment Diagnostic Tool"

# Estrutura para armazenar resultados
$results = @{
    Timestamp   = Get-Date
    System      = @{
        OSVersion      = [System.Environment]::OSVersion.VersionString
        Is64BitOS      = [System.Environment]::Is64BitOperatingSystem
        Is64BitProcess = [System.Environment]::Is64BitProcess
    }
    NodeJS      = @{
        Installed = $false
        Version   = "Não detectado"
        Path      = "Não encontrado"
        Is64Bit   = $false
    }
    NPX         = @{
        Found   = $false
        Path    = "Não encontrado"
        Version = "Não detectado"
    }
    NPM         = @{
        Found        = $false
        Path         = "Não encontrado"
        Version      = "Não detectado"
        GlobalPrefix = "Não encontrado"
    }
    UVX         = @{
        Found   = $false
        Path    = "Não encontrado"
        Version = "Não detectado"
    }
    MCPPackages = @{
        Installed = @()
        Missing   = @()
    }
    PATH        = @{
        Values           = @()
        ContainsNodePath = $false
    }
}

Clear-Host

# Verificar Node.js
Write-Header "Verificando Node.js"
try {
    $nodeCommand = Get-Command node -ErrorAction Stop
    $nodeVersion = node -v
    $results.NodeJS.Installed = $true
    $results.NodeJS.Version = $nodeVersion
    $results.NodeJS.Path = $nodeCommand.Source
    
    # Determinar se Node é 32 ou 64 bit
    $nodeArch = & node -e "console.log(process.arch)"
    $results.NodeJS.Is64Bit = ($nodeArch -eq "x64")
    
    Write-Host "✅ Node.js está instalado" -ForegroundColor Green
    Write-Host "   Versão: $nodeVersion"
    Write-Host "   Caminho: $($nodeCommand.Source)"
    Write-Host "   Arquitetura: $nodeArch"
}
catch {
    $results.NodeJS.Installed = $false
    Write-Host "❌ Node.js não está instalado ou não está no PATH" -ForegroundColor Red
    Write-Host "   Erro: $($_.Exception.Message)"
}

# Verificar NPX
Write-Header "Verificando NPX"
try {
    $npxCommand = Get-Command npx -ErrorAction Stop
    $npxVersion = & npx --version
    $results.NPX.Found = $true
    $results.NPX.Path = $npxCommand.Source
    $results.NPX.Version = $npxVersion
    
    Write-Host "✅ NPX está instalado" -ForegroundColor Green
    Write-Host "   Versão: $npxVersion"
    Write-Host "   Caminho: $($npxCommand.Source)"
}
catch {
    $results.NPX.Found = $false
    Write-Host "❌ NPX não está instalado ou não está no PATH" -ForegroundColor Red
    Write-Host "   Erro: $($_.Exception.Message)"
}

# Verificar NPM
Write-Header "Verificando NPM"
try {
    $npmCommand = Get-Command npm -ErrorAction Stop
    $npmVersion = & npm --version
    $npmPrefix = & npm config get prefix
    
    $results.NPM.Found = $true
    $results.NPM.Path = $npmCommand.Source
    $results.NPM.Version = $npmVersion
    $results.NPM.GlobalPrefix = $npmPrefix
    
    Write-Host "✅ NPM está instalado" -ForegroundColor Green
    Write-Host "   Versão: $npmVersion"
    Write-Host "   Caminho: $($npmCommand.Source)"
    Write-Host "   Prefixo Global: $npmPrefix"
    
    # Verificar pacotes MCP instalados globalmente
    Write-Host "`nVerificando pacotes MCP instalados globalmente..."
    $globalPackages = & npm list -g --depth=0 2>$null
    
    $mcpPackages = @(
        "@modelcontextprotocol/server-github",
        "@modelcontextprotocol/server-filesystem",
        "@modelcontextprotocol/server-memory",
        "@modelcontextprotocol/server-sequential-thinking",
        "@modelcontextprotocol/server-everything"
    )
    
    foreach ($pkg in $mcpPackages) {
        if ($globalPackages -like "*$pkg*") {
            $results.MCPPackages.Installed += $pkg
            Write-Host "   ✅ $pkg está instalado globalmente" -ForegroundColor Green
        }
        else {
            $results.MCPPackages.Missing += $pkg
            Write-Host "   ❌ $pkg não está instalado globalmente" -ForegroundColor Yellow
        }
    }
    
}
catch {
    $results.NPM.Found = $false
    Write-Host "❌ NPM não está instalado ou não está no PATH" -ForegroundColor Red
    Write-Host "   Erro: $($_.Exception.Message)"
}

# Verificar UVX
Write-Header "Verificando UVX"
try {
    $uvxCommand = Get-Command uvx -ErrorAction Stop
    $uvxVersion = & uvx --version
    $results.UVX.Found = $true
    $results.UVX.Path = $uvxCommand.Source
    $results.UVX.Version = $uvxVersion
    
    Write-Host "✅ UVX está instalado" -ForegroundColor Green
    Write-Host "   Versão: $uvxVersion"
    Write-Host "   Caminho: $($uvxCommand.Source)"
}
catch {
    $results.UVX.Found = $false
    Write-Host "❌ UVX não está instalado ou não está no PATH" -ForegroundColor Red
    Write-Host "   Erro: $($_.Exception.Message)"
}

# Verificar PATH
Write-Header "Verificando variável PATH"
$envPath = $env:PATH
$pathValues = $envPath -split ";"

$results.PATH.Values = $pathValues

$nodeDir = if ($results.NodeJS.Path) {
    Split-Path -Parent $results.NodeJS.Path
}
else {
    $null
}

if ($nodeDir -and ($pathValues -contains $nodeDir)) {
    $results.PATH.ContainsNodePath = $true
    Write-Host "✅ Diretório do Node.js está no PATH" -ForegroundColor Green
}
elseif ($nodeDir) {
    $results.PATH.ContainsNodePath = $false
    Write-Host "❌ Diretório do Node.js não está no PATH" -ForegroundColor Red
    Write-Host "   Diretório do Node: $nodeDir"
}
else {
    $results.PATH.ContainsNodePath = $false
    Write-Host "❌ Não foi possível verificar diretório do Node.js no PATH" -ForegroundColor Red
}

# Testar executar um comando NPX diretamente
Write-Header "Testando comando NPX diretamente"
try {
    $tempDir = [System.IO.Path]::GetTempPath()
    $testOutput = Join-Path -Path $tempDir -ChildPath "npx-test-output.txt"
    
    # Tente executar um comando simples com npx
    & npx --version > $testOutput 2>&1
    $testResult = Get-Content $testOutput -Raw
    
    Write-Host "Resultado do teste NPX:"
    Write-Host $testResult
    
    # Limpar
    if (Test-Path $testOutput) { Remove-Item $testOutput -Force }
}
catch {
    Write-Host "❌ Erro ao testar NPX diretamente" -ForegroundColor Red
    Write-Host "   Erro: $($_.Exception.Message)"
}

# Resumo e diagnóstico
Write-Header "Diagnóstico e Recomendações"

if (-not $results.NodeJS.Installed) {
    Write-Host "❌ PROBLEMA: Node.js não está instalado ou não está no PATH" -ForegroundColor Red
    Write-Host "   SOLUÇÃO: Instale o Node.js da página oficial: https://nodejs.org/" -ForegroundColor Yellow
}
elseif (-not $results.NPX.Found) {
    Write-Host "❌ PROBLEMA: NPX não está disponível, mas Node.js está instalado" -ForegroundColor Red
    Write-Host "   SOLUÇÃO: Reinstale Node.js ou execute 'npm install -g npx'" -ForegroundColor Yellow
}
else {
    if (-not $results.NodeJS.Is64Bit -and $results.System.Is64BitOS) {
        Write-Host "⚠️ ATENÇÃO: Node.js 32-bit está instalado em um sistema 64-bit" -ForegroundColor Yellow
        Write-Host "   RECOMENDAÇÃO: Considere instalar a versão 64-bit do Node.js" -ForegroundColor Yellow
    }
    
    if ($results.MCPPackages.Missing.Count -gt 0) {
        Write-Host "⚠️ ATENÇÃO: Alguns pacotes MCP não estão instalados globalmente" -ForegroundColor Yellow
        Write-Host "   RECOMENDAÇÃO: Instale os pacotes globalmente com:" -ForegroundColor Yellow
        foreach ($pkg in $results.MCPPackages.Missing) {
            Write-Host "   npm install -g $pkg" -ForegroundColor Cyan
        }
    }
}

# Salvar resultados do diagnóstico
try {
    $logDir = Split-Path -Parent $diagnosticoPath
    if (-not (Test-Path $logDir)) {
        New-Item -Path $logDir -ItemType Directory -Force | Out-Null
    }
    
    $results | ConvertTo-Json -Depth 5 | Out-File -FilePath $diagnosticoPath -Force
    Write-Host "`n📊 Diagnóstico completo salvo em: $diagnosticoPath" -ForegroundColor Green
}
catch {
    Write-Host "`n❌ Não foi possível salvar o arquivo de diagnóstico" -ForegroundColor Red
    Write-Host "   Erro: $($_.Exception.Message)"
}

Write-Header "Conclusão"
Write-Host "Execute este diagnóstico com o comando: .\.scripts\diagnose-mcp-environment.ps1"
Write-Host "Consulte a documentação para resolver problemas específicos em docs\mcp-servers.md"
