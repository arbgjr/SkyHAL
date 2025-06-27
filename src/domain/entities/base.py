from datetime import UTC, datetime
from typing import Any, Dict, Optional
from uuid import UUID


class BaseEntity:
    """Classe base para todas as entidades do domínio."""

    def __init__(
        self,
        id: Optional[Any] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
    ) -> None:
        """Inicializa uma nova instância da entidade base.

        Args:
            id: ID único da entidade.
            created_at: Data de criação. Se não fornecida, usa o momento atual.
            updated_at: Data de última atualização. Se não fornecida, usa momento atual.
        """
        self.id = id
        self.created_at = created_at or datetime.now(UTC)
        self.updated_at = updated_at or self.created_at

    def __eq__(self, other: object) -> bool:
        """Compara duas entidades por igualdade.

        Args:
            other: Outra entidade a ser comparada.

        Returns:
            bool: True se as entidades são iguais, False caso contrário.
        """
        if not isinstance(other, BaseEntity):
            return NotImplemented
        return self.id == other.id

    def __str__(self) -> str:
        """Retorna uma representação em string da entidade.

        Returns:
            str: Representação em string da entidade.
        """
        return f"BaseEntity(id={self.id})"

    def to_dict(self) -> Dict[str, Any]:
        """Converte a entidade para um dicionário.

        Returns:
            Dict[str, Any]: A entidade como um dicionário.
        """
        return {
            "id": str(self.id),
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    def update(self) -> None:
        """Atualiza o timestamp de última modificação."""
        self.updated_at = datetime.now(UTC)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "BaseEntity":
        """Cria uma nova instância da entidade a partir de um dicionário.

        Args:
            data: Dicionário com os dados da entidade.

        Returns:
            BaseEntity: Nova instância da entidade.
        """
        return cls(
            id=UUID(data["id"]) if isinstance(data["id"], str) else data["id"],
            created_at=datetime.fromisoformat(data["created_at"])
            if isinstance(data["created_at"], str)
            else data["created_at"],
            updated_at=datetime.fromisoformat(data["updated_at"])
            if isinstance(data["updated_at"], str)
            else data["updated_at"],
        )
