# Script para iniciar servidores MCP automaticamente
# Criado em: 05/06/2025
# Última modificação: 05/06/2025 - Adicionado suporte para caminhos absolutos de executáveis e verificação de ambiente

# Permitir que o script continue em caso de erro
$ErrorActionPreference = "Continue"

Clear-Host

Write-Host "🚀 Iniciando servidores MCP..." -ForegroundColor Cyan

# Adicionar DEBUG mode para mais detalhes
$DEBUG_MODE = $false
if ($args -contains "-debug" -or $args -contains "--debug") {
    $DEBUG_MODE = $true
    Write-Host "🔍 Modo DEBUG ativado" -ForegroundColor Yellow
}

# Função para verificar a existência dos pacotes MCP e instalar se necessário
function Ensure-MCPPackagesInstalled {
    param (
        [string[]]$Packages
    )
    
    Write-Host "🔍 Verificando pacotes MCP necessários..." -ForegroundColor Cyan
    
    $npm = Get-Command npm -ErrorAction SilentlyContinue
    if (-not $npm) {
        Write-Host "❌ NPM não encontrado no PATH. Verifique a instalação do Node.js." -ForegroundColor Red
        return $false
    }
    
    # Listar pacotes globais para verificar o que já está instalado
    $installedPackages = & npm list -g --depth=0 2>$null
    $packagesToInstall = @()
    
    foreach ($package in $Packages) {
        if ($installedPackages -notcontains $package) {
            $packagesToInstall += $package
        }
    }
    
    # Instalar pacotes faltantes
    if ($packagesToInstall.Count -gt 0) {
        Write-Host "📦 Instalando pacotes MCP faltantes: $($packagesToInstall -join ', ')" -ForegroundColor Yellow
        & npm install -g $packagesToInstall
        if ($LASTEXITCODE -ne 0) {
            Write-Host "❌ Falha ao instalar pacotes MCP. Verifique se você tem permissão para instalar pacotes globais." -ForegroundColor Red
            return $false
        }
        Write-Host "✅ Pacotes MCP instalados com sucesso!" -ForegroundColor Green
    }
    else {
        Write-Host "✅ Todos os pacotes MCP necessários já estão instalados." -ForegroundColor Green
    }
    
    return $true
}

# Função para verificar e corrigir permissões do Node.js
function Verify-NodePermissions {
    # Verificar se está rodando como administrador
    $isAdmin = ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
    
    if (-not $isAdmin) {
        Write-Host "⚠️ Este script não está sendo executado como administrador." -ForegroundColor Yellow
        Write-Host "   Algumas operações podem falhar por falta de permissões." -ForegroundColor Yellow
        Write-Host "   Considere reexecutar como administrador se encontrar problemas." -ForegroundColor Yellow
    }
    
    # Verificar permissões do diretório de pacotes NPM globais
    try {
        $npmPrefix = & npm config get prefix
        $npmNodeModules = Join-Path -Path $npmPrefix -ChildPath "node_modules"
        
        if (Test-Path $npmNodeModules) {
            $acl = Get-Acl $npmNodeModules
            $currentUser = [System.Security.Principal.WindowsIdentity]::GetCurrent().Name
            
            $hasWriteAccess = $acl.Access | Where-Object { 
                $_.IdentityReference.Value -eq $currentUser -and 
                ($_.FileSystemRights -band [System.Security.AccessControl.FileSystemRights]::Write)
            }
            
            if (-not $hasWriteAccess) {
                Write-Host "⚠️ O usuário atual não tem permissões de escrita para $npmNodeModules" -ForegroundColor Yellow
                
                if ($isAdmin) {
                    Write-Host "   Tentando corrigir permissões..." -ForegroundColor Cyan
                    $rule = New-Object System.Security.AccessControl.FileSystemAccessRule(
                        $currentUser,
                        "FullControl",
                        "ContainerInherit,ObjectInherit",
                        "None",
                        "Allow"
                    )
                    $acl.AddAccessRule($rule)
                    Set-Acl -Path $npmNodeModules -AclObject $acl
                    Write-Host "✅ Permissões corrigidas!" -ForegroundColor Green
                }
                else {
                    Write-Host "   Execute este script como administrador para corrigir as permissões." -ForegroundColor Yellow
                }
            }
            else {
                Write-Host "✅ Permissões de NPM corretas." -ForegroundColor Green
            }
        }
    }
    catch {
        Write-Host "⚠️ Não foi possível verificar permissões do NPM: $_" -ForegroundColor Yellow
    }
}

