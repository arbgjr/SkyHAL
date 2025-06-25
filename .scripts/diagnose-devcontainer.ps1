# Script de diagnóstico para DevContainer
# Autor: GitHub Copilot
# Data: 24/06/2025
# Descrição: Ferramenta para diagnóstico e resolução de problemas comuns com DevContainer

# Função para exibir mensagens coloridas
function Write-ColorOutput {
    param (
        [Parameter(Mandatory = $true)]
        [string]$Message,

        [Parameter(Mandatory = $false)]
        [string]$ForegroundColor = "White"
    )

    $originalColor = $host.UI.RawUI.ForegroundColor
    $host.UI.RawUI.ForegroundColor = $ForegroundColor
    Write-Output $Message
    $host.UI.RawUI.ForegroundColor = $originalColor
}

function Write-Header {
    param (
        [Parameter(Mandatory = $true)]
        [string]$Title
    )

    Write-ColorOutput "`n===== $Title =====" -ForegroundColor "Cyan"
}

function Write-Success {
    param (
        [Parameter(Mandatory = $true)]
        [string]$Message
    )

    Write-ColorOutput "[✓] $Message" -ForegroundColor "Green"
}

function Write-Warning {
    param (
        [Parameter(Mandatory = $true)]
        [string]$Message
    )

    Write-ColorOutput "[!] $Message" -ForegroundColor "Yellow"
}

function Write-Error {
    param (
        [Parameter(Mandatory = $true)]
        [string]$Message
    )

    Write-ColorOutput "[✗] $Message" -ForegroundColor "Red"
}

function Test-Command {
    param (
        [Parameter(Mandatory = $true)]
        [string]$Command
    )

    try {
        Invoke-Expression $Command | Out-Null
        return $true
    } catch {
        return $false
    }
}

# Verificar se estamos no Windows
$isWindows = $env:OS -match "Windows"

Write-Header "Diagnóstico de DevContainer SkyHAL"
Write-ColorOutput "Sistema: $($isWindows ? 'Windows' : 'Linux/macOS')"
Write-ColorOutput "Data: $(Get-Date)`n"

# Verificar WSL (somente Windows)
if ($isWindows) {
    Write-Header "Verificação do WSL"

    $wslEnabled = Test-Command "wsl --status"
    if ($wslEnabled) {
        $wslVersion = (wsl --status | Select-String -Pattern "Default Version:") -replace "Default Version: ", ""
        Write-Success "WSL instalado. Versão padrão: $wslVersion"

        $defaultDistro = (wsl --status | Select-String -Pattern "Default Distribution:") -replace "Default Distribution: ", ""
        Write-Success "Distribuição padrão: $defaultDistro"
    } else {
        Write-Error "WSL não está instalado ou não pode ser encontrado"
        Write-ColorOutput "Para instalar o WSL, execute o seguinte comando em um PowerShell com privilégios administrativos:"
        Write-ColorOutput "    wsl --install" -ForegroundColor "Cyan"
    }
}

# Verificar Docker
Write-Header "Verificação do Docker"

$dockerInstalled = Test-Command "docker --version"
if ($dockerInstalled) {
    $dockerVersion = (docker --version)
    Write-Success "Docker instalado: $dockerVersion"

    # Verificar se o Docker está em execução
    $dockerRunning = Test-Command "docker info"
    if ($dockerRunning) {
        Write-Success "Docker está em execução"
    } else {
        Write-Error "Docker não está em execução"
        if ($isWindows) {
            Write-ColorOutput "Verifique se o Docker Desktop está iniciado"
        } else {
            Write-ColorOutput "Inicie o Docker com: sudo systemctl start docker"
        }
    }
} else {
    Write-Error "Docker não está instalado ou não está no PATH"
    if ($isWindows) {
        Write-ColorOutput "Instale o Docker Desktop em: https://www.docker.com/products/docker-desktop/"
    } else {
        Write-ColorOutput "Instale o Docker com: sudo apt-get install docker.io"
    }
}

# Verificar VS Code e extensões
Write-Header "Verificação do VS Code"

