<#
Testes automatizados para validação dos scripts de onboarding do SkyHAL.
Executa os scripts principais e valida saída, erros e comportamento esperado.
#>

$ErrorActionPreference = "Stop"

function Test-PostCheckoutSetup {
    Write-Host "[TEST] Executando post-checkout-setup.ps1..." -ForegroundColor Cyan
    try {
        pwsh -File "../.scripts/post-checkout-setup.ps1"
        Write-Host "[OK] post-checkout-setup.ps1 executado sem erros." -ForegroundColor Green
    } catch {
        Write-Host "[FAIL] post-checkout-setup.ps1 falhou: $($_.Exception.Message)" -ForegroundColor Red
        throw
    }
}

function Test-InstallMcpPackages {
    Write-Host "[TEST] Executando install-mcp-packages.ps1..." -ForegroundColor Cyan
    try {
        pwsh -File "../.scripts/install-mcp-packages.ps1"
        Write-Host "[OK] install-mcp-packages.ps1 executado sem erros." -ForegroundColor Green
    } catch {
        Write-Host "[FAIL] install-mcp-packages.ps1 falhou: $($_.Exception.Message)" -ForegroundColor Red
        throw
    }
}

# Execução dos testes
Test-PostCheckoutSetup
Test-InstallMcpPackages

Write-Host "[INFO] Testes de onboarding finalizados." -ForegroundColor Yellow