# Determinar o caminho do workspace
$workspacePath = $PSScriptRoot | Split-Path -Parent
$mcpConfigPath = Join-Path -Path $workspacePath -ChildPath ".vscode\mcp.json"
$logPath = Join-Path -Path $workspacePath -ChildPath "logs"
$logFile = Join-Path -Path $logPath -ChildPath "mcp-servers-log.txt"
$diagnosticoPath = Join-Path -Path $logPath -ChildPath "mcp-diagnostico.json"

# Criar diretório de logs se não existir
if (-not (Test-Path $logPath)) {
    New-Item -Path $logPath -ItemType Directory -Force | Out-Null
}

if (-not (Test-Path $mcpConfigPath)) {
    $errorMessage = "❌ Arquivo de configuração MCP não encontrado: $mcpConfigPath"
    Write-Host $errorMessage -ForegroundColor Red
    Add-Content -Path $logFile -Value "$(Get-Date) - ERRO: $errorMessage"
    exit 1
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

# Limpar o arquivo de log se estiver muito grande (>1MB)
if ((Test-Path $logFile) -and ((Get-Item $logFile).Length -gt 1MB)) {
    $backupLog = "$logFile.bak"
    if (Test-Path $backupLog) { Remove-Item $backupLog -Force }
    Move-Item $logFile $backupLog -Force
}

Write-Log "Iniciando servidores MCP..." "INFO"

# Verificar e corrigir permissões do Node.js
Verify-NodePermissions

# Extrair nomes de pacotes MCP do arquivo de configuração
$mcpPackages = @()
try {
    $mcpConfig = Get-Content $mcpConfigPath -Raw | ConvertFrom-Json
    foreach ($server in $mcpConfig.servers.PSObject.Properties) {
        $serverConfig = $server.Value
        # Verificar se o comando é npx e extrair nomes de pacotes
        if ($serverConfig.command -eq "npx") {
            $args = $serverConfig.args
            # Ignorar -y ou outros flags
            $packageArgs = $args | Where-Object { -not $_.StartsWith("-") }
            if ($packageArgs.Count -gt 0) {
                foreach ($arg in $packageArgs) {
                    if ($arg -match '^@') {
                        $mcpPackages += $arg
                    }
                }
            }
        }
    }
    
    # Remover duplicatas
    $mcpPackages = $mcpPackages | Select-Object -Unique
    
    # Garantir que os pacotes estão instalados
    if ($mcpPackages.Count -gt 0) {
        Write-Log "📦 Encontrados $($mcpPackages.Count) pacotes MCP necessários: $($mcpPackages -join ', ')" "INFO"
        Ensure-MCPPackagesInstalled -Packages $mcpPackages
    }
}
catch {
    $errorMessage = $_.Exception.Message
    Write-Log "⚠️ Erro ao verificar pacotes MCP: $errorMessage" "AVISO"
}

# Criar diretório global para npm/npx se não existir
$npmGlobalDir = Join-Path $env:APPDATA "npm"
if (-not (Test-Path $npmGlobalDir)) {
    try {
        New-Item -Path $npmGlobalDir -ItemType Directory -Force | Out-Null
        Write-Log "✅ Criado diretório global do NPM em $npmGlobalDir" "SUCESSO"
    }
    catch {
        Write-Log "⚠️ Não foi possível criar diretório global do NPM: $_" "AVISO"
    }
}

# Verificar instalação do Node.js e comandos relacionados
$nodeInstalled = $false
$nodePath = ""
$npxPath = ""
$uvxPath = ""

try {
    $nodeCommand = Get-Command node -ErrorAction SilentlyContinue
    if ($nodeCommand) {
        $nodeInstalled = $true
        $nodePath = $nodeCommand.Source
        $nodeVersion = & node -v
        Write-Log "✅ Node.js $nodeVersion encontrado: $nodePath" "SUCESSO"
    }
    else {
        Write-Log "⚠️ Node.js não encontrado no PATH!" "AVISO"
        
        # Tentar localizar node em diretórios comuns
        $potentialNodePaths = @(
            "C:\Program Files\nodejs\node.exe",
            "C:\Program Files (x86)\nodejs\node.exe",
            "${env:APPDATA}\nvm\*\node.exe"
        )
        
        foreach ($path in $potentialNodePaths) {
            if (Test-Path $path) {
                $nodePath = $path
                $nodeInstalled = $true
                $nodeVersion = & $nodePath -v
                Write-Log "✅ Node.js $nodeVersion encontrado em: $nodePath" "SUCESSO"
                break
            }
        }
        
        if (-not $nodeInstalled) {
            Write-Log "❌ Node.js não encontrado. Os servidores MCP podem falhar." "ERRO"
        }
    }
    
    # Preferir usar npm diretamente com node para evitar problemas com npx
    $npmCommand = Get-Command npm -ErrorAction SilentlyContinue
    $npmPath = ""
    if ($npmCommand) {
        $npmPath = $npmCommand.Source
        $npmVersion = & npm -v
        Write-Log "✅ NPM $npmVersion encontrado: $npmPath" "SUCESSO"
    }
    
    # Configurar npx diretamente como node + npx.js para evitar problemas do Win32
    $npxCommand = Get-Command npx -ErrorAction SilentlyContinue
    if ($npxCommand) {
        $npxPath = $npxCommand.Source
        
        # Verificar se é um arquivo .ps1 ou .cmd que pode causar problemas Win32
        if ($npxPath -match '\.(ps1|cmd)$') {
            # Substituir por chamada direta a node + caminho para npx.js
            $npmRoot = & npm root -g
            $npxJsPath = Join-Path -Path $npmRoot -ChildPath "npm\bin\npx-cli.js"
            
            if (Test-Path $npxJsPath) {
                Write-Log "✅ NPX encontrado em: $npxPath (usando node + npx-cli.js)" "SUCESSO"
                # Usar o caminho direto para npx-cli.js
                $npxPath = "node"  # Vamos chamar node diretamente
                $GLOBAL:npxJsFullPath = $npxJsPath  # Salvar para uso posterior
            }
            else {
                # Tentar localizar npx-cli.js
                $npxCliPaths = @(
                    (Join-Path -Path (Split-Path -Parent $npmPath | Split-Path -Parent) -ChildPath "node_modules\npm\bin\npx-cli.js"),
                    "C:\Program Files\nodejs\node_modules\npm\bin\npx-cli.js",
                    "${env:APPDATA}\npm\node_modules\npm\bin\npx-cli.js"
                )
                
                foreach ($path in $npxCliPaths) {
                    if (Test-Path $path) {
                        $GLOBAL:npxJsFullPath = $path
                        Write-Log "✅ NPX encontrado em: $path (usando node + npx-cli.js)" "SUCESSO"
                        $npxPath = "node"  # Vamos chamar node diretamente
                        break
                    }
                }
            }
        }
        else {
            Write-Log "✅ NPX encontrado: $npxPath" "SUCESSO"
        }
    }
    else {
        Write-Log "⚠️ NPX não encontrado no PATH!" "AVISO"
        
        # Tentar localizar npx em diretórios comuns
        $potentialNPXPaths = @(
            (Join-Path -Path $env:APPDATA -ChildPath "npm\npx.cmd"),
            (Join-Path -Path (Split-Path -Parent $nodePath) -ChildPath "npx.cmd"),
            (Join-Path -Path $env:ProgramFiles -ChildPath "nodejs\npx.cmd"),
            (Join-Path -Path ${env:ProgramFiles(x86)} -ChildPath "nodejs\npx.cmd")
        )
        
        foreach ($path in $potentialNPXPaths) {
            if (Test-Path $path) {
                $npxPath = $path
                Write-Log "✅ NPX encontrado em caminho alternativo: $npxPath" "SUCESSO"
                break
            }
        }
        
        if (-not $npxPath) {
            # Buscar em pastas no PATH
            $pathFolders = $env:PATH -split ";"
            foreach ($folder in $pathFolders) {
                $potentialPath = Join-Path -Path $folder -ChildPath "npx.cmd"
                if (Test-Path $potentialPath) {
                    $npxPath = $potentialPath
                    Write-Log "✅ NPX encontrado no PATH: $npxPath" "SUCESSO"
                    break
                }
            }
        }
        
        if (-not $npxPath) {
            Write-Log "❌ NPX não encontrado em nenhum local comum" "ERRO"
        }
    }
    
    $uvxCommand = Get-Command uvx -ErrorAction SilentlyContinue
    if ($uvxCommand) {
        $uvxPath = $uvxCommand.Source
        Write-Log "✅ UVX encontrado: $uvxPath" "SUCESSO"
    }
    else {
        Write-Log "⚠️ UVX não encontrado no PATH!" "AVISO"
        
        # Tentar buscar UVX em pastas no PATH
        $pathFolders = $env:PATH -split ";"
        foreach ($folder in $pathFolders) {
            $potentialPath = Join-Path -Path $folder -ChildPath "uvx.cmd"
            if (Test-Path $potentialPath) {
                $uvxPath = $potentialPath
                Write-Log "✅ UVX encontrado no PATH: $uvxPath" "SUCESSO"
                break
            }
        }
        
        if (-not $uvxPath) {
            Write-Log "⚠️ UVX não encontrado! Servidores que dependem dele podem falhar" "AVISO"
        }
    }
    
}
catch {
    $errorMessage = $_.Exception.Message
    Write-Log "❌ Erro ao verificar ambiente Node.js: $errorMessage" "ERRO"
}

# Carregar configuração
try {
    $mcpConfig = Get-Content $mcpConfigPath -Raw | ConvertFrom-Json

    # Verificar servidores configurados
    $serverCount = ($mcpConfig.servers.PSObject.Properties | Measure-Object).Count
    Write-Log "📋 $serverCount servidores MCP encontrados na configuração" "INFO"
    
    # Inicializar array para rastrear falhas
    $failedServers = @()
    $successCount = 0
    # Função para obter o caminho absoluto do executável
    function Get-ExecutablePath {
        param (
            [string]$Command
        )
        
        switch ($Command) {
            "npx" { return $npxPath }
            "uvx" { return $uvxPath }
            "npm" { return $npmPath }
            default {
                $cmdPath = (Get-Command $Command -ErrorAction SilentlyContinue).Source
                return $cmdPath
            }
        }
    }

    # Iniciar cada servidor configurado
    foreach ($server in $mcpConfig.servers.PSObject.Properties) {
        $serverName = $server.Name
        $serverConfig = $server.Value
        $commandName = $serverConfig.command
        $serverArgs = $serverConfig.args -join " "
        
        # Obter caminho absoluto do executável
        $executablePath = Get-ExecutablePath -Command $commandName
        
        Write-Log "📡 Iniciando servidor MCP: $serverName" "INFO"
        
        if (-not $executablePath) {
            $errorMsg = "Executável '$commandName' não encontrado no sistema"
            $failedServers += @{
                Name      = $serverName
                Error     = $errorMsg
                Command   = $commandName
                Args      = $serverArgs
                Timestamp = Get-Date
            }
            
            Write-Log "❌ Falha ao iniciar servidor $serverName - Executável não encontrado" "ERRO"
            continue
        }
        
        Write-Log "   Comando: $executablePath $serverArgs" "INFO"
        
        # Substituir variáveis no comando
        $serverArgs = $serverArgs.Replace('${workspaceFolder}', $workspacePath)
        try {
            # Verificar se estamos usando npx e se temos o caminho do npx-cli.js
            if ($commandName -eq "npx" -and $executablePath -eq "node" -and $GLOBAL:npxJsFullPath) {
                # Montar os argumentos usando o caminho para npx-cli.js
                $fullArgs = @($GLOBAL:npxJsFullPath) + $serverArgs.Split(" ")
                Write-Log "   Usando node + npx-cli.js com: $executablePath $($fullArgs -join ' ')" "INFO"
                
                # Iniciar processo com caminho absoluto para node + npx-cli.js
                $process = Start-Process -FilePath $executablePath -ArgumentList $fullArgs -NoNewWindow -PassThru
            }
            # Alternativa: usar npm exec se npx falhar
            elseif ($commandName -eq "npx" -and (-not $executablePath -eq "node")) {
                # Tentar usar npm exec como alternativa
                $npmPath = Get-ExecutablePath -Command "npm"
                if ($npmPath) {
                    Write-Log "   Tentando npm exec como alternativa a npx..." "INFO"
                    $npmArgs = @("exec", "--") + $serverArgs.Split(" ")
                    $process = Start-Process -FilePath $npmPath -ArgumentList $npmArgs -NoNewWindow -PassThru
                }
                else {
                    # Tentar usar o comando npx diretamente como último recurso
                    $process = Start-Process -FilePath $executablePath -ArgumentList $serverArgs -NoNewWindow -PassThru
                }
            }
            else {
                # Iniciar processo com caminho absoluto normalmente
                $process = Start-Process -FilePath $executablePath -ArgumentList $serverArgs -NoNewWindow -PassThru
            }
            
            # Esperar um pouco para verificar se o processo está em execução
            Start-Sleep -Milliseconds 1000
            
            # Verificar se o processo ainda está em execução
            if ($process.HasExited) {
                throw "O processo foi iniciado mas encerrou imediatamente com código de saída $($process.ExitCode)"
            }
            
            $successCount++
            Write-Log "✅ Servidor $serverName iniciado com sucesso (PID: $($process.Id))" "SUCESSO"
        }
        catch {
            $errorMessage = $_.Exception.Message
            $failedServers += @{
                Name      = $serverName
                Error     = $errorMessage
                Command   = $executablePath
                Args      = $serverArgs
                Timestamp = Get-Date
            }
            
            Write-Log "❌ Falha ao iniciar servidor $serverName - Erro: $errorMessage" "ERRO"
        }
        
        # Aguardar um pouco para evitar sobrecarga
        Start-Sleep -Milliseconds 500
    }

    # Relatório final
    if ($successCount -eq $serverCount) {
        Write-Log "✅ Todos os $serverCount servidores MCP iniciados com sucesso!" "SUCESSO"
    }
    else {
        $failedCount = $failedServers.Count
        Write-Log "⚠️ $successCount de $serverCount servidores iniciados. $failedCount servidores falharam." "AVISO"
        # Relatório detalhado de falhas
        Write-Log "📄 Detalhes dos servidores com falha:" "AVISO"
        foreach ($failed in $failedServers) {
            Write-Log "   - $($failed.Name) - Erro: $($failed.Error)" "ERRO"
        }
        
        Write-Log "👉 Execute o script de diagnóstico para mais detalhes: .\.scripts\diagnose-mcp-environment.ps1" "AVISO"
    }
}
catch {
    $errorMessage = $_.Exception.Message
    Write-Log "❌ Erro geral ao iniciar servidores MCP - Erro: $errorMessage" "ERRO"
}
    
# Gerar arquivo de resumo
try {
    $summaryFile = Join-Path -Path $logPath -ChildPath "mcp-servers-status.json"
    $summary = @{
        Timestamp     = Get-Date
        TotalServers  = $serverCount
        SuccessCount  = $successCount
        FailedCount   = $failedServers.Count
        FailedServers = $failedServers
        Environment   = @{
            NodeInstalled = $nodeInstalled
            NodePath      = $nodePath
            NPXPath       = $npxPath
            UVXPath       = $uvxPath
        }
    }

    $summary | ConvertTo-Json -Depth 3 | Out-File -FilePath $summaryFile -Force
    Write-Log "📊 Relatório de status salvo em $summaryFile" "INFO"
}
catch {
    $errorMessage = $_.Exception.Message
    Write-Log "⚠️ Não foi possível salvar o relatório de status - Erro: $errorMessage" "AVISO"
}

# Tentar corrigir problemas conhecidos se houver falhas
if ($failedServers.Count -gt 0) {
    Write-Host "`n⚠️ Detectadas falhas em servidores. Tentando resolver automaticamente..." -ForegroundColor Yellow

    # Verificar padrões comuns nos erros
    $hasWin32AppError = $failedServers | Where-Object { $_.Error -like "*not a valid Win32 application*" } | Measure-Object
    $hasNotFoundError = $failedServers | Where-Object { $_.Error -like "*not found*" -or $_.Error -like "*não encontrado*" } | Measure-Object

    if ($hasWin32AppError.Count -gt 0) {
        Write-Host "   🔍 Erro 'not a valid Win32 application' detectado - tentando corrigir..." -ForegroundColor Yellow

        # Corrigir problema Win32 tentando reinstalar os pacotes sem usar .cmd/.ps1
        $packagesToReinstall = $failedServers | Where-Object { $_.Error -like "*not a valid Win32 application*" } | ForEach-Object {
            $serverName = $_.Name
            $serverConfig = $mcpConfig.servers.$serverName
            if ($serverConfig.command -eq "npx" -and $serverConfig.args.Count -gt 0) {
                # Extrair nome do pacote (remover -y e outros flags)
                $packageArgs = $serverConfig.args | Where-Object { -not $_.StartsWith("-") }
                if ($packageArgs.Count -gt 0) {
                    $packageArgs[0]  # Retornar o primeiro argumento não-flag que deve ser o pacote
                }
            }
        } | Select-Object -Unique
    
        if ($packagesToReinstall.Count -gt 0) {
            # Limpar cache do npm
            Write-Host "   🧹 Limpando cache do NPM..." -ForegroundColor Yellow
            & npm cache clean --force
    
            # Reinstalar pacotes
            Write-Host "   📦 Reinstalando pacotes MCP: $($packagesToReinstall -join ', ')" -ForegroundColor Yellow
            & npm install -g $packagesToReinstall
    
            Write-Host "   ✅ Reinstalação concluída. Tente executar o script novamente." -ForegroundColor Green
        }
    }

    # Exibir sugestões para resolução de problemas
    Write-Host "`n⚠️ SUGESTÕES PARA RESOLVER PROBLEMAS:" -ForegroundColor Yellow

    if ($hasWin32AppError.Count -gt 0) {
        Write-Host "   🔍 Erro 'not a valid Win32 application' detectado:" -ForegroundColor Yellow
        Write-Host "      1. Execute o comando: npm install -g npx" -ForegroundColor White
        Write-Host "      2. Reinstale o Node.js (versão LTS recomendada)" -ForegroundColor White
        Write-Host "      3. Execute 'npm cache clean --force' e reinstale os pacotes MCP" -ForegroundColor White
        Write-Host "      4. Execute este script como administrador" -ForegroundColor White
    }

    if ($hasNotFoundError.Count -gt 0) {
        Write-Host "   🔍 Erro 'not found' detectado:" -ForegroundColor Yellow
        Write-Host "      1. Instale os pacotes MCP globalmente com 'npm install -g @modelcontextprotocol/server-xxx'" -ForegroundColor White
        Write-Host "      2. Verifique se o NODE_PATH está configurado corretamente" -ForegroundColor White
    }

    Write-Host "   💡 Consulte a documentação em docs\mcp-servers.md para mais detalhes"
    Write-Host "   🔧 Execute o diagnóstico completo: .\.scripts\diagnose-mcp-environment.ps1"
    Write-Host "   🚀 Tente executar o script como administrador: Start-Process powershell -Verb RunAs -ArgumentList '-File .\.scripts\start-mcp-servers.ps1'" -ForegroundColor Cyan
}

Write-Host "`n✅ Script finalizado!" -ForegroundColor Green
 