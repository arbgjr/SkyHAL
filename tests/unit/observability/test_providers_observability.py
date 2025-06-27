"""Testes unitários para os provedores de observabilidade."""

from src.infrastructure.observability.providers.logging_provider import (
    StructuredLoggingProvider,
)
from src.infrastructure.observability.providers.metrics_provider import (
    MetricsProvider,
)
from src.infrastructure.observability.providers.tracing_provider import (
    TracingProvider,
)


class TestStructuredLoggingProvider:
    """Testes para o provedor de logging estruturado."""

    def test_provider_initialization(self) -> None:
        """Testa a inicialização do provedor."""
        config = {"level": "INFO", "format": "json", "output": "console"}
        provider = StructuredLoggingProvider(config)

        assert provider.config == config
        assert not provider._is_configured

    def test_provider_configuration(self) -> None:
        """Testa a configuração do provedor."""
        config = {"level": "DEBUG", "format": "console", "output": "console"}
        provider = StructuredLoggingProvider(config)
        provider.configure()

        assert provider._is_configured

    def test_get_logger(self) -> None:
        """Testa a obtenção de um logger."""
        config = {"level": "INFO"}
        provider = StructuredLoggingProvider(config)

        logger = provider.get_logger("test_module")
        assert logger is not None

    def test_bind_context(self) -> None:
        """Testa o binding de contexto ao logger."""
        config = {"level": "INFO"}
        provider = StructuredLoggingProvider(config)

        bound_logger = provider.bind_context(request_id="test-123", user_id="user-456")
        assert bound_logger is not None


class TestMetricsProvider:
    """Testes para o provedor de métricas."""

    def test_provider_initialization(self) -> None:
        """Testa a inicialização do provedor."""
        config = {
            "http_server": {"enabled": False},
            "default_metrics": {"enabled": True},
        }
        provider = MetricsProvider(config)

        assert provider.config == config
        assert not provider._server_started

    def test_provider_configuration(self) -> None:
        """Testa a configuração do provedor."""
        config = {
            "http_server": {"enabled": False},
            "default_metrics": {"enabled": True},
        }
        provider = MetricsProvider(config)
        provider.configure()

        # Verificar se métricas padrão foram criadas
        assert "http_requests_total" in provider._metrics
        assert "http_request_duration_seconds" in provider._metrics

    def test_increment_counter(self) -> None:
        """Testa o incremento de contador."""
        config = {
            "http_server": {"enabled": False},
            "default_metrics": {"enabled": True},
        }
        provider = MetricsProvider(config)
        provider.configure()

        # Incrementar contador
        provider.increment_counter(
            "http_requests_total",
            labels={"method": "GET", "endpoint": "/test", "status_code": "200"},
        )

        # Verificar se foi incrementado (sem erro)
        counter = provider.get_metric("http_requests_total")
        assert counter is not None

    def test_set_gauge(self) -> None:
        """Testa a definição de valor em gauge."""
        config = {
            "http_server": {"enabled": False},
            "default_metrics": {"enabled": True},
        }
        provider = MetricsProvider(config)
        provider.configure()

        # Definir valor do gauge
        provider.set_gauge("http_requests_active", 5)

        # Verificar se foi definido (sem erro)
        gauge = provider.get_metric("http_requests_active")
        assert gauge is not None


class TestTracingProvider:
    """Testes para o provedor de tracing."""

    def test_provider_initialization(self) -> None:
        """Testa a inicialização do provedor."""
        config = {
            "service_name": "test-service",
            "exporters": {"jaeger": {"enabled": False}},
        }
        provider = TracingProvider(config)

        assert provider.config == config
        assert not provider._is_configured

    def test_provider_configuration(self) -> None:
        """Testa a configuração do provedor."""
        config = {
            "service_name": "test-service",
            "exporters": {"jaeger": {"enabled": False}},
        }
        provider = TracingProvider(config)
        provider.configure()

        assert provider._is_configured
        assert provider._tracer_provider is not None

    def test_get_tracer(self) -> None:
        """Testa a obtenção de um tracer."""
        config = {
            "service_name": "test-service",
            "exporters": {"jaeger": {"enabled": False}},
        }
        provider = TracingProvider(config)

        tracer = provider.get_tracer("test_module")
        assert tracer is not None

    def test_create_span(self) -> None:
        """Testa a criação de um span."""
        config = {
            "service_name": "test-service",
            "exporters": {"jaeger": {"enabled": False}},
        }
        provider = TracingProvider(config)
        provider.configure()

        span = provider.create_span(
            "test_operation", http_method="GET", http_url="/test"
        )
        assert span is not None
        span.end()  # Finalizar span para limpeza

    def test_shutdown(self) -> None:
        """Testa o encerramento do provider."""
        config = {
            "service_name": "test-service",
            "exporters": {"jaeger": {"enabled": False}},
        }
        provider = TracingProvider(config)
        provider.configure()

        # Não deve gerar erro
        provider.shutdown()
