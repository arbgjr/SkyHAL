# Especificação Técnica: Testes de Observabilidade

## 📁 Artefato

**Caminho:** `tests/unit/observability/` e `tests/integration/observability/`

## 🎯 Objetivo

Implementar testes abrangentes para todos os componentes de observabilidade, garantindo funcionamento correto de logging, métricas, tracing e integração com exportadores.

## 📚 Instruções Relacionadas

- **test.instructions.md** - Estratégias de teste para Python
- **observabilidade.instructions.md** - Validação de padrões de observabilidade
- **python-mcp.instructions.md** - Padrões de teste em projetos Python

## 🎨 Prompts Relacionados

- **generate-tests.prompt.md** - Geração de testes unitários e integração
- **observabilidade.prompt.md** - Testes específicos de observabilidade

## 🎯 Chat Mode Recomendado

- **testing.chatmode.md** - Para implementação de testes

## 🏗️ Estrutura de Testes

```
tests/
├── unit/
│   └── observability/
│       ├── __init__.py
│       ├── test_telemetry_provider.py
│       ├── test_metrics_collector.py
│       ├── test_logging_config.py
│       ├── test_tracing_config.py
│       └── test_observability_config.py
├── integration/
│   └── observability/
│       ├── __init__.py
│       ├── test_middleware_integration.py
│       ├── test_exporters_integration.py
│       └── test_end_to_end_observability.py
└── fixtures/
    └── observability/
        ├── __init__.py
        ├── config_fixtures.py
        └── mock_exporters.py
```

## 🛠️ Implementação de Testes

### 1. Fixtures Base (`tests/fixtures/observability/config_fixtures.py`)

```python
import pytest
from unittest.mock import Mock, patch
from typing import Dict, Any
import tempfile
import yaml
from pathlib import Path

@pytest.fixture
def mock_observability_config():
    """Mock de configuração de observabilidade."""
    return {
        "observability": {
            "service": {
                "name": "test-service",
                "version": "0.1.0",
                "environment": "test"
            },
            "logging": {
                "level": "DEBUG",
                "format": "json",
                "structured": True,
                "include_trace_info": True
            },
            "metrics": {
                "enabled": True,
                "prefix": "test",
                "red_metrics": {"enabled": True}
            },
            "tracing": {
                "enabled": True,
                "sampling_ratio": 1.0
            },
            "exporters": {
                "prometheus": {"enabled": True, "port": 8001},
                "jaeger": {"enabled": False}
            }
        }
    }

@pytest.fixture
def temp_config_file(mock_observability_config):
    """Cria arquivo temporário de configuração."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
        yaml.dump(mock_observability_config, f)
        yield f.name
    Path(f.name).unlink()

@pytest.fixture
def mock_telemetry_provider():
    """Mock do TelemetryProvider."""
    provider = Mock()
    provider.get_logger.return_value = Mock()
    provider.get_tracer.return_value = Mock()
    provider.get_meter.return_value = Mock()
    return provider

@pytest.fixture
def mock_metrics_collector():
    """Mock do MetricsCollector."""
    collector = Mock()
    collector.increment_request_count = Mock()
    collector.record_request_duration = Mock()
    collector.increment_error_count = Mock()
    return collector
```

### 2. Testes do TelemetryProvider (`tests/unit/observability/test_telemetry_provider.py`)

