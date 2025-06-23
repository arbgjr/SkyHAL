<#
 Executado automaticamente pelo hook Git post-checkout
 Instala extensões VS Code necessárias ao projeto.
#>
 
Write-Host "Instalando extensões VS Code obrigatórias..."
$extensions = @(
  "VisualStudioExptTeam.vscodeintellicode",
  "humao.rest-client",
  "ms-azuretools.vscode-docker",
  "EditorConfig.EditorConfig",
  "redhat.vscode-xml",
  "eamodio.gitlens",
  "GitHub.copilot",
  "GitHub.copilot-chat",
  "ms-vscode.powershell",
  "github.copilot-workspace",
  "github.vscode-pull-request-github",
  "ms-vscode.vscode-copilot-vision",
  "ms-vscode.vscode-websearchforcopilot",
  "teamsdevapp.vscode-ai-foundry"
)
 
foreach ($ext in $extensions) {
  code --install-extension $ext --force
}
Write-Host "Extensões instaladas."