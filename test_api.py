"""Script para testar os endpoints de auto-extensão.

Este script testa os endpoints da API de auto-extensão para verificar
se estão funcionando corretamente.
"""

import json
from typing import Any, Dict, Optional
from urllib.parse import urlparse

import urllib3

# URLs para teste
BASE_URL = "http://localhost:8000"
ENDPOINTS = {
    "health": "/health",
    "capability_gaps": "/auto-extension/capability-gaps",
    "create_tool": "/auto-extension/tools",
    "feedback": "/auto-extension/tools/test-123/feedback",
}

# Dados para testes
TOOL_SPEC = {
    "name": "social_media_connector",
    "description": "Conecta com APIs de redes sociais",
    "parameters": {
        "platform": {"type": "string", "enum": ["twitter", "facebook"]},
        "action": {"type": "string", "enum": ["post", "get"]},
        "data": {"type": "object"},
    },
    "return_type": "object",
    "template_id": "api_connector",
    "security_level": "standard",
    "resource_requirements": {"memory_mb": 128, "timeout_seconds": 10},
}

FEEDBACK_DATA = {
    "rating": 4,
    "comments": "Funciona bem, mas é um pouco lento",
    "issues": [],
    "context": {},
}


def make_request(
    url: str, method: str = "GET", data: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """Faz uma requisição HTTP."""
    headers = {"Content-Type": "application/json"}

    encoded_data: Optional[bytes] = None
    # Validar o esquema da URL
    parsed_url = urlparse(url)
    if parsed_url.scheme not in ["http", "https"]:
        raise ValueError("Apenas URLs HTTP(S) são permitidas")

    # Configurar pool HTTP com certificação SSL
    http = urllib3.PoolManager(cert_reqs="CERT_REQUIRED", ca_certs=None)

    # Preparar dados
    encoded_data = json.dumps(data).encode("utf-8") if data else None

    try:
        # Fazer requisição com urllib3
        response = http.request(
            method=method,
            url=url,
            body=encoded_data,
            headers=headers,
            timeout=urllib3.Timeout(connect=5.0, read=10.0),
        )

        response_data = response.data.decode("utf-8")
        return {
            "status": response.status,
            "data": json.loads(response_data) if response_data else None,
        }
    except Exception as e:
        print(f"Erro ao fazer requisição: {e}")
        return {"status": 500, "error": str(e)}


def test_endpoint(
    name: str, url: str, method: str = "GET", data: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """Testa um endpoint específico."""
    print(f"\n--- Testando {name} ---")
    print(f"URL: {url}")
    print(f"Método: {method}")

    if data:
        print(f"Dados: {json.dumps(data, indent=2)}")

    result = make_request(url, method, data)

    print(f"Status: {result.get('status')}")

    if "error" in result:
        print(f"Erro: {result['error']}")
    elif result.get("data"):
        print(f"Resposta: {json.dumps(result['data'], indent=2)}")
    else:
        print("Sem dados na resposta")

    return result


def run_tests() -> None:
    """Executa todos os testes."""
    # Testar health check
    test_endpoint("Health Check", f"{BASE_URL}{ENDPOINTS['health']}")

    # Testar lacunas de capacidade
    test_endpoint("Capability Gaps", f"{BASE_URL}{ENDPOINTS['capability_gaps']}")

    # Testar criação de ferramenta
    test_endpoint(
        "Create Tool", f"{BASE_URL}{ENDPOINTS['create_tool']}", "POST", TOOL_SPEC
    )

    # Testar feedback
    test_endpoint(
        "Tool Feedback", f"{BASE_URL}{ENDPOINTS['feedback']}", "POST", FEEDBACK_DATA
    )


if __name__ == "__main__":
    print("Iniciando testes da API de auto-extensão...")
    run_tests()
    print("\nTestes concluídos!")