$codeInstalled = Test-Command "code --version"
if ($codeInstalled) {
    $codeVersion = (code --version | Select-Object -First 1)
    Write-Success "VS Code instalado: $codeVersion"

    # Verificar extensão Dev Containers
    $extensionInstalled = Test-Command "code --list-extensions | Select-String -Pattern ms-vscode-remote.remote-containers"
    if ($extensionInstalled) {
        Write-Success "Extensão Dev Containers instalada"
    } else {
        Write-Warning "Extensão Dev Containers não instalada"
        Write-ColorOutput "Instale a extensão com: code --install-extension ms-vscode-remote.remote-containers"
    }
} else {
    Write-Warning "VS Code não está instalado ou não está no PATH"
    Write-ColorOutput "Instale o VS Code em: https://code.visualstudio.com/download"
}

# Verificar arquivo .devcontainer/devcontainer.json
Write-Header "Verificação dos Arquivos de Configuração"

$devcontainerPath = Join-Path (Get-Location) ".devcontainer/devcontainer.json"
if (Test-Path $devcontainerPath) {
    Write-Success "Arquivo devcontainer.json encontrado"

    # Verificar conteúdo do arquivo
    try {
        $devcontainerContent = Get-Content $devcontainerPath -Raw | ConvertFrom-Json
        Write-Success "Arquivo devcontainer.json é um JSON válido"

        # Verificar campos obrigatórios
        if ($devcontainerContent.image) {
            Write-Success "Imagem base configurada: $($devcontainerContent.image)"
        } else {
            Write-Warning "Campo 'image' não encontrado no devcontainer.json"
        }
    } catch {
        Write-Error "Erro ao analisar devcontainer.json: $_"
    }
} else {
    Write-Error "Arquivo devcontainer.json não encontrado"
    Write-ColorOutput "Certifique-se de estar no diretório raiz do projeto"
}

# Verificar se o diretório .ssh existe
Write-Header "Verificação do Diretório SSH"

$sshPath = ""
if ($isWindows) {
    $sshPath = Join-Path $env:USERPROFILE ".ssh"
} else {
    $sshPath = Join-Path $env:HOME ".ssh"
}

if (Test-Path $sshPath) {
    Write-Success "Diretório .ssh encontrado em: $sshPath"
} else {
    Write-Warning "Diretório .ssh não encontrado"
    Write-ColorOutput "Para criar o diretório .ssh, execute:"
    if ($isWindows) {
        Write-ColorOutput "    New-Item -Path $sshPath -ItemType Directory" -ForegroundColor "Cyan"
    } else {
        Write-ColorOutput "    mkdir -p ~/.ssh && chmod 700 ~/.ssh" -ForegroundColor "Cyan"
    }
}

# Sugestões de correção
Write-Header "Recomendações e Próximos Passos"

if ($isWindows -and -not $wslEnabled) {
    Write-ColorOutput "1. Instale e configure o WSL 2" -ForegroundColor "Yellow"
}

if (-not $dockerInstalled -or -not $dockerRunning) {
    Write-ColorOutput "2. Instale e inicie o Docker" -ForegroundColor "Yellow"
}

if (-not $codeInstalled -or -not $extensionInstalled) {
    Write-ColorOutput "3. Instale o VS Code e a extensão Dev Containers" -ForegroundColor "Yellow"
}

if (-not (Test-Path $sshPath)) {
    Write-ColorOutput "4. Configure o diretório SSH" -ForegroundColor "Yellow"
}

Write-ColorOutput "`nPara mais informações, consulte: docs/devcontainer-setup.md" -ForegroundColor "Cyan"
Write-ColorOutput "Se os problemas persistirem, abra uma issue no GitHub."

# Instruções para reconstrução do container
Write-Header "Reconstrução do Container"

Write-ColorOutput "Se precisar reconstruir o DevContainer:"
Write-ColorOutput "1. No VS Code, pressione Ctrl+Shift+P" -ForegroundColor "Cyan"
Write-ColorOutput "2. Digite 'Remote-Containers: Rebuild Container'" -ForegroundColor "Cyan"
Write-ColorOutput "3. Aguarde a reconstrução completa do container" -ForegroundColor "Cyan"

Write-Header "Diagnóstico Concluído"
