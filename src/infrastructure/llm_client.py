"""
Módulo de integração com provedores LLM (ex: OpenAI, Azure OpenAI).
Responsável por enviar prompts e receber respostas de geração de código.
"""
from typing import Any, Dict, Optional

import httpx
import structlog

logger = structlog.get_logger()


class LLMClient:
    def __init__(
        self,
        base_url: str,
        api_key: str,
        family: str = "openai",
        model: str = "o4-mini",
        timeout: int = 30,
        max_retries: int = 3,
        quota_limit: int = 1000,
        config: Optional[Dict[str, Any]] = None,
    ):
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.model = model
        self.family = family
        self.timeout = timeout
        self.max_retries = max_retries
        self.quota_limit = quota_limit
        self.usage_count = 0
        self.config = config or {}

    async def generate_code(
        self,
        prompt: str,
        temperature: float = 0.2,
        max_tokens: int = 1024,
        extra_params: Optional[Dict[str, Any]] = None,
    ) -> str:
        if self.usage_count >= self.quota_limit:
            logger.warning("Limite de uso do LLM atingido", quota=self.quota_limit)
            raise RuntimeError("Limite de uso do LLM atingido")
        payload = {
            "family": self.config.get("family", self.family),
            "model": self.config.get("model", self.model),
            "prompt": prompt,
            "temperature": self.config.get("temperature", temperature),
            "max_tokens": self.config.get("max_tokens", max_tokens),
        }
        if extra_params:
            payload.update(extra_params)
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        last_exc: Optional[Exception] = None
        for attempt in range(1, self.max_retries + 1):
            try:
                async with httpx.AsyncClient(timeout=self.timeout) as client:
                    response = await client.post(
                        f"{self.base_url}/v1/completions", json=payload, headers=headers
                    )
                    response.raise_for_status()
                    data = response.json()
                    self.usage_count += 1
                    logger.info("llm_request_success", attempt=attempt, prompt=prompt)
                    return str(data["choices"][0]["text"])
            except Exception as e:
                last_exc = e
                logger.warning(
                    "Tentativa LLM falhou", attempt=attempt, error=str(e), prompt=prompt
                )
        logger.error(
            "Erro ao chamar LLM após retries", error=str(last_exc), prompt=prompt
        )
        # Garante que sempre temos uma exceção válida para lançar
        if last_exc is not None:
            raise last_exc
        else:
            raise RuntimeError(
                "Falha ao executar requisição LLM após todas as tentativas"
            )
