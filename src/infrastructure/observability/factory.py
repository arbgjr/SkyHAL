"""
Factory de observabilidade para configuração centralizada.

Este módulo fornece um factory para configurar e integrar todos os
componentes de observabilidade (logging, métricas, tracing).
"""

import os
from pathlib import Path
from typing import Any, Dict, Optional, Tuple

import yaml

from .providers.logging_provider import StructuredLoggingProvider
from .providers.metrics_provider import MetricsProvider
from .providers.tracing_provider import TracingProvider


class ObservabilityFactory:
    """
    Factory para configuração centralizada de observabilidade.

    Carrega configurações e inicializa todos os provedores de
    observabilidade de forma coordenada.
    """

    def __init__(self, config_path: Optional[str] = None):
        """
        Inicializa o factory de observabilidade.

        Args:
            config_path: Caminho para arquivo de configuração.
                        Se None, usa config/observability.yaml.
        """
        self.config_path = config_path or "config/observability.yaml"
        self.config: Dict[str, Any] = {}
        self._providers_initialized = False

    def load_config(self, environment: Optional[str] = None) -> Dict[str, Any]:
        """
        Carrega configuração de observabilidade.

        Args:
            environment: Ambiente específico (development, production, etc).
                        Se None, usa ENVIRONMENT ou development.

        Returns:
            Configuração carregada e mesclada.
        """
        # Determinar ambiente
        env = environment or os.getenv("ENVIRONMENT", "development")

        # Carregar configuração base
        base_config = self._load_config_file(self.config_path)

        # Carregar configuração específica do ambiente
        env_config_path = f"config/environments/{env}.yaml"
        env_config = self._load_config_file(env_config_path)

        # Mesclar configurações
        self.config = self._merge_configs(base_config, env_config)
        self.config["environment"] = env

        return self.config

    def _load_config_file(self, path: str) -> Dict[str, Any]:
        """
        Carrega arquivo de configuração YAML.

        Args:
            path: Caminho para o arquivo.

        Returns:
            Configuração carregada ou dict vazio se arquivo não existe.
        """
        config_file = Path(path)
        if not config_file.exists():
            return {}

        try:
            with open(config_file, "r", encoding="utf-8") as f:
                return yaml.safe_load(f) or {}
        except Exception as e:
            print(f"Warning: Failed to load config from {path}: {e}")
            return {}

    def _merge_configs(
        self, base: Dict[str, Any], override: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Mescla configurações recursivamente.

        Args:
            base: Configuração base.
            override: Configuração que sobrescreve a base.

        Returns:
            Configuração mesclada.
        """
        result = base.copy()

        for key, value in override.items():
            if (
                key in result
                and isinstance(result[key], dict)
                and isinstance(value, dict)
            ):
                result[key] = self._merge_configs(result[key], value)
            else:
                result[key] = value

        return result

    def create_providers(
        self, environment: Optional[str] = None
    ) -> Tuple[StructuredLoggingProvider, MetricsProvider, TracingProvider]:
        """
        Cria e configura todos os provedores de observabilidade.

        Args:
            environment: Ambiente específico para configuração.

        Returns:
            Tupla com (logging_provider, metrics_provider, tracing_provider).
        """
        # Carregar configuração se necessário
        if not self.config:
            self.load_config(environment)

        # Criar provedores
        logging_provider = self._create_logging_provider()
        metrics_provider = self._create_metrics_provider()
        tracing_provider = self._create_tracing_provider()

        # Configurar provedores
        logging_provider.configure()
        metrics_provider.configure()
        tracing_provider.configure()

        self._providers_initialized = True

        return logging_provider, metrics_provider, tracing_provider

    def _create_logging_provider(self) -> StructuredLoggingProvider:
        """
        Cria provedor de logging estruturado.

        Returns:
            Provedor de logging configurado.
        """
        logging_config = self.config.get("logging", {})
        return StructuredLoggingProvider(logging_config)

    def _create_metrics_provider(self) -> MetricsProvider:
        """
        Cria provedor de métricas.

        Returns:
            Provedor de métricas configurado.
        """
        metrics_config = self.config.get("metrics", {})
        return MetricsProvider(metrics_config)

    def _create_tracing_provider(self) -> TracingProvider:
        """
        Cria provedor de tracing.

        Returns:
            Provedor de tracing configurado.
        """
        tracing_config = self.config.get("tracing", {})

        # Adicionar informações do ambiente
        tracing_config.setdefault("service_name", "skyhal")
        tracing_config.setdefault("environment", self.config.get("environment"))

        return TracingProvider(tracing_config)

    def setup_instrumentation(self) -> None:
        """
        Configura instrumentação automática do OpenTelemetry.

        Instrumenta bibliotecas automaticamente para captura de traces.
        """
        try:
            from opentelemetry.instrumentation.fastapi import (
                FastAPIInstrumentor,
            )
            from opentelemetry.instrumentation.logging import (
                LoggingInstrumentor,
            )
            from opentelemetry.instrumentation.requests import (
                RequestsInstrumentor,
            )

            # Instrumentar FastAPI
            if not FastAPIInstrumentor().is_instrumented_by_opentelemetry:
                FastAPIInstrumentor().instrument()

            # Instrumentar requests
            if not RequestsInstrumentor().is_instrumented_by_opentelemetry:
                RequestsInstrumentor().instrument()

            # Instrumentar logging
            if not LoggingInstrumentor().is_instrumented_by_opentelemetry:
                LoggingInstrumentor().instrument()

        except ImportError as e:
            print(f"Warning: Could not setup auto-instrumentation: {e}")

    def get_config(self) -> Dict[str, Any]:
        """
        Obtém configuração atual.

        Returns:
            Configuração de observabilidade.
        """
        return self.config.copy()

    def is_configured(self) -> bool:
        """
        Verifica se os provedores foram inicializados.

        Returns:
            True se todos os provedores foram configurados.
        """
        return self._providers_initialized
