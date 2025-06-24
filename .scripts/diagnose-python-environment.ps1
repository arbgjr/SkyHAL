#!/usr/bin/env pwsh

# Configuração de encoding para UTF-8
$OutputEncoding = [System.Text.Encoding]::UTF8
[System.Console]::OutputEncoding = [System.Text.Encoding]::UTF8

# Função para verificar se um comando existe
function Test-Command {
    param($Command)
    return [bool](Get-Command -Name $Command -ErrorAction SilentlyContinue)
}

# Função para log colorido
function Write-Log {
    param(
        [Parameter(Mandatory=$true)]
        [string]$Message,
        [string]$Type = "INFO"
    )
    $color = switch ($Type) {
        "ERROR" { "Red" }
        "SUCCESS" { "Green" }
        "WARN" { "Yellow" }
        "CHECK" { "Magenta" }
        default { "Cyan" }
    }
    Write-Host "$(Get-Date -Format "yyyy-MM-dd HH:mm:ss") [$Type] $Message" -ForegroundColor $color
}

# Função para verificar versão do Python
function Test-PythonVersion {
    if (-not (Test-Command "python")) {
        Write-Log "❌ Python não encontrado." "ERROR"
        return $false
    }

    $pythonVersion = python -c "import sys; print('.'.join(map(str, sys.version_info[:2])))"
    Write-Log "Python versão: $pythonVersion" "INFO"

    if ([version]$pythonVersion -lt [version]"3.11") {
        Write-Log "❌ Python 3.11 ou superior é necessário." "ERROR"
        return $false
    }
    return $true
}

# Função para verificar Poetry
function Test-Poetry {
    if (-not (Test-Command "poetry")) {
        Write-Log "❌ Poetry não encontrado." "ERROR"
        return $false
    }

    $poetryVersion = poetry --version
    Write-Log "Poetry versão: $poetryVersion" "INFO"
    return $true
}

# Função para verificar ambiente virtual
function Test-VirtualEnv {
    if (-not (Test-Path ".venv")) {
        Write-Log "❌ Ambiente virtual não encontrado (.venv/)" "ERROR"
        return $false
    }

    if (-not (Test-Path "poetry.lock")) {
        Write-Log "❌ poetry.lock não encontrado" "ERROR"
        return $false
    }

    Write-Log "✅ Ambiente virtual configurado" "SUCCESS"
    return $true
}

# Função para verificar ferramentas de qualidade
function Test-QualityTools {
    $tools = @(
        @{Name="black"; Desc="Formatador"},
        @{Name="ruff"; Desc="Linter"},
        @{Name="mypy"; Desc="Verificador de tipos"},
        @{Name="pytest"; Desc="Framework de testes"},
        @{Name="bandit"; Desc="Análise de segurança"}
    )

    $allOk = $true
    foreach ($tool in $tools) {
        if (poetry run $tool.Name --version 2>$null) {
            Write-Log "✅ $($tool.Name) instalado ($($tool.Desc))" "SUCCESS"
        }
        else {
            Write-Log "❌ $($tool.Name) não encontrado ($($tool.Desc))" "ERROR"
            $allOk = $false
        }
    }
    return $allOk
}

# Função para verificar pre-commit
function Test-PreCommit {
    if (-not (Test-Path ".git/hooks/pre-commit")) {
        Write-Log "❌ pre-commit hooks não instalados" "ERROR"
        return $false
    }

    Write-Log "✅ pre-commit hooks configurados" "SUCCESS"
    return $true
}

# Função para testar configuração do VS Code
function Test-VSCode {
    $requiredExtensions = @(
        "ms-python.python",
        "ms-python.vscode-pylance",
        "ms-python.black-formatter",
        "charliermarsh.ruff"
    )

    $allOk = $true
    foreach ($ext in $requiredExtensions) {
        $result = code --list-extensions | Select-String -Pattern $ext -Quiet
        if ($result) {
            Write-Log "✅ Extensão VS Code instalada: $ext" "SUCCESS"
        }
        else {
            Write-Log "❌ Extensão VS Code faltando: $ext" "ERROR"
            $allOk = $false
        }
    }
    return $allOk
}

# Cabeçalho
Write-Log "🔍 Iniciando diagnóstico do ambiente Python..." "INFO"
Write-Log "=================================================" "INFO"

# Execute todas as verificações
$checks = @(
    @{Name="Python 3.11+"; Function={Test-PythonVersion}},
    @{Name="Poetry"; Function={Test-Poetry}},
    @{Name="Ambiente Virtual"; Function={Test-VirtualEnv}},
    @{Name="Ferramentas de Qualidade"; Function={Test-QualityTools}},
    @{Name="Pre-commit"; Function={Test-PreCommit}},
    @{Name="VS Code"; Function={Test-VSCode}}
)

$results = @()
foreach ($check in $checks) {
    Write-Log "`nVerificando $($check.Name)..." "CHECK"
    $success = & $check.Function
    $results += @{
        Name = $check.Name
        Success = $success
    }
}

# Resumo
Write-Log "`n=================================================" "INFO"
Write-Log "📊 Resumo do Diagnóstico:" "INFO"
Write-Log "=================================================" "INFO"

$totalChecks = $checks.Count
$passedChecks = ($results | Where-Object { $_.Success -eq $true }).Count

foreach ($result in $results) {
    $status = if ($result.Success) { "✅" } else { "❌" }
    Write-Log "$status $($result.Name)" $(if ($result.Success) { "SUCCESS" } else { "ERROR" })
}

Write-Log "`nResultado Final: $passedChecks/$totalChecks verificações passaram" "INFO"

if ($passedChecks -eq $totalChecks) {
    Write-Log "🎉 O ambiente está completamente configurado!" "SUCCESS"
} else {
    Write-Log "⚠️ Algumas verificações falharam. Execute .scripts\install-mcp-packages.ps1 para corrigir." "WARN"
}
