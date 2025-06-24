---
applyTo: "**"
---
# 🛰️ Observabilidade - Padrões e Boas Práticas

## Objetivo
Garantir rastreabilidade ponta a ponta, diagnóstico rápido e confiável, e padronização de sinais (logs, métricas, traces) em todos os microserviços .NET do projeto.

## Ferramentas Obrigatórias
- **Métricas:** OpenTelemetry + Prometheus
- **Tracing:** OpenTelemetry + Jaeger
- **Logs:** Serilog (JSON) + Loki
- **Visualização:** Grafana

## Padrões de Nomenclatura
- **Métricas:**
  - `servico_operacao_requests_total` (ex: `mensagem_entrada_requests_total`)
  - `servico_operacao_errors_total`
  - `servico_operacao_duration_seconds`
- **Spans/Traces:**
  - Nome: Serviço + Operação (ex: `MSG.Mensagem.EntradaIntegracao.ProcessarMensagem`)
  - Atributos obrigatórios: `mensagem_id`, `usuario`, `status`

## Instrumentação Obrigatória
- Todos endpoints HTTP (APIs)
- Chamadas a bancos de dados e mensageria (Kafka, MQ)
- Operações críticas de negócio

## Logging Estruturado
- Sempre em JSON
- Incluir `trace_id` e `span_id` em todos os logs
- Nunca logar dados sensíveis

## Correlacionamento
- O `trace_id` deve estar presente em logs, métricas e traces para rastreabilidade ponta a ponta

## Exemplos
- Métrica: `mensagem_entrada_requests_total{status="success"}`
- Log: `{ "level": "Information", "mensagemId": "123", "trace_id": "..." }`
- Span: `MSG.Mensagem.EntradaIntegracao.ProcessarMensagem`

## Referências
- `docs/observabilidade/Padrões_de_Observabilidade.md`
- Exemplos práticos em `docs/observabilidade/`

---

# 🛰️ Observabilidade - Padrões e Boas Práticas Python

## 🎯 Objetivos
- Rastreabilidade ponta a ponta
- Diagnóstico rápido e confiável
- Padronização de sinais

## 🛠️ Stack de Observabilidade

### Ferramentas
- **Métricas**: OpenTelemetry + Prometheus
- **Tracing**: OpenTelemetry + Jaeger
- **Logs**: Structlog + Loki
- **Visualização**: Grafana

### Configuração OpenTelemetry
```python
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

# Configuração do Provider
provider = TracerProvider()
processor = BatchSpanProcessor(OTLPSpanExporter())
provider.add_span_processor(processor)
trace.set_tracer_provider(provider)

# Tracer para o serviço
tracer = trace.get_tracer(__name__)
```

### Logging Estruturado
```python
import structlog

# Configuração do logger
structlog.configure(
    processors=[
        structlog.processors.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.JSONRenderer()
    ],
)

logger = structlog.get_logger()

# Uso correto
logger.info(
    "user_action",
    user_id=user.id,
    action="login",
    status="success"
)
```

## 📊 Métricas Padrão

### Nomenclatura
- **Requests**: `app_http_requests_total{method="GET", path="/users"}`
- **Latência**: `app_http_request_duration_seconds{method="POST"}`
- **Erros**: `app_errors_total{type="validation"}`

### Implementação
```python
from prometheus_client import Counter, Histogram
from functools import wraps

# Métricas
requests = Counter(
    'app_http_requests_total',
    'Total de requisições HTTP',
    ['method', 'path']
)

latency = Histogram(
    'app_http_request_duration_seconds',
    'Latência das requisições HTTP',
    ['method']
)

# Decorator para endpoints
def track_metrics(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        requests.labels(method="GET", path="/users").inc()
        with latency.labels(method="GET").time():
            return await func(*args, **kwargs)
    return wrapper
```

## 🔍 Tracing

### Padrões de Span
- Nome: `<servico>.<modulo>.<operacao>`
- Atributos obrigatórios: `user_id`, `trace_id`, `status`

### Implementação
```python
@router.get("/users/{user_id}")
async def get_user(user_id: int):
    with tracer.start_as_current_span(
        "user_service.get_user"
    ) as span:
        span.set_attribute("user_id", user_id)
        try:
            user = await user_service.get_user(user_id)
            span.set_status(Status(StatusCode.OK))
            return user
        except Exception as e:
            span.set_status(Status(StatusCode.ERROR))
            span.record_exception(e)
            raise
```

## ✅ Checklist de Implementação

### Métricas (RED)
- [ ] Rate (requests/segundo)
- [ ] Errors (erros/segundo)
- [ ] Duration (latência)

### Traces
- [ ] Spans nomeados corretamente
- [ ] Atributos obrigatórios
- [ ] Propagação de contexto
- [ ] Gestão de erros

### Logs
- [ ] Formato JSON
- [ ] Campos obrigatórios
- [ ] Níveis apropriados
- [ ] Sanitização de dados

### Alertas
- [ ] Latência > 500ms
- [ ] Error rate > 1%
- [ ] Saturação de recursos
- [ ] Falhas de dependências
