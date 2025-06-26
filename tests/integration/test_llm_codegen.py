"""
Testes de integração para o endpoint de geração de código via LLM.
"""
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from src.presentation.api.llm_codegen import router

app = FastAPI()
app.include_router(router)


@pytest.fixture
def client():
    return TestClient(app)


def test_generate_code_unauthorized(client):
    resp = client.post("/llm-codegen/generate", json={"prompt": "print('oi')"})
    assert resp.status_code == 401


def test_generate_code_invalid_prompt(client):
    # Simula autenticação fake
    headers = {"Authorization": "Bearer fake"}
    resp = client.post("/llm-codegen/generate", json={"prompt": "oi"}, headers=headers)
    assert resp.status_code == 400
    assert "curto" in resp.json()["detail"]


def test_generate_code_semantic_validation(client, monkeypatch):
    # Simula autenticação fake
    headers = {"Authorization": "Bearer fake"}

    # Monkeypatch para forçar resposta sem função Python
    async def fake_generate_code(*a, **kw):
        return "# apenas comentário, sem função"

    # Patcha o llm_client já instanciado no módulo da API
    from src.presentation.api import llm_codegen

    monkeypatch.setattr(
        llm_codegen.llm_client,
        "generate_code",
        fake_generate_code,
    )
    resp = client.post(
        "/llm-codegen/generate", json={"prompt": "crie uma função"}, headers=headers
    )
    assert resp.status_code == 400
    assert "função Python" in resp.json()["detail"]


def test_generate_code_quota_limit(client, monkeypatch):
    # Simula autenticação fake
    headers = {"Authorization": "Bearer fake"}

    # Monkeypatch para simular quota excedida
    def fake_generate_code(*a, **kw):
        raise RuntimeError("Limite de uso do LLM atingido")

    from src.application import llm_code_orchestrator

    monkeypatch.setattr(
        llm_code_orchestrator.LLMCodeOrchestrator,
        "generate_code",
        lambda self, req: fake_generate_code(),
    )
    resp = client.post(
        "/llm-codegen/generate", json={"prompt": "crie uma função"}, headers=headers
    )
    assert resp.status_code == 400
    assert "Limite de uso" in resp.json()["detail"]
