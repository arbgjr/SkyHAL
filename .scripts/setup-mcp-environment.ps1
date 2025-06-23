# Script para configuração completa do ambiente MCP
# Este script verifica, instala e configura todo o ambiente necessário para os servidores MCP
# Criado em: 05/06/2025

Write-Host "🚀 Configuração Completa do Ambiente MCP" -ForegroundColor Cyan
Write-Host "=============================================" -ForegroundColor Cyan

# Definir caminhos
$workspacePath = $PSScriptRoot | Split-Path -Parent
$logPath = Join-Path -Path $workspacePath -ChildPath "logs"
$logFile = Join-Path -Path $logPath -ChildPath "mcp-setup-log.txt"

# Criar diretório de logs se não existir
if (-not (Test-Path $logPath)) {
    New-Item -Path $logPath -ItemType Directory -Force | Out-Null
}

# Função para registrar no arquivo de log
function Write-Log {
    param (
        [Parameter(Mandatory = $true)]
        [string]$Message,
        
        [Parameter(Mandatory = $false)]
        [ValidateSet("INFO", "AVISO", "ERRO", "SUCESSO")]
        [string]$Level = "INFO"
    )
    
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $logMessage = "$timestamp - $Level - $Message"
    Add-Content -Path $logFile -Value $logMessage
    
    # Também exibir no console com cores apropriadas
    switch ($Level) {
        "INFO" { Write-Host $Message -ForegroundColor Gray }
        "AVISO" { Write-Host $Message -ForegroundColor Yellow }
        "ERRO" { Write-Host $Message -ForegroundColor Red }
        "SUCESSO" { Write-Host $Message -ForegroundColor Green }
        default { Write-Host $Message }
    }
}

# Função para exibir cabeçalho
function Write-Header {
    param (
        [Parameter(Mandatory = $true)]
        [string]$Text
    )
    
    Write-Host "`n===== $Text =====" -ForegroundColor Cyan
    Write-Log "===== $Text ====="
}

# Função para executar etapas com controle de erro
function Invoke-SetupStep {
    param (
        [Parameter(Mandatory = $true)]
        [string]$StepName,
        
        [Parameter(Mandatory = $true)]
        [scriptblock]$ScriptBlock
    )
    
    Write-Header $StepName
    
    try {
        & $ScriptBlock
        return $true
    }
    catch {
        Write-Log "❌ Erro em '$StepName': $($_.Exception.Message)" "ERRO"
        return $false
    }
}

# Iniciar log
Write-Log "Iniciando configuração do ambiente MCP" "INFO"

# Etapa 1: Verificar Node.js
$nodeInstalled = Invoke-SetupStep "Verificar Node.js" {
    try {
        $nodeVersion = node -v
        Write-Log "✅ Node.js $nodeVersion está instalado" "SUCESSO"
        $true
    }
    catch {
        Write-Log "❌ Node.js não está instalado ou não está no PATH" "ERRO"
        Write-Log "🔧 Por favor, instale o Node.js da página oficial: https://nodejs.org/" "AVISO"
        Write-Log "🔍 Recomendada a versão LTS (64-bit) para melhor compatibilidade" "AVISO"
        $false
    }
}

if (-not $nodeInstalled) {
    $installNode = Read-Host "Deseja abrir a página de download do Node.js? (S/N)"
    if ($installNode -eq "S" -or $installNode -eq "s") {
        Start-Process "https://nodejs.org/en/download/"
        Write-Log "🌐 Página de download do Node.js aberta no navegador" "INFO"
        Write-Log "⚠️ Após instalar o Node.js, reinicie este script" "AVISO"
        exit
    }
    else {
        Write-Log "⚠️ Configuração não pode continuar sem Node.js" "AVISO"
        exit
    }
}

# Etapa 2: Verificar NPM e NPX
Invoke-SetupStep "Verificar NPM e NPX" {
    $npmVersion = npm -v
    Write-Log "✅ NPM $npmVersion está instalado" "SUCESSO"
    
    try {
        $npxVersion = npx --version
        Write-Log "✅ NPX $npxVersion está instalado" "SUCESSO"
    }
    catch {
        Write-Log "⚠️ NPX não está disponível. Tentando instalar..." "AVISO"
        npm install -g npx
        $npxVersion = npx --version
        Write-Log "✅ NPX $npxVersion foi instalado" "SUCESSO"
    }
}

