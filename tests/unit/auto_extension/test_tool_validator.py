"""Testes unitários para o validador de ferramentas.

Este módulo contém testes unitários para verificar o funcionamento
do validador de ferramentas (tools) do sistema de auto-extensão.
"""

from unittest.mock import AsyncMock

import pytest

from src.domain.auto_extension.tool_generator import GeneratedTool, ToolSpec
from src.domain.auto_extension.tool_validator import ToolValidator, ValidationResult


class TestToolValidator:
    """Conjunto de testes para o validador de ferramentas."""

    @pytest.fixture
    def security_sandbox(self) -> AsyncMock:
        """Cria um mock para o sandbox de segurança."""
        sandbox = AsyncMock()
        sandbox.execute_safely.return_value = (
            True,
            {"result": "success", "output": "Teste executado com sucesso"},
        )
        return sandbox

    @pytest.fixture
    def test_runner(self) -> AsyncMock:
        """Cria um mock para o executor de testes."""
        runner = AsyncMock()
        runner.run_tests.return_value = {
            "passed": True,
            "total": 5,
            "passed_count": 5,
            "failed_tests": [],
        }
        return runner

    @pytest.fixture
    def metrics_provider(self) -> AsyncMock:
        """Cria um mock para o provedor de métricas."""
        provider = AsyncMock()
        provider.record_validation.return_value = None
        return provider

    @pytest.fixture
    def mock_tool(self) -> GeneratedTool:
        """Cria uma ferramenta mock para testes."""
        tool_code = """
def test_calculator(operation, a, b):
    \"\"\"Ferramenta que executa operações aritméticas básicas.

    Args:
        operation: Operação a realizar (add, subtract, multiply, divide)
        a: Primeiro número
        b: Segundo número

    Returns:
        Resultado da operação
    \"\"\"
    if operation == "add":
        return a + b
    elif operation == "subtract":
        return a - b
    elif operation == "multiply":
        return a * b
    elif operation == "divide":
        return a / b if b != 0 else "Erro: divisão por zero"
"""

        return GeneratedTool(
            tool_id="test-123",
            name="test_calculator",
            code=tool_code,
            spec=ToolSpec(
                name="test_calculator",
                description="Uma ferramenta simples de cálculo",
                parameters={
                    "operation": {
                        "type": "string",
                        "enum": ["add", "subtract", "multiply", "divide"],
                    },
                    "a": {"type": "number"},
                    "b": {"type": "number"},
                },
                return_type="number",
                template_id="basic_function",
                security_level="standard",
                resource_requirements={"memory_mb": 128, "timeout_seconds": 5},
            ),
            validation_results={},
            version="1.0.0",
            created_at="2023-01-01T00:00:00Z",
        )

    @pytest.mark.asyncio
    async def test_validate_tool(
        self,
        security_sandbox: AsyncMock,
        test_runner: AsyncMock,
        metrics_provider: AsyncMock,
        mock_tool: GeneratedTool,
    ) -> None:
        """Testa a validação completa de uma ferramenta."""
        # Configurar validador
        validator = ToolValidator(
            sandbox_provider=security_sandbox,
            security_analyzer=metrics_provider,
            test_runner=test_runner,
        )

        # Definir retornos dos mocks
        security_sandbox.create_sandbox.return_value = security_sandbox
        metrics_provider.analyze.return_value = {
            "passed": True,
            "score": 0.95,
            "issues": [],
        }
        # Definir retorno bem-sucedido para teste
        test_runner.run_tests.return_value = {
            "all_passed": True,
            "passed": True,
            "total": 5,
            "passed_count": 5,
            "failed_tests": [],
            "performance_score": 0.95,
        }

        # Validar ferramenta
        result = await validator.validate_tool(mock_tool)

        # Verificar resultado
        assert result.result == ValidationResult.PASSED
        assert result.security_score >= 0.9
        assert len(result.recommendations) >= 0

        # Verificar chamadas aos mocks
        security_sandbox.create_sandbox.assert_called_once()
        metrics_provider.analyze.assert_called_once()
        test_runner.run_tests.assert_called_once()

    @pytest.mark.asyncio
    async def test_validate_tool_with_security_failure(
        self, security_sandbox, test_runner, metrics_provider, mock_tool
    ):
        """Testa a validação de uma ferramenta com falha de segurança."""
        # Configurar validador
        validator = ToolValidator(
            sandbox_provider=security_sandbox,
            security_analyzer=metrics_provider,
            test_runner=test_runner,
        )

        # Configurar falha de segurança
        security_sandbox.create_sandbox.return_value = security_sandbox
        metrics_provider.analyze.return_value = {
            "passed": False,
            "score": 0.3,
            "issues": [
                {
                    "type": "security_violation",
                    "severity": "high",
                    "description": "Acesso inseguro ao sistema de arquivos",
                }
            ],
        }

        # Validar ferramenta
        result = await validator.validate_tool(mock_tool)

        # Verificar resultado
        assert result.result == ValidationResult.FAILED_SECURITY
        assert result.security_score < 0.5
        assert len(result.issues) > 0
        assert any(
            "sistema de arquivos" in i.get("description", "") for i in result.issues
        )

        # Verificar que ainda executou os testes
        test_runner.run_tests.assert_called_once()

    @pytest.mark.asyncio
    async def test_validate_test_coverage(
        self, security_sandbox, test_runner, metrics_provider, mock_tool
    ):
        """Testa a validação de cobertura de testes."""
        # Configurar validador
        validator = ToolValidator(
            sandbox_provider=security_sandbox,
            security_analyzer=metrics_provider,
            test_runner=test_runner,
        )

        # Configurar mocks
        security_sandbox.create_sandbox.return_value = security_sandbox
        metrics_provider.analyze.return_value = {
            "passed": True,
            "score": 0.95,
            "issues": [],
        }  # Configurar resultados de testes com baixa cobertura
        test_runner.run_tests.return_value = {
            "passed": True,
            "total": 4,
            "passed_count": 3,
            "failed_tests": [
                {
                    "name": "test_divide_by_zero",
                    "error": (
                        "AssertionError: Expected 'Erro', got 'Erro: divisão por zero'"
                    ),
                }
            ],
            "coverage": {"percentage": 75.0, "missed_lines": [15, 16]},
        }
        # Validar ferramenta
        result = await validator.validate_tool(mock_tool)
        # Verificar resultado - com falha nos testes
        # O resultado esperado é FAILED_FUNCTIONALITY
        assert result.result == ValidationResult.FAILED_FUNCTIONALITY
        assert any("test_divide_by_zero" in rec for rec in result.recommendations)
