"""
Testes unitários para o orquestrador de geração de código via LLM.
"""
import pytest

from src.application.llm_code_orchestrator import CodeGenRequest, LLMCodeOrchestrator


class MockLLMClient:
    """Cliente LLM simulado para testes."""

    def __init__(self, output=None, error=None):
        self.output = output or "def example_function():\n    return 'Hello, world!'"
        self.error = error
        self.calls = []

    async def generate_code(self, *args, **kwargs):
        self.calls.append((args, kwargs))
        if self.error:
            raise self.error
        return self.output


@pytest.mark.asyncio
async def test_validate_short_prompt():
    """Testa validação de prompt muito curto."""
    client = MockLLMClient()
    orchestrator = LLMCodeOrchestrator(client)

    with pytest.raises(ValueError) as excinfo:
        await orchestrator.generate_code(CodeGenRequest(prompt="oi"))

    assert "curto" in str(excinfo.value)
    assert not client.calls  # Cliente não deve ser chamado


@pytest.mark.asyncio
async def test_validate_semantics_no_function():
    """Testa validação semântica quando não há função no código."""
    client = MockLLMClient(output="# apenas comentário, sem função")
    orchestrator = LLMCodeOrchestrator(client)

    with pytest.raises(ValueError) as excinfo:
        await orchestrator.generate_code(CodeGenRequest(prompt="crie uma função"))

    assert "função Python" in str(excinfo.value)
    assert len(client.calls) == 1  # Cliente deve ser chamado uma vez


@pytest.mark.asyncio
async def test_quota_limit():
    """Testa erro quando o limite de quota é atingido."""
    client = MockLLMClient(error=RuntimeError("Limite de uso do LLM atingido"))
    orchestrator = LLMCodeOrchestrator(client)

    with pytest.raises(RuntimeError) as excinfo:
        await orchestrator.generate_code(CodeGenRequest(prompt="crie uma função"))

    assert "Limite de uso" in str(excinfo.value)
    assert len(client.calls) == 1  # Cliente deve ser chamado uma vez


@pytest.mark.asyncio
async def test_successful_code_generation():
    """Testa geração de código bem-sucedida."""
    expected_code = "def hello_world():\n    return 'Hello, world!'"
    client = MockLLMClient(output=expected_code)
    orchestrator = LLMCodeOrchestrator(client)

    result = await orchestrator.generate_code(
        CodeGenRequest(prompt="crie uma função de saudação")
    )

    assert result == expected_code
    assert len(client.calls) == 1  # Cliente deve ser chamado uma vez
