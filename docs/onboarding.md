# Onboarding e Setup de Ambiente

## Fluxo Dinâmico de Instalação de Dependências

O ambiente de desenvolvimento do SkyHAL agora utiliza scripts dinâmicos para garantir que todas as extensões do VS Code e pacotes MCP estejam sempre alinhados com as configurações do projeto.

### 1. Instalação de Extensões VS Code

- O script `.scripts/post-checkout-setup.ps1` lê automaticamente o arquivo `.vscode/extensions.json` e instala todas as extensões listadas em `recommendations`.
- Para adicionar ou remover extensões recomendadas, edite apenas o arquivo `.vscode/extensions.json`.
- O script realiza logging estruturado e validação, abortando em caso de erro.

### 2. Instalação de Pacotes MCP

- O script `.scripts/install-mcp-packages.ps1` lê o arquivo `.vscode/mcp.json` e instala globalmente todos os pacotes MCP necessários, extraindo os nomes dos comandos dos servidores.
- Para adicionar/remover servidores MCP, edite apenas `.vscode/mcp.json`.
- O script valida a presença do Node.js/NPM e faz logging detalhado de cada etapa.

### 3. Execução dos Scripts

- Execute os scripts manualmente ou utilize os hooks/tarefas automatizadas do projeto.
- Exemplo:

  ```powershell
  pwsh .scripts/post-checkout-setup.ps1
  pwsh .scripts/install-mcp-packages.ps1
  ```

### 4. Boas Práticas

- Sempre rode os scripts após atualizar as configurações de extensões ou MCP.
- Consulte o Memory Bank antes de iniciar tarefas relevantes.
- Em caso de erro, consulte os logs exibidos pelo script para diagnóstico.

### 5. Observabilidade Avançada

- Todos os componentes core do sistema de auto-extensão estão instrumentados com métricas Prometheus, tracing OpenTelemetry e logs estruturados.
- Build, lint e testes automatizados validados.
- Artefato de validação: [`docs/especificacoes-tecnicas/artefatos/observability-validation-20250625.md`](../docs/especificacoes-tecnicas/artefatos/observability-validation-20250625.md)
- Consulte o [README principal](../README.md#5-observabilidade-avancada-e-monitoramento) e a [documentação de observabilidade](../docs/observabilidade/README.md) para exemplos e troubleshooting.

---

Dúvidas ou problemas? Consulte o README principal ou abra uma issue.
