"""
Orquestrador para geração de código via LLM.
Responsável por receber prompts, acionar o client LLM, validar e sanitizar o código gerado.
"""

import re
from typing import Any, Dict, Optional

import structlog
from opentelemetry import trace
from opentelemetry.trace import Status, StatusCode
from prometheus_client import Counter, Histogram
from pydantic import BaseModel

orchestrator_requests = Counter(
    "llm_orchestrator_requests_total",
    "Total de chamadas ao orquestrador de geração de código via LLM",
    ["status"],
)
orchestrator_latency = Histogram(
    "llm_orchestrator_latency_seconds",
    "Latência das chamadas ao orquestrador de geração de código via LLM",
)
tracer = trace.get_tracer(__name__)
logger = structlog.get_logger()


class CodeGenRequest(BaseModel):
    prompt: str
    temperature: float = 0.2
    max_tokens: int = 1024
    extra_params: Optional[Dict[str, Any]] = None


class LLMCodeOrchestrator:
    def __init__(self, llm_client):
        """
        Aceita qualquer objeto com método async generate_code.
        Isso permite mocks e dublês em testes.
        """
        self.llm_client = llm_client

    async def generate_code(self, req: CodeGenRequest) -> str:
        with orchestrator_latency.time():
            with tracer.start_as_current_span("llm_orchestrator.generate_code") as span:
                span.set_attribute("prompt_len", len(req.prompt) if req.prompt else 0)
                try:
                    if not req.prompt or len(req.prompt) < 10:
                        orchestrator_requests.labels(status="error").inc()
                        raise ValueError("Prompt muito curto para geração de código.")
                    # Sempre executa fluxo de sanitização e validação, mesmo se monkeypatchado
                    code = await self.llm_client.generate_code(
                        prompt=req.prompt,
                        temperature=req.temperature,
                        max_tokens=req.max_tokens,
                        extra_params=req.extra_params,
                    )
                    code = self._sanitize_code(code)
                    self._validate_code(code)
                    self._validate_semantics(code)
                    orchestrator_requests.labels(status="success").inc()
                    span.set_status(Status(StatusCode.OK))
                    return str(code)
                except Exception as e:
                    orchestrator_requests.labels(status="error").inc()
                    logger.error(
                        "Erro no orquestrador LLM", error=str(e), prompt=req.prompt
                    )
                    span.set_status(Status(StatusCode.ERROR))
                    span.record_exception(e)
                    raise

    def _sanitize_code(self, code: str) -> str:
        # Remove execuções perigosas e imports proibidos
        dangerous = [
            r"import os",
            r"import sys",
            r"exec(",
            r"eval(",
            r"subprocess",
            r"open(",
        ]
        for pattern in dangerous:
            try:
                code = re.sub(
                    pattern, "# REMOVIDO POR SEGURANÇA", code, flags=re.IGNORECASE
                )
            except re.error as e:
                logger.error(
                    "Regex inválido em _sanitize_code", error=str(e), pattern=pattern
                )
        return code

    def _validate_code(self, code: str) -> None:
        # Exemplo: valida se é Python e não contém comandos proibidos
        if "# REMOVIDO POR SEGURANÇA" in code:
            raise ValueError("Código gerado contém comandos inseguros.")
        if len(code.strip()) < 10:
            raise ValueError("Código gerado muito curto ou vazio.")

    def _validate_semantics(self, code: str) -> None:
        # Validação semântica simples: verifica se há pelo menos uma função Python
        if not re.search(r"def \w+\(.*\):", code):
            logger.warning(
                "Código gerado não contém função Python detectada", code=code
            )
            raise ValueError("Código gerado não contém função Python detectada.")
