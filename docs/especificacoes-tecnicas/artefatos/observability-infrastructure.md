# Especificação Técnica: Infraestrutura de Observabilidade

## 📁 Artefato
**Caminho:** `src/infrastructure/observability/`

## 🎯 Objetivo
Implementar a infraestrutura base de observabilidade seguindo Clean Architecture, incluindo configuração de OpenTelemetry, logging estruturado e métricas.

## 📚 Instruções Relacionadas
- **observabilidade.instructions.md** - Padrões de nomenclatura e configuração
- **python-mcp.instructions.md** - Padrões Python e Clean Architecture
- **api-security.instructions.md** - Não expor dados sensíveis em logs

## 🎨 Prompts Relacionados
- **observabilidade.prompt.md** - Prompt específico para implementação
- **clean-architecture.prompt.md** - Manter aderência arquitetural

## 🎯 Chat Mode Recomendado
- **arquiteto.chatmode.md** - Para decisões de arquitetura da stack

## 🏗️ Estrutura de Arquivos

```
src/infrastructure/observability/
├── __init__.py
├── config/
│   ├── __init__.py
│   ├── logging_config.py      # Configuração structlog
│   ├── metrics_config.py      # Configuração métricas OpenTelemetry
│   ├── tracing_config.py      # Configuração tracing OpenTelemetry
│   └── exporters_config.py    # Configuração exportadores
├── providers/
│   ├── __init__.py
│   ├── telemetry_provider.py  # Provider principal OpenTelemetry
│   ├── metrics_provider.py    # Provider de métricas
│   └── logger_provider.py     # Provider de logging
├── collectors/
│   ├── __init__.py
│   ├── metrics_collector.py   # Coletor de métricas RED
│   └── trace_collector.py     # Coletor de traces
└── interfaces/
    ├── __init__.py
    ├── observability.py       # Interfaces base
    └── metrics.py             # Interfaces de métricas
```

## 🛠️ Implementação Técnica

### 1. Interface Base (`interfaces/observability.py`)
```python
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
from opentelemetry.trace import Span
from structlog import BoundLogger

class IObservabilityProvider(ABC):
    """Interface para provider de observabilidade."""

    @abstractmethod
    def get_logger(self, name: str) -> BoundLogger:
        """Retorna logger estruturado."""
        pass

    @abstractmethod
    def get_tracer(self, name: str) -> Any:
        """Retorna tracer OpenTelemetry."""
        pass

    @abstractmethod
    def get_meter(self, name: str) -> Any:
        """Retorna meter para métricas."""
        pass

class IMetricsCollector(ABC):
    """Interface para coletor de métricas."""

    @abstractmethod
    def increment_request_count(self, method: str, path: str, status: str) -> None:
        """Incrementa contador de requisições."""
        pass

    @abstractmethod
    def record_request_duration(self, method: str, duration: float) -> None:
        """Registra duração de requisição."""
        pass

    @abstractmethod
    def increment_error_count(self, error_type: str) -> None:
        """Incrementa contador de erros."""
        pass
```

### 2. Configuração de Logging (`config/logging_config.py`)
```python
import structlog
import logging
from typing import Dict, Any
from opentelemetry import trace

class LoggingConfig:
    """Configuração de logging estruturado com structlog."""

    @staticmethod
    def configure_structlog() -> None:
        """Configura structlog para logs JSON com correlação."""

        def add_trace_info(logger, method_name, event_dict):
            """Adiciona informações de trace aos logs."""
            span = trace.get_current_span()
            if span and span.is_recording():
                span_context = span.get_span_context()
                event_dict["trace_id"] = format(span_context.trace_id, "032x")
                event_dict["span_id"] = format(span_context.span_id, "016x")
            return event_dict

        structlog.configure(
            processors=[
                structlog.stdlib.filter_by_level,
                structlog.stdlib.add_logger_name,
                structlog.stdlib.add_log_level,
                structlog.stdlib.PositionalArgumentsFormatter(),
                structlog.processors.TimeStamper(fmt="iso"),
                add_trace_info,
                structlog.processors.StackInfoRenderer(),
                structlog.processors.format_exc_info,
                structlog.processors.UnicodeDecoder(),
                structlog.processors.JSONRenderer()
            ],
            context_class=dict,
            logger_factory=structlog.stdlib.LoggerFactory(),
            wrapper_class=structlog.stdlib.BoundLogger,
            cache_logger_on_first_use=True,
        )
```

