"""
Provedor de tracing distribuído usando OpenTelemetry.

Este módulo configura e fornece funcionalidades de tracing distribuído
para rastreamento de requisições através dos serviços.
"""

from typing import Any, Dict, Optional

from opentelemetry import trace
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import (
    OTLPSpanExporter,
)
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor


class TracingProvider:
    """
    Provedor de tracing distribuído usando OpenTelemetry.

    Configura exportadores para Jaeger e OTLP com suporte a múltiplos
    ambientes e configurações.
    """

    def __init__(self, config: Dict[str, Any]):
        """
        Inicializa o provedor de tracing.

        Args:
            config: Configuração do tracing contendo service_name, exporters, etc.
        """
        self.config = config
        self._tracer_provider: Optional[TracerProvider] = None
        self._is_configured = False

    def configure(self) -> None:
        """Configura o tracing distribuído."""
        if self._is_configured:
            return

        # Criar resource com informações do serviço
        resource = Resource.create(
            {
                "service.name": self.config.get("service_name", "skyhal"),
                "service.version": self.config.get("service_version", "0.1.0"),
                "deployment.environment": self.config.get("environment", "development"),
            }
        )

        # Configurar tracer provider
        self._tracer_provider = TracerProvider(resource=resource)

        # Configurar exportadores
        self._configure_exporters()

        # Definir como provider global
        trace.set_tracer_provider(self._tracer_provider)

        self._is_configured = True

    def _configure_exporters(self) -> None:
        """Configura os exportadores de traces."""
        if not self._tracer_provider:
            return

        exporters_config = self.config.get("exporters", {})

        # Configurar exportador Jaeger se habilitado
        if exporters_config.get("jaeger", {}).get("enabled", False):
            self._configure_jaeger_exporter(exporters_config["jaeger"])

        # Configurar exportador OTLP se habilitado
        if exporters_config.get("otlp", {}).get("enabled", False):
            self._configure_otlp_exporter(exporters_config["otlp"])

    def _configure_jaeger_exporter(self, jaeger_config: Dict[str, Any]) -> None:
        """
        Configura o exportador Jaeger.

        Args:
            jaeger_config: Configuração específica do Jaeger.
        """
        if not self._tracer_provider:
            return

        jaeger_exporter = JaegerExporter(
            agent_host_name=jaeger_config.get("agent_host", "localhost"),
            agent_port=jaeger_config.get("agent_port", 6831),
            collector_endpoint=jaeger_config.get("collector_endpoint"),
        )

        span_processor = BatchSpanProcessor(jaeger_exporter)
        self._tracer_provider.add_span_processor(span_processor)

    def _configure_otlp_exporter(self, otlp_config: Dict[str, Any]) -> None:
        """
        Configura o exportador OTLP.

        Args:
            otlp_config: Configuração específica do OTLP.
        """
        if not self._tracer_provider:
            return

        otlp_exporter = OTLPSpanExporter(
            endpoint=otlp_config.get("endpoint", "http://localhost:4317"),
            headers=otlp_config.get("headers", {}),
        )

        span_processor = BatchSpanProcessor(otlp_exporter)
        self._tracer_provider.add_span_processor(span_processor)

    def get_tracer(self, name: str) -> trace.Tracer:
        """
        Obtém um tracer configurado.

        Args:
            name: Nome do tracer (geralmente nome do módulo).

        Returns:
            Tracer configurado para o módulo especificado.
        """
        if not self._is_configured:
            self.configure()

        return trace.get_tracer(name)

    def create_span(
        self, name: str, tracer_name: Optional[str] = None, **kwargs: Any
    ) -> trace.Span:
        """
        Cria um span para rastreamento.

        Args:
            name: Nome da operação sendo rastreada.
            tracer_name: Nome do tracer. Se None, usa "skyhal".
            **kwargs: Atributos adicionais para o span.

        Returns:
            Span configurado e iniciado.
        """
        tracer = self.get_tracer(tracer_name or "skyhal")
        span = tracer.start_span(name)

        # Adicionar atributos ao span
        for key, value in kwargs.items():
            span.set_attribute(key, value)

        return span

    def shutdown(self) -> None:
        """Encerra o tracing provider e força o flush dos spans."""
        if self._tracer_provider:
            self._tracer_provider.shutdown()
