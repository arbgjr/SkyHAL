---
description: "Instruções personalizadas e padronizadas para projetos Python com GitHub Copilot"
applyTo: "**"
---

# Instruções para GitHub Copilot – Projeto Python (MCP Server)

## 🎯 Contexto

- **Linguagem principal**: Python 3.11+
- **Framework arquitetural**: Clean Architecture
- **Filosofia do time**: Qualidade, segurança e manutenibilidade primeiro
- **Gerenciador de dependências**: [Poetry](https://python-poetry.org/)
- **Testes**: [pytest](https://docs.pytest.org/)
- **Observabilidade**: OpenTelemetry
- **Logging estruturado**: `structlog`
- **Diretório principal**: `mcp_server/src/`
- **Testes**: `mcp_server/tests/`

---

## 🧠 Princípios Fundamentais

- **Código > Documentação** – o código deve ser autoexplicativo
- **Simplicidade > Complexidade** – mantenha legibilidade
- **Segurança em primeiro lugar** – evite falhas previsíveis
- **Fail Fast** – falhas devem ser visíveis e explícitas
- **Testabilidade obrigatória** – todo código precisa ser testável
- **Evite mágica** – código explícito é melhor que implícito

---

## 🎨 Estilo de Código Python

- Siga **PEP 8** e **PEP 257**
- Use **docstrings** em todas as classes e funções públicas
- Classes devem seguir **princípios SOLID**
- Evite **strings mágicas** e números hardcoded
- Prefira composição a herança
- Funções devem ter no máximo **20 linhas** e **1 responsabilidade**
- Use `typing` sempre que possível

---

## 🧪 Estratégia de Testes

- Use **pytest** como test runner padrão
- Siga o padrão **AAA**: Arrange, Act, Assert
- Testes devem cobrir: casos felizes, edge cases e falhas esperadas
- Use **mocks** para dependências externas
- Testes devem ser **determinísticos** e **isolados**
- Estrutura recomendada:
  ```bash
  tests/
  ├── unit/
  ├── integration/
  └── conftest.py
  ```

### Cobertura

* Mínimo de **80%** de cobertura global
* **100%** em lógica crítica (domínio)
* Use `pytest-cov` para análise de cobertura

---

## 🧰 Ferramentas Obrigatórias

| Categoria           | Ferramenta          |
| ------------------- | ------------------- |
| Testes              | pytest, pytest-mock |
| Coverage            | pytest-cov          |
| Logging             | structlog           |
| Observabilidade     | OpenTelemetry SDK   |
| Segurança           | Bandit, safety      |
| Linter              | flake8, ruff        |
| Formatador          | black               |
| Tipagem Estática    | mypy                |
| Gerenciador de deps | poetry              |

---

## 🚧 Tratamento de Erros

* Use `try/except` com logging de exceções inesperadas
* Nunca oculte erros silenciosamente
* Crie exceções específicas do domínio (`class RegraNegocioInvalida(Exception)`)
* Logue com contexto: `logger.error("Erro ao processar pagamento", exc_info=True, extra={"id_pagamento": id})`

---

## 🔐 Segurança

* Valide toda entrada de dados, mesmo interna
* Nunca exponha segredos, tokens ou dados sensíveis em logs
* Use `pydantic` ou `attrs` para validação de estruturas
* Implemente autenticação e autorização explícitas
* Limite privilégios e escopos de acesso em APIs

---

## 📦 Arquitetura de Pastas (Clean Architecture)

```
mcp_server/
├── src/
│   ├── domain/         # Regras de negócio
│   ├── application/    # Casos de uso e orquestração
│   ├── infrastructure/ # Banco de dados, APIs externas
│   └── main.py         # Ponto de entrada
├── tests/
│   ├── unit/
│   └── integration/
└── config/             # Arquivos YAML, .env, etc.
```

---

## ✅ Checklist de Conformidade

Antes de finalizar código:

* [ ] Segue arquitetura e organização do projeto?
* [ ] Código está testável e com testes criados?
* [ ] Aplica princípios SOLID?
* [ ] Tipagem e validações completas?
* [ ] Logs estruturados com contexto?
* [ ] Evita acoplamento excessivo?
* [ ] Respeita limites de camada da Clean Architecture?
* [ ] Segue PEP8 + black + mypy?
* [ ] Não há segredos nem informações sensíveis hardcoded?

---

## 📝 Referências Internas

* [`prompts/regras-gerais.prompt.md`](./prompts/regras-gerais.prompt.md) – Persona padrão
* [`prompts/mcp-server/testing.prompt.md`](./prompts/mcp-server/testing.prompt.md) – Estratégia de testes
* [`instructions/python-mcp.instructions.md`](./instructions/python-mcp.instructions.md) – Instruções específicas do servidor
* [`memory-bank.instructions.md`](./instructions/memory-bank.instructions.md) – Persistência de contexto

---

**Importante**: Qualquer violação desses padrões deve ser justificada em [`tech-debt.instructions.md`](./instructions/tech-debt.instructions.md) ou registrada como bug em [`bugs_founded.instructions.md`](./instructions/bugs_founded.instructions.md).

```

---