### 3. Configuração de Métricas (`config/metrics_config.py`)
```python
from opentelemetry import metrics
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.exporter.prometheus import PrometheusMetricReader
from prometheus_client import start_http_server
from typing import Optional

class MetricsConfig:
    """Configuração de métricas OpenTelemetry com Prometheus."""

    def __init__(self, port: int = 8000):
        self.port = port
        self._meter_provider: Optional[MeterProvider] = None

    def configure_metrics(self) -> MeterProvider:
        """Configura provider de métricas com exportador Prometheus."""

        # Inicia servidor Prometheus
        start_http_server(port=self.port)

        # Configura reader Prometheus
        reader = PrometheusMetricReader()

        # Cria provider de métricas
        self._meter_provider = MeterProvider(metric_readers=[reader])
        metrics.set_meter_provider(self._meter_provider)

        return self._meter_provider

    @property
    def meter_provider(self) -> MeterProvider:
        """Retorna meter provider configurado."""
        if not self._meter_provider:
            self.configure_metrics()
        return self._meter_provider
```

### 4. Provider Principal (`providers/telemetry_provider.py`)
```python
from typing import Any
import structlog
from opentelemetry import trace, metrics
from .interfaces.observability import IObservabilityProvider
from .config.logging_config import LoggingConfig
from .config.metrics_config import MetricsConfig
from .config.tracing_config import TracingConfig

class TelemetryProvider(IObservabilityProvider):
    """Provider principal de telemetria."""

    def __init__(self):
        self._configure_all()

    def _configure_all(self) -> None:
        """Configura todos os componentes de observabilidade."""
        LoggingConfig.configure_structlog()

        self._metrics_config = MetricsConfig()
        self._metrics_config.configure_metrics()

        self._tracing_config = TracingConfig()
        self._tracing_config.configure_tracing()

    def get_logger(self, name: str) -> structlog.BoundLogger:
        """Retorna logger estruturado."""
        return structlog.get_logger(name)

    def get_tracer(self, name: str) -> Any:
        """Retorna tracer OpenTelemetry."""
        return trace.get_tracer(name)

    def get_meter(self, name: str) -> Any:
        """Retorna meter para métricas."""
        return metrics.get_meter(name)
```

## 📋 Dependências Adicionais Necessárias

```toml
# Adicionar ao pyproject.toml
opentelemetry-exporter-prometheus = "^1.20.0"
opentelemetry-exporter-otlp = "^1.20.0"
opentelemetry-instrumentation-logging = "^0.41b0"
prometheus-client = "^0.17.0"
```

## ✅ Checklist de Implementação

- [ ] Implementar interfaces base de observabilidade
- [ ] Configurar structlog com correlação de traces
- [ ] Configurar métricas OpenTelemetry + Prometheus
- [ ] Configurar tracing distribuído
- [ ] Implementar provider principal
- [ ] Criar coletores de métricas RED
- [ ] Adicionar testes unitários (cobertura >= 80%)
- [ ] Validar não exposição de dados sensíveis
- [ ] Documentar configurações e uso

## 🔗 Dependências de Outros Artefatos

- **observability-middleware.md** - Usa os providers criados aqui
- **dependencies-update.md** - Adiciona dependências necessárias
- **observability-config.md** - Configura parâmetros via YAML

## 📝 Notas Técnicas

- Seguir padrões de nomenclatura do `observabilidade.instructions.md`
- Implementar seguindo Clean Architecture (camada Infrastructure)
- Garantir configuração flexível via injeção de dependências
- Implementar lazy loading para evitar overhead desnecessário
- Validar sanitização de dados sensíveis em logs
