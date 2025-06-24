# 🧪 Testes

Este diretório contém os testes automatizados do projeto.

## Estrutura

```plaintext
tests/
├── unit/           # Testes unitários
├── integration/    # Testes de integração
└── conftest.py    # Fixtures compartilhadas
```

## Tipos de Testes

### Testes Unitários
- Testam componentes isoladamente
- Sem dependências externas
- Rápidos e determinísticos
- Cobertura de casos de borda

### Testes de Integração
- Testam interações entre componentes
- Usam banco de dados em memória
- Validam fluxos completos
- Testam APIs e interfaces

## Fixtures

O arquivo `conftest.py` contém fixtures compartilhadas:

- `app`: Instância FastAPI para testes
- `db_engine`: Engine SQLAlchemy assíncrono
- `session_factory`: Fábrica de sessões
- `db_session`: Sessão de banco isolada
- `client`: Cliente HTTP para testes

## Execução

```bash
# Todos os testes
poetry run pytest

# Com cobertura
poetry run pytest --cov=src

# Relatório HTML
poetry run pytest --cov=src --cov-report=html

# Testes específicos
poetry run pytest tests/unit/
poetry run pytest tests/integration/
```

## Cobertura

- Mínimo: 80% de cobertura
- Relatório em HTML: `htmlcov/index.html`
- Exclusões documentadas em `pyproject.toml`

## Boas Práticas

1. **Organização**
   - Um módulo de teste por módulo de código
   - Nomes descritivos para testes
   - Agrupar testes relacionados em classes

2. **Estrutura**
   - Seguir padrão Arrange-Act-Assert
   - Usar fixtures para setup comum
   - Testar casos de sucesso e erro

3. **Manutenção**
   - Manter testes simples e focados
   - Evitar duplicação de código
   - Documentar casos complexos

4. **Performance**
   - Testes unitários rápidos
   - Usar async/await apropriadamente
   - Minimizar setup/teardown
