"""Módulo de configuração da aplicação FastAPI."""
from fastapi import FastAPI

from .routers import auto_extension, health, llm_codegen


def create_app(testing: bool = False) -> FastAPI:
    """Cria e configura a aplicação FastAPI.

    Args:
        testing: Se True, configura a aplicação para testes.

    Returns:
        FastAPI: Aplicação FastAPI configurada.
    """
    app = FastAPI(
        title="SkyHAL API",
        description="API para o projeto SkyHAL",
        version="0.1.0",
        docs_url="/docs" if not testing else None,
        redoc_url="/redoc" if not testing else None,
    )

    # Incluindo rotas
    app.include_router(health.router, tags=["health"])
    app.include_router(auto_extension.router)
    app.include_router(llm_codegen.router)

    # TODO: Configurar observabilidade quando o middleware estiver pronto
    # Middleware de observabilidade será adicionado aqui

    return app


# Instância global da aplicação para desenvolvimento e testes
app = create_app()
