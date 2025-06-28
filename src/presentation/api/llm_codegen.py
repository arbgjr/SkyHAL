"""
API REST para geração de código via LLM.
Inclui autenticação, autorização e rate limiting.
"""
import os
from typing import Optional

import structlog
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordBearer
from opentelemetry import trace
from opentelemetry.trace import Status, StatusCode
from prometheus_client import Counter, Histogram
from slowapi import Limiter
from slowapi.util import get_remote_address

from src.application.llm_code_orchestrator import CodeGenRequest, LLMCodeOrchestrator
from src.infrastructure.llm_client import LLMClient
from src.infrastructure.llm_client_myai import MyAILLMClient

router = APIRouter(prefix="/llm-codegen", tags=["llm-codegen"])
logger = structlog.get_logger()

# Configuração de autenticação e rate limiting
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
limiter = Limiter(key_func=get_remote_address)


def get_llm_client(llm_config: Optional[dict] = None) -> LLMClient:
    """Seleciona o client LLM conforme provider informado no payload/config."""
    provider = (
        (llm_config or {}).get("provider", os.getenv("LLM_PROVIDER", "openai")).lower()
    )
    if provider == "myai":
        # MyAILLMClient deve herdar de LLMClient
        client = MyAILLMClient(
            base_url=os.getenv(
                "LLM_API_URL", "http://localhost:4242/api/v0/chat/completions"
            ),
            api_key=os.getenv("LLM_API_KEY", "42m4n)0-2063210-824n)40-6u1m42435jun102"),
            family=os.getenv("LLM_FAMILY", "openai"),
            model=os.getenv("LLM_MODEL", "o4-mini"),
        )
        # Garantir que o tipo é compatível
        return client
    # Default: OpenAI
    return LLMClient(
        base_url=os.getenv("LLM_API_URL", "https://api.openai.com"),
        api_key=os.getenv("LLM_API_KEY", "42m4n)0-2063210-824n)40-6u1m42435jun102"),
        family=os.getenv("LLM_FAMILY", "openai"),
        model=os.getenv("LLM_MODEL", "gpt-4"),
    )


llm_codegen_requests = Counter(
    "llm_codegen_requests_total",
    "Total de requisições ao endpoint de geração de código via LLM",
    ["status"],
)
llm_codegen_latency = Histogram(
    "llm_codegen_latency_seconds",
    "Latência das requisições ao endpoint de geração de código via LLM",
)
tracer = trace.get_tracer(__name__)


def get_client_ip(request: Request) -> str:
    """Obtém o IP do cliente de forma segura, tratando proxies."""
    # Verifica headers de proxy primeiro
    forwarded_for = request.headers.get("X-Forwarded-For")
    if forwarded_for:
        # Pega o primeiro IP da lista (cliente original)
        return forwarded_for.split(",")[0].strip()

    # Verifica header X-Real-IP
    real_ip = request.headers.get("X-Real-IP")
    if real_ip:
        return real_ip

    # Usa request.client se disponível
    if request.client:
        return request.client.host

    # Retorna valor padrão se nada estiver disponível
    return "unknown"


@router.post("/generate", dependencies=[Depends(oauth2_scheme)])
@limiter.limit("3/minute")
async def generate_code(request: Request, req: CodeGenRequest) -> dict:
    """Gera código a partir de um prompt usando LLM."""
    client_ip = get_client_ip(request)
    with llm_codegen_latency.time():
        with tracer.start_as_current_span("llm_codegen.generate_code") as span:
            span.set_attribute("user_ip", client_ip)
            span.set_attribute("prompt_len", len(req.prompt) if req.prompt else 0)
            try:
                # Seleção dinâmica do client conforme provider no payload
                llm_config = getattr(req, "extra_params", None) or {}
                client = get_llm_client(llm_config=llm_config.get("llm_config", {}))
                orchestrator = LLMCodeOrchestrator(client)
                code = await orchestrator.generate_code(req)
                logger.info("llm_codegen_success", user=client_ip, prompt=req.prompt)
                llm_codegen_requests.labels(status="success").inc()
                span.set_status(Status(StatusCode.OK))
                return {"code": code}
            except Exception as e:
                logger.error("llm_codegen_error", error=str(e), user=client_ip)
                llm_codegen_requests.labels(status="error").inc()
                span.set_status(Status(StatusCode.ERROR))
                span.record_exception(e)
                raise HTTPException(
                    status_code=400, detail="Erro ao gerar código: " + str(e)
                ) from e
