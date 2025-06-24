---
applyTo: "**"
---

# 🧪 Estratégia de Testes - Implementação Prática

## 🎯 Para GitHub Copilot: Geração Automática de Testes

### Padrão AAA Obrigatório

```python
def test_user_service_create_user_returns_created_user():
    # Arrange
    user_data = {"name": "Test User", "email": "test@example.com"}
    user_service = UserService()
    
    # Act
    result = user_service.create_user(user_data)
    
    # Assert
    assert result.name == user_data["name"]
    assert result.email == user_data["email"]
```

### Nomenclatura Padrão

**Formato**: `test_<classe>_<método>_<cenário>_<resultado_esperado>`

**Exemplos**:

```python
def test_user_service_create_user_with_valid_email_returns_user():
    """Testa criação de usuário com email válido."""

def test_user_service_create_user_with_invalid_email_raises_validation_error():
    """Testa que email inválido lança erro."""

def test_user_service_create_user_when_email_exists_raises_conflict():
    """Testa que email duplicado lança erro."""
```

### Fixtures e Mocks

```python
import pytest
from unittest.mock import Mock, patch

@pytest.fixture
def mock_user_repo():
    return Mock()

@pytest.fixture
def user_service(mock_user_repo):
    return UserService(repo=mock_user_repo)

def test_get_user_when_exists_returns_user(user_service, mock_user_repo):
    # Arrange
    expected_user = User(id=1, name="Test")
    mock_user_repo.get_by_id.return_value = expected_user
    
    # Act
    result = user_service.get_user(1)
    
    # Assert
    assert result == expected_user
    mock_user_repo.get_by_id.assert_called_once_with(1)
```

### Testes de API (FastAPI)

```python
from fastapi.testclient import TestClient

@pytest.fixture
def client():
    return TestClient(app)

def test_get_user_returns_200(client):
    # Arrange
    user_id = 1
    
    # Act
    response = client.get(f"/users/{user_id}")
    
    # Assert
    assert response.status_code == 200
    assert response.json()["id"] == user_id
```

### Testes Parametrizados

```python
@pytest.mark.parametrize("name,expected_error", [
    ("", "Nome é obrigatório"),
    ("a", "Nome deve ter pelo menos 2 caracteres"),
    (None, "Nome é obrigatório")
])
def test_create_user_with_invalid_name_raises_error(
    name, expected_error, user_service
):
    with pytest.raises(ValidationError) as exc:
        user_service.create_user({"name": name})
    assert str(exc.value) == expected_error
```

### Testes Assíncronos

```python
@pytest.mark.asyncio
async def test_async_operation():
    # Arrange
    service = AsyncService()
    
    # Act
    result = await service.process()
    
    # Assert
    assert result is not None
```

## ✅ Diretrizes de Cobertura

- Mínimo 80% de cobertura total
- 100% em domínio e casos de uso
- Usar `pytest-cov` para relatórios
- Configurar no CI/CD

## 📊 Relatórios

```bash
pytest --cov=src --cov-report=html tests/
```
