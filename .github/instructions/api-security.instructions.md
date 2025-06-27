---
applyTo: "**"
---

# 🛡️ Segurança da API - Diretrizes Específicas

## 🎯 Para GitHub Copilot: Implementação Automática

### Autenticação (Sempre Implementar)

```python
from fastapi import Depends, FastAPI, HTTPException, Security
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from pydantic import BaseModel

# Configuração de autenticação
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.get("/resource")
async def get_resource(
    current_user: User = Depends(get_current_user)
):
    """Endpoint protegido com JWT."""
    return {"data": "protected"}
```

### Validação de Entrada (Padrão Obrigatório)

```python
from pydantic import BaseModel, Field, validator
from typing import Optional

class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: str = Field(..., regex=r"^[\w\.-]+@[\w\.-]+\.\w+$")
    password: str = Field(..., min_length=8)

    @validator("username")
    def validate_username(cls, v):
        if not v.isalnum():
            raise ValueError("Username deve conter apenas letras e números")
        return v
```

### Rate Limiting com FastAPI

```python
from fastapi import FastAPI
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app = FastAPI()
app.state.limiter = limiter

@app.get("/api/resource")
@limiter.limit("5/minute")
async def read_resource(request: Request):
    return {"data": "rate-limited-resource"}
```

### Logging Seguro (Estruturado)

```python
import structlog

logger = structlog.get_logger()

# ✅ CORRETO - Logging estruturado seguro
logger.info(
    "user_action",
    user_id=user.id,
    action="resource_access",
    resource_id=resource_id
)

# ❌ NUNCA FAZER - Expor dados sensíveis
# logger.info(f"User login: {user.email} with password: {password}")
```

## 🔒 Checklist de Segurança por Feature

### APIs REST
- [ ] Autenticação JWT implementada (via FastAPI security)
- [ ] Autorização baseada em roles/scopes
- [ ] Validação Pydantic em todas entradas
- [ ] Rate limiting configurado (slowapi)
- [ ] Headers de segurança (via middleware)
- [ ] HTTPS forçado
- [ ] Logging estruturado (structlog)

### Acesso a Dados
- [ ] SQLAlchemy com parâmetros escapados
- [ ] Validação de permissões (Row Level Security)
- [ ] Auditoria via OpenTelemetry
- [ ] SSL/TLS para conexões
- [ ] Secrets via env ou vault

### Tratamento de Erros
```python
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from fastapi.requests import Request

@app.exception_handler(HTTPException)
async def custom_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "code": exc.status_code,
                "message": "Erro no processamento da requisição"
            }
        }
    )
```
