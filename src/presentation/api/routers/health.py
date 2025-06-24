"""Módulo com rotas de health check."""
from typing import Annotated

from fastapi import APIRouter, Depends, FastAPI

router = APIRouter()


def get_app() -> FastAPI:
    """Retorna a instância da aplicação FastAPI.

    Returns:
        FastAPI: Aplicação FastAPI.
    """
    from ..app import create_app  # pylint: disable=import-outside-toplevel

    return create_app()


@router.get("/health")
async def health_check(
    app: Annotated[FastAPI, Depends(get_app)],
) -> dict[str, str]:
    """Verifica a saúde da aplicação.

    Args:
        app: Instância da aplicação FastAPI.

    Returns:
        dict[str, str]: Resposta indicando o status da aplicação.
    """
    return {
        "status": "healthy",
        "version": app.version,
        "environment": "testing",
    }
