<#
 Executado automaticamente pelo hook Git post-checkout
 Instala extensões VS Code necessárias ao projeto.
#>

Write-Host "[INFO] Iniciando instalação dinâmica de extensões VS Code..." -ForegroundColor Cyan
$extensionsFile = Join-Path $PSScriptRoot "..\.vscode\extensions.json"
if (-Not (Test-Path $extensionsFile)) {
    Write-Host "[ERRO] Arquivo de extensões não encontrado: $extensionsFile" -ForegroundColor Red
    exit 1
}

try {
    $json = Get-Content $extensionsFile -Raw | ConvertFrom-Json
    if (-not $json.recommendations -or $json.recommendations.Count -eq 0) {
        Write-Host "[WARN] Nenhuma extensão recomendada encontrada em $extensionsFile" -ForegroundColor Yellow
        exit 0
    }
    foreach ($ext in $json.recommendations) {
        if ([string]::IsNullOrWhiteSpace($ext)) {
            Write-Host "[WARN] Extensão inválida ignorada." -ForegroundColor Yellow
            continue
        }
        Write-Host ("[INFO] Instalando extensão: {0}" -f $ext) -ForegroundColor Cyan
        try {
            code --install-extension $ext --force
            if ($LASTEXITCODE -eq 0) {
                Write-Host ("[OK] {0} instalada com sucesso." -f $ext) -ForegroundColor Green
            } else {
                Write-Host ("[ERRO] Falha ao instalar {0}. Código de saída: {1}" -f $ext, $LASTEXITCODE) -ForegroundColor Red
            }
        } catch {
            Write-Host ("[ERRO] Exceção ao instalar {0}: {1}" -f $ext, $_.Exception.Message) -ForegroundColor Red
        }
    }
    Write-Host "[INFO] Instalação de extensões concluída." -ForegroundColor Green
} catch {
    Write-Host ("[ERRO] Falha ao processar {0}: {1}" -f $extensionsFile, $_.Exception.Message) -ForegroundColor Red
    exit 1
}
