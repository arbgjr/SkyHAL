# Políticas de Acesso e Práticas Seguras – Auto-Extensão MCP

## Autenticação e Autorização

- Todos os endpoints protegidos por autenticação JWT (ver exemplos em `api-security.instructions.md`)
- Autorização baseada em roles/scopes para operações críticas
- Tokens com expiração curta e renovação via refresh token

## Práticas Seguras

- Validação rigorosa de todas as entradas (Pydantic)
- Logging estruturado sem dados sensíveis
- Rate limiting configurado (slowapi)
- Headers de segurança aplicados via middleware
- Uso de variáveis de ambiente para secrets

## Exemplo de Endpoint Seguro

```python
from fastapi import Depends, APIRouter
from src.infrastructure.security import get_current_user

router = APIRouter()

@router.get("/tools/{tool_id}")
async def get_tool(tool_id: str, user=Depends(get_current_user)):
    # ... lógica ...
    return {"tool_id": tool_id}
```

## Referências

- `api-security.instructions.md`
- `src/presentation/api/`
- `config/observability.yaml`
