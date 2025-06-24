# 📦 Código-Fonte

## Estrutura

O projeto segue os princípios da Clean Architecture, organizando o código em camadas com responsabilidades bem definidas:

```plaintext
src/
├── domain/          # Regras de negócio e entidades
├── application/     # Casos de uso e interfaces
├── infrastructure/  # Implementações concretas
└── presentation/    # APIs e interfaces de usuário
```

## Camadas

### Domain Layer (🎯)
- Regras de negócio fundamentais
- Entidades e objetos de valor
- Interfaces de repositório
- Sem dependências externas

### Application Layer (🏗️)
- Casos de uso da aplicação
- Serviços de domínio
- DTOs e interfaces
- Depende apenas do domínio

### Infrastructure Layer (🔧)
- Implementações de repositórios
- Adaptadores externos
- Configurações técnicas
- Implementa interfaces da aplicação

### Presentation Layer (🖥️)
- APIs REST
- Middlewares
- Validação de entrada
- Formatação de resposta

## Princípios

1. Dependências fluem de fora para dentro
2. Camadas internas não conhecem externas
3. Domínio é independente de frameworks
4. Interfaces definem contratos entre camadas

## Fluxo de Dados

```plaintext
Request → Presentation → Application → Domain
Response ← Presentation ← Application ← Domain
```

## Decisões Técnicas

- Python 3.11+ com type hints
- FastAPI para APIs REST
- Pydantic para validação
- SQLAlchemy para ORM
- OpenTelemetry para observabilidade

## Padrões de Código

- Seguir PEP 8 e PEP 257
- Type hints obrigatórios
- Docstrings em todas as funções públicas
- Testes unitários para cada módulo
