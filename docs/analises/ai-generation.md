
# Análise Técnica e Proposta de Arquitetura para Suporte a LLMs (OpenAI, Anthropic, Gemini, etc.)

## Resumo da Análise do Workspace

O workspace atual possui uma arquitetura baseada em templates para geração de código e especificação, com componentes como `ToolGenerator`, `TemplateProvider`, `CodeGenerator` e `PromptTemplateManager`. Não há integração nativa com LLMs, mas a arquitetura é modular e permite extensão para uso de provedores externos como OpenAI, Anthropic, Gemini, etc.

### Pontos-Chave

- O fluxo atual depende de templates locais, mas pode ser expandido para aceitar providers LLM.
- O endpoint de API pode ser adaptado para receber configurações dinâmicas de LLM (URL, chave, payload, prompt, etc.).
- O sistema deve permitir fallback automático para template local caso a LLM não esteja configurada ou falhe.
- A validação de segurança e logging estruturado já estão previstos e devem ser mantidos para respostas de LLM.

## Proposta de Arquitetura para Suporte a LLMs

1. **Providers Polimórficos**: Implementar providers para geração de código/especificação que possam usar tanto templates locais quanto LLMs externas, selecionando dinamicamente conforme configuração.
2. **Configuração Flexível**: Permitir configuração de endpoint, headers, payload, modelo, prompt e parsing do response para cada LLM provider.
3. **Prompt Customizável**: Gerenciar prompts para geração de código e especificação via `PromptTemplateManager`, permitindo versionamento e testes.
4. **Fallback e Logging**: Usar template local como fallback e registrar qual provider foi utilizado, além de logar payloads e respostas para auditoria.
5. **Segurança**: Toda resposta de LLM deve passar pela validação de segurança já existente.

### Interfaces Sugeridas

```python
class CodeGenerationProvider(Protocol):
    async def generate(self, spec: ToolSpec, prompt: str = None) -> str: ...

class SpecGenerationProvider(Protocol):
    async def generate(self, context: dict, prompt: str = None) -> ToolSpec: ...
```

### Exemplo de Configuração YAML

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

---

# Enabling the use of LLMs (OpenAI, Anthropic, Gemini, etc.) for generating specifications and code

Here is a summary of all code and documentation in your workspace relevant to the request of enabling the use of LLMs (OpenAI, Anthropic, Gemini, etc.) for generating specifications and code, in addition to the current template-based approach. This includes the ability to flexibly configure payload, response, URL, key, and prompts, and to auto-adapt to the LLM provider.

---

## 1. Componentes Atuais de Geração de Especificação e Código

### a) ToolGenerator (src/domain/auto_extension/tool_generator.py)

- Classe principal responsável por gerar novas tools a partir de especificações.
- Usa um `template_provider` para obter templates e um `code_generator` para gerar o código.
- O método `generate_tool`:
  - Valida a especificação (`_validate_spec`)
  - Obtém o template (`template_provider.get_template`)
  - Gera o código (`code_generator.generate`)
  - Valida segurança (`security_validator.validate`)
  - Cria e retorna a tool gerada.
- O template é atualmente obrigatório para geração do código.

### b) TemplateProvider e CodeGenerator

- Interfaces/abstrações para prover templates e gerar código a partir deles.
- Não há menção explícita a integração com LLMs, mas a arquitetura é modular e permite extensão.

### c) PromptTemplateManager (README.md)

- Responsável por gerenciar e versionar templates de prompt usados pelo ToolGenerator.
- Permite otimização e reuso de estratégias de prompt (ex: Chain-of-Thought).

---

## 2. Documentação e Especificações Técnicas

### a) Especificações Técnicas (docs/especificacoes-tecnicas/artefatos/auto-extensao-artefatos.md, issue-11-auto-extensao-mcp.md, auto-extensao-arquitetura.md)

- O fluxo atual é: análise de gap → geração de especificação → geração de código via template → validação → deploy.
- O uso de templates é central, mas a arquitetura prevê extensibilidade.
- Não há menção explícita a LLMs, mas há espaço para plugabilidade de novos providers.

### b) API de Auto-Extensão (README.md, auto-extensao-arquitetura.md)

- Endpoint POST `/api/tools` recebe uma especificação e retorna a tool gerada.
- O payload inclui nome, descrição, parâmetros, template, requisitos.
- Não há campo para configuração de LLM, mas a estrutura pode ser expandida.

---

## 3. Pontos de Extensão e Impacto

### a) Pontos de Impacto para Suporte a LLM

- O `ToolGenerator` e o `CodeGenerator` precisariam ser adaptados para:
  - Detectar se uma chave de LLM foi fornecida.
  - Permitir fallback para template se não houver LLM.
  - Permitir configuração dinâmica de prompts, payload, response, URL, chave.
  - Adaptar o payload/response conforme o provider (OpenAI, Anthropic, Gemini, etc.).
- O `PromptTemplateManager` pode ser usado para armazenar/configurar prompts para LLM.

### b) Flexibilidade e Autoadaptação

- O sistema deve permitir:
  - Configuração de endpoint, headers, payload, response mapping para cada LLM.
  - Configuração de prompts para geração de especificação e código.
  - Plugabilidade de novos providers sem alterar o core.

---

## 4. Exemplos de Código e Estruturas Relacionadas

### a) Estruturas de Especificação e Tool

```python
@dataclass
class ToolSpec:
    name: str
    description: str
    parameters: Dict[str, Any]
    return_type: str
    template_id: str
    security_level: str
    resource_requirements: Dict[str, Any]

@dataclass
class GeneratedTool:
    tool_id: str
    name: str
    code: str
    spec: ToolSpec
    validation_results: Dict[str, Any]
    version: str
    created_at: str
```

### b) Exemplo de Uso de Template no ToolGenerator

```python
template = await self.template_provider.get_template(spec.template_id)
code = await self.code_generator.generate(template, spec)
```

---

## 5. Referências de Documentação

- docs/especificacoes-tecnicas/artefatos/auto-extensao-artefatos.md (Seções: Gerador de Tools, API, Troubleshooting)
- docs/especificacoes-tecnicas/issue-11-auto-extensao-mcp.md (Seções: Gerador de Tools, Fluxos, Critérios de Aceitação)
- docs/especificacoes-tecnicas/auto-extensao-arquitetura.md (Seções: Componentes, Fluxo, Contratos de API)
- README.md (Seções: ToolGenerator, PromptTemplateManager, API de criação de tools)

---

## 6. Resumo para Especificação de Discussão

### Proposta de Especificação para Suporte a LLM + Template

- Adicionar ao ToolGenerator a capacidade de usar LLM para gerar especificação e/ou código, se uma chave de LLM for fornecida.
- Permitir configuração dinâmica de:
  - URL do endpoint da LLM
  - Headers (incluindo chave/token)
  - Payload (prompt, parâmetros, etc.)
  - Mapeamento do response (campo do código, erros, etc.)
  - Prompt para geração de especificação
  - Prompt para geração de código
- Permitir fallback para template se não houver LLM ou em caso de erro.
- Permitir múltiplos providers (OpenAI, Anthropic, Gemini, etc.) via configuração.
- O PromptTemplateManager pode ser usado para armazenar/configurar prompts para cada provider/tipo de geração.
- O endpoint da API pode aceitar um campo opcional para configuração de LLM (ou usar configuração global).

---

## 7. Principais Arquivos de Código e Documentação Envolvidos

- src/domain/auto_extension/tool_generator.py
- src/domain/auto_extension/entities/ (ToolSpec, GeneratedTool)
- src/domain/auto_extension/template_provider.py (se existir)
- src/domain/auto_extension/code_generator.py (se existir)
- src/domain/auto_extension/prompt_template_manager.py (se existir)
- docs/especificacoes-tecnicas/artefatos/auto-extensao-artefatos.md
- docs/especificacoes-tecnicas/issue-11-auto-extensao-mcp.md
- docs/especificacoes-tecnicas/auto-extensao-arquitetura.md
- README.md

---

## 1. Análise do Código Atual

O core atual (`ToolGenerator`, `DefaultTemplateProvider`, etc.) utiliza providers de template e um gerador de código desacoplado, mas não há suporte nativo para uso de LLMs externas (OpenAI, Anthropic, Gemini, etc.) para gerar especificações ou código. O fluxo é:

- Recebe uma `ToolSpec`
- Busca um template (por id)
- Gera código via provider
- Valida segurança
- Retorna a tool

## 2. Impacto de Permitir Geração por IA

### Pontos de impacto

- O provider de template/código precisa ser polimórfico: pode usar template local ou LLM.
- O sistema deve aceitar configuração dinâmica de:
  - URL do endpoint da LLM
  - Chave de API
  - Payload customizado (parâmetros, modelo, prompt, etc.)
  - Parsing do response (flexível para diferentes LLMs)
  - Prompt para geração de especificação e código (editável)
- O fallback para template local deve ser automático se não houver chave/configuração de LLM.
- O fluxo de validação de segurança e logging permanece igual.

### Benefícios

- Flexibilidade para usar IA de qualquer fornecedor.
- Possibilidade de experimentar diferentes modelos e prompts.
- Permite evolução incremental: pode-se começar só com template, depois ativar IA.

### Riscos

- Geração por IA pode ser inconsistente se o prompt não for bem controlado.
- Necessidade de tratamento de erros e timeouts de API.
- Custo e limites de uso das LLMs.

## 3. Especificação Proposta

### 3.1. Interfaces

```python
class CodeGenerationProvider(Protocol):
    async def generate(self, spec: ToolSpec, prompt: str = None) -> str: ...

class SpecGenerationProvider(Protocol):
    async def generate(self, context: dict, prompt: str = None) -> ToolSpec: ...
```

### 3.2. Providers

- `TemplateCodeProvider`: Usa template local (como hoje)
- `LLMCodeProvider`: Usa LLM externa (OpenAI, Anthropic, Gemini, etc.)
  - Recebe config dinâmica: url, chave, payload extra, prompt customizado
  - Faz parsing do response conforme config
- `HybridCodeProvider`: Decide qual usar (LLM ou template) conforme config/chave

### 3.3. Configuração

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
      ...
  spec_generation:
    provider: "llm"
    llm:
      ...
```

### 3.4. Prompt Customizável

- Prompt para geração de especificação e código deve ser editável via config ou arquivo.
- Pode ser versionado e testado.

### 3.5. Adaptação a Diferentes LLMs

- O provider LLM deve aceitar:
  - URL customizada
  - Headers customizados
  - Payload customizado (ex: modelo, temperatura, etc.)
  - Caminho para extrair o resultado do response (ex: `choices[0].message.content`)
- Permitir múltiplos providers configuráveis.

### 3.6. Fallback

- Se não houver chave/configuração de LLM, usar template local.
- Logar qual provider foi usado.

### 3.7. Segurança

- Toda resposta da LLM deve passar por validação de segurança já existente.
- Logar payloads e respostas para auditoria (sem dados sensíveis).

## 4. Fluxo Proposto

1. Recebe requisição para gerar tool/spec.
2. Verifica config: provider = "llm" ou "template" ou "hybrid".
3. Se "llm" e chave/config presente, monta payload, envia para LLM, extrai resposta.
4. Se falhar ou não houver config, usa template local.
5. Valida segurança, registra logs, retorna resultado.

---
