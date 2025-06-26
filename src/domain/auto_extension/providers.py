"""
Interfaces para providers de geração de código e especificação (LLM, template, híbrido).
Atende à especificação técnica em docs/especificacoes-tecnicas/llm-auto-extensao.md.
"""

from typing import Any, Dict, Optional, Protocol

import structlog

try:
    from .entities import ToolSpec
except ImportError:
    from src.domain.auto_extension.entities import ToolSpec

logger = structlog.get_logger()


class CodeGenerationProvider(Protocol):
    async def generate(self, spec: ToolSpec, prompt: Optional[str] = None) -> str:
        ...


class SpecGenerationProvider(Protocol):
    async def generate(
        self, context: Dict[str, Any], prompt: Optional[str] = None
    ) -> ToolSpec:
        ...


class ProviderError(Exception):
    """Exceção base para erros de providers de geração."""

    pass


class TemplateCodeProvider:
    """Provider que gera código a partir de template local."""

    def __init__(self, template_manager: Any):
        self.template_manager = template_manager
        self.logger = logger.bind(provider="TemplateCodeProvider")

    async def generate(self, spec: ToolSpec, prompt: Optional[str] = None) -> str:
        try:
            # Suporta tanto método síncrono quanto assíncrono
            get_template = getattr(self.template_manager, "get_template", None)
            if get_template is None:
                raise ProviderError(
                    "PromptTemplateManager não possui método get_template"
                )
            import inspect

            if inspect.iscoroutinefunction(get_template):
                template = await get_template(spec.template_id)
            else:
                template = get_template(spec.template_id)
            self.logger.info("template_obtido", template_id=spec.template_id)
            # Simples substituição, pode ser expandido
            params: Any = spec.parameters or {}
            # Se for lista de dicts, mescla tudo em um só dict
            if isinstance(params, list):
                merged: Dict[str, Any] = {}
                for d in params:
                    if isinstance(d, dict):
                        for k, v in d.items():
                            merged[k] = v
                params = merged
            elif not isinstance(params, dict):
                params = dict(params)
            # Garante que todas as chaves são str
            params = {str(k): v for k, v in params.items()}
            code = template.get(
                "code_template", "# Código gerado por template não definido"
            ).format(**params)
            if not code:
                code = "# Código gerado por template não definido"
            self.logger.info("codigo_gerado", tool=spec.name)
            return str(code)
        except Exception as e:
            self.logger.error("erro_template_provider", error=str(e), tool=spec.name)
            raise ProviderError(f"Erro ao gerar código via template: {e}") from e


class LLMCodeProvider:
    """Provider que gera código usando LLM externa (OpenAI, Anthropic, etc.)."""

    def __init__(self, llm_config: Dict[str, Any]):
        self.llm_config = llm_config
        self.logger = logger.bind(provider="LLMCodeProvider")

    async def generate(self, spec: ToolSpec, prompt: Optional[str] = None) -> str:
        try:
            # Monta payload dinâmico
            _ = self._build_payload(spec, prompt)  # payload pode ser usado futuramente
            self.logger.info(
                "enviando_llm",
                url=self.llm_config.get("url"),
                model=self.llm_config.get("model"),
            )
            # Aqui seria feita a chamada HTTP assíncrona (placeholder)
            # response = await httpx.post(...)
            # code = self._parse_response(response)
            code = "# Código gerado pela LLM (placeholder)"
            self.logger.info("codigo_gerado_llm", tool=spec.name)
            return str(code)
        except Exception as e:
            self.logger.error("erro_llm_provider", error=str(e), tool=spec.name)
            raise ProviderError(f"Erro ao gerar código via LLM: {e}") from e

    def _build_payload(self, spec: ToolSpec, prompt: Optional[str]) -> Dict[str, Any]:
        # Monta payload conforme config e prompt
        payload = dict(self.llm_config.get("request_payload", {}))
        payload["prompt"] = prompt or self.llm_config.get("prompt_template", "")
        payload["tool_spec"] = spec.__dict__
        return payload


class HybridCodeProvider:
    """Provider que seleciona dinamicamente entre dois providers compatíveis (LLM, template, etc.)."""

    def __init__(self, llm_provider: Any, template_provider: Any, mode: str = "hybrid"):
        self.llm_provider = llm_provider
        self.template_provider = template_provider
        self.mode = mode
        self.logger = logger.bind(provider="HybridCodeProvider")

    async def generate(self, spec: ToolSpec, prompt: Optional[str] = None) -> str:
        try:
            if self.mode == "llm":
                return str(await self.llm_provider.generate(spec, prompt))
            elif self.mode == "template":
                return str(await self.template_provider.generate(spec, prompt))
            else:  # hybrid
                try:
                    return str(await self.llm_provider.generate(spec, prompt))
                except ProviderError:
                    self.logger.warning("fallback_template", tool=spec.name)
                    return str(await self.template_provider.generate(spec, prompt))
        except Exception as e:
            self.logger.error("erro_hybrid_provider", error=str(e), tool=spec.name)
            raise ProviderError(f"Erro no HybridCodeProvider: {e}") from e
