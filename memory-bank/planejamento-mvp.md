# 📅 Planejamento Incremental MVP SkyHAL

Este documento detalha o planejamento incremental para o MVP do SkyHAL, considerando Clean Architecture, Memory Bank, segurança, testabilidade, observabilidade e automação CI/CD. As tarefas são pequenas, independentes e organizadas em sprints de 1 semana, permitindo trabalho paralelo.

---

## 🗓️ Sprint 1: Fundamentos do Ambiente e Estrutura Inicial

1. **Configurar DevContainer Linux**
   - Criar `.devcontainer/devcontainer.json` com dependências básicas (.NET, Node, Docker, utilitários CLI).
   - Documentar uso no `README.md`.

2. **Estruturar Pastas do Projeto (Clean Architecture)**
   - Criar diretórios: `/src`, `/tests`, `/infra`, `/docs`, `/memory-bank`, `.github/instructions`, `.github/prompts`.
   - Adicionar arquivos README em cada pasta explicando propósito.

3. **Configurar Ambiente de Build e Tasks**
   - Revisar e ajustar `.vscode/tasks.json` para build, test, lint, integração Memory Bank.
   - Garantir tasks para Windows e Linux.

4. **Configurar Extensões e Settings VS Code**
   - Revisar `.vscode/extensions.json` e `.vscode/settings.json` conforme guia e necessidades do projeto.
   - Documentar recomendações no `README.md`.

5. **Revisar e Atualizar Arquivos de Instruções**
   - Revisar: `.github/instructions/*.md`, `.github/prompts/*.md`, `.github/copilot-instructions.md`, `.vscode/extensions.json`, `.vscode/settings.json`, `.vscode/tasks.json`, `.vscode/mcp.json`, `github-copilot-instrucoes-personalizadas-guia.md`.
   - Garantir alinhamento com Clean Architecture, Memory Bank e práticas do guia.

---

## 🗓️ Sprint 2: Infraestrutura Básica e Observabilidade

1. **Configurar Projeto Base MCP Server**
   - Scaffold do servidor MCP (ex: ASP.NET Core WebAPI).
   - Estrutura inicial de camadas: Apresentação, Aplicação, Domínio, Infraestrutura.

2. **Implementar Observabilidade**
   - Adicionar Serilog (JSON), OpenTelemetry (tracing/métricas), Prometheus, Jaeger.
   - Garantir logging estruturado com trace_id.

3. **Configurar Pipeline CI/CD Inicial**
   - Pipeline YAML para build, lint, testes e publicação de artefatos.
   - Incluir validação de tasks e instruções do projeto.

4. **Documentar Processo de Contribuição**
   - Adicionar/consolidar `CONTRIBUTING.md` e instruções de PR.
   - Checklist de conformidade com Memory Bank e padrões.

---

## 🗓️ Sprint 3: Segurança, Testes e API MVP

1. **Implementar Autenticação e Segurança Básica**
   - JWT, autorização por roles/claims, headers de segurança.
   - Rate limiting e validação de entrada (DTOs, Annotations).

2. **Criar Endpoints de Healthcheck e Status**
   - `/health`, `/status`, `/metrics` (Prometheus).
   - Testes automatizados para cada endpoint.

3. **Estruturar Testes Unitários e de Integração**
   - Configurar frameworks de teste (xUnit/NUnit/Moq).
   - Criar exemplos de testes AAA para cada camada.

4. **Documentar APIs e Segurança**
   - Adicionar Swagger/OpenAPI.
   - Documentar exemplos de autenticação e uso seguro.

---

## 🗓️ Sprint 4: Integração Memory Bank e Automação

1. **Implementar Integração com Memory Bank**
   - Leitura/escrita incremental dos arquivos do Memory Bank.
   - API para consulta e atualização do contexto.

2. **Automatizar Atualização do Memory Bank**
   - Task/script para atualizar arquivos do Memory Bank via CI/CD.
   - Validação automática de consistência.

3. **Testes de API e Segurança**
   - Testes automatizados para cenários de autenticação, autorização, erros e limites.

4. **Revisão e Melhoria Contínua das Instruções**
   - Rodar task de revisão dos arquivos de instruções e prompts.
   - Propor melhorias e registrar débitos técnicos.

---

## 🗓️ Sprint 5: Publicação, Monitoramento e Feedback

1. **Publicar Servidor MCP em Ambiente de Homologação**
   - Pipeline de deploy automatizado (preferencialmente Azure, Docker ou similar).
   - Garantir HTTPS e variáveis seguras.

2. **Configurar Monitoramento e Alertas**
   - Dashboards Grafana, alertas Prometheus/Jaeger.
   - Documentar procedimentos de observabilidade.

3. **Coletar Feedback e Planejar Incrementos**
   - Checklist de funcionalidades do MVP.
   - Planejar backlog para features avançadas.

---

### 📋 Observações Gerais

- Todas as tarefas devem ser pequenas, independentes e bem documentadas.
- Cada dev pode pegar qualquer tarefa da sprint sem depender de outra.
- Revisão de instruções e tasks é contínua e sempre paralela.
- Débitos técnicos e bugs devem ser registrados nos arquivos apropriados.
- Sempre alinhar decisões com o Memory Bank e atualizar quando necessário.

---

Este planejamento segue as diretrizes do Memory Bank e Clean Architecture, garantindo evolução incremental, rastreabilidade e qualidade desde o início.