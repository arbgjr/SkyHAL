# Guia de uso: Geração de Código via LLM

## Como adicionar um novo provider LLM

### Exemplo prático: Integração com MyAI

#### 1. Implementação do client

Crie `src/infrastructure/llm_client_myai.py`:

```python
import httpx

class MyAILLMClient:
    def __init__(self, base_url, api_key, model="o4-mini", timeout=30):
        self.base_url = base_url
        self.api_key = api_key
        self.model = model
        self.timeout = timeout

    async def generate_code(self, prompt, temperature=0.7, max_tokens=5000, extra_params=None):
        system_prompt = (
            "Você é um assistente para ajudar as pessoas a gerar código python de forma segura para ser usado como um agent de um MCP server. "
            "Sempre responda SOMENTE o código, sem explicação, e sempre um código completo em um único arquivo."
        )
        payload = {
            "knowledge_base": None,
            "llm_family": "openai",
            "model": self.model,
            "max_output_tokens": max_tokens,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "human", "content": prompt}
            ],
            "temperature": temperature
        }
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "accept": "*/*"
        }
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.post(self.base_url, json=payload, headers=headers)
            response.raise_for_status()
            data = response.json()
            # Extrai apenas o código do campo message.content, removendo markdown se necessário
            content = data.get("message", {}).get("content", "")
            if content.startswith("```python"):
                content = content.removeprefix("```python").removesuffix("```")
            return content.strip()
```

#### 2. Configuração do payload

```json
{
  "provider": "llm",
  "llm_config": {
    "provider": "myai",
    "model": "o4-mini"
  },
  "name": "soma",
  "description": "Função que soma dois números inteiros"
}
```

#### 3. Variáveis de ambiente

```
LLM_API_URL=http://localhost:8080/api/v3/chat/completions
LLM_API_KEY=xyxabc123
LLM_MODEL=o4-mini
```

#### 4. Observações

- O campo de resposta relevante é `message.content`.
- O client já remove o markdown ```python do início/fim.
- O system prompt foi adaptado para garantir resposta só com código, sem explicação.

### 1. Implementação de um novo client LLM

- Crie um novo client Python em `src/infrastructure/llm_client_<provider>.py` seguindo o padrão do `llm_client.py`.
- O client deve implementar um método `async generate_code(prompt, temperature, max_tokens, extra_params)`.
- Adapte o orquestrador (`src/application/llm_code_orchestrator.py`) para aceitar o novo provider, usando lógica condicional ou uma factory.
- Exemplo de estrutura mínima:

```python
class NovoProviderLLMClient:
    async def generate_code(self, prompt, temperature=0.2, max_tokens=1024, extra_params=None):
        # Implemente a chamada HTTP para o novo provider
        ...
```

### 2. Configuração do payload para o novo provider

No payload da requisição, use:

```json
{
  "provider": "llm",
  "llm_config": {
    "provider": "nome_do_provider",
    "model": "nome_do_modelo"
    // outros parâmetros se necessário
  }
}
```

### 3. Testes

- Adicione testes unitários e de integração para o novo client e fluxo.
- Teste o endpoint `/llm-codegen/generate` com o novo provider.

---

## Como configurar variáveis de ambiente para LLMs

### OpenAI (padrão)

```
LLM_API_URL=https://api.openai.com
LLM_API_KEY=sua-chave-openai
LLM_MODEL=gpt-4
```

### Exemplo para outro provider (ex: Anthropic, Azure, Mistral)

```
LLM_API_URL=https://api.anthropic.com
LLM_API_KEY=sua-chave-anthropic
LLM_MODEL=claude-3-opus
# Parâmetros extras se necessário:
LLM_API_VERSION=v1
LLM_TENANT_ID=...
```

## Visão Geral

Permite gerar código Python automaticamente a partir de prompts usando LLMs (ex: OpenAI GPT-4) via API REST.

## Pré-requisitos

- Definir as variáveis de ambiente conforme o provider desejado (ver exemplos acima)
- Usuário autenticado (OAuth2 Bearer Token)

## Passo a Passo

### 1. Enviar requisição para geração de código

```bash
curl -X POST http://localhost:8000/llm-codegen/generate \
  -H "Authorization: Bearer <TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Crie uma função Python que soma dois números"}'
```

### 2. Resposta esperada (exemplo real)

```json
{
  "code": "def soma(a, b):\n    return a + b",
  "validation_results": {"passed": true, "score": 0.95, "issues_count": 0},
  "trace_id": "e1f2a3b4c5d6e7f8",
  "metrics": {
    "latency_seconds": 0.42,
    "quota_remaining": 97
  }
}
```

## Exemplos de Prompt

- "Crie uma função Python que soma dois números"
- "Implemente um endpoint FastAPI para health check"
- "Gere uma classe Pydantic para usuário com validação de email"

## Observabilidade

- Todas as requisições são rastreadas via OpenTelemetry (trace_id incluso na resposta)
- Métricas Prometheus expostas: `llm_codegen_requests_total`, `llm_codegen_latency_seconds`
- Logs estruturados (structlog) com contexto de usuário, prompt e status

## Limitações e Segurança

- Limite de 3 requisições por minuto por usuário (rate limiting)
- Código gerado é sanitizado para evitar comandos perigosos (ex: `os`, `sys`, `exec`, `eval`, `subprocess`, `open`)
- Prompts muito curtos retornam 400
- Erros de autenticação retornam 401
- Respostas inseguras ou inválidas são bloqueadas
- Não exponha segredos ou dados sensíveis em prompts

## Troubleshooting

- 401 Unauthorized: Verifique o token
- 400 Bad Request: Prompt inválido, código inseguro ou quota excedida
- 500 Internal Error: Falha na comunicação com o LLM

## Fluxo Fim a Fim

1. Usuário envia prompt autenticado para `/llm-codegen/generate`
2. API valida autenticação, quota e formato do prompt
3. Orquestrador aciona LLM, sanitiza e valida o código gerado
4. Resposta inclui código, validação, trace_id e métricas
5. Logs e métricas são registrados para auditoria e monitoramento

> Para payloads avançados, fallback, critérios de segurança e integração, consulte `docs/especificacoes-tecnicas/llm-auto-extensao.md`.
