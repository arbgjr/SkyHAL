# 🎯 Domain Layer

## Propósito
Esta camada contém as regras de negócio fundamentais e entidades do sistema.

## Princípios
- Não possui dependências externas
- Contém regras de negócio puras
- Define interfaces para serviços
- Independente de frameworks

## Estrutura
```
domain/
├── entities/       # Entidades de negócio
├── value_objects/  # Objetos de valor
├── interfaces/     # Interfaces de repositório/serviço
└── exceptions/     # Exceções de domínio
```

## Regras
1. Código aqui deve ser puro Python
2. Sem dependências de frameworks
3. Sem imports de outras camadas
4. Define contratos via interfaces
