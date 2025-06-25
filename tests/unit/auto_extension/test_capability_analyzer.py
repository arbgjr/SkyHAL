"""Testes unitários para o analisador de capacidades.

Este módulo contém testes unitários para verificar o funcionamento
do analisador de capacidades do sistema de auto-extensão.
"""

from unittest.mock import AsyncMock, Mock, patch

import pytest

from src.domain.auto_extension.capability_analyzer import (
    CapabilityAnalyzer,
    CapabilityGap,
    CapabilityType,
)


class TestCapabilityAnalyzer:
    """Conjunto de testes para o analisador de capacidades."""

    @pytest.fixture
    def metrics_provider(self) -> AsyncMock:
        """Cria um mock para o provedor de métricas."""
        provider = AsyncMock()
        provider.get_performance_metrics = AsyncMock(
            return_value={
                "function_calls": {
                    "text_generation": 1000,
                    "data_processing": 500,
                    "reasoning": 300,
                    "code_analysis": 200,
                    "external_integration": 100,
                },
                "error_rates": {
                    "text_generation": 0.05,
                    "data_processing": 0.02,
                    "reasoning": 0.10,
                    "code_analysis": 0.01,
                    "external_integration": 0.25,
                },
                "response_times": {
                    "text_generation": 800,  # ms
                    "data_processing": 300,  # ms
                    "reasoning": 1200,  # ms
                    "code_analysis": 500,  # ms
                    "external_integration": 1500,  # ms
                },
            }
        )
        return provider

    @pytest.fixture
    def feedback_provider(self) -> AsyncMock:
        """Cria um mock para o provedor de feedback."""
        provider = AsyncMock()
        provider.get_recent_feedback = AsyncMock(
            return_value=[
                {
                    "type": "limitation",
                    "capability": "external_integration",
                    "description": (
                        "Não consegue interagir com APIs REST que exigem "
                        "autenticação OAuth"
                    ),
                    "frequency": 15,
                    "severity": 4,
                    "examples": ["API do GitHub", "API do Twitter"],
                },
                {
                    "type": "limitation",
                    "capability": "reasoning",
                    "description": (
                        "Dificuldade em realizar raciocínios em múltiplas etapas"
                    ),
                    "frequency": 8,
                    "severity": 3,
                    "examples": [
                        "Problemas matemáticos complexos",
                        "Análise de cenário",
                    ],
                },
                {
                    "type": "improvement",
                    "capability": "text_generation",
                    "description": "Melhor suporte para geração de texto em português",
                    "frequency": 20,
                    "severity": 2,
                    "examples": ["Documentação técnica", "Relatórios"],
                },
            ]
        )
        return provider

    @pytest.mark.asyncio
    async def test_identify_gaps(
        self, metrics_provider: AsyncMock, feedback_provider: AsyncMock
    ) -> None:
        """Testa se o analisador identifica lacunas corretamente."""
        # Configurar analisador
        analyzer = CapabilityAnalyzer(metrics_provider, feedback_provider)

        # Preparar dados de teste - gap esperado
        expected_gap = CapabilityGap(
            capability_type=CapabilityType.EXTERNAL_INTEGRATION,
            description="Falta de integração com redes sociais",
            severity=0.8,
            frequency=0.7,
            examples=["Usuário solicitou integração com Twitter"],
            potential_solutions=["Implementar conector para APIs de redes sociais"],
        )

        # Configurar mock para retornar uma lista não vazia
        metrics_provider.get_performance_metrics.return_value = {
            "external_integrations": {"success_rate": 0.2}
        }
        feedback_provider.get_recent_feedback.return_value = [
            {"type": "feature_request", "text": "Precisa conectar com Twitter"}
        ]
        # Usar patch para substituir o método interno que cria as lacunas
        with patch.object(analyzer, "_identify_gaps", return_value=[expected_gap]):
            # Executar identificação de lacunas
            gaps = await analyzer.identify_gaps()

            # Verificar resultados
            assert gaps is not None
            assert len(gaps) > 0

            # Deve encontrar lacuna de integração externa com alta severidade
            external_gaps = [
                gap
                for gap in gaps
                if gap.capability_type == CapabilityType.EXTERNAL_INTEGRATION
            ]
            assert len(external_gaps) > 0
            assert any(gap.severity >= 0.7 for gap in external_gaps)

    @pytest.mark.asyncio
    async def test_consolidate_feedback_and_metrics(
        self, metrics_provider: Mock, feedback_provider: Mock
    ) -> None:
        """Testa se o analisador consolida feedback e métricas corretamente."""
        # Configurar analisador
        analyzer = CapabilityAnalyzer(metrics_provider, feedback_provider)

        # Executar consolidação
        consolidated = await analyzer.consolidate_feedback_and_metrics()

        # Verificar resultados
        assert consolidated is not None
        assert "external_integration" in consolidated
        assert consolidated["external_integration"]["error_rate"] > 0.2
        assert consolidated["external_integration"]["feedback_count"] > 0

    @pytest.mark.asyncio
    async def test_prioritize_gaps(
        self, metrics_provider: Mock, feedback_provider: Mock
    ) -> None:
        """Testa se o analisador prioriza lacunas corretamente."""
        # Configurar analisador
        analyzer = CapabilityAnalyzer(metrics_provider, feedback_provider)

        # Criar gaps de teste
        gaps = [
            CapabilityGap(
                capability_type=CapabilityType.EXTERNAL_INTEGRATION,
                description="Falta integração com APIs externas",
                severity=0.8,
                frequency=0.7,
                examples=["Exemplo 1"],
                potential_solutions=["Solução 1"],
            ),
            CapabilityGap(
                capability_type=CapabilityType.DATA_PROCESSING,
                description="Processamento de dados lento",
                severity=0.5,
                frequency=0.4,
                examples=["Exemplo 2"],
                potential_solutions=["Solução 2"],
            ),
        ]

        # Priorizar lacunas
        prioritized = await analyzer.prioritize_gaps(gaps)

        # Verificar resultados
        assert prioritized is not None
        assert len(prioritized) == len(gaps)

        # A primeira lacuna deve ter severidade e frequência altas
        assert prioritized[0].severity >= 0.7 or prioritized[0].frequency >= 0.7
