from types import SimpleNamespace

import pytest

from src.domain.auto_extension.providers import (
    HybridCodeProvider,
    LLMCodeProvider,
    ProviderError,
    TemplateCodeProvider,
)


class DummyTemplateManager:
    async def get_template(self, template_id=None, **kwargs):
        return {"code_template": "def foo(x):\n    return x + 1"}


def make_spec():
    return SimpleNamespace(
        name="foo",
        description="Soma 1",
        parameters={"x": 1},
        return_type="int",
        template_id="dummy",
        security_level="low",
        resource_requirements={},
    )


@pytest.mark.asyncio
async def test_llm_code_provider_success():
    config = {"url": "https://fake-llm.com", "model": "fake-model"}
    provider = LLMCodeProvider(config)
    spec = make_spec()
    code = await provider.generate(spec, prompt="Gere uma função foo")
    assert "# Código gerado pela LLM" in code


@pytest.mark.asyncio
async def test_hybrid_code_provider_fallback():
    class FailingLLM:
        async def generate(self, spec, prompt=None):
            raise ProviderError("LLM indisponível")

    template_provider = TemplateCodeProvider(DummyTemplateManager())
    hybrid = HybridCodeProvider(FailingLLM(), template_provider, mode="hybrid")
    spec = make_spec()
    code = await hybrid.generate(spec)
    assert "def foo" in code


@pytest.mark.asyncio
async def test_hybrid_code_provider_llm_mode():
    class DummyLLM:
        async def generate(self, spec, prompt=None):
            return "# Código LLM"

    template_provider = TemplateCodeProvider(DummyTemplateManager())
    hybrid = HybridCodeProvider(DummyLLM(), template_provider, mode="llm")
    spec = make_spec()
    code = await hybrid.generate(spec)
    assert code == "# Código LLM"


@pytest.mark.asyncio
async def test_hybrid_code_provider_template_mode():
    class DummyLLM:
        async def generate(self, spec, prompt=None):
            return "# Código LLM"

    template_provider = TemplateCodeProvider(DummyTemplateManager())
    hybrid = HybridCodeProvider(DummyLLM(), template_provider, mode="template")
    spec = make_spec()
    code = await hybrid.generate(spec)
    assert "def foo" in code
