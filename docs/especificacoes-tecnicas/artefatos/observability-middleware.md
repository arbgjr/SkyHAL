# Especificação Técnica: Middleware de Observabilidade

## 📁 Artefato

**Caminho:** `src/application/middleware/observability_middleware.py`

## 🎯 Objetivo

Implementar middleware FastAPI para instrumentação automática de requisições HTTP, capturando métricas RED (Rate, Errors, Duration), traces e logs correlacionados.

## 📚 Instruções Relacionadas

- **observabilidade.instructions.md** - Padrões de instrumentação e métricas RED
- **api-security.instructions.md** - Não expor dados sensíveis em logs
- **python-mcp.instructions.md** - Padrões de middleware e Clean Architecture

## 🎨 Prompts Relacionados

- **observabilidade.prompt.md** - Instrumentação de endpoints
- **clean-architecture.prompt.md** - Organização de camadas

## 🎯 Chat Mode Recomendado

- **backend.chatmode.md** - Para implementação de middleware

## 🏗️ Estrutura de Arquivos

```
src/application/middleware/
├── __init__.py
├── observability_middleware.py    # Middleware principal
├── metrics_middleware.py          # Middleware específico de métricas
├── tracing_middleware.py          # Middleware específico de tracing
└── logging_middleware.py          # Middleware específico de logging
```

## 🛠️ Implementação Técnica

### 1. Middleware Principal (`observability_middleware.py`)

```python
import time
from typing import Callable
import structlog
from fastapi import Request, Response
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from opentelemetry import trace
from src.infrastructure.observability.providers.telemetry_provider import TelemetryProvider
from src.infrastructure.observability.collectors.metrics_collector import MetricsCollector

class ObservabilityMiddleware(BaseHTTPMiddleware):
    """Middleware para instrumentação automática de observabilidade."""

    def __init__(
        self,
        app,
        telemetry_provider: TelemetryProvider,
        metrics_collector: MetricsCollector
    ):
        super().__init__(app)
        self.logger = telemetry_provider.get_logger(__name__)
        self.tracer = telemetry_provider.get_tracer(__name__)
        self.metrics = metrics_collector

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """Processa requisição com instrumentação completa."""

        start_time = time.time()
        method = request.method
        path = str(request.url.path)

        # Inicia span para a requisição
        with self.tracer.start_as_current_span(
            f"http_request_{method.lower()}",
            attributes={
                "http.method": method,
                "http.url": str(request.url),
                "http.path": path,
                "http.user_agent": request.headers.get("user-agent", ""),
            }
        ) as span:

            # Log de início da requisição
            self.logger.info(
                "http_request_started",
                method=method,
                path=path,
                remote_addr=request.client.host if request.client else None
            )

            try:
                # Processa requisição
                response = await call_next(request)

                # Calcula duração
                duration = time.time() - start_time
                status_code = response.status_code
                status = "success" if status_code < 400 else "error"

                # Atualiza span com informações de resposta
                span.set_attribute("http.status_code", status_code)
                span.set_attribute("http.response.duration", duration)

                # Registra métricas
                self.metrics.increment_request_count(method, path, status)
                self.metrics.record_request_duration(method, duration)

                if status_code >= 400:
                    error_type = self._get_error_type(status_code)
                    self.metrics.increment_error_count(error_type)

                # Log de conclusão da requisição
                self.logger.info(
                    "http_request_completed",
                    method=method,
                    path=path,
                    status_code=status_code,
                    duration_ms=round(duration * 1000, 2),
                    status=status
                )

                return response

            except Exception as e:
                # Calcula duração em caso de erro
                duration = time.time() - start_time

                # Atualiza span com erro
                span.set_status(trace.Status(trace.StatusCode.ERROR))
                span.record_exception(e)

                # Registra métricas de erro
                self.metrics.increment_request_count(method, path, "error")
                self.metrics.record_request_duration(method, duration)
                self.metrics.increment_error_count("internal_server_error")

                # Log de erro
                self.logger.error(
                    "http_request_failed",
                    method=method,
                    path=path,
                    duration_ms=round(duration * 1000, 2),
                    error=str(e),
                    exc_info=True
                )

                # Retorna resposta de erro estruturada
                return JSONResponse(
                    status_code=500,
                    content={
                        "error": {
                            "code": 500,
                            "message": "Erro interno do servidor",
                            "trace_id": format(span.get_span_context().trace_id, "032x")
                        }
                    }
                )

    def _get_error_type(self, status_code: int) -> str:
        """Determina tipo de erro baseado no status code."""
        if 400 <= status_code < 500:
            return "client_error"
        elif 500 <= status_code < 600:
            return "server_error"
        else:
            return "unknown_error"
```

