# 👨‍💻 Guia de Observabilidade para Desenvolvedores

## 🎯 Visão Geral

Este guia ensina como instrumentar seu código para aproveitarr a stack de observabilidade do SkyHAL.

## 📝 Logging Estruturado

### Obtendo o Logger

```python
from src.infrastructure.observability import get_observability_providers

# Obter provedores de observabilidade
logging_provider, metrics_provider, tracing_provider = get_observability_providers()

# Obter logger para seu componente
logger = logging_provider.get_logger("meu_componente")
```

### Padrões de Log

#### Log Básico
```python
# Informação simples
logger.info("Usuário autenticado com sucesso")

# Com contexto
logger.info(
    "Operação de sincronização concluída",
    operation="data_sync",
    duration_ms=150,
    records_processed=1000
)
```

#### Log de Erro
```python
try:
    result = risky_operation()
except Exception as e:
    logger.error(
        "Falha na operação",
        error=str(e),
        operation="data_processing",
        user_id=user_id,
        exc_info=True  # Adiciona stack trace
    )
```

#### Log com Correlação
```python
# O trace_id é automaticamente adicionado pelo middleware
logger.info(
    "Processando solicitação",
    user_id="12345",
    request_id="req-789",
    operation="user_profile_update"
)
```

### Níveis de Log

| Nível | Uso | Exemplo |
|-------|-----|---------|
| `DEBUG` | Informações detalhadas para debug | Valores de variáveis, fluxo detalhado |
| `INFO` | Eventos importantes do sistema | Login de usuário, operações concluídas |
| `WARNING` | Situações anômalas mas recuperáveis | Rate limit atingido, retry necessário |
| `ERROR` | Erros que afetam a operação | Falha na conexão com BD, erro de validação |
| `CRITICAL` | Erros que podem parar o sistema | Falha na inicialização, out of memory |

### Campos Obrigatórios

Sempre inclua estes campos quando relevante:

```python
logger.info(
    "Mensagem descritiva",
    # Identificação
    user_id="12345",           # ID do usuário (se aplicável)
    request_id="req-789",      # ID da requisição
    session_id="sess-456",     # ID da sessão

    # Contexto da operação
    operation="operation_name", # Nome da operação
    component="component_name", # Nome do componente

    # Métricas
    duration_ms=150,           # Duração em milissegundos
    status="success",          # Status da operação

    # Dados de negócio (sem informações sensíveis)
    count=10,                  # Quantidade de itens processados
    category="user_data"       # Categoria da operação
)
```

## 📊 Métricas

### Tipos de Métricas

#### Counter - Contadores
```python
# Incrementar contador de operações
metrics_provider.increment_counter(
    "user_operations_total",
    labels={
        "operation": "profile_update",
        "status": "success",
        "user_type": "premium"
    }
)

# Incrementar com valor específico
metrics_provider.increment_counter(
    "bytes_processed_total",
    labels={"component": "data_processor"},
    value=1024
)
```

#### Gauge - Medições Instantâneas
```python
# Definir valor atual
metrics_provider.set_gauge("active_connections", 42.0)

# Conexões ativas no pool
metrics_provider.set_gauge(
    "database_connections_active",
    connection_pool.active_count(),
    labels={"pool": "primary"}
)
```

#### Histogram - Distribuições de Valores
```python
# Medir duração de operações
start_time = time.time()
try:
    result = expensive_operation()
    status = "success"
except Exception:
    status = "error"
    raise
finally:
    duration = time.time() - start_time
    metrics_provider.observe_histogram(
        "operation_duration_seconds",
        duration,
        labels={
            "operation": "data_processing",
            "status": status
        }
    )
```

### Métricas RED Padrão

O sistema automaticamente captura métricas RED para HTTP:

- **Rate**: `http_requests_total` - Total de requisições
- **Errors**: `http_requests_total{status_code!~"2.."}` - Requisições com erro
- **Duration**: `http_request_duration_seconds` - Duração das requisições

### Métricas Customizadas

