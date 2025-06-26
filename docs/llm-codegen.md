# Guia de uso: Geração de Código via LLM

## Visão Geral

Permite gerar código Python automaticamente a partir de prompts usando LLMs (ex: OpenAI GPT-4) via API REST.

## Pré-requisitos

- Variáveis de ambiente:
  - LLM_API_URL
  - LLM_API_KEY
  - LLM_MODEL
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
