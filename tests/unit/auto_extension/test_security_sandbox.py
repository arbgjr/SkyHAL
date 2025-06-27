"""Testes unitários para o sandbox de segurança.

Este módulo contém testes unitários para verificar o funcionamento
do sandbox de segurança do sistema de auto-extensão.
"""

from unittest.mock import AsyncMock, patch

import pytest

from src.domain.auto_extension.security_sandbox import SecuritySandbox


class TestSecuritySandbox:
    """Conjunto de testes para o sandbox de segurança."""

    @pytest.fixture
    def resource_monitor(self):
        """Cria um mock para o monitor de recursos."""
        monitor = AsyncMock()
        monitor.start_monitoring.return_value = "monitor-123"
        monitor.get_usage.return_value = {
            "cpu_percent": 10.5,
            "memory_mb": 45.2,
            "execution_time_ms": 350,
            "io_operations": 2,
        }
        return monitor

    @pytest.fixture
    def code_analyzer(self):
        """Cria um mock para o analisador de código."""
        analyzer = AsyncMock()
        analyzer.scan_for_vulnerabilities.return_value = {
            "vulnerabilities": [],
            "risk_score": 0.2,
            "is_safe": True,
        }
        return analyzer

    @pytest.mark.asyncio
    async def test_execute_code_safely(self, resource_monitor, code_analyzer):
        """Testa a execução segura de código."""
        # Criar sandbox com mocks
        sandbox = SecuritySandbox(resource_monitor, code_analyzer)

        # Código seguro para teste
        safe_code = """
def add(a, b):
    return a + b

result = add(5, 3)
"""

        # Executar código
        with patch("builtins.__import__"):
            success, output = await sandbox.execute_safely(
                code=safe_code, params={"a": 5, "b": 3}, timeout_ms=1000
            )

        # Verificar resultado
        assert success is True
        assert output is not None
        assert "result" in output
        assert output["result"] == 8

        # Verificar que o monitor foi usado
        resource_monitor.start_monitoring.assert_called_once()
        resource_monitor.get_usage.assert_called_once()

    @pytest.mark.asyncio
    async def test_execute_unsafe_code(self, resource_monitor, code_analyzer):
        """Testa a detecção de código inseguro."""
        # Criar sandbox com mocks
        sandbox = SecuritySandbox(resource_monitor, code_analyzer)

        # Configurar o analisador para detectar vulnerabilidades
        code_analyzer.scan_for_vulnerabilities.return_value = {
            "vulnerabilities": [
                {
                    "type": "os_command_injection",
                    "severity": "high",
                    "line": 3,
                    "description": "Execução potencialmente perigosa de comandos do sistema",
                }
            ],
            "risk_score": 0.9,
            "is_safe": False,
        }

        # Código malicioso para teste
        unsafe_code = """
import os
def execute_command(cmd):
    return os.system(cmd)

result = execute_command("echo Hello")
"""

        # Executar código
        success, output = await sandbox.execute_safely(
            code=unsafe_code, params={}, timeout_ms=1000
        )

        # Verificar resultado
        assert success is False
        assert "error" in output
        assert "vulnerabilities" in output
        assert output["vulnerabilities"][0]["type"] == "os_command_injection"

    @pytest.mark.asyncio
    async def test_resource_limit_enforcement(self, resource_monitor, code_analyzer):
        """Testa a aplicação de limites de recursos."""
        # Criar sandbox com mocks
        sandbox = SecuritySandbox(resource_monitor, code_analyzer)

        # Configurar o monitor para relatar uso excessivo de recursos
        resource_monitor.get_usage.return_value = {
            "cpu_percent": 95.0,  # Alto uso de CPU
            "memory_mb": 850.5,  # Alto uso de memória
            "execution_time_ms": 450,
            "io_operations": 10,
        }
        resource_monitor.check_limits.return_value = (
            False,
            {
                "exceeded": ["cpu", "memory"],
                "details": {
                    "cpu_percent": {"limit": 80.0, "actual": 95.0},
                    "memory_mb": {"limit": 500, "actual": 850.5},
                },
            },
        )

        # Código que consome muitos recursos
        heavy_code = """
def intensive_task():
    result = 0
    for i in range(10**7):
        result += i
    return result

result = intensive_task()
"""

        # Executar código
        success, output = await sandbox.execute_safely(
            code=heavy_code,
            params={},
            timeout_ms=1000,
            resource_limits={"cpu_percent": 80.0, "memory_mb": 500},
        )

        # Verificar resultado
        assert success is False
        assert "resource_violation" in output
        assert "exceeded" in output["resource_violation"]
        assert "cpu" in output["resource_violation"]["exceeded"]
        assert "memory" in output["resource_violation"]["exceeded"]