```python
class UserService:
    def __init__(self):
        _, self.metrics, _ = get_observability_providers()

    def create_user(self, user_data):
        # Incrementar tentativas
        self.metrics.increment_counter(
            "user_creation_attempts_total",
            labels={"source": "api"}
        )

        try:
            user = self._validate_and_create(user_data)

            # Sucesso
            self.metrics.increment_counter(
                "user_creation_total",
                labels={"status": "success", "user_type": user.type}
            )

            # Atualizar total de usuários
            total_users = self._get_total_users()
            self.metrics.set_gauge("users_total", total_users)

            return user

        except ValidationError as e:
            self.metrics.increment_counter(
                "user_creation_total",
                labels={"status": "validation_error"}
            )
            raise
        except Exception as e:
            self.metrics.increment_counter(
                "user_creation_total",
                labels={"status": "error"}
            )
            raise
```

## 🔍 Tracing Distribuído

### Criando Spans

#### Span Simples
```python
with tracing_provider.create_span("database_query") as span:
    span.set_attribute("table", "users")
    span.set_attribute("query_type", "select")

    result = database.query("SELECT * FROM users WHERE active = true")

    span.set_attribute("row_count", len(result))
```

#### Span com Status
```python
with tracing_provider.create_span("user_validation") as span:
    span.set_attribute("user_id", user_id)

    try:
        validation_result = validate_user(user_id)
        span.set_status("OK")
        span.set_attribute("validation_passed", True)
        return validation_result

    except ValidationError as e:
        span.set_status("ERROR", str(e))
        span.set_attribute("validation_passed", False)
        span.set_attribute("error_type", "validation")
        raise
```

#### Spans Aninhados
```python
with tracing_provider.create_span("process_order") as parent_span:
    parent_span.set_attribute("order_id", order_id)

    # Validar pedido
    with tracing_provider.create_span("validate_order") as validate_span:
        validate_span.set_attribute("order_id", order_id)
        validation_result = validate_order(order_id)
        validate_span.set_attribute("valid", validation_result.is_valid)

    # Processar pagamento
    with tracing_provider.create_span("process_payment") as payment_span:
        payment_span.set_attribute("order_id", order_id)
        payment_span.set_attribute("amount", order.total)
        payment_result = process_payment(order)
        payment_span.set_attribute("payment_id", payment_result.id)

    parent_span.set_attribute("status", "completed")
```

### Propagação de Contexto

#### Entre Funções
```python
def service_method():
    with tracing_provider.create_span("service_operation") as span:
        span.set_attribute("operation", "user_sync")

        # O contexto é propagado automaticamente
        result = call_another_service()
        return result

def call_another_service():
    # Este span será filho do anterior automaticamente
    with tracing_provider.create_span("external_service_call") as span:
        span.set_attribute("service", "user_api")
        response = requests.get("https://api.example.com/users")
        span.set_attribute("status_code", response.status_code)
        return response.json()
```

#### Para Requisições HTTP
```python
import requests
from opentelemetry.instrumentation.requests import RequestsInstrumentor

# Instrumentar automaticamente requests
RequestsInstrumentor().instrument()

def call_external_api():
    with tracing_provider.create_span("external_api_call") as span:
        span.set_attribute("api", "external_service")

        # Headers de tracing são automaticamente adicionados
        response = requests.get("https://external-api.com/data")

        span.set_attribute("status_code", response.status_code)
        return response.json()
```

## 🔗 Correlação entre Logs, Métricas e Traces

### Exemplo Completo

