---
mode: "agent"
---
# Gerenciamento de Entidades do Knowledge Graph

Crie, atualize e delete entidades no knowledge graph do projeto.

## Tipos de Entidade Padrão

### 1. Context

```json
{
  "name": "SprintContext_2025_Q1",
  "entityType": "Context",
  "observations": [
    "Foco em melhorias de performance",
    "Migração para nova arquitetura",
    "Prazo: 3 meses"
  ]
}
```

### 2. Feature

```json
{
  "name": "AuthenticationModule",
  "entityType": "Feature",
  "observations": [
    "Implementa JWT authentication",
    "Suporta MFA",
    "Status: Em desenvolvimento"
  ]
}
```

### 3. Decision

```json
{
  "name": "UseCleanArchitecture",
  "entityType": "Decision",
  "observations": [
    "Adotada para melhor separação de responsabilidades",
    "Facilita testes e manutenção",
    "Data: 2025-01-15"
  ]
}
```

### 4. TechDebt

```json
{
  "name": "RefactorLegacyAPI",
  "entityType": "Debt",
  "observations": [
    "API antiga não segue padrões REST",
    "Impacto: Médio",
    "Estimativa: 2 sprints"
  ]
}
```

## Operações CRUD

### Create

```
mcp_memory_create_entities com array de entidades
```

### Read

```
mcp_memory_search_nodes com query específica
```

### Update

```
1. Delete observações antigas: mcp_memory_delete_observations
2. Adicione novas: mcp_memory_add_observations
```

### Delete

```
mcp_memory_delete_entities com array de nomes
```

## Boas Práticas

1. **Nomenclatura**: Use PascalCase para nomes de entidades
2. **Observações**: Seja específico e inclua datas quando relevante
3. **Relações**: Sempre crie relações relevantes após criar entidades
4. **Limpeza**: Remova entidades obsoletas regularmente
