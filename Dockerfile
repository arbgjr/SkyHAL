# syntax=docker/dockerfile:1
FROM python:3.11-slim AS base

# Evitar prompts durante a instalação de pacotes
ENV DEBIAN_FRONTEND=noninteractive \
    # Impedir que Python grave arquivos pyc
    PYTHONDONTWRITEBYTECODE=1 \
    # Garantir que a saída do Python seja enviada imediatamente ao terminal
    PYTHONUNBUFFERED=1 \
    # Poetry não criará um ambiente virtual
    POETRY_VIRTUALENVS_CREATE=false \
    # Diretório de trabalho
    WORKDIR=/app

# Stage de desenvolvimento
FROM base AS development

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Instalar Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Adicionar Poetry ao PATH
ENV PATH="/root/.local/bin:$PATH"

# Copiar arquivos de configuração
COPY pyproject.toml poetry.lock ./

# Instalar dependências de desenvolvimento
RUN poetry install --no-interaction --no-ansi --with dev

# Copiar código fonte
COPY . .

# Stage de produção
FROM base AS production

# Instalar dependências do sistema mínimas
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Instalar Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Adicionar Poetry ao PATH
ENV PATH="/root/.local/bin:$PATH"

# Copiar arquivos de configuração
COPY pyproject.toml poetry.lock ./

# Instalar apenas dependências de produção
RUN poetry install --no-interaction --no-ansi --no-dev

# Copiar código fonte
COPY . .

# Expor porta da aplicação
EXPOSE 8000

# Comando para executar a aplicação
CMD ["poetry", "run", "uvicorn", "src.presentation.api.app:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
