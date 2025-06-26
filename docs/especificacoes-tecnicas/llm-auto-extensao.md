# Especificação Técnica: Suporte a LLMs para Geração de Código e Especificação

## 1. Visão Geral

Esta especificação detalha a arquitetura, interfaces, fluxo, configuração, requisitos de segurança e análise de impacto para permitir o uso de LLMs (OpenAI, Anthropic, Gemini, etc.) na geração de código e especificação, além do modelo baseado em templates.

---

## 2. Arquitetura de Providers

- **Abstrações:**
  - `CodeGenerationProvider`: Interface para geração de código.
  - `SpecGenerationProvider`: Interface para geração de especificação.
- **Implementações:**
  - `TemplateCodeProvider`: Usa template local.
  - `LLMCodeProvider`: Usa LLM externa (configurável).
  - `HybridCodeProvider`: Seleciona provider dinamicamente.
- **Plugabilidade:**
  - Providers são plugáveis e configuráveis via YAML.
  - Suporte a múltiplos providers simultâneos.

---

## 3. Interfaces Detalhadas

```python
class CodeGenerationProvider(Protocol):
    async def generate(self, spec: ToolSpec, prompt: str = None) -> str:
        ...

class SpecGenerationProvider(Protocol):
    async def generate(self, context: dict, prompt: str = None) -> ToolSpec:
        ...
```

- Métodos assíncronos, parâmetros obrigatórios, tratamento de exceções e logging estruturado.
- Extensibilidade para novos providers e fácil integração de LLMs.

---

## 4. Fluxo de Decisão

1. Recebe requisição para geração de tool/spec.
2. Identifica provider ativo (llm/template/híbrido) via config.
3. Valida configuração e parâmetros.
4. Monta payload dinâmico (prompt, modelo, etc.).
5. Executa provider e trata resposta.
6. Aplica fallback automático para template local em caso de erro.
7. Registra logs/auditoria do processo.

---

## 5. Configuração YAML

```yaml
auto_extension:
  code_generation:
    provider: "llm"  # ou "template" ou "hybrid"
    llm:
      url: "https://api.openai.com/v1/chat/completions"
      api_key: "sk-..."
      model: "gpt-4o"
      prompt_template: "..."
      request_payload: {...}
      response_path: "choices[0].message.content"
    template:
      default_template_id: "default"
  spec_generation:
    provider: "llm"
    llm:
      ...
```

- Suporte a múltiplos providers e versionamento de prompts.
- Fallback automático para template local.

---

## 6. Integração com PromptTemplateManager

- Gerenciamento centralizado de prompts para geração de código e especificação.
- Versionamento e testes de prompts.
- Permite customização por provider/modelo.

---

## 7. Impacto em APIs

- O endpoint `/api/tools` deve aceitar configuração de LLM opcional.
- Novos campos: provider, config de LLM, prompt customizado.
- Compatibilidade retroativa garantida.
- Atualização da documentação OpenAPI/Swagger.

---

## 8. Segurança

- Validação rigorosa de todas as respostas de LLM.
- Sanitização de entradas e saídas.
- Logging estruturado sem dados sensíveis.
- Rate limiting, autenticação e autorização nos endpoints.
- Rastreabilidade via logs e auditoria.

---

## 9. Impacto em Domínio e Testes

- Adaptar `ToolSpec` e `GeneratedTool` para novos campos de provider/config.
- Garantir testabilidade dos providers (mocks para LLM).
- Criar testes unitários e de integração para todos fluxos.
- Atualizar documentação e exemplos.

---

## 10. Análise de Impacto

### Pontos Positivos

- Flexibilidade para uso de múltiplos LLMs e templates.
- Evolução incremental sem breaking changes.
- Facilidade de experimentação e ajuste de prompts.
- Logging e rastreabilidade aprimorados.

### Riscos e Mitigações

- Inconsistência de respostas de LLM: mitigar com prompts controlados e fallback.
- Custo e limites de uso: monitorar e limitar via configuração.
- Segurança: validação e sanitização obrigatórias.
- Complexidade de configuração: abstrair via PromptTemplateManager e exemplos claros.

---

## 11. Exemplos de Uso

### Geração de Tool com LLM

```python
provider = LLMCodeProvider(config)
code = await provider.generate(spec, prompt)
```

### Geração de Tool com Template

```python
provider = TemplateCodeProvider(config)
code = await provider.generate(spec)
```

---

## 12. Checklist de Implementação

- [ ] Interfaces e abstrações implementadas
- [ ] Configuração YAML documentada
- [ ] Integração com PromptTemplateManager
- [ ] Testes unitários e de integração
- [ ] Segurança validada
- [ ] Documentação OpenAPI/Swagger atualizada
- [ ] Logging estruturado implementado

