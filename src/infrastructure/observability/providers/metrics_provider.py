"""
Provedor de métricas usando Prometheus.

Este módulo configura e fornece funcionalidades de coleta de métricas
usando o cliente oficial do Prometheus para Python.
"""

import time
from typing import Any, Dict, Optional

from prometheus_client import (
    Counter,
    Gauge,
    Histogram,
    Info,
    Summary,
    start_http_server,
)
from prometheus_client.core import CollectorRegistry


class MetricsProvider:
    """
    Provedor de métricas usando Prometheus.

    Gerencia métricas customizadas e expõe endpoint para scraping
    do Prometheus.
    """

    def __init__(self, config: Dict[str, Any]):
        """
        Inicializa o provedor de métricas.

        Args:
            config: Configuração das métricas contendo port, metrics, etc.
        """
        self.config = config
        self._registry = CollectorRegistry()
        self._metrics: Dict[str, Any] = {}
        self._server_started = False

    def configure(self) -> None:
        """Configura o provedor de métricas."""
        # Registrar métricas padrão se habilitado
        if self.config.get("default_metrics", {}).get("enabled", True):
            self._register_default_metrics()

        # Registrar métricas customizadas
        custom_metrics = self.config.get("custom_metrics", {})
        for metric_name, metric_config in custom_metrics.items():
            self._register_custom_metric(metric_name, metric_config)

        # Iniciar servidor HTTP se habilitado
        if self.config.get("http_server", {}).get("enabled", True):
            self._start_http_server()

    def _register_default_metrics(self) -> None:
        """Registra métricas padrão da aplicação."""
        # Métrica de requisições HTTP
        self._metrics["http_requests_total"] = Counter(
            "http_requests_total",
            "Total number of HTTP requests",
            ["method", "endpoint", "status_code"],
            registry=self._registry,
        )

        # Métrica de duração de requisições
        self._metrics["http_request_duration_seconds"] = Histogram(
            "http_request_duration_seconds",
            "HTTP request duration in seconds",
            ["method", "endpoint"],
            registry=self._registry,
        )

        # Métrica de requisições ativas
        self._metrics["http_requests_active"] = Gauge(
            "http_requests_active",
            "Number of active HTTP requests",
            registry=self._registry,
        )

        # Informações da aplicação
        self._metrics["application_info"] = Info(
            "application_info", "Application information", registry=self._registry
        )
        self._metrics["application_info"].info(
            {
                "name": "skyhal",
                "version": "0.1.0",
                "environment": self.config.get("environment", "development"),
            }
        )

    def _register_custom_metric(self, name: str, config: Dict[str, Any]) -> None:
        """
        Registra uma métrica customizada.

        Args:
            name: Nome da métrica.
            config: Configuração da métrica contendo type, description, etc.
        """
        metric_type = config.get("type", "counter").lower()
        description = config.get("description", f"Custom metric: {name}")
        labels = config.get("labels", [])

        if metric_type == "counter":
            self._metrics[name] = Counter(
                name, description, labels, registry=self._registry
            )
        elif metric_type == "gauge":
            self._metrics[name] = Gauge(
                name, description, labels, registry=self._registry
            )
        elif metric_type == "histogram":
            buckets = config.get("buckets")
            if buckets is not None:
                self._metrics[name] = Histogram(
                    name, description, labels, buckets=buckets, registry=self._registry
                )
            else:
                self._metrics[name] = Histogram(
                    name, description, labels, registry=self._registry
                )
        elif metric_type == "summary":
            self._metrics[name] = Summary(
                name, description, labels, registry=self._registry
            )

    def _start_http_server(self) -> None:
        """Inicia o servidor HTTP para exposição das métricas."""
        if self._server_started:
            return

        port = self.config.get("http_server", {}).get("port", 8000)
        addr = self.config.get("http_server", {}).get("addr", "")

        start_http_server(port, addr=addr, registry=self._registry)
        self._server_started = True

    def get_metric(self, name: str) -> Optional[Any]:
        """
        Obtém uma métrica registrada.

        Args:
            name: Nome da métrica.

        Returns:
            Métrica registrada ou None se não encontrada.
        """
        return self._metrics.get(name)

    def increment_counter(
        self, name: str, value: float = 1, labels: Optional[Dict[str, str]] = None
    ) -> None:
        """
        Incrementa um contador.

        Args:
            name: Nome do contador.
            value: Valor a incrementar.
            labels: Labels para a métrica.
        """
        counter = self.get_metric(name)
        if counter and isinstance(counter, Counter):
            if labels:
                counter.labels(**labels).inc(value)
            else:
                counter.inc(value)

    def set_gauge(
        self, name: str, value: float, labels: Optional[Dict[str, str]] = None
    ) -> None:
        """
        Define o valor de um gauge.

        Args:
            name: Nome do gauge.
            value: Valor a definir.
            labels: Labels para a métrica.
        """
        gauge = self.get_metric(name)
        if gauge and isinstance(gauge, Gauge):
            if labels:
                gauge.labels(**labels).set(value)
            else:
                gauge.set(value)

    def observe_histogram(
        self, name: str, value: float, labels: Optional[Dict[str, str]] = None
    ) -> None:
        """
        Adiciona uma observação a um histograma.

        Args:
            name: Nome do histograma.
            value: Valor a observar.
            labels: Labels para a métrica.
        """
        histogram = self.get_metric(name)
        if histogram and isinstance(histogram, Histogram):
            if labels:
                histogram.labels(**labels).observe(value)
            else:
                histogram.observe(value)

    def time_histogram(self, name: str, labels: Optional[Dict[str, str]] = None) -> Any:
        """
        Context manager para medir tempo automaticamente.

        Args:
            name: Nome do histograma.
            labels: Labels para a métrica.

        Returns:
            Context manager para medição de tempo.
        """
        histogram = self.get_metric(name)
        if histogram and isinstance(histogram, Histogram):
            if labels:
                return histogram.labels(**labels).time()
            else:
                return histogram.time()

        # Fallback para context manager vazio
        class EmptyTimer:
            def __enter__(self) -> Any:
                self.start_time = time.time()
                return self

            def __exit__(self, *args: Any) -> None:
                pass

        return EmptyTimer()

    def get_registry(self) -> CollectorRegistry:
        """
        Obtém o registry de métricas.

        Returns:
            Registry de métricas do Prometheus.
        """
        return self._registry
