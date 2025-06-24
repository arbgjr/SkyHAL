<#
Testes automatizados para validação dos scripts de onboarding do SkyHAL.
Executa os scripts principais e valida saída, erros e comportamento esperado.
#>

$ErrorActionPreference = "Stop"

# Função para verificar se um comando existe
function Test-Command {
    param($Command)
    return [bool](Get-Command -Name $Command -ErrorAction SilentlyContinue)
}

# Função para log colorido
function Write-TestLog {
    param(
        [Parameter(Mandatory=$true)]
        [string]$Message,
        [string]$Type = "INFO"
    )
    $color = switch ($Type) {
        "ERROR" { "Red" }
        "SUCCESS" { "Green" }
        "TEST" { "Magenta" }
        default { "Cyan" }
    }
    Write-Host "$(Get-Date -Format "yyyy-MM-dd HH:mm:ss") [$Type] $Message" -ForegroundColor $color
}

# Função para executar um script e validar resultado
function Test-Script {
    param(
        [Parameter(Mandatory=$true)]
        [string]$ScriptPath,
        [string]$Description
    )
    Write-TestLog "Executando $ScriptPath..." "TEST"
    Write-TestLog $Description "INFO"
    try {
        pwsh -File $ScriptPath
        if ($LASTEXITCODE -eq 0) {
            Write-TestLog "$ScriptPath executado com sucesso." "SUCCESS"
            return $true
        } else {
            Write-TestLog "$ScriptPath falhou com código $LASTEXITCODE" "ERROR"
            return $false
        }
    } catch {
        Write-TestLog "$ScriptPath falhou com erro: $($_.Exception.Message)" "ERROR"
        return $false
    }
}

# Testa ambiente Python
function Test-PythonEnvironment {
    Write-TestLog "Validando ambiente Python..." "TEST"

    # Python 3.11+
    if (-not (Test-Command "python")) {
        Write-TestLog "Python não encontrado" "ERROR"
        return $false
    }
    $pythonVersion = python -c "import sys; print('.'.join(map(str, sys.version_info[:2])))"
    if ([version]$pythonVersion -lt [version]"3.11") {
        Write-TestLog "Python 3.11+ requerido. Versão atual: $pythonVersion" "ERROR"
        return $false
    }
    Write-TestLog "Python $pythonVersion encontrado" "SUCCESS"

    # Poetry
    if (-not (Test-Command "poetry")) {
        Write-TestLog "Poetry não encontrado" "ERROR"
        return $false
    }
    Write-TestLog "Poetry encontrado" "SUCCESS"

    # Ambiente virtual
    if (-not (Test-Path "../.venv")) {
        Write-TestLog "Ambiente virtual não encontrado" "ERROR"
        return $false
    }
    Write-TestLog "Ambiente virtual encontrado" "SUCCESS"

    # poetry.lock
    if (-not (Test-Path "../poetry.lock")) {
        Write-TestLog "poetry.lock não encontrado" "ERROR"
        return $false
    }
    Write-TestLog "poetry.lock encontrado" "SUCCESS"

    # pre-commit
    if (-not (Test-Path "../.git/hooks/pre-commit")) {
        Write-TestLog "pre-commit hooks não instalados" "ERROR"
        return $false
    }
    Write-TestLog "pre-commit hooks instalados" "SUCCESS"

    return $true
}

function Test-PostCheckoutSetup {
    $result = Test-Script `
        -ScriptPath "../.scripts/post-checkout-setup.ps1" `
        -Description "Validando instalação de extensões VS Code"

    return $result
}

function Test-InstallMcpPackages {
    $result = Test-Script `
        -ScriptPath "../.scripts/install-mcp-packages.ps1" `
        -Description "Validando instalação de pacotes MCP"

    return $result
}

function Test-DiagnosePythonEnvironment {
    $result = Test-Script `
        -ScriptPath "../.scripts/diagnose-python-environment.ps1" `
        -Description "Executando diagnóstico do ambiente Python"

    return $result
}

# Execução dos testes
Write-TestLog "🧪 Iniciando testes de onboarding..." "TEST"
Write-TestLog "========================================" "INFO"

$tests = @(
    @{Name="Ambiente Python"; Function={Test-PythonEnvironment}},
    @{Name="Post-Checkout Setup"; Function={Test-PostCheckoutSetup}},
    @{Name="Instalação MCP"; Function={Test-InstallMcpPackages}},
    @{Name="Diagnóstico Python"; Function={Test-DiagnosePythonEnvironment}}
)

$results = @()
foreach ($test in $tests) {
    Write-TestLog "`nExecutando teste: $($test.Name)..." "TEST"
    $success = & $test.Function
    $results += @{
        Name = $test.Name
        Success = $success
    }
}

# Resumo
Write-TestLog "`n========================================" "INFO"
Write-TestLog "📊 Resumo dos Testes:" "INFO"
Write-TestLog "========================================" "INFO"

$totalTests = $tests.Count
$passedTests = ($results | Where-Object { $_.Success -eq $true }).Count

foreach ($result in $results) {
    $status = if ($result.Success) { "✅" } else { "❌" }
    Write-TestLog "$status $($result.Name)" $(if ($result.Success) { "SUCCESS" } else { "ERROR" })
}

Write-TestLog "`nResultado Final: $passedTests/$totalTests testes passaram" "INFO"

if ($passedTests -eq $totalTests) {
    Write-TestLog "🎉 Todos os testes passaram!" "SUCCESS"
    exit 0
} else {
    Write-TestLog "❌ Alguns testes falharam. Verifique os logs acima." "ERROR"
    exit 1
}
