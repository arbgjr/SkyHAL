---
mode: "agent"
---
# Atualização do Memory Bank via MCP

Atualize o Memory Bank do projeto usando ferramentas MCP.

## Processo de Atualização

1. **Análise do Estado Atual**

   - Use `mcp_memory_read_graph` para entender o contexto
   - Identifique o que precisa ser atualizado

2. **Criar/Atualizar Entidades**

   ```
   Entidades principais:
   - projectContext (tipo: Context)
   - currentFeature (tipo: Feature)
   - techDecisions (tipo: Decision)
   - techDebts (tipo: Debt)
   ```

3. **Estabelecer Relações**
   - Feature IMPLEMENTS Requirement
   - Decision AFFECTS Architecture
   - Debt BLOCKS Feature

## Comandos MCP

Use os seguintes comandos em sequência:

1. `mcp_memory_create_entities` - Para novas entidades
2. `mcp_memory_add_observations` - Para adicionar contexto
3. `mcp_memory_create_relations` - Para conectar entidades

## Template de Entidade

```json
{
  "name": "[NOME_DA_ENTIDADE]",
  "entityType": "[Context|Feature|Decision|Debt]",
  "observations": ["Descrição detalhada", "Impacto no projeto", "Status atual"]
}
```

## Validação

Após atualização, execute `mcp_memory_search_nodes` para verificar se as mudanças foram aplicadas corretamente.
