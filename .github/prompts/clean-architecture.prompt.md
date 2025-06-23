---
mode: "agent"
description: "Implementar código seguindo Clean Architecture com princípios SOLID, separando responsabilidades entre camadas e garantindo testabilidade."
---

# Implementação Clean Architecture

Refatore ou implemente código seguindo Clean Architecture com princípios SOLID.

## Camadas e Responsabilidades

- **Domain**: Entidades, Value Objects, Interfaces de Repository
- **Application**: Use Cases, DTOs, Interfaces de Services
- **Infrastructure**: Implementações de Repository, Services externos
- **Presentation**: Controllers, ViewModels, Mappers

## Regras de Dependência

- Dependências apontam sempre para dentro
- Domain não conhece outras camadas
- Application conhece apenas Domain
- Infrastructure implementa interfaces de Application/Domain

## Verificações Obrigatórias

- [ ] Princípios SOLID aplicados
- [ ] Inversão de dependência respeitada
- [ ] Separação clara de responsabilidades
- [ ] Testabilidade garantida
