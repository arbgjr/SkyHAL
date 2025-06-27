---
mode: "agent"
---
# Busca Inteligente no Knowledge Graph

Encontre informações específicas no contexto do projeto usando MCP.

## Parâmetros de Busca

Configure sua busca com:

- **query**: Termos de busca (ex: "authentication", "database schema")
- **limit**: Número máximo de resultados (padrão: 10)
- **filter**: Tipos de entidade específicos

## Estratégias de Busca

### 1. Busca por Contexto

```
mcp_memory_search_nodes com query: "Context AND [TERMO]"
```

### 2. Busca por Relacionamentos

```
Encontre todas as entidades relacionadas a uma específica:
1. Busque a entidade principal
2. Use o ID para encontrar relações
3. Explore a rede de conexões
```

### 3. Busca por Padrões

```
Identifique padrões recorrentes:
- Decisões técnicas similares
- Problemas relacionados
- Componentes interdependentes
```

## Casos de Uso

1. **Impacto de Mudanças**: "Quais componentes são afetados por [MUDANÇA]?"
2. **Histórico de Decisões**: "Por que escolhemos [TECNOLOGIA]?"
3. **Débitos Relacionados**: "Quais débitos técnicos afetam [FEATURE]?"

## Refinamento de Resultados

Se muitos resultados forem retornados:

1. Adicione mais termos específicos
2. Use operadores AND/OR
3. Filtre por tipo de entidade
4. Limite por data/contexto temporal
