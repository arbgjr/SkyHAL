# 🚀 Guia de Desenvolvimento

## Requisitos

- Python 3.11+
- Poetry
- Git

## Configuração do Ambiente

1. **Clone o repositório**
```bash
git clone https://github.com/arbgjr/SkyHAL.git
cd SkyHAL
```

2. **Configure o Poetry**
```bash
# Instalar Poetry (se necessário)
curl -sSL https://install.python-poetry.org | python3 -

# Configurar ambiente virtual no projeto
poetry config virtualenvs.in-project true

# Instalar dependências
poetry install
```

3. **Configurar pre-commit hooks**
```bash
poetry run pre-commit install
```

## Comandos Úteis

### Desenvolvimento
```bash
# Ativar ambiente virtual
poetry shell

# Adicionar dependência
poetry add pacote

# Adicionar dependência de desenvolvimento
poetry add --group dev pacote
```

### Testes
```bash
# Rodar todos os testes
poetry run pytest

# Com cobertura
poetry run pytest --cov=src --cov-report=html

# Testes específicos
poetry run pytest tests/path/to/test.py
```

### Qualidade de Código
```bash
# Formatar código
poetry run black src tests

# Verificar estilo
poetry run ruff check src tests

# Verificar tipos
poetry run mypy src

# Análise de segurança
poetry run bandit -r src
poetry run safety check
```

## VS Code Settings

Para melhor experiência de desenvolvimento, configure o VS Code:

```json
{
  "python.defaultInterpreterPath": "${workspaceFolder}/.venv/bin/python",
  "python.formatting.provider": "black",
  "python.linting.enabled": true,
  "python.linting.flake8Enabled": false,
  "python.linting.mypyEnabled": true,
  "editor.formatOnSave": true,
  "editor.codeActionsOnSave": {
    "source.organizeImports": true
  }
}
```

## Estrutura do Projeto

```plaintext
SkyHAL/
├── src/               # Código fonte
│   ├── domain/       # Regras de negócio
│   ├── application/  # Casos de uso
│   ├── infrastructure/ # Implementações
│   └── presentation/ # APIs
├── tests/            # Testes
├── docs/             # Documentação
└── pyproject.toml    # Configuração Poetry
```

## Padrões de Código

1. **Estilo**
   - Seguir PEP 8
   - Usar Black para formatação
   - Manter linha máxima de 88 caracteres

2. **Tipos**
   - Usar type hints em todo código novo
   - Validar com mypy em modo estrito

3. **Testes**
   - Manter cobertura mínima de 80%
   - Usar pytest para testes
   - Seguir padrão Arrange-Act-Assert

4. **Documentação**
   - Docstrings em todas as funções públicas
   - README.md atualizado em cada diretório
   - Documentar decisões arquiteturais

## Observabilidade

O projeto usa OpenTelemetry para observabilidade:

- Logs estruturados via `structlog`
- Traces distribuídos
- Métricas de aplicação
- Exportação para backends compatíveis