### 2. Coletor de Métricas (`collectors/metrics_collector.py`)

```python
from opentelemetry import metrics
from opentelemetry.metrics import Counter, Histogram
from typing import Dict, Any

class MetricsCollector:
    """Coletor de métricas RED para observabilidade."""

    def __init__(self, meter_provider):
        self.meter = meter_provider.get_meter(__name__)

        # Métricas RED
        self._request_counter = self.meter.create_counter(
            name="app_http_requests_total",
            description="Total de requisições HTTP",
            unit="1"
        )

        self._request_duration = self.meter.create_histogram(
            name="app_http_request_duration_seconds",
            description="Duração das requisições HTTP",
            unit="s"
        )

        self._error_counter = self.meter.create_counter(
            name="app_errors_total",
            description="Total de erros",
            unit="1"
        )

    def increment_request_count(self, method: str, path: str, status: str) -> None:
        """Incrementa contador de requisições."""
        self._request_counter.add(
            1,
            attributes={
                "method": method,
                "path": self._sanitize_path(path),
                "status": status
            }
        )

    def record_request_duration(self, method: str, duration: float) -> None:
        """Registra duração de requisição."""
        self._request_duration.record(
            duration,
            attributes={"method": method}
        )

    def increment_error_count(self, error_type: str) -> None:
        """Incrementa contador de erros."""
        self._error_counter.add(
            1,
            attributes={"type": error_type}
        )

    def _sanitize_path(self, path: str) -> str:
        """Sanitiza path para evitar alta cardinalidade em métricas."""
        # Remove IDs dinâmicos dos paths
        import re

        # Substitui números por placeholder
        sanitized = re.sub(r'/\d+', '/{id}', path)

        # Substitui UUIDs por placeholder
        sanitized = re.sub(
            r'/[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}',
            '/{uuid}',
            sanitized,
            flags=re.IGNORECASE
        )

        return sanitized
```

### 3. Configuração no FastAPI (`presentation/api/app.py`)

```python
from fastapi import FastAPI
from src.application.middleware.observability_middleware import ObservabilityMiddleware
from src.infrastructure.observability.providers.telemetry_provider import TelemetryProvider
from src.infrastructure.observability.collectors.metrics_collector import MetricsCollector

def create_app() -> FastAPI:
    """Cria aplicação FastAPI com middleware de observabilidade."""

    app = FastAPI(
        title="SkyHAL API",
        description="Assistente de IA para automação e gerenciamento de infraestrutura",
        version="0.1.0"
    )

    # Configura observabilidade
    telemetry_provider = TelemetryProvider()
    metrics_collector = MetricsCollector(telemetry_provider.meter_provider)

    # Adiciona middleware de observabilidade
    app.add_middleware(
        ObservabilityMiddleware,
        telemetry_provider=telemetry_provider,
        metrics_collector=metrics_collector
    )

    return app
```

## 📋 Recursos Implementados

### Métricas RED Capturadas

- **Rate:** `app_http_requests_total{method, path, status}`
- **Errors:** `app_errors_total{type}`
- **Duration:** `app_http_request_duration_seconds{method}`

### Logs Estruturados

```json
{
  "timestamp": "2025-06-24T10:30:45.123Z",
  "level": "info",
  "event": "http_request_completed",
  "method": "GET",
  "path": "/health",
  "status_code": 200,
  "duration_ms": 12.34,
  "status": "success",
  "trace_id": "abcd1234...",
  "span_id": "efgh5678..."
}
```

### Traces Distribuídos

- Span por requisição HTTP
- Atributos padrão: method, url, status_code, duration
- Propagação de contexto automática
- Correlação com logs via trace_id

## ✅ Checklist de Implementação

- [ ] Implementar middleware principal de observabilidade
- [ ] Criar coletor de métricas RED
- [ ] Configurar correlação entre logs, métricas e traces
- [ ] Implementar sanitização de paths para métricas
- [ ] Adicionar tratamento de erros estruturado
- [ ] Configurar middleware no FastAPI
- [ ] Implementar testes unitários (cobertura >= 80%)
- [ ] Validar não exposição de dados sensíveis
- [ ] Documentar configuração e uso

## 🔗 Dependências de Outros Artefatos

- **observability-infrastructure.md** - Usa providers e configurações
- **observability-config.md** - Parâmetros de configuração

## 📝 Notas Técnicas

- Middleware processa todas as requisições automaticamente
- Métricas seguem padrão Prometheus com labels adequadas
- Logs incluem trace_id para correlação
- Sanitização de paths previne alta cardinalidade
- Tratamento de erros retorna trace_id para debugging