# Etapa 3: Verificar ambiente Python/UVX
Invoke-SetupStep "Verificar Python e UVX" {
    try {
        $pythonVersion = python --version
        Write-Log "✅ Python está instalado: $pythonVersion" "SUCESSO"
    }
    catch {
        try {
            $pythonVersion = py --version
            Write-Log "✅ Python está instalado (py launcher): $pythonVersion" "SUCESSO"
        }
        catch {
            Write-Log "⚠️ Python não encontrado. Alguns servidores MCP podem não funcionar." "AVISO"
        }
    }
    
    try {
        $pipVersion = pip --version
        Write-Log "✅ PIP está instalado" "SUCESSO"
        
        try {
            $uvicornVersion = pip show uvicorn
            Write-Log "✅ Uvicorn está instalado" "SUCESSO"
        }
        catch {
            Write-Log "⚠️ Uvicorn não encontrado. Tentando instalar..." "AVISO"
            pip install uvicorn
            Write-Log "✅ Uvicorn instalado" "SUCESSO"
        }
        
        try {
            $uvxVersion = uvx --version
            Write-Log "✅ UVX está instalado: $uvxVersion" "SUCESSO"
        }
        catch {
            Write-Log "⚠️ UVX não encontrado. Alguns servidores MCP podem não funcionar." "AVISO"
        }
    }
    catch {
        Write-Log "⚠️ PIP não encontrado. Alguns servidores MCP podem não funcionar." "AVISO"
    }
}

# Etapa 4: Instalar pacotes MCP
Invoke-SetupStep "Instalar Pacotes MCP" {
    $mcpPackages = @(
        "@modelcontextprotocol/server-github",
        "@modelcontextprotocol/server-filesystem",
        "@modelcontextprotocol/server-memory",
        "@modelcontextprotocol/server-sequential-thinking",
        "@modelcontextprotocol/server-everything"
    )
    
    foreach ($pkg in $mcpPackages) {
        Write-Log "📦 Instalando $pkg globalmente..." "INFO"
        try {
            npm install -g $pkg
            Write-Log "✅ $pkg instalado com sucesso" "SUCESSO"
        }
        catch {
            Write-Log ("⚠️ Erro ao instalar " + $pkg + ": " + $_.Exception.Message) "AVISO"
        }
    }
}

# Etapa 5: Configurar arquivo MCP.json
Invoke-SetupStep "Configurar arquivo MCP.json" {
    $vscodePath = Join-Path -Path $workspacePath -ChildPath ".vscode"
    $mcpJsonPath = Join-Path -Path $vscodePath -ChildPath "mcp.json"
    
    if (-not (Test-Path $vscodePath)) {
        New-Item -Path $vscodePath -ItemType Directory -Force | Out-Null
    }
    
    if (Test-Path $mcpJsonPath) {
        Write-Log "✅ Arquivo MCP.json já existe" "SUCESSO"
    }
    else {
        $mcpJson = @{
            servers = @{
                github = @{
                    command = "npx"
                    args    = @("-y", "@modelcontextprotocol/server-github")
                    env     = @{
                        GITHUB_PERSONAL_ACCESS_TOKEN = '${input:github_token}'
                    }
                }
                filesystem = @{
                    command = "npx"
                    args    = @("-y", "@modelcontextprotocol/server-filesystem", '${workspaceFolder}')
                }
                git = @{
                    command = "uvx"
                    args    = @("mcp-server-git")
                }
                memory = @{
                    command = "npx"
                    args    = @("-y", "@modelcontextprotocol/server-memory")
                }
                sequentialthinking = @{
                    command = "npx"
                    args    = @("-y", "@modelcontextprotocol/server-sequential-thinking")
                }
                time = @{
                    command = "uvx"
                    args    = @("mcp-server-time", "--local-timezone", "America/Sao_Paulo")
                }
                everything = @{
                    command = "npx"
                    args    = @("-y", "@modelcontextprotocol/server-everything")
                }
            }
        }
        
        $mcpJson | ConvertTo-Json -Depth 4 | Out-File -FilePath $mcpJsonPath -Encoding UTF8
        Write-Log "✅ Arquivo MCP.json criado" "SUCESSO"
    }
}

