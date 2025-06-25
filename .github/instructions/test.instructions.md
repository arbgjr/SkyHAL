---
applyTo: "**/tests/**/*.py"
description: "Instruções padronizadas para testes automatizados em Python"
---

# 🧪 Instruções para Testes Automatizados em Projetos Python

## 🎯 Filosofia

- Qualidade vem com prevenção, não detecção tardia
- Testes são documentação executável
- Feedback rápido e confiável é mais valioso que cobertura absoluta
- Testes bem escritos facilitam refatorações seguras

---

## 📂 Organização e Estrutura

### Padrão de Diretórios

```
project/
├── src/
│   └── ...            # Código fonte
├── tests/
│   ├── unit/
│   ├── integration/
│   ├── e2e/
│   ├── conftest.py
│   └── **init**.py
```

### Nome dos Arquivos

- `test_<modulo>_<classe>_<cenario>_<resultado>.py`

---

## ✅ Estratégia de Testes

### Tipos de Teste

| Tipo         | Objetivo                                 | Exemplo de ferramenta         |
|--------------|-------------------------------------------|-------------------------------|
| Unitário     | Lógica isolada                           | `pytest`, `unittest.mock`     |
| Integração   | API + DB, Serviços externos              | `pytest + httpx` ou `TestClient` |
| E2E          | Fluxo completo da aplicação              | `Playwright`, `Selenium`      |
| Assíncrono   | Operações `async/await`                  | `pytest-asyncio`              |
| Parametrizado| Testar múltiplas entradas de forma concisa| `pytest.mark.parametrize`     |

---

## 🧱 Padrão AAA

Sempre use o padrão **Arrange → Act → Assert**:

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

---

## 🧪 Testes com pytest

### Fixtures e Mocks

```python
import pytest
from unittest.mock import Mock

@pytest.fixture
def mock_user_repo():
    return Mock()

@pytest.fixture
def user_service(mock_user_repo):
    return UserService(repo=mock_user_repo)

def test_get_user_when_exists_returns_user(user_service, mock_user_repo):
    expected_user = User(id=1, name="Test")
    mock_user_repo.get_by_id.return_value = expected_user

    result = user_service.get_user(1)

    assert result == expected_user
    mock_user_repo.get_by_id.assert_called_once_with(1)
```

### Teste com FastAPI

```python
from fastapi.testclient import TestClient
from app import app

@pytest.fixture
def client():
    return TestClient(app)

def test_get_user_returns_200(client):
    response = client.get("/users/1")
    assert response.status_code == 200
    assert "id" in response.json()
```

### Teste Assíncrono

```python
import pytest

@pytest.mark.asyncio
async def test_async_op():
    service = AsyncService()
    result = await service.run()
    assert result is not None
```

### Parametrização

```python
@pytest.mark.parametrize("name,error", [
    ("", "Nome é obrigatório"),
    (None, "Nome é obrigatório"),
    ("a", "Nome deve ter pelo menos 2 caracteres")
])
def test_create_user_invalid_name_raises_error(name, error, user_service):
    with pytest.raises(ValidationError) as exc:
        user_service.create_user({"name": name})
    assert str(exc.value) == error
```

---

## 🧼 Boas Práticas

* Teste comportamento, não implementação interna
* Evite mocks excessivos em testes de integração
* Testes devem rodar rapidamente e de forma confiável
* Utilize `conftest.py` para fixtures compartilhadas
* Sempre limpe recursos após execução (ex: `tmp_path`, banco, conexões)

---

## 🧮 Cobertura e Métricas

* Cobertura mínima: **80%**
* Use `pytest-cov`:

```bash
pytest --cov=src --cov-report=term-missing --cov-report=html tests/
```

* Priorize 100% de cobertura em regras de negócio
* Configure verificação de cobertura no CI/CD

---

## 📊 Métricas de Qualidade

* Tempo médio de execução por suite
* Número de testes flaky
* Tempo médio até detecção de falha (MTTD)
* Cobertura por tipo (unit/integration)

---

## 🔧 Ferramentas Recomendadas

| Categoria   | Ferramenta                     |
| ----------- | ------------------------------ |
| Test runner | `pytest`, `pytest-asyncio`     |
| Mock/Stub   | `unittest.mock`, `pytest-mock` |
| Cobertura   | `pytest-cov`                   |
| Validação   | `pydantic`, `voluptuous`       |
| Segurança   | `bandit`, `safety`             |
| Linter      | `ruff`, `flake8`               |
| Formatador  | `black`                        |
| Tipagem     | `mypy`                         |
| Relatório   | `coverage html`                |

---