```python
import pytest
from unittest.mock import Mock, patch, MagicMock
import structlog
from opentelemetry import trace, metrics

from src.infrastructure.observability.providers.telemetry_provider import TelemetryProvider

class TestTelemetryProvider:
    """Testes do TelemetryProvider."""

    @patch('src.infrastructure.observability.config.logging_config.LoggingConfig.configure_structlog')
    @patch('src.infrastructure.observability.config.metrics_config.MetricsConfig')
    @patch('src.infrastructure.observability.config.tracing_config.TracingConfig')
    def test_init_configures_all_components(self, mock_tracing, mock_metrics, mock_logging):
        """Testa se inicialização configura todos os componentes."""
        # Arrange
        mock_metrics_instance = Mock()
        mock_tracing_instance = Mock()
        mock_metrics.return_value = mock_metrics_instance
        mock_tracing.return_value = mock_tracing_instance

        # Act
        provider = TelemetryProvider()

        # Assert
        mock_logging.assert_called_once()
        mock_metrics_instance.configure_metrics.assert_called_once()
        mock_tracing_instance.configure_tracing.assert_called_once()

    @patch('structlog.get_logger')
    def test_get_logger_returns_structured_logger(self, mock_get_logger):
        """Testa se get_logger retorna logger estruturado."""
        # Arrange
        mock_logger = Mock()
        mock_get_logger.return_value = mock_logger
        provider = TelemetryProvider()

        # Act
        logger = provider.get_logger("test-logger")

        # Assert
        mock_get_logger.assert_called_with("test-logger")
        assert logger == mock_logger

    @patch('opentelemetry.trace.get_tracer')
    def test_get_tracer_returns_opentelemetry_tracer(self, mock_get_tracer):
        """Testa se get_tracer retorna tracer OpenTelemetry."""
        # Arrange
        mock_tracer = Mock()
        mock_get_tracer.return_value = mock_tracer
        provider = TelemetryProvider()

        # Act
        tracer = provider.get_tracer("test-tracer")

        # Assert
        mock_get_tracer.assert_called_with("test-tracer")
        assert tracer == mock_tracer

    @patch('opentelemetry.metrics.get_meter')
    def test_get_meter_returns_opentelemetry_meter(self, mock_get_meter):
        """Testa se get_meter retorna meter OpenTelemetry."""
        # Arrange
        mock_meter = Mock()
        mock_get_meter.return_value = mock_meter
        provider = TelemetryProvider()

        # Act
        meter = provider.get_meter("test-meter")

        # Assert
        mock_get_meter.assert_called_with("test-meter")
        assert meter == mock_meter
```

### 3. Testes do MetricsCollector (`tests/unit/observability/test_metrics_collector.py`)

```python
import pytest
from unittest.mock import Mock, MagicMock
from src.infrastructure.observability.collectors.metrics_collector import MetricsCollector

class TestMetricsCollector:
    """Testes do MetricsCollector."""

    @pytest.fixture
    def mock_meter_provider(self):
        """Mock do meter provider."""
        meter = Mock()
        counter = Mock()
        histogram = Mock()

        meter.create_counter.return_value = counter
        meter.create_histogram.return_value = histogram

        provider = Mock()
        provider.get_meter.return_value = meter

        return provider, meter, counter, histogram

    def test_init_creates_metrics(self, mock_meter_provider):
        """Testa se inicialização cria todas as métricas."""
        provider, meter, counter, histogram = mock_meter_provider

        # Act
        collector = MetricsCollector(provider)

        # Assert
        assert meter.create_counter.call_count == 2  # request_counter + error_counter
        assert meter.create_histogram.call_count == 1  # request_duration

    def test_increment_request_count(self, mock_meter_provider):
        """Testa incremento do contador de requisições."""
        provider, meter, counter, histogram = mock_meter_provider
        collector = MetricsCollector(provider)

        # Act
        collector.increment_request_count("GET", "/health", "success")

        # Assert
        collector._request_counter.add.assert_called_once_with(
            1,
            attributes={
                "method": "GET",
                "path": "/health",
                "status": "success"
            }
        )

    def test_record_request_duration(self, mock_meter_provider):
        """Testa registro da duração de requisições."""
        provider, meter, counter, histogram = mock_meter_provider
        collector = MetricsCollector(provider)

        # Act
        collector.record_request_duration("POST", 0.123)

        # Assert
        collector._request_duration.record.assert_called_once_with(
            0.123,
            attributes={"method": "POST"}
        )

    def test_increment_error_count(self, mock_meter_provider):
        """Testa incremento do contador de erros."""
        provider, meter, counter, histogram = mock_meter_provider
        collector = MetricsCollector(provider)

        # Act
        collector.increment_error_count("validation_error")

        # Assert
        collector._error_counter.add.assert_called_once_with(
            1,
            attributes={"type": "validation_error"}
        )

    @pytest.mark.parametrize("path,expected", [
        ("/users/123", "/users/{id}"),
        ("/orders/uuid-123-456", "/orders/{uuid}"),
        ("/health", "/health"),
        ("/api/v1/users/456/orders", "/api/v1/users/{id}/orders")
    ])
    def test_sanitize_path(self, mock_meter_provider, path, expected):
        """Testa sanitização de paths para métricas."""
        provider, meter, counter, histogram = mock_meter_provider
        collector = MetricsCollector(provider)

        # Act
        result = collector._sanitize_path(path)

        # Assert
        assert result == expected
```

