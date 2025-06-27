"""
Middleware de observabilidade para FastAPI.

Este middleware instrumenta automaticamente as requisições HTTP com
logging, métricas e tracing distribuído.
"""

import time
from typing import Any, Callable, Dict, Optional

import structlog
from fastapi import Request, Response
from opentelemetry import trace
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp

from ..providers.logging_provider import StructuredLoggingProvider
from ..providers.metrics_provider import MetricsProvider
from ..providers.tracing_provider import TracingProvider


class ObservabilityMiddleware(BaseHTTPMiddleware):
    """
    Middleware de observabilidade para instrumentação automática.

    Captura métricas, logs e traces para todas as requisições HTTP
    passando pela aplicação.
    """

    def __init__(
        self,
        app: ASGIApp,
        logging_provider: Optional[StructuredLoggingProvider] = None,
        metrics_provider: Optional[MetricsProvider] = None,
        tracing_provider: Optional[TracingProvider] = None,
        config: Optional[Dict[str, Any]] = None,
    ):
        """
        Inicializa o middleware de observabilidade.

        Args:
            app: Aplicação ASGI.
            logging_provider: Provedor de logging estruturado.
            metrics_provider: Provedor de métricas.
            tracing_provider: Provedor de tracing.
            config: Configuração adicional do middleware.
        """
        super().__init__(app)
        self.logging_provider = logging_provider
        self.metrics_provider = metrics_provider
        self.tracing_provider = tracing_provider
        self.config = config or {}

        # Configurar logger
        if self.logging_provider:
            self.logger = self.logging_provider.get_logger(__name__)
        else:
            self.logger = structlog.get_logger(__name__)

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """
        Processa a requisição com instrumentação de observabilidade.

        Args:
            request: Requisição HTTP recebida.
            call_next: Próximo handler na cadeia.

        Returns:
            Resposta HTTP processada.
        """
        start_time = time.time()

        # Extrair informações da requisição
        method = request.method
        path = self._get_route_path(request)
        client_ip = self._get_client_ip(request)

        # Incrementar contador de requisições ativas
        if self.metrics_provider:
            active_gauge = self.metrics_provider.get_metric("http_requests_active")
            if active_gauge:
                active_gauge.inc()

        # Criar span para tracing
        span = None
        if self.tracing_provider:
            span = self.tracing_provider.create_span(
                f"{method} {path}",
                attributes={
                    "http.method": method,
                    "http.url": str(request.url),
                    "http.route": path,
                    "http.client_ip": client_ip,
                },
            )

        # Log de início da requisição
        request_context = {
            "method": method,
            "path": path,
            "client_ip": client_ip,
            "user_agent": request.headers.get("user-agent", ""),
            "request_id": request.headers.get("x-request-id", ""),
        }

        self.logger.info("Request started", **request_context)

        try:
            # Processar requisição
            response = await call_next(request)
            status_code = response.status_code

            # Calcular duração
            duration = time.time() - start_time

            # Registrar métricas de sucesso
            self._record_metrics(method, path, status_code, duration)

            # Adicionar informações ao span
            if span:
                span.set_attribute("http.status_code", status_code)
                response_size = len(response.body) if hasattr(response, "body") else 0
                span.set_attribute("http.response_size", response_size)

            # Log de sucesso
            self.logger.info(
                "Request completed",
                status_code=status_code,
                duration=duration,
                **request_context,
            )

            return response  # type: ignore[no-any-return]

        except Exception as exc:
            # Calcular duração em caso de erro
            duration = time.time() - start_time

            # Registrar métricas de erro
            self._record_metrics(method, path, 500, duration)

            # Adicionar erro ao span
            if span:
                span.set_attribute("http.status_code", 500)
                span.record_exception(exc)
                span.set_status(trace.Status(trace.StatusCode.ERROR, str(exc)))

            # Log de erro
            self.logger.error(
                "Request failed",
                error=str(exc),
                error_type=type(exc).__name__,
                duration=duration,
                **request_context,
                exc_info=True,
            )

            raise

        finally:
            # Finalizar span
            if span:
                span.end()

            # Decrementar contador de requisições ativas
            if self.metrics_provider:
                active_gauge = self.metrics_provider.get_metric("http_requests_active")
                if active_gauge:
                    active_gauge.dec()

    def _get_route_path(self, request: Request) -> str:
        """
        Extrai o path da rota da requisição.

        Args:
            request: Requisição HTTP.

        Returns:
            Path da rota ou URL path se não encontrado.
        """
        if hasattr(request, "scope") and "route" in request.scope:
            route = request.scope["route"]
            return getattr(route, "path", request.url.path)
        return request.url.path

    def _get_client_ip(self, request: Request) -> str:
        """
        Extrai o IP do cliente considerando proxies.

        Args:
            request: Requisição HTTP.

        Returns:
            IP do cliente.
        """
        # Verificar headers de proxy comuns
        forwarded_for = request.headers.get("x-forwarded-for")
        if forwarded_for:
            return forwarded_for.split(",")[0].strip()

        real_ip = request.headers.get("x-real-ip")
        if real_ip:
            return real_ip

        # Fallback para IP direto
        if request.client:
            return request.client.host

        return "unknown"

    def _record_metrics(
        self, method: str, path: str, status_code: int, duration: float
    ) -> None:
        """
        Registra métricas da requisição.

        Args:
            method: Método HTTP.
            path: Path da requisição.
            status_code: Código de status da resposta.
            duration: Duração da requisição em segundos.
        """
        if not self.metrics_provider:
            return

        labels = {"method": method, "endpoint": path, "status_code": str(status_code)}

        # Incrementar contador de requisições
        self.metrics_provider.increment_counter("http_requests_total", labels=labels)

        # Observar duração da requisição
        duration_labels = {"method": method, "endpoint": path}
        self.metrics_provider.observe_histogram(
            "http_request_duration_seconds", duration, labels=duration_labels
        )
