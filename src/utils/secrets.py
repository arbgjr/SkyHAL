"""
Módulo utilitário para centralização de acesso a segredos e variáveis de ambiente.
"""
import os
from typing import Optional


class SecretsManager:
    """Centraliza acesso seguro a segredos e variáveis de ambiente."""

    @staticmethod
    def get_secret(key: str, default: Optional[str] = None) -> str:
        """
        Retorna o valor de uma variável de ambiente (segredo).
        Args:
            key (str): Nome da variável de ambiente.
            default (Optional[str]): Valor padrão se não encontrado.
        Returns:
            str: Valor do segredo ou padrão.
        Raises:
            RuntimeError: Se o segredo não for encontrado e não houver padrão.
        """
        value = os.getenv(key, default)
        if value is None:
            raise RuntimeError(
                f"Segredo '{key}' não encontrado e nenhum padrão definido."
            )
        return value
