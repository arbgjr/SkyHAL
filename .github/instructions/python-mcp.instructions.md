---
applyTo: "**.py*"
---
# 🐍 Desenvolvimento Python MCP - Diretrizes

## 🎯 Objetivos
- Garantir qualidade e consistência no desenvolvimento de servidores MCP
- Aplicar boas práticas Python e padrões MCP
- Facilitar manutenção e evolução do código

## 📋 Padrões de Código

### Estilo e Organização
- Seguir PEP 8 rigorosamente
- Usar classes ao invés de funções soltas
- Manter código modular e orientado a objetos
- Documentar usando docstrings (Google style)
- Limitar funções a 20 linhas

### Estrutura do Projeto
```
mcp_server/
├── src/
│   ├── core/           # Lógica central e abstrações
│   ├── endpoints/      # Endpoints MCP
│   ├── services/      # Serviços e regras de negócio
│   ├── models/        # Modelos e DTOs
│   └── utils/         # Utilitários e helpers
├── tests/            # Testes organizados em espelho com src/
└── config/          # Configurações e ambiente
```

### Dependências
- Usar Poetry para gerenciamento de dependências
- Manter `pyproject.toml` atualizado
- Documentar dependências no README
- Usar ambientes virtuais isolados

## 🔧 Desenvolvimento MCP

### Endpoints
```python
from typing import Dict, Any

class ExampleEndpoint:
    """Exemplo de endpoint MCP seguindo boas práticas."""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.logger = setup_logger(__name__)

    async def handle_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        try:
            # Validação de entrada
            self._validate_request(request)

            # Processamento
            result = await self._process_request(request)

            # Logging estruturado
            self.logger.info("Request processed", extra={
                "request_id": request.get("id"),
                "result": "success"
            })

            return result

        except ValidationError as e:
            self.logger.warning("Validation failed", exc_info=e)
            raise
        except Exception as e:
            self.logger.error("Processing failed", exc_info=e)
            raise
```

### Validação
```python
from dataclasses import dataclass
from typing import Optional

@dataclass
class RequestDTO:
    """Data Transfer Object para validação de requests."""
    id: str
    data: dict
    metadata: Optional[dict] = None

    def validate(self) -> None:
        """Valida os dados do request."""
        if not self.id:
            raise ValidationError("ID é obrigatório")
```

## 🧪 Testes

### Estrutura de Testes
```python
import pytest
from unittest.mock import Mock, patch

class TestExampleEndpoint:
    @pytest.fixture
    def endpoint(self):
        return ExampleEndpoint(config={"key": "value"})

    @pytest.mark.asyncio
    async def test_handle_request_success(self, endpoint):
        # Arrange
        request = {"id": "123", "data": {}}

        # Act
        result = await endpoint.handle_request(request)

        # Assert
        assert result["status"] == "success"
```

### Cobertura
- Mínimo 90% de cobertura
- Testar cenários de erro
- Incluir testes de integração
- Usar fixtures para setup comum

## 📊 Observabilidade

### Logging
```python
import structlog

logger = structlog.get_logger()
logger.info("action_performed",
    action="process_request",
    request_id="123",
    duration_ms=42
)
```

### Métricas
- Usar OpenTelemetry para métricas
- Monitorar latência de endpoints
- Tracking de erros e exceções
- Métricas de uso de recursos

## 🔒 Segurança

### Boas Práticas
- Validar todas as entradas
- Sanitizar dados
- Usar secrets management
- Implementar rate limiting
- Seguir princípio do menor privilégio

### Exemplo de Rate Limiting
```python
from functools import wraps
from ratelimit import limits, RateLimitException

CALLS = 100
RATE_LIMIT = 60  # 1 minute

@limits(calls=CALLS, period=RATE_LIMIT)
async def rate_limited_endpoint(request):
    """Endpoint com rate limiting."""
    return await process_request(request)
```

## 🔄 Integração com Memory Bank

### Atualização
- Documentar mudanças significativas
- Registrar decisões de arquitetura
- Manter padrões consistentes
- Atualizar exemplos e referências

### Links
- [Documentação MCP](../docs/mcp/)
- [Padrões Python](../docs/python/)
- [Guia de Testes](../docs/testing/)
