# 🏗️ Application Layer

## Propósito

Esta camada contém os casos de uso da aplicação e interfaces de serviço.

## Princípios

- Orquestra entidades do domínio
- Implementa casos de uso
- Define interfaces de infraestrutura
- Gerencia transações e fluxo de dados

## Estrutura

```plaintext
application/
├── use_cases/     # Implementação dos casos de uso
├── interfaces/    # Interfaces para infraestrutura
├── services/      # Serviços de aplicação
└── dtos/         # Objetos de transferência de dados
```

## Regras

1. Depende apenas da camada de domínio
2. Não conhece detalhes de infraestrutura
3. Define contratos para camadas externas
4. Coordena fluxo de dados entre camadas
