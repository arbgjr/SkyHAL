from unittest.mock import AsyncMock, patch

import pytest

from src.infrastructure.llm_client_myai import MyAILLMClient


@pytest.mark.asyncio
async def test_myai_generate_code_success():
    client = MyAILLMClient(base_url="https://fake-myai.com", api_key="fake-key")
    fake_response = {
        "message": {"content": "```python\ndef foo():\n    return 42\n```"}
    }
    with patch("httpx.AsyncClient.post", new_callable=AsyncMock) as mock_post:
        mock_post.return_value.json = lambda: fake_response
        mock_post.return_value.raise_for_status.return_value = None
        code = await client.generate_code("def foo(): return 42")
        assert code.strip().startswith("def foo():")
        assert "```" not in code


@pytest.mark.asyncio
async def test_myai_generate_code_no_markdown():
    client = MyAILLMClient(base_url="https://fake-myai.com", api_key="fake-key")
    fake_response = {"message": {"content": "def bar():\n    return 1"}}
    with patch("httpx.AsyncClient.post", new_callable=AsyncMock) as mock_post:
        mock_post.return_value.json = lambda: fake_response
        mock_post.return_value.raise_for_status.return_value = None
        code = await client.generate_code("def bar(): return 1")
        assert code.strip().startswith("def bar():")


@pytest.mark.asyncio
async def test_myai_generate_code_error():
    client = MyAILLMClient(base_url="https://fake-myai.com", api_key="fake-key")
    with patch("httpx.AsyncClient.post", new_callable=AsyncMock) as mock_post:
        mock_post.side_effect = Exception("erro de rede")
        with pytest.raises(Exception) as exc:
            await client.generate_code("def fail(): pass")
        assert "erro de rede" in str(exc.value)