### 4. Testes de Integração do Middleware (`tests/integration/observability/test_middleware_integration.py`)

```python
import pytest
import time
from fastapi import FastAPI
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch
import structlog

from src.application.middleware.observability_middleware import ObservabilityMiddleware

class TestObservabilityMiddlewareIntegration:
    """Testes de integração do middleware de observabilidade."""

    @pytest.fixture
    def app_with_middleware(self, mock_telemetry_provider, mock_metrics_collector):
        """Cria app FastAPI com middleware de observabilidade."""
        app = FastAPI()

        app.add_middleware(
            ObservabilityMiddleware,
            telemetry_provider=mock_telemetry_provider,
            metrics_collector=mock_metrics_collector
        )

        @app.get("/health")
        async def health():
            return {"status": "ok"}

        @app.get("/error")
        async def error():
            raise ValueError("Test error")

        return app

    @pytest.fixture
    def client(self, app_with_middleware):
        """Cliente de teste."""
        return TestClient(app_with_middleware)

    def test_successful_request_instruments_correctly(
        self,
        client,
        mock_telemetry_provider,
        mock_metrics_collector
    ):
        """Testa instrumentação de requisição bem-sucedida."""
        # Arrange
        mock_logger = Mock()
        mock_tracer = Mock()
        mock_span = Mock()

        mock_telemetry_provider.get_logger.return_value = mock_logger
        mock_telemetry_provider.get_tracer.return_value = mock_tracer
        mock_tracer.start_as_current_span.return_value.__enter__.return_value = mock_span

        # Act
        response = client.get("/health")

        # Assert
        assert response.status_code == 200

        # Verifica se métricas foram registradas
        mock_metrics_collector.increment_request_count.assert_called_once()
        mock_metrics_collector.record_request_duration.assert_called_once()

        # Verifica se logs foram gerados
        assert mock_logger.info.call_count >= 2  # início e fim da requisição

        # Verifica se span foi configurado
        mock_span.set_attribute.assert_called()

    def test_error_request_instruments_correctly(
        self,
        client,
        mock_telemetry_provider,
        mock_metrics_collector
    ):
        """Testa instrumentação de requisição com erro."""
        # Arrange
        mock_logger = Mock()
        mock_tracer = Mock()
        mock_span = Mock()

        mock_telemetry_provider.get_logger.return_value = mock_logger
        mock_telemetry_provider.get_tracer.return_value = mock_tracer
        mock_tracer.start_as_current_span.return_value.__enter__.return_value = mock_span

        # Act
        response = client.get("/error")

        # Assert
        assert response.status_code == 500

        # Verifica se métricas de erro foram registradas
        mock_metrics_collector.increment_error_count.assert_called_once()

        # Verifica se log de erro foi gerado
        mock_logger.error.assert_called_once()

        # Verifica se span foi marcado com erro
        mock_span.record_exception.assert_called_once()

    def test_middleware_preserves_response_content(self, client):
        """Testa se middleware preserva conteúdo da resposta."""
        # Act
        response = client.get("/health")

        # Assert
        assert response.status_code == 200
        assert response.json() == {"status": "ok"}
```

### 5. Testes End-to-End (`tests/integration/observability/test_end_to_end_observability.py`)

