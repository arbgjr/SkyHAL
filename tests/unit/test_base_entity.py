"""Example unit test module."""
from datetime import UTC, datetime
from typing import Optional

import pytest

from src.domain.entities.base import BaseEntity


class TestBaseEntity:
    """Testes unitários para a classe BaseEntity."""

    def test_base_entity_creation(self) -> None:
        """Test BaseEntity creation and attributes."""
        # Arrange
        entity_id = 1
        created_at = datetime.now(UTC)
        updated_at = datetime.now(UTC)

        # Act
        entity = BaseEntity(
            id=entity_id,
            created_at=created_at,
            updated_at=updated_at,
        )

        # Assert
        assert entity.id == entity_id
        assert entity.created_at == created_at
        assert entity.updated_at == updated_at

    def test_base_entity_equality(self) -> None:
        """Test BaseEntity equality comparison."""
        # Arrange
        entity1 = BaseEntity(id=1)
        entity2 = BaseEntity(id=1)
        entity3 = BaseEntity(id=2)

        # Act & Assert
        assert entity1 == entity2
        assert entity1 != entity3
        assert entity2 != entity3

    @pytest.mark.parametrize(
        "entity_id,expected_str",
        [
            (1, "BaseEntity(id=1)"),
            (None, "BaseEntity(id=None)"),
        ],
    )
    def test_base_entity_string_representation(
        self, entity_id: Optional[int], expected_str: str
    ) -> None:
        """Testa a representação em string de uma entidade base."""
        # Arrange
        entity = BaseEntity(id=entity_id)

        # Act & Assert
        assert str(entity) == expected_str