---

---

## 14. Planejamento Incremental – Suporte a LLMs na Auto-Extensão

### Fase 1: Arquitetura e Interfaces (Sprint 1)

- [ ] Definir e documentar interfaces `CodeGenerationProvider` e `SpecGenerationProvider`
- [ ] Especificar contratos de provider (assinaturas, exceptions, logging)
- [ ] Mapear pontos de integração com PromptTemplateManager
- [ ] Atualizar documentação técnica e YAML de configuração

### Fase 2: Providers e Configuração (Sprint 2)

- [ ] Implementar `TemplateCodeProvider` (refatorar provider atual)
- [ ] Implementar `LLMCodeProvider` (OpenAI, Anthropic, Gemini, etc.)
- [ ] Implementar `HybridCodeProvider` (seleção dinâmica)
- [ ] Suporte a múltiplos providers e fallback automático
- [ ] Testes unitários para cada provider

### Fase 3: Integração e API (Sprint 3)

- [x] Adaptar endpoint `/api/tools` para aceitar config dinâmica de LLM
- [x] Validar parâmetros e garantir compatibilidade retroativa
- [x] Atualizar OpenAPI/Swagger e exemplos de uso
- [x] Logging estruturado e rastreabilidade de provider usado

#### Exemplo de Payload para `/api/tools`

**Provider: template (padrão retrocompatível)**

```json
{
  "name": "enviar_email",
  "description": "Envia um email para o destinatário informado",
  "parameters": {"destinatario": {"type": "str"}, "mensagem": {"type": "str"}},
  "return_type": "bool",
  "template_id": "default",
  "security_level": "standard",
  "resource_requirements": {"memory_mb": 64, "timeout_seconds": 10}
}
```

**Provider: llm (OpenAI, Anthropic, etc.)**

```json
{
  "name": "gerar_relatorio",
  "description": "Gera um relatório financeiro a partir de dados JSON",
  "parameters": {"dados": {"type": "dict"}},
  "return_type": "str",
  "provider": "llm",
  "llm_config": {
    "url": "https://api.openai.com/v1/chat/completions",
    "api_key": "sk-...",
    "model": "gpt-4o",
    "prompt_template": "Você é um gerador de relatórios Python..."
  },
  "prompt_customizado": "Gere uma função Python que recebe dados e retorna um relatório."
}
```

**Provider: hybrid (fallback automático)**

```json
{
  "name": "converter_moeda",
  "description": "Converte valores entre moedas usando API externa",
  "parameters": {"valor": {"type": "float"}, "de": {"type": "str"}, "para": {"type": "str"}},
  "return_type": "float",
  "provider": "hybrid",
  "llm_config": {
    "url": "https://api.openai.com/v1/chat/completions",
    "model": "gpt-4o"
  }
}
```

#### OpenAPI/Swagger (resumo)

- O endpoint `/api/tools` aceita todos os campos do modelo `ToolRequest`.
- Campos opcionais: `provider`, `llm_config`, `prompt_customizado`.
- Resposta: `ToolResponse` com código gerado, status, validação e rastreabilidade.
- Compatível com clientes antigos (sem provider = template).

#### Logging e rastreabilidade

- Todos os requests logam o provider selecionado, parâmetros e resultado.
- Fallbacks e erros de provider são registrados com contexto.

#### Observações

- O PromptTemplateManager permite versionamento e customização de prompts por provider/modelo.
- O sistema é extensível para novos providers e integrações futuras.

### Fase 4: Segurança e Observabilidade (Sprint 4)

- [ ] Validar e sanitizar todas as respostas de LLM
- [ ] Implementar rate limiting, autenticação e autorização
- [ ] Logging seguro (sem dados sensíveis)
- [ ] Métricas e tracing para geração via LLM/template

### Fase 5: Testes, Documentação e Ready/Done (Sprint 5)

- [ ] Testes de integração (mock LLM, fallback, erros)
- [ ] Atualizar exemplos e documentação de onboarding
- [ ] Checklist de Ready/Done: cobertura, segurança, documentação, rastreabilidade

### Critérios de Aceite de Pronto ai fim de cada sprint (Ready/Done)

- [ ] O sistema deve passar em **todos os testes unitários** (pytest, cobertura mínima definida)
- [ ] O sistema deve cumprir **todos os critérios de pre-commit** (lint, formatação, validação de mensagens de commit, etc.)
- [ ] Checklist de Ready/Done: cobertura, segurança, documentação, rastreabilidade
- [ ] Revisão final e atualização do Memory Bank
- [ ] Revisão final e atualização do Memory Bank
