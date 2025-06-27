# Especificação Técnica: Atualização de Dependências

## 📁 Artefato

**Caminho:** `pyproject.toml`

## 🎯 Objetivo

Atualizar dependências do projeto para incluir todas as bibliotecas necessárias para implementação da stack de observabilidade com OpenTelemetry, Prometheus e estrutlog.

## 📚 Instruções Relacionadas

- **observabilidade.instructions.md** - Ferramentas obrigatórias para observabilidade
- **python-mcp.instructions.md** - Gerenciamento de dependências com Poetry

## 🎨 Prompts Relacionados

- **observabilidade.prompt.md** - Dependências NuGet sugeridas (adaptar para Python)

## 🎯 Chat Mode Recomendado

- **backend.chatmode.md** - Para gerenciamento de dependências

## 🛠️ Dependências a Adicionar

### Observabilidade Core

```toml
# OpenTelemetry Core
opentelemetry-api = "^1.20.0"               # Já existe
opentelemetry-sdk = "^1.20.0"               # Já existe
opentelemetry-instrumentation = "^0.41b0"

# OpenTelemetry Instrumentações
opentelemetry-instrumentation-fastapi = "^0.41b0"    # Já existe
opentelemetry-instrumentation-requests = "^0.41b0"
opentelemetry-instrumentation-sqlalchemy = "^0.41b0"
opentelemetry-instrumentation-logging = "^0.41b0"

# OpenTelemetry Exportadores
opentelemetry-exporter-prometheus = "^1.12.0rc1"
opentelemetry-exporter-otlp = "^1.20.0"
opentelemetry-exporter-jaeger = "^1.20.0"

# Métricas e Monitoramento
prometheus-client = "^0.17.0"
structlog = "^23.1.0"                       # Já existe

# Utilitários
python-json-logger = "^2.0.7"
```

### Dependências de Desenvolvimento

```toml
# Testes de Observabilidade
pytest-mock = "^3.11.1"
responses = "^0.23.3"

# Análise de Cobertura
pytest-cov = "^4.1.0"                       # Já existe
```

## 📋 Arquivo pyproject.toml Atualizado

### Seção [tool.poetry.dependencies]

```toml
[tool.poetry.dependencies]
python = "^3.11"
fastapi = "^0.100.0"
uvicorn = "^0.22.0"
sqlalchemy = "^2.0.17"
pydantic = "^2.0.2"
python-jose = {extras = ["cryptography"], version = "^3.3.0"}
passlib = {extras = ["bcrypt"], version = "^1.7.4"}
python-multipart = "^0.0.6"
aiofiles = "^23.1.0"

# Observabilidade
structlog = "^23.1.0"
opentelemetry-api = "^1.20.0"
opentelemetry-sdk = "^1.20.0"
opentelemetry-instrumentation = "^0.41b0"
opentelemetry-instrumentation-fastapi = "^0.41b0"
opentelemetry-instrumentation-requests = "^0.41b0"
opentelemetry-instrumentation-sqlalchemy = "^0.41b0"
opentelemetry-instrumentation-logging = "^0.41b0"
opentelemetry-exporter-prometheus = "^1.12.0rc1"
opentelemetry-exporter-otlp = "^1.20.0"
opentelemetry-exporter-jaeger = "^1.20.0"
prometheus-client = "^0.17.0"
python-json-logger = "^2.0.7"
```

### Seção [tool.poetry.group.dev.dependencies]

```toml
[tool.poetry.group.dev.dependencies]
pytest = "^7.4.0"
pytest-cov = "^4.1.0"
pytest-asyncio = "^0.21.0"
pytest-mock = "^3.11.1"
black = "^23.3.0"
ruff = "^0.5.3"
mypy = "^1.4.1"
bandit = "^1.7.5"
safety = "^2.3.5"
pre-commit = "^3.3.3"
httpx = "^0.24.1"
responses = "^0.23.3"
```

## 🔧 Comandos de Instalação

### Para instalar todas as dependências

```bash
# Instalar dependências principais
poetry install

# Instalar dependências de desenvolvimento
poetry install --with dev

# Atualizar lock file
poetry lock --no-update

# Verificar dependências instaladas
poetry show
```

### Para verificar compatibilidade

```bash
# Verificar conflitos de dependências
poetry check

# Verificar vulnerabilidades de segurança
poetry run safety check

# Verificar versões desatualizadas
poetry show --outdated
```

## 📊 Impacto das Novas Dependências

### Tamanho Adicional Estimado

- OpenTelemetry (core + instrumentações): ~15MB
- Prometheus client: ~2MB
- Exportadores: ~8MB
- Utilitários: ~3MB
- **Total estimado:** ~28MB adicionais

### Compatibilidade

- Todas as dependências são compatíveis com Python 3.11+
- OpenTelemetry tem compatibilidade com FastAPI
- Prometheus client é thread-safe
- Estrutlog integra bem com OpenTelemetry

## ⚠️ Considerações de Segurança

### Dependências com Atenção Especial

```toml
# Verificar regularmente por vulnerabilidades
opentelemetry-exporter-otlp = "^1.20.0"    # Comunicação de rede
prometheus-client = "^0.17.0"              # Exposição de métricas
python-json-logger = "^2.0.7"              # Processamento de logs
```

### Comandos de Verificação de Segurança

```bash
# Verificar vulnerabilidades conhecidas
poetry run safety check

# Análise de segurança do código
poetry run bandit -r src/

# Verificar dependências desatualizadas
poetry show --outdated
```

## 🚀 Configuração de CI/CD

### GitHub Actions - Verificação de Dependências

```yaml
# .github/workflows/dependencies.yml
name: Dependencies Check

on: [push, pull_request]

jobs:
  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install Poetry
        run: |
          curl -sSL https://install.python-poetry.org | python3 -
          poetry --version

      - name: Check lock file
        run: poetry check

      - name: Install dependencies
        run: poetry install --with dev

      - name: Security check
        run: poetry run safety check

      - name: Check for outdated dependencies
        run: poetry show --outdated
```

## ✅ Checklist de Implementação

- [ ] Adicionar dependências de observabilidade ao pyproject.toml
- [ ] Executar `poetry install` para instalar novas dependências
- [ ] Executar `poetry check` para verificar compatibilidade
- [ ] Executar `poetry run safety check` para verificar segurança
- [ ] Atualizar poetry.lock com `poetry lock`
- [ ] Verificar se todas as importações funcionam
- [ ] Executar testes para validar funcionamento
- [ ] Documentar dependências adicionadas
- [ ] Configurar verificação de segurança no CI/CD

## 🔗 Dependências de Outros Artefatos

- **observability-infrastructure.md** - Usa as dependências instaladas
- **observability-middleware.md** - Depende das bibliotecas OpenTelemetry

## 📝 Notas Técnicas

- OpenTelemetry está em versão beta para algumas instrumentações
- Prometheus exporters podem ter versões release candidate
- Manter dependências atualizadas por questões de segurança
- Poetry permite instalação seletiva por grupos (dev, test, prod)
- Verificar compatibilidade entre versões do OpenTelemetry
