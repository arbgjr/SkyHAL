from types import SimpleNamespace

import pytest

from src.domain.auto_extension.providers import ProviderError, TemplateCodeProvider


class DummyTemplateManager:
    async def get_template(self, template_id):
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
async def test_template_code_provider_success():
    provider = TemplateCodeProvider(DummyTemplateManager())
    spec = make_spec()
    code = await provider.generate(spec)
    assert "def foo" in code
    assert "return x + 1" in code


@pytest.mark.asyncio
async def test_template_code_provider_error(monkeypatch):
    class FailingManager:
        async def get_template(self, template_id):
            raise Exception("template not found")

    provider = TemplateCodeProvider(FailingManager())
    spec = make_spec()
    with pytest.raises(ProviderError):
        await provider.generate(spec)
