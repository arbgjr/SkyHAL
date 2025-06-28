# Gera .devcontainer/devcontainer.local.json a partir do devcontainer.json, ajustando o mount do SSH para o ambiente correto

$devcontainerPath = ".devcontainer/devcontainer.json"
$localPath = ".devcontainer/devcontainer.local.json"

# Lê o devcontainer.json
$json = Get-Content $devcontainerPath -Raw | ConvertFrom-Json

# Detecta ambiente
if ($env:WSL_DISTRO_NAME) {
    $sshPath = "/mnt/c/Users/$env:USER/.ssh"
}
else {
    $sshPath = "$env:USERPROFILE\.ssh"
}

# Atualiza o campo mounts
$json.mounts = @("source=$sshPath,target=/root/.ssh,type=bind,consistency=cached")

# Salva o novo arquivo
$json | ConvertTo-Json -Depth 10 | Set-Content $localPath -Encoding UTF8
Write-Host "Arquivo $localPath gerado para mount: $sshPath" -ForegroundColor Green
Write-Host ""
Write-Host "Para usar o DevContainer com SSH local:" -ForegroundColor Yellow
Write-Host "1. Feche o Dev Container remoto (Ctrl+Shift+P > Dev Containers: Fechar janela remota)." -ForegroundColor Yellow
Write-Host "2. Reabra o projeto no Dev Container normalmente." -ForegroundColor Yellow
Write-Host "   - O VS Code deve detectar automaticamente o devcontainer.local.json." -ForegroundColor Yellow
Write-Host "   - Se não detectar, use: Ctrl+Shift+P > Dev Containers: Reabrir na janela de contêiner com arquivo de definição diferente... e selecione o .devcontainer/devcontainer.local.json" -ForegroundColor Yellow
