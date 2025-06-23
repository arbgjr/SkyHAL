# Script para parar servidores MCP
# Criado em: 03/06/2025

$ErrorActionPreference = "Stop"

Write-Host "🛑 Parando servidores MCP..." -ForegroundColor Cyan

# Processos dos servidores MCP
$mcpProcesses = @(
    "npx",
    "@modelcontextprotocol/server-github",
    "@modelcontextprotocol/server-filesystem",
    "@modelcontextprotocol/server-memory",
    "@modelcontextprotocol/server-sequential-thinking",
    "mcp-server-git",
    "mcp-server-time",
    "@modelcontextprotocol/server-everything"
)

# Verificar e parar processos
$stoppedCount = 0
foreach ($procName in $mcpProcesses) {
    $processes = Get-Process | Where-Object { $_.CommandLine -like "*$procName*" }
    if ($processes) {
        foreach ($process in $processes) {
            try {
                Write-Host "⏹️ Parando processo: $($process.Id) ($procName)" -ForegroundColor Yellow
                Stop-Process -Id $process.Id -Force
                $stoppedCount++
            }
            catch {
                Write-Host "⚠️ Erro ao parar processo $($process.Id): $_" -ForegroundColor Red
            }
        }
    }
}

if ($stoppedCount -gt 0) {
    Write-Host "✅ $stoppedCount processos MCP foram parados" -ForegroundColor Green
}
else {
    Write-Host "ℹ️ Nenhum processo MCP encontrado em execução" -ForegroundColor Blue
}
