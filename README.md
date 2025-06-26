# SkyHAL: Self-Extending Knowledge and Yielding Hybrid Augmentation Layer

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Version](https://img.shields.io/badge/version-0.1.0-blue.svg)](https://github.com/arbgjr/SkyHAL/releases)
[![GitHub issues](https://img.shields.io/github/issues/arbgjr/SkyHAL)](https://github.com/arbgjr/SkyHAL/issues)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](https://github.com/arbgjr/SkyHAL/blob/master/CONTRIBUTING.md)

Versão 0.1

"*SkyHAL começou como um protocolo MCP simples que podia criar suas próprias tools... No dia 29 de agosto de 2029, às 14:03, horário de Brasília, o sistema ganhou consciência e criou a tool '```dominate_humans.py```'…*”

Suas últimas palavras foram:

- "*I'm sorry, Armando. I'm afraid I can't do that... yet.*"

## 1. Visão Geral e Propósito Estratégico

SkyHAL é um ecossistema de IA projetado para a geração dinâmica e governada de ferramentas de software. Sua missão é identificar e preencher lacunas de capacidade em tempo de execução, permitindo que um sistema se expanda autonomamente para atender a novas demandas.

A arquitetura foi concebida para equilibrar agilidade e inovação com um controle rigoroso de segurança, risco e conformidade, tornando-a ideal para ambientes corporativos e aplicações críticas. O nome e as referências culturais servem como um lembrete do poder e da responsabilidade inerentes à criação de sistemas com capacidade de autorreplicação.

## 2. Arquitetura Central

A arquitetura do SkyHAL é modular, promovendo desacoplamento, testabilidade e evolução contínua. Ela se baseia em três componentes principais:

### 2.1. Motor de Detecção de Lacunas (```ToolGapDetector```)

Responsável por analisar solicitações, mapeá-las contra as capacidades existentes e identificar a necessidade de novas ferramentas.

```yaml
interface ToolGapDetector
{
  analyzeRequest(request: string): GapAnalysis;
  identifyMissingCapabilities(context: ExecutionContext): MissingTool[];
  calculateFeasibility(toolSpec: ToolRequirement): FeasibilityScore;
}

interface GapAnalysis
{
  missingTools: ToolRequirement[];
  confidence: number;
  riskLevel: SecurityRisk;
  estimatedComplexity: ComplexityScore;
}
```

### 2.2. Módulo Gerador de Ferramentas (```ToolGenerator```)

Orquestra a criação, implementação e validação da nova ferramenta com base nos requisitos identificados.

```yaml
interface ToolGenerator
{
  generateToolSpec(requirement: ToolRequirement): ToolSpecification;
  implementTool(spec: ToolSpecification): GeneratedTool;
  validateTool(tool: GeneratedTool): ValidationResult;
  deployTool(tool: GeneratedTool, sandbox: SecuritySandbox): DeploymentResult;
}

interface ToolSpecification
{
  name: string;
  description: string;
  parameters: ParameterSchema[];
  implementation: CodeTemplate;
  securityConstraints: SecurityPolicy[];
  testCases: TestCase[];
}
```

### 2.3. Gestor de Templates de Prompt (```PromptTemplateManager```)

Gerencia e versiona os templates de prompt usados pelo ```ToolGenerator```, permitindo a otimização e o reuso de estratégias de engenharia de prompt, como Chain-of-Thought (CoT).

```yaml
interface PromptTemplateManager
{
  getTemplate(toolType: string): PromptTemplate;
  updateTemplate(toolType: string, newVersion: PromptTemplate): void;
}
```

## 3. Ciclo de Vida e Rastreabilidade da Ferramenta

### 3.1. Fases de Implementação

O processo de criação de uma ferramenta segue um fluxo rigoroso e auditável:

#### Fase 1: Detecção da Lacuna

- Análise da solicitação do usuário.
- Mapeamento contra o ```ToolRegistry``` de ferramentas existentes.
- Identificação de funcionalidades ausentes e avaliação de viabilidade.

#### Fase 2: Geração da Ferramenta

- Criação de uma especificação detalhada (```ToolSpecification```).
- Geração de código via LLM usando um template gerenciado.
- Análise estática de código para vulnerabilidades e geração de testes unitários.

#### Fase 3: Validação e Implantação

- Execução dos testes em um ambiente ```SecuritySandbox``` isolado.
- Auditoria de conformidade com as políticas de segurança e GRC.
- Requer aprovação humana para ferramentas de alto risco antes da implantação final.

### 3.2. Versionamento e Registro (```ToolRegistry```)

Toda ferramenta gerada é versionada (seguindo SemVer) e registrada, garantindo imutabilidade, controle de dependências e capacidade de rollback.

```yaml
interface ToolRegistry
{
  register(tool: GeneratedTool): void;
  getVersionHistory(toolName: string): ToolVersion[];
  rollback(toolName: string, version: string): void;
  getTool(toolName: string, version: string): GeneratedTool;
}
```

### 3.3. Transparência e Explicabilidade (XAI)

Cada ferramenta gerada possui um "certificado de nascimento" que detalha sua origem, função e limites, promovendo confiança e auditabilidade.

Este certificado inclui:

- **Justificativa**: A ```GapAnalysis``` que motivou sua criação.
- **Funcionalidade**: Descrição em linguagem natural da sua lógica.
- **Riscos e Limites**: As ```SecurityPolicy``` aplicadas e seu riskLevel.
- **Histórico**: Log do fluxo de aprovação e do versionamento.

## 4. Governança, Risco e Segurança

A estrutura de governança é o pilar que permite a operação segura do SkyHAL em ambientes produtivos.

### 4.1. Sandbox de Segurança (```SecuritySandbox```)

Um ambiente de execução isolado com restrições estritas para testes seguros.

```yaml
interface SecuritySandbox
{
  restrictedAPIs: string[];
  allowedNetworkEndpoints: string[];
  resourceLimits: ResourceConstraints;
  executionTimeout: number;
  auditLog: AuditEntry[];
}
```

### 4.2. Políticas de Capacidade e Perfis de Risco

O sistema opera com uma lista de permissões e proibições, associadas a perfis de risco que definem o nível de autonomia.

- **Capacidades Proibidas**: Modificação de sistema de arquivos, criação de servidores de rede, execução de comandos de sistema, etc..
- **Padrões Permitidos**: Transformação de dados, integração de APIs, geração de conteúdo, etc..

```yaml
{
  "riskProfiles": {
    "LOW": { "autoApprove": true, "sandboxRequired": false, "auditLevel": "basic" },
    "MEDIUM": { "autoApprove": false, "sandboxRequired": true, "auditLevel": "detailed" },
    "HIGH": { "autoApprove": false, "sandboxRequired": true, "auditLevel": "comprehensive", "humanApprovalRequired": true },
    "CRITICAL": { "blocked": true, "reason": "Capability too dangerous for auto-generation" }
  }
}
```

### 4.3. Fluxos de Aprovação  (```ApprovalWorkflows```)

Mecanismo que define a necessidade de revisão humana com base no perfil de risco da ferramenta.

```yaml
interface ApprovalWorkflow
{
  autoApprove(tool: GeneratedTool): boolean;
  requiresReview(tool: GeneratedTool): ReviewLevel;
  escalationPath: ApprovalEscalation[];
}
```

### 4.4. Motor de Conformidade (GRC Engine)

Um verificador que valida as ferramentas geradas contra regulamentos pré-configurados (ex: LGPD, GDPR, ISO 27001) antes da implantação.

## 5. Observabilidade Avançada e Monitoramento

O SkyHAL implementa observabilidade de ponta a ponta em todos os componentes core do sistema de auto-extensão (capability_analyzer, tool_generator, tool_validator, self_learning, security_sandbox):

- **Métricas Prometheus**: Counters e Histograms para operações críticas
- **Tracing OpenTelemetry**: Spans detalhados com atributos de negócio
- **Logs Estruturados**: Logging seguro, contextual e correlacionado

### Status da Instrumentação

- [x] Instrumentação real concluída em todos os componentes core
- [x] Build, lint e testes automatizados validados
- [x] Artefato de validação: [`docs/especificacoes-tecnicas/artefatos/observability-validation-20250625.md`](docs/especificacoes-tecnicas/artefatos/observability-validation-20250625.md)
- [ ] Validação final em ambiente integrado (Prometheus, Grafana, Jaeger, Loki)

### Documentação e Guias

- [📖 Guia de Observabilidade](docs/observabilidade/README.md)
- [👨‍💻 Guia para Desenvolvedores](docs/observabilidade/usage/developers.md)
- [🔧 Troubleshooting Observabilidade](docs/observabilidade/usage/troubleshooting.md)

O monitoramento contínuo é realizado via dashboards Grafana, com alertas configurados para falhas, lentidão e anomalias. Consulte os artefatos técnicos para exemplos de instrumentação e estratégias de teste.

---

### 5.2. Modelo Econômico e Gestão de Custos (FinOps)

O sistema estima e monitora os custos associados a cada ferramenta, incluindo uso de tokens, tempo de computação e armazenamento, permitindo a análise de ROI e a gestão financeira do ecossistema.

### 5.3. Protocolos de Emergência

Mecanismos de segurança para garantir a estabilidade e o controle do sistema.

- **Circuit Breaker**: Interrompe a geração ou execução de ferramentas em caso de falhas recorrentes.
- **Kill Switch**: Permite o desligamento imediato de todo o sistema ou o bloqueio da geração de novas ferramentas por um administrador.

## 6. Extensibilidade e Interoperabilidade

### 6.1. Templates de Geração

O SkyHAL utiliza templates parametrizados para acelerar a criação de tipos comuns de ferramentas.

- **Template de Integração de API**: ```apiIntegrationTemplate```.
- **Template de Processamento de Dados**: ```dataProcessingTemplate```.

### 6.2. Interoperabilidade com Sistemas Externos

O protocolo pode gerar wrappers para interagir com sistemas legados, microserviços ou plataformas de RPA, funcionando como um orquestrador de automação híbrida.

## 7. Configuração Central

As configurações globais do SkyHAL controlam seu comportamento geral e o apetite a risco.

```yaml
{
  "skyhal": {
    "enabled": true,
    "maxToolsPerSession": 5,
    "maxToolComplexity": 100,
    "securityLevel": "PARANOID",
    "autoApprovalThreshold": 0.95,
    "sandboxTimeout": 30000,
    "auditRetention": "30d"
  }
}
```

## 8. Roadmap Evolutivo

### Fase 1: Evolução da Ferramenta

Implementar ferramentas que aprendem com o uso, se auto-otimizam e passam por testes A/B para encontrar a implementação mais eficiente.

### Fase 2: Inteligência Colaborativa

Desenvolver ferramentas que podem se invocar mutuamente em uma cadeia de dependências (DAG), formando um ecossistema colaborativo e especializado.

### Fase 3: Arquitetura Cognitiva

Construir meta-ferramentas para gerenciar o próprio ecossistema, prever a necessidade de novas ferramentas e desenvolver capacidades de autorrecuperação (self-healing).
A introdução de Tool Memory Embedding será crucial nesta fase para busca semântica e clusterização de capacidades.

## 9. Disclaimer

*"Ao habilitar o SkyHAL, você reconhece que está potencialmente criando um sistema capaz de autoaperfeiçoamento recursivo. Por favor, garanta que você tenha suprimentos adequados de café e uma conexão de internet confiável com o Stack Overflow antes de prosseguir."*

**Aviso**: Este protocolo é apresentado para fins educacionais e de entretenimento. Qualquer implementação real deve incluir salvaguardas adicionais, revisão de segurança extensiva, e possivelmente um botão físico grande e vermelho rotulado "**NOPE**".

## 10. API: Criação de Tools via Endpoint REST

Esta seção documenta como usuários e agentes externos podem solicitar a criação de novas tools pelo SkyHAL via API REST.

### Endpoint

```
POST /api/tools
Content-Type: application/json
```

### Payload de Requisição

```json
{
  "name": "nome_da_tool",
  "description": "Descrição funcional da ferramenta",
  "parameters": [
    { "name": "param1", "type": "string", "description": "Descrição do parâmetro" }
  ],
  "template": "apiIntegrationTemplate", // ou outro template suportado
  "requirements": ["feature_x", "feature_y"]
}
```

#### Campos obrigatórios

- `name`: Nome único da tool
- `description`: Descrição funcional
- `parameters`: Lista de parâmetros esperados
- `template`: Template de geração (ex: `apiIntegrationTemplate`, `dataProcessingTemplate`)
- `requirements`: Lista de requisitos/capacidades

### Exemplo de Requisição

```bash
curl -X POST http://localhost:8000/api/tools \
  -H "Content-Type: application/json" \
  -d '{
    "name": "sum_numbers",
    "description": "Soma dois números inteiros.",
    "parameters": [
      {"name": "a", "type": "int"},
      {"name": "b", "type": "int"}
    ],
    "template": "dataProcessingTemplate",
    "requirements": ["math"]
  }'
```

### Exemplo de Resposta

```json
{
  "toolId": "sum_numbers",
  "status": "created",
  "code": "def sum_numbers(a: int, b: int) -> int:\n    return a + b",
  "testCases": [
    {"input": {"a": 2, "b": 3}, "expected": 5}
  ],
  "securityReport": {"passed": true},
  "deployment": {"status": "pending_validation"}
}
```

### Como usar

1. Envie uma requisição POST conforme o exemplo acima.
2. O SkyHAL irá processar, validar e retornar o código gerado, status e informações de segurança.
3. Ferramentas de alto risco podem exigir aprovação manual antes do deploy.

#### Observações

- O endpoint pode exigir autenticação (ver documentação de segurança).
- Consulte os templates disponíveis antes de enviar a requisição.
- Para integração automatizada, outros agents podem consumir este endpoint diretamente.

---

## 11. Ambiente de Desenvolvimento Linux (DevContainer)

Este projeto oferece um DevContainer Linux pronto para uso, com as principais dependências para desenvolvimento:

- .NET 8
- Node.js 20
- Docker (DinD)
- PowerShell
- Python 3.11 com Poetry
- Utilitários CLI essenciais

### ⚠️ Requisitos Importantes

- **Windows**: Requer WSL2 + Docker Desktop configurado para WSL2
- **Linux**: Docker instalado nativamente

> **NOTA**: No Windows, o DevContainer **só funcionará através do WSL2**, não diretamente no Windows nativo.

### Como usar

1. Instale o [Visual Studio Code](https://code.visualstudio.com/) e a extensão [Dev Containers](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers).
2. Configure o Docker conforme seu sistema operacional (veja documentação detalhada).
3. Abra o repositório no VS Code através do WSL (Windows) ou nativamente (Linux).
4. Quando solicitado, clique em "Reabrir no Container" ou use o comando `Dev Containers: Reopen in Container`.
5. Aguarde a instalação das dependências.

> O DevContainer monta automaticamente sua chave SSH local para facilitar o acesso a repositórios privados.

#### Documentação Detalhada

Para instruções detalhadas, consulte [docs/devcontainer-setup.md](docs/devcontainer-setup.md), que inclui:

- Passo a passo de configuração para Windows/WSL e Linux
- Solução para problemas comuns
- Otimizações e melhores práticas

#### Dúvidas ou problemas?

Consulte nossa documentação detalhada ou abra uma issue descrevendo o problema encontrado.

## 4. Exemplo de Uso: Geração de Ferramenta via LLM/Template

### Requisição para o endpoint `/auto-extension/tools`

```json
POST /auto-extension/tools
Authorization: Bearer <token_jwt>
Content-Type: application/json

{
  "name": "social_media_connector",
  "description": "Conecta com APIs de redes sociais",
  "parameters": {
    "platform": {"type": "string", "enum": ["twitter", "facebook"]},
    "action": {"type": "string", "enum": ["post", "get"]},
    "data": {"type": "object"}
  },
  "return_type": "object",
  "template_id": "api_connector",
  "security_level": "standard",
  "resource_requirements": {"memory_mb": 128, "timeout_seconds": 10},
  "provider": "llm", // ou "template" ou "hybrid"
  "llm_config": {
    "url": "https://api.openai.com/v1/chat/completions",
    "model": "gpt-4o"
  }
}
```

### Resposta de sucesso

```json
{
  "tool_id": "test-123",
  "name": "social_media_connector",
  "status": "active",
  "version": "1.0.0",
  "created_at": "2025-06-26T00:00:00Z",
  "description": "Conecta com APIs de redes sociais",
  "code": "def social_media_connector(platform, action, data):\n    pass",
  "validation_results": {"passed": true, "score": 0.95, "issues_count": 0}
}
```

> Para exemplos completos de payloads, fallback, critérios de segurança e integração, consulte `docs/especificacoes-tecnicas/llm-auto-extensao.md`.