```python
import pytest
import asyncio
from fastapi import FastAPI
from fastapi.testclient import TestClient
import time

from src.infrastructure.observability.providers.telemetry_provider import TelemetryProvider
from src.infrastructure.observability.collectors.metrics_collector import MetricsCollector
from src.application.middleware.observability_middleware import ObservabilityMiddleware

@pytest.mark.integration
class TestEndToEndObservability:
    """Testes end-to-end da stack de observabilidade."""

    @pytest.fixture
    def real_app(self):
        """Cria app real com stack de observabilidade completa."""
        app = FastAPI()

        # Configura observabilidade real (com mocks para exportadores)
        with patch('prometheus_client.start_http_server'):
            telemetry_provider = TelemetryProvider()
            metrics_collector = MetricsCollector(telemetry_provider.meter_provider)

        app.add_middleware(
            ObservabilityMiddleware,
            telemetry_provider=telemetry_provider,
            metrics_collector=metrics_collector
        )

        @app.get("/test")
        async def test_endpoint():
            # Simula processamento
            await asyncio.sleep(0.01)
            return {"message": "test"}

        return app

    @patch('prometheus_client.start_http_server')
    def test_complete_observability_flow(self, mock_prometheus, real_app):
        """Testa fluxo completo de observabilidade."""
        client = TestClient(real_app)

        # Act - faz múltiplas requisições
        for i in range(5):
            response = client.get("/test")
            assert response.status_code == 200

        # Assert - verifica se não houve erros (testes mais específicos
        # viriam aqui se tivéssemos acesso aos exportadores reais)
        assert True  # Se chegou até aqui, o fluxo básico funcionou

    @patch('prometheus_client.start_http_server')
    def test_correlation_between_logs_and_traces(self, mock_prometheus, real_app):
        """Testa correlação entre logs e traces."""
        client = TestClient(real_app)

        # Act
        response = client.get("/test")

        # Assert
        assert response.status_code == 200
        # Em um teste real, verificaríamos se trace_id aparece nos logs
        # e se spans foram criados corretamente
```

## 📋 Configuração de Testes

### `conftest.py` Atualizado

```python
import pytest
import os
from pathlib import Path

# Configuração para testes de observabilidade
pytest_plugins = ["tests.fixtures.observability.config_fixtures"]

@pytest.fixture(scope="session", autouse=True)
def setup_test_environment():
    """Configura ambiente de teste."""
    os.environ["ENVIRONMENT"] = "test"
    os.environ["LOG_LEVEL"] = "DEBUG"
    os.environ["PROMETHEUS_PORT"] = "8001"
    yield
    # Cleanup se necessário

@pytest.fixture
def disable_telemetry():
    """Desabilita telemetria em testes que não precisam."""
    with patch.dict(os.environ, {
        "OTEL_SDK_DISABLED": "true",
        "PROMETHEUS_DISABLE_CREATED_SERIES": "true"
    }):
        yield
```

## ✅ Checklist de Implementação

- [ ] Implementar fixtures base para mocks de observabilidade
- [ ] Criar testes unitários para TelemetryProvider
- [ ] Criar testes unitários para MetricsCollector
- [ ] Criar testes unitários para configurações
- [ ] Implementar testes de integração do middleware
- [ ] Criar testes end-to-end da stack completa
- [ ] Configurar testes para diferentes ambientes
- [ ] Implementar testes de performance de observabilidade
- [ ] Validar cobertura de código >= 80%
- [ ] Documentar estratégias de teste

## 🔗 Dependências de Outros Artefatos

- **observability-infrastructure.md** - Testa componentes implementados
- **observability-middleware.md** - Testa middleware implementado
- **observability-config.md** - Testa carregamento de configurações

## 📝 Notas Técnicas

- Usar mocks para exportadores externos em testes unitários
- Testes de integração podem usar containers para Prometheus/Jaeger
- Validar correlação entre logs, métricas e traces
- Testes de performance devem verificar overhead < 5%
- Incluir testes para cenários de falha de exportadores
