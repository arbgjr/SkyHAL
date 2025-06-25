#!/usr/bin/env python3
"""
Script de demonstração da observabilidade do SkyHAL.

Este script demonstra o uso dos provedores de observabilidade
de forma isolada e integrada.
"""

import asyncio
import time
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.testclient import TestClient

from src.infrastructure.observability import (
    # ObservabilityMiddleware,  # Temporariamente comentado
    setup_observability,
)


def demo_standalone_providers() -> None:
    """Demonstra o uso dos provedores de forma standalone."""
    print("🔧 Demonstração dos provedores standalone...")
    print("=" * 60)

    # Configurar observabilidade
    logging_provider, metrics_provider, tracing_provider = setup_observability(
        environment="development"
    )

    # Demo do logging estruturado
    print("\n📝 Logging estruturado:")
    logger = logging_provider.get_logger("demo")
    logger.info("Iniciando demonstração", component="demo", version="1.0.0")

    # Demo de métricas
    print("\n📊 Métricas:")
    metrics_provider.increment_counter(
        "http_requests_total",
        labels={"method": "GET", "endpoint": "/demo", "status_code": "200"},
    )
    print("✅ Contador incrementado")

    metrics_provider.set_gauge("demo_gauge", 42.0)
    print("✅ Gauge definido")

    # Demo de tracing
    print("\n🔍 Tracing:")
    with tracing_provider.create_span("demo_operation") as span:
        span.set_attribute("demo.value", "test")
        time.sleep(0.1)  # Simular trabalho
        print("✅ Span criado e finalizado")

    print("\n✅ Demonstração standalone concluída!")


def demo_fastapi_integration() -> None:
    """Demonstra a integração com FastAPI."""
    print("\n🚀 Demonstração da integração com FastAPI...")
    print("=" * 60)

    # Configurar observabilidade
    logging_provider, metrics_provider, tracing_provider = setup_observability(
        environment="development"
    )

    # Criar app FastAPI de demonstração
    @asynccontextmanager
    async def lifespan(app: FastAPI):  # type: ignore
        logger = logging_provider.get_logger("demo")
        logger.info("Aplicação iniciada")
        yield
        logger.info("Aplicação encerrada")

    app = FastAPI(title="Demo Observability", version="1.0.0", lifespan=lifespan)

    # Temporariamente comentado devido a problemas de tipagem
    # app.add_middleware(
    #     ObservabilityMiddleware,
    #     logging_provider=logging_provider,
    #     metrics_provider=metrics_provider,
    #     tracing_provider=tracing_provider,
    # )

    @app.get("/demo")
    async def demo_endpoint():  # type: ignore
        """Endpoint de demonstração."""
        logger = logging_provider.get_logger("demo.endpoint")
        logger.info("Processando requisição de demo")

        # Simular algum trabalho
        await asyncio.sleep(0.1)

        return {"message": "Demo successful!", "status": "ok"}

    @app.get("/demo/error")
    async def demo_error() -> None:
        """Endpoint que gera erro para demonstração."""
        logger = logging_provider.get_logger("demo.endpoint")
        logger.info("Simulando erro para demonstração")
        raise Exception("Erro simulado para demonstração")

    # Testar endpoints com TestClient
    print("\n🧪 Testando endpoints...")
    with TestClient(app) as client:
        # Requisição com sucesso
        response = client.get("/demo")
        print(f"✅ GET /demo - Status: {response.status_code}")
        print(f"   Response: {response.json()}")

        # Requisição com erro
        try:
            response = client.get("/demo/error")
        except Exception:
            print("✅ GET /demo/error - Erro capturado conforme esperado")

    print("\n✅ Demonstração da integração concluída!")


def main() -> None:
    """Executa todas as demonstrações."""
    print("🌟 DEMONSTRAÇÃO DA OBSERVABILIDADE SKYHAL")
    print("=" * 60)

    try:
        # Demo dos provedores standalone
        demo_standalone_providers()

        # Demo da integração com FastAPI
        demo_fastapi_integration()

        print("\n🎉 Todas as demonstrações concluídas com sucesso!")
        print("\n📊 Para verificar métricas, acesse: http://localhost:8000")
        print("📝 Logs estruturados foram exibidos no console")
        print("🔍 Traces foram criados (visíveis em sistemas como Jaeger)")

    except Exception as e:
        print(f"\n❌ Erro durante demonstração: {e}")
        raise


if __name__ == "__main__":
    main()
