"""
Testes unitários para o LLMClient.
"""
from unittest.mock import AsyncMock, patch

import pytest

from src.application.llm_code_orchestrator import CodeGenRequest, LLMCodeOrchestrator
from src.infrastructure.llm_client import LLMClient


@pytest.mark.asyncio
async def test_generate_code_success():
    client = LLMClient(base_url="https://fake-llm.com", api_key="fake", model="gpt-4")
    fake_response = {"choices": [{"text": "print('hello world')"}]}
    with patch("httpx.AsyncClient.post", new_callable=AsyncMock) as mock_post:
        mock_post.return_value.json = lambda: fake_response  # método síncrono
        mock_post.return_value.raise_for_status.return_value = None
        code = await client.generate_code("print hello", temperature=0.1, max_tokens=10)
        assert code == "print('hello world')"


@pytest.mark.asyncio
async def test_generate_code_error():
    client = LLMClient(base_url="https://fake-llm.com", api_key="fake", model="gpt-4")
    with patch("httpx.AsyncClient.post", new_callable=AsyncMock) as mock_post:
        mock_post.side_effect = Exception("erro de rede")
        with pytest.raises(Exception) as exc:
            await client.generate_code("print hello")
        assert "erro de rede" in str(exc.value)


@pytest.mark.asyncio
async def test_generate_code_quota_limit():
    client = LLMClient(base_url="https://fake-llm.com", api_key="fake", quota_limit=1)
    fake_response = {"choices": [{"text": "print('ok')"}]}
    with patch("httpx.AsyncClient.post", new_callable=AsyncMock) as mock_post:
        mock_post.return_value.json = lambda: fake_response  # método síncrono
        mock_post.return_value.raise_for_status.return_value = None
        # Primeira chamada deve passar
        code = await client.generate_code("print ok")
        assert code == "print('ok')"
        # Segunda chamada deve estourar quota
        with pytest.raises(RuntimeError) as exc:
            await client.generate_code("print again")
        assert "Limite de uso" in str(exc.value)


@pytest.mark.asyncio
async def test_generate_code_retries():
    client = LLMClient(base_url="https://fake-llm.com", api_key="fake", max_retries=2)
    with patch("httpx.AsyncClient.post", new_callable=AsyncMock) as mock_post:
        # Falha nas duas tentativas
        mock_post.side_effect = Exception("erro de rede")
        with pytest.raises(Exception) as exc:
            await client.generate_code("print fail")
        assert "erro de rede" in str(exc.value)


@pytest.mark.asyncio
async def test_orchestrator_semantic_validation():
    class DummyLLM:
        async def generate_code(self, *a, **kw):
            return "# apenas comentário, sem função"

    orchestrator = LLMCodeOrchestrator(DummyLLM())
    req = CodeGenRequest(prompt="teste função", temperature=0.1, max_tokens=10)
    with pytest.raises(ValueError) as exc:
        await orchestrator.generate_code(req)
    assert "função Python" in str(exc.value)
    assert "função Python" in str(exc.value)