```python
from src.infrastructure.observability import get_observability_providers
import time

class OrderProcessor:
    def __init__(self):
        self.logger, self.metrics, self.tracing = get_observability_providers()
        self.logger = self.logger.get_logger("order_processor")

    def process_order(self, order_id: str, user_id: str):
        with self.tracing.create_span("process_order") as span:
            # Configurar contexto do span
            span.set_attribute("order_id", order_id)
            span.set_attribute("user_id", user_id)

            # Log inicial (trace_id é automaticamente incluído)
            self.logger.info(
                "Iniciando processamento do pedido",
                order_id=order_id,
                user_id=user_id,
                operation="process_order"
            )

            # Métrica: tentativa de processamento
            self.metrics.increment_counter(
                "order_processing_attempts_total",
                labels={"user_type": "premium"}
            )

            start_time = time.time()

            try:
                # Simular processamento
                result = self._validate_and_process(order_id, user_id, span)

                # Sucesso
                duration = time.time() - start_time

                span.set_status("OK")
                span.set_attribute("status", "success")

                self.logger.info(
                    "Pedido processado com sucesso",
                    order_id=order_id,
                    user_id=user_id,
                    duration_ms=int(duration * 1000),
                    status="success"
                )

                self.metrics.increment_counter(
                    "orders_processed_total",
                    labels={"status": "success"}
                )

                self.metrics.observe_histogram(
                    "order_processing_duration_seconds",
                    duration,
                    labels={"status": "success"}
                )

                return result

            except Exception as e:
                duration = time.time() - start_time

                span.set_status("ERROR", str(e))
                span.set_attribute("status", "error")
                span.set_attribute("error_type", type(e).__name__)

                self.logger.error(
                    "Falha no processamento do pedido",
                    order_id=order_id,
                    user_id=user_id,
                    error=str(e),
                    duration_ms=int(duration * 1000),
                    status="error",
                    exc_info=True
                )

                self.metrics.increment_counter(
                    "orders_processed_total",
                    labels={"status": "error"}
                )

                self.metrics.observe_histogram(
                    "order_processing_duration_seconds",
                    duration,
                    labels={"status": "error"}
                )

                raise

    def _validate_and_process(self, order_id: str, user_id: str, parent_span):
        with self.tracing.create_span("validate_order", parent=parent_span) as span:
            span.set_attribute("order_id", order_id)

            # Simular validação
            if order_id.startswith("invalid"):
                raise ValueError("Pedido inválido")

            self.logger.debug(
                "Pedido validado",
                order_id=order_id,
                validation_status="passed"
            )

            return {"order_id": order_id, "status": "processed"}
```

## 🛠️ Ferramentas de Debug

### Testando Instrumentação

```python
# Script para testar instrumentação local
if __name__ == "__main__":
    processor = OrderProcessor()

    # Teste de sucesso
    try:
        result = processor.process_order("order_123", "user_456")
        print(f"Sucesso: {result}")
    except Exception as e:
        print(f"Erro: {e}")

    # Teste de erro
    try:
        result = processor.process_order("invalid_order", "user_456")
    except Exception as e:
        print(f"Erro esperado: {e}")
```

### Verificando Dados

```bash
# Ver métricas expostas pela aplicação
curl http://localhost:8000/metrics

# Ver traces no Jaeger
# Abrir http://localhost:16686 e procurar por spans

# Ver logs estruturados
docker-compose logs skyhal-api | grep "order_processing"
```

## 📋 Checklist de Instrumentação

### Para Cada Nova Funcionalidade

- [ ] **Logging**
  - [ ] Logs de início e fim de operações importantes
  - [ ] Logs de erro com contexto suficiente
  - [ ] Campos obrigatórios incluídos
  - [ ] Sem informações sensíveis nos logs

- [ ] **Métricas**
  - [ ] Counters para eventos importantes
  - [ ] Gauges para valores atuais
  - [ ] Histogramas para durações
  - [ ] Labels apropriados

- [ ] **Tracing**
  - [ ] Spans para operações principais
  - [ ] Atributos descritivos nos spans
  - [ ] Status apropriado (OK/ERROR)
  - [ ] Propagação de contexto

- [ ] **Correlação**
  - [ ] IDs consistentes entre logs, métricas e traces
  - [ ] Contexto suficiente para debug
  - [ ] Performance medida adequadamente

## 🚨 Alertas Importantes

### O que NÃO fazer

```python
# ❌ NÃO incluir dados sensíveis
logger.info("Login", password=user_password)  # NUNCA!

# ❌ NÃO criar métricas com cardinalidade alta
metrics.increment_counter(
    "requests_total",
    labels={"user_id": user_id}  # Pode ser milhões de valores!
)

# ❌ NÃO criar spans em loops densos
for item in huge_list:  # Milhares de items
    with tracing.create_span("process_item"):  # Muitos spans!
        process(item)
```

### Boas Práticas

```python
# ✅ Dados sensíveis mascarados ou omitidos
logger.info("Login", username=username[:3] + "***")

# ✅ Cardinalidade controlada
metrics.increment_counter(
    "requests_total",
    labels={"user_type": get_user_type(user_id)}  # Poucos valores
)

# ✅ Spans em operações significativas
with tracing.create_span("process_batch") as span:
    span.set_attribute("batch_size", len(huge_list))
    for item in huge_list:
        process(item)  # Sem spans individuais
    span.set_attribute("processed_count", processed_count)
```
