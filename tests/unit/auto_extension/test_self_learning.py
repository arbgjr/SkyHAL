"""Testes unitários para o sistema de auto-aprendizado.

Este módulo contém testes unitários para verificar o funcionamento
do sistema de auto-aprendizado do módulo de auto-extensão.
"""

from unittest.mock import AsyncMock

import pytest

from src.domain.auto_extension.self_learning import (
    PerformanceAnalysis,
    SelfLearningSystem,
)


class TestSelfLearningSystem:
    """Conjunto de testes para o sistema de auto-aprendizado."""

    @pytest.fixture
    def feedback_store(self) -> AsyncMock:
        """Cria um mock para o armazenamento de feedback."""
        store = AsyncMock()
        store.get_all_feedback.return_value = [
            {
                "tool_id": "123",
                "user_id": "user-1",
                "rating": 4,
                "comments": "Ferramenta útil, mas poderia ser mais rápida",
                "improvement_suggestions": ["Otimizar performance"],
                "created_at": "2023-01-01T10:00:00Z",
            },
            {
                "tool_id": "123",
                "user_id": "user-2",
                "rating": 2,
                "comments": "Muitos erros e resultados inconsistentes",
                "improvement_suggestions": ["Melhorar validação de entrada"],
                "created_at": "2023-01-02T11:00:00Z",
            },
            {
                "tool_id": "456",
                "user_id": "user-1",
                "rating": 5,
                "comments": "Excelente, funcionou perfeitamente",
                "improvement_suggestions": [],
                "created_at": "2023-01-03T09:00:00Z",
            },
        ]
        return store

    @pytest.fixture
    def tool_store(self) -> AsyncMock:
        """Cria um mock para o armazenamento de ferramentas."""
        store = AsyncMock()
        store.get_tool.return_value = {
            "tool_id": "123",
            "name": "test_tool",
            "code": "def test_tool(): pass",
            "status": "active",
            "version": "1.0.0",
            "created_at": "2023-01-01T00:00:00Z",
        }
        return store

    @pytest.fixture
    def metrics_provider(self) -> AsyncMock:
        """Cria um mock para o provedor de métricas."""
        provider = AsyncMock()
        provider.get_tool_metrics.return_value = {
            "usages": 120,
            "avg_execution_time": 45,
            "error_rate": 0.15,
            "successes": 102,
            "failures": 18,
        }
        return provider

    @pytest.mark.asyncio
    async def test_analyze_tool_performance(
        self,
        feedback_store: AsyncMock,
        tool_store: AsyncMock,
        metrics_provider: AsyncMock,
    ) -> None:
        """Testa a análise de desempenho de uma ferramenta."""
        # Configurar sistema de auto-aprendizado
        self_learning = SelfLearningSystem(feedback_store, tool_store, metrics_provider)

        # Analisar ferramenta
        analysis = await self_learning.analyze_tool_performance("123")

        # Verificar resultado
        assert isinstance(analysis, PerformanceAnalysis)
        assert analysis.tool_id == "123"
        assert "rating" in analysis.metrics
        assert "error_rate" in analysis.metrics
        assert len(analysis.feedback_summary) > 0
        assert len(analysis.improvement_suggestions) > 0

        # A média de avaliações deve estar correta
        assert 2.0 <= analysis.metrics["rating"] <= 4.0

        # Deve haver sugestões de melhoria
        assert any("performance" in s.lower() for s in analysis.improvement_suggestions)

    """Testa a geração de sugestões de melhoria."""

    @pytest.mark.asyncio
    async def test_generate_improvement_suggestions(
        self, feedback_store, tool_store, metrics_provider
    ):
        """Testa a geração de sugestões de melhoria."""
        # Configurar sistema de auto-aprendizado
        self_learning = SelfLearningSystem(feedback_store, tool_store, metrics_provider)

        # Configurar métricas com alta taxa de erro
        metrics_provider.get_tool_metrics.return_value = {
            "usages": 100,
            "avg_execution_time": 120,  # tempo elevado
            "error_rate": 0.35,  # taxa de erro elevada
            "successes": 65,
            "failures": 35,
        }

        # Gerar sugestões
        suggestions = await self_learning.generate_improvement_suggestions("123")

        # Verificar resultado
        assert len(suggestions) >= 2
        assert any("erro" in s.lower() for s in suggestions)
        assert any(
            "performance" in s.lower() or "desempenho" in s.lower() for s in suggestions
        )

    @pytest.mark.asyncio
    async def test_update_learning_model(
        self, feedback_store, tool_store, metrics_provider
    ):
        """Testa a atualização do modelo de aprendizado."""
        # Configurar sistema de auto-aprendizado
        self_learning = SelfLearningSystem(feedback_store, tool_store, metrics_provider)

        # Diversos feedbacks de diferentes ferramentas
        feedback_store.get_all_feedback.return_value = [
            {"tool_id": "123", "rating": 4, "comments": "Bom, mas lento"},
            {"tool_id": "123", "rating": 3, "comments": "Razoável"},
            {"tool_id": "456", "rating": 5, "comments": "Excelente"},
            {"tool_id": "456", "rating": 5, "comments": "Perfeito"},
            {"tool_id": "789", "rating": 1, "comments": "Não funciona"},
        ]

        # Atualizar modelo
        update_result = await self_learning.update_learning_model()

        # Verificar resultado
        assert update_result.success is True
        assert update_result.processed_feedback >= 5
        assert update_result.updated_tools >= 3
        assert len(update_result.insights) > 0
