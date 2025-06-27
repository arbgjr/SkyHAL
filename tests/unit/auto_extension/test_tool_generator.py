"""Testes unitários para o módulo de geração de ferramentas.

Este módulo contém testes unitários para verificar o funcionamento
do gerador de ferramentas (tools) do sistema de auto-extensão.
"""

from unittest.mock import AsyncMock

import pytest

from src.domain.auto_extension.tool_generator import (
    GeneratedTool,
    ToolGenerator,
    ToolSpec,
)


class TestToolGenerator:
    """Conjunto de testes para o gerador de ferramentas."""

    @pytest.fixture
    def template_provider(self) -> AsyncMock:
        """Cria um mock para o provedor de templates."""
        provider = AsyncMock()
        provider.get_template.return_value = (
            "def {{name}}({{params}}):\n" "    # Template de código\n" "    pass"
        )
        return provider

    @pytest.fixture
    def code_generator(self) -> AsyncMock:
        """Cria um mock para o gerador de código."""
        generator = AsyncMock()
        generator.generate.return_value = """def test_calculator(operation, a, b):
    if operation == 'add':
        return a + b
    elif operation == 'subtract':
        return a - b
    elif operation == 'multiply':
        return a * b
    elif operation == 'divide':
        return a / b if b != 0 else 'Erro: divisão por zero'"""
        return generator

    @pytest.fixture
    def security_validator(self) -> AsyncMock:
        """Cria um mock para o validador de segurança."""
        validator = AsyncMock()
        validator.validate.return_value = {"passed": True, "score": 0.95, "issues": []}
        return validator

    @pytest.fixture
    def tool_spec(self) -> ToolSpec:
        """Cria uma especificação de ferramenta para testes."""
        return ToolSpec(
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
        )

    @pytest.mark.asyncio
    async def test_generate_tool(
        self,
        template_provider: AsyncMock,
        code_generator: AsyncMock,
        security_validator: AsyncMock,
        tool_spec: ToolSpec,
    ) -> None:
        """Testa a geração completa de uma nova ferramenta."""
        # Configurar gerador
        generator = ToolGenerator(template_provider, code_generator, security_validator)

        # Gerar tool
        tool = await generator.generate_tool(tool_spec)

        # Verificar resultado
        assert isinstance(tool, GeneratedTool)
        assert tool.name == "test_calculator"
        assert "def test_calculator" in tool.code
        assert "add" in tool.code
        assert "multiply" in tool.code
        assert tool.validation_results["passed"] is True
        assert tool.validation_results["score"] == 0.95

    def test_validate_spec(
        self,
        template_provider: AsyncMock,
        code_generator: AsyncMock,
        security_validator: AsyncMock,
    ) -> None:
        """Testa a validação de especificação."""
        # Configurar gerador
        generator = ToolGenerator(template_provider, code_generator, security_validator)

        # Especificação válida
        valid_spec = ToolSpec(
            name="validtool",
            description="Uma ferramenta válida para testes",
            parameters={"input": {"type": "string"}},
            return_type="string",
            template_id="basic_function",
            security_level="standard",
            resource_requirements={"memory_mb": 128, "timeout_seconds": 30},
        )

        # Não deve lançar exceção
        generator._validate_spec(valid_spec)

        # Testar validação com erro: nome inválido
        with pytest.raises(ValueError) as excinfo:
            invalid_spec = ToolSpec(
                name="",  # Nome inválido
                description="Uma ferramenta inválida",
                parameters={"input": {"type": "string"}},
                return_type="string",
                template_id="basic_function",
                security_level="standard",
                resource_requirements={"memory_mb": 128, "timeout_seconds": 30},
            )
            generator._validate_spec(invalid_spec)

        assert "Nome" in str(excinfo.value)

    @pytest.mark.asyncio
    async def test_generate_tool_with_security_failure(
        self, template_provider, code_generator, security_validator, tool_spec
    ):
        """Testa a geração de ferramenta com falha de segurança."""
        # Configurar gerador
        generator = ToolGenerator(template_provider, code_generator, security_validator)

        # Configurar falha de segurança
        security_validator.validate.return_value = {
            "passed": False,
            "score": 0.3,
            "issues": ["Acesso inseguro ao sistema de arquivos"],
        }

        # Gerar tool
        tool = await generator.generate_tool(tool_spec)

        # Verificar que a validação falhou
        assert tool.validation_results["passed"] is False
        assert len(tool.validation_results["issues"]) > 0
        assert "sistema de arquivos" in tool.validation_results["issues"][0]