# Etapa 6: Configurar tasks.json
Invoke-SetupStep "Configurar tasks.json" {
    $vscodePath = Join-Path -Path $workspacePath -ChildPath ".vscode"
    $tasksJsonPath = Join-Path -Path $vscodePath -ChildPath "tasks.json"
    
    if (-not (Test-Path $vscodePath)) {
        New-Item -Path $vscodePath -ItemType Directory -Force | Out-Null
    }
    
    $taskContent = $null
    if (Test-Path $tasksJsonPath) {
        $taskContent = Get-Content -Path $tasksJsonPath -Raw | ConvertFrom-Json
    }
    else {
        $taskContent = @{
            version = "2.0.0"
            tasks   = @()
        }
    }
    
    # Verificar se já existe uma task para iniciar servidores MCP
    $mcpTaskExists = $false
    foreach ($task in $taskContent.tasks) {
        if ($task.label -eq "Iniciar Servidores MCP") {
            $mcpTaskExists = $true
            break
        }
    }
    
    if (-not $mcpTaskExists) {
        $mcpTask = @{
            label         = "Iniciar Servidores MCP"
            type          = "shell"
            command       = "powershell"
            args          = @("-File", '${workspaceFolder}\.scripts\start-mcp-servers-fix.ps1')
            problemMatcher = @()
            presentation  = @{
                reveal = "always"
                panel  = "dedicated"
                focus  = $false
            }
            runOptions    = @{
                runOn = "folderOpen"
            }
        }
        
        $taskContent.tasks += $mcpTask
        $taskContent | ConvertTo-Json -Depth 4 | Out-File -FilePath $tasksJsonPath -Encoding UTF8
        Write-Log "✅ Task 'Iniciar Servidores MCP' adicionada ao tasks.json" "SUCESSO"
    }
    else {
        Write-Log "✅ Task 'Iniciar Servidores MCP' já existe em tasks.json" "SUCESSO"
    }
}

# Etapa 7: Configurar settings.json
Invoke-SetupStep "Configurar settings.json" {
    $vscodePath = Join-Path -Path $workspacePath -ChildPath ".vscode"
    $settingsJsonPath = Join-Path -Path $vscodePath -ChildPath "settings.json"
    
    if (-not (Test-Path $vscodePath)) {
        New-Item -Path $vscodePath -ItemType Directory -Force | Out-Null
    }
    
    $settingsContent = $null
    if (Test-Path $settingsJsonPath) {
        $settingsContent = Get-Content -Path $settingsJsonPath -Raw | ConvertFrom-Json
    }
    else {
        $settingsContent = [PSCustomObject]@{}
    }
    
    # Adicionar configuração para rodar task automaticamente
    try {
        $settingsContent | Add-Member -NotePropertyName "runOnStartupTasks" -NotePropertyValue @("Iniciar Servidores MCP") -ErrorAction SilentlyContinue
        $settingsContent | ConvertTo-Json -Depth 4 | Out-File -FilePath $settingsJsonPath -Encoding UTF8
        Write-Log "✅ Configuração 'runOnStartupTasks' adicionada/atualizada no settings.json" "SUCESSO"
    }
    catch {
        Write-Log "⚠️ Configuração 'runOnStartupTasks' já existe no settings.json" "AVISO"
    }
}

# Etapa 8: Executar diagnóstico final
Invoke-SetupStep "Diagnóstico Final do Ambiente" {
    $diagScriptPath = Join-Path -Path $workspacePath -ChildPath ".scripts\diagnose-mcp-environment.ps1"
    if (Test-Path $diagScriptPath) {
        Write-Log "🔍 Executando diagnóstico do ambiente MCP..." "INFO"
        & $diagScriptPath
    }
    else {
        Write-Log "⚠️ Script de diagnóstico não encontrado" "AVISO"
    }
}

# Etapa 9: Testar inicialização dos servidores
Invoke-SetupStep "Testar Inicialização dos Servidores MCP" {
    $startScriptPath = Join-Path -Path $workspacePath -ChildPath ".scripts\start-mcp-servers-fix.ps1"
    if (Test-Path $startScriptPath) {
        Write-Log "🚀 Testando inicialização dos servidores MCP..." "INFO"
        & $startScriptPath
    }
    else {
        Write-Log "⚠️ Script de inicialização não encontrado" "AVISO"
    }
}

# Mensagem final
Write-Header "Configuração Concluída"
Write-Log "✨ Configuração do ambiente MCP concluída!" "SUCESSO"
Write-Log "📋 Log completo disponível em: $logFile" "INFO"
Write-Log "📚 Documentação: docs\mcp-servers.md" "INFO"
Write-Log "" "INFO"
Write-Log "Comandos úteis:" "INFO"
Write-Log "  - Iniciar servidores MCP: .\.scripts\start-mcp-servers-fix.ps1" "INFO"
Write-Log "  - Parar servidores MCP: .\.scripts\stop-mcp-servers.ps1" "INFO"
Write-Log "  - Diagnóstico do ambiente: .\.scripts\diagnose-mcp-environment.ps1" "INFO"
Write-Log "" "INFO"
Write-Log "Reinicie o VS Code para que as mudanças sejam aplicadas completamente." "INFO"
