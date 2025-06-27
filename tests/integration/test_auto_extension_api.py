"""Testes de integração para o sistema de auto-extensão.

Este módulo contém testes de integração para verificar o funcionamento
conjunto dos componentes do sistema de auto-extensão.
"""

from unittest.mock import AsyncMock, patch

import pytest
from fastapi.testclient import TestClient

from src.domain.auto_extension.capability_analyzer import CapabilityAnalyzer
from src.domain.auto_extension.tool_generator import ToolGenerator
from src.presentation.api.app import app


class TestAutoExtensionAPI:
    """Testes de integração para a API de auto-extensão."""

    @pytest.fixture
    def client(self) -> TestClient:
        """Cria um cliente de teste para a API."""
        return TestClient(app)

    @pytest.fixture
    def mock_capability_analyzer(self) -> AsyncMock:
        """Retorna um mock do analisador de capacidades."""
        analyzer = AsyncMock(spec=CapabilityAnalyzer)
        analyzer.identify_gaps.return_value = [
            {
                "capability_type": "external_integration",
                "description": "Falta de integração com APIs de redes sociais",
                "severity": 0.8,
                "frequency": 0.7,
                "examples": ["Twitter API", "Facebook API"],
                "potential_solutions": ["Desenvolver connector específico"],
            }
        ]
        return analyzer

    @pytest.fixture
    def mock_tool_generator(self) -> AsyncMock:
        """Retorna um mock do gerador de ferramentas."""
        generator = AsyncMock(spec=ToolGenerator)
        generator.generate_tool.return_value = {
            "tool_id": "test-123",
            "name": "social_media_connector",
            "code": "def social_media_connector(platform, action, data):\n    pass",
            "spec": {
                "name": "social_media_connector",
                "description": "Conecta com APIs de redes sociais",
                "parameters": {
                    "platform": {"type": "string", "enum": ["twitter", "facebook"]},
                    "action": {"type": "string", "enum": ["post", "get"]},
                    "data": {"type": "object"},
                },
                "return_type": "object",
            },
            "validation_results": {"passed": True, "score": 0.95},
            "version": "1.0.0",
        }
        return generator

    @pytest.mark.asyncio
    async def test_get_capability_gaps(
        self, client: TestClient, mock_capability_analyzer: AsyncMock
    ) -> None:
        """Testa a obtenção de lacunas de capacidade via API."""
        # Mock da função de análise de capacidades
        with patch(
            "src.presentation.api.routers.auto_extension.get_capability_analyzer",
            return_value=mock_capability_analyzer,
        ):
            # Fazer requisição para obter lacunas
            response = client.get("/auto-extension/capability-gaps")

        # Verificar resposta
        assert response.status_code == 200
        data = response.json()
        assert "gaps" in data
        assert len(data["gaps"]) > 0
        assert data["gaps"][0]["capability_type"] == "external_integration"

    @pytest.mark.asyncio
    async def test_generate_tool(
        self, client: TestClient, mock_tool_generator: AsyncMock
    ) -> None:
        """Testa a geração de uma nova ferramenta via API."""

        # Mock do validator usando AsyncMock
        from unittest.mock import AsyncMock

        mock_validator = AsyncMock()
        mock_validator.validate_tool.return_value = {
            "passed": True,
            "score": 0.95,
            "issues": [],
        }

        # Garante que o mock do generator sempre retorna um dicionário novo
        def generator_return(*args, **kwargs):
            return {
                "tool_id": "test-123",
                "name": "social_media_connector",
                "code": "def social_media_connector(platform, action, data):\n    pass",
                "spec": {
                    "name": "social_media_connector",
                    "description": "Conecta com APIs de redes sociais",
                    "parameters": {
                        "platform": {"type": "string", "enum": ["twitter", "facebook"]},
                        "action": {"type": "string", "enum": ["post", "get"]},
                        "data": {"type": "object"},
                    },
                    "return_type": "object",
                },
                "validation_results": {"passed": True, "score": 0.95},
                "version": "1.0.0",
            }

        mock_tool_generator.generate_tool.side_effect = generator_return

        with patch(
            "src.presentation.api.routers.auto_extension.get_tool_generator",
            return_value=mock_tool_generator,
        ), patch(
            "src.presentation.api.routers.auto_extension.get_tool_validator",
            return_value=mock_validator,
        ):
            from tests.integration.jwt_test_utils import generate_test_jwt

            token = generate_test_jwt()
            tool_spec = {
                "name": "social_media_connector",
                "description": "Conecta com APIs de redes sociais",
                "parameters": {
                    "platform": {"type": "string", "enum": ["twitter", "facebook"]},
                    "action": {"type": "string", "enum": ["post", "get"]},
                    "data": {"type": "object"},
                },
                "return_type": "object",
                "template_id": "api_connector",
                "security_level": "standard",
                "resource_requirements": {"memory_mb": 128, "timeout_seconds": 10},
            }
            response = client.post(
                "/auto-extension/tools",
                json=tool_spec,
                headers={"Authorization": f"Bearer {token}"},
            )

        assert response.status_code == 201
        data = response.json()
        assert "tool_id" in data
        assert data["name"] == "social_media_connector"
        assert "code" in data
        assert data["validation_results"]["passed"] is True

    @pytest.mark.asyncio
    async def test_tool_feedback(self, client):
        """Testa o envio de feedback sobre uma ferramenta via API."""
        # Mock da função que lida com feedback
        with patch(
            "src.presentation.api.routers.auto_extension.process_feedback",
            return_value={"feedback_id": "feedback-123", "status": "processed"},
        ) as mock_process:
            # Dados do feedback
            feedback_data = {
                "tool_id": "test-123",
                "user_id": "user-456",
                "rating": 4,
                "comments": "Funciona bem, mas é um pouco lento",
                "improvement_suggestions": ["Melhorar performance"],
            }

            # Fazer requisição para enviar feedback
            response = client.post(
                "/auto-extension/tools/test-123/feedback", json=feedback_data
            )

        # Verificar que a função de processamento foi chamada
        mock_process.assert_called_once()

        # Verificar resposta
        assert response.status_code == 202
        data = response.json()
        assert "feedback_id" in data
        assert data["status"] == "processed"
