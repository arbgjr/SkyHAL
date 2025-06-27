"""
Pacote de observabilidade do SkyHAL.

Este pacote implementa a infraestrutura completa de observabilidade incluindo:
- Logging estruturado com structlog
- Métricas com Prometheus
- Tracing distribuído com OpenTelemetry
- Middleware para instrumentação automática
"""

from typing import Optional, Tuple

from .factory import ObservabilityFactory
from .middleware.observability_middleware import ObservabilityMiddleware
from .providers.logging_provider import StructuredLoggingProvider
from .providers.metrics_provider import MetricsProvider
from .providers.tracing_provider import TracingProvider

__version__ = "0.1.0"

__all__ = [
    "ObservabilityFactory",
    "ObservabilityMiddleware",
    "StructuredLoggingProvider",
    "MetricsProvider",
    "TracingProvider",
]


# Factory global para uso simplificado
_global_factory: Optional[ObservabilityFactory] = None


def get_observability_factory() -> ObservabilityFactory:
    """
    Obtém a instância global do factory de observabilidade.

    Returns:
        Factory de observabilidade configurado.
    """
    global _global_factory
    if _global_factory is None:
        _global_factory = ObservabilityFactory()
    return _global_factory


def setup_observability(
    config_path: Optional[str] = None, environment: Optional[str] = None
) -> Tuple[StructuredLoggingProvider, MetricsProvider, TracingProvider]:
    """
    Configura observabilidade de forma simplificada.

    Args:
        config_path: Caminho para arquivo de configuração.
        environment: Ambiente específico (development, production, etc).

    Returns:
        Tupla com (logging_provider, metrics_provider, tracing_provider).
    """
    factory = ObservabilityFactory(config_path)
    providers = factory.create_providers(environment)
    factory.setup_instrumentation()
    return providers
