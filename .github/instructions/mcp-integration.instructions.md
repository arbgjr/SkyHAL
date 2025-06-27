---
applyTo: "**"
---
# Integração com MCP Tools

## Ferramentas Disponíveis

### 1. Memory (Knowledge Graph)

- **Propósito**: Manter contexto persistente do projeto
- **Uso**: Armazenar decisões, features, débitos técnicos
- **Comandos principais**:
  - `mcp_memory_create_entities`: Criar novas entidades
  - `mcp_memory_search_nodes`: Buscar informações
  - `mcp_memory_create_relations`: Conectar entidades

### 2. Sequential Thinking

- **Propósito**: Decompor problemas complexos
- **Uso**: Planejamento de features, resolução de bugs complexos
- **Comando**: `mcp_sequentialthinking_sequentialthinking`

### 3. Time

- **Propósito**: Trabalhar com datas e horários
- **Uso**: Logging, agendamento, cálculos temporais
- **Timezone**: America/Sao_Paulo

## Quando Usar MCP Tools

### Durante Planejamento

1. Use Sequential Thinking para decompor a tarefa
2. Busque contexto relevante no Memory
3. Documente decisões como novas entidades

### Durante Desenvolvimento

1. Consulte Memory para padrões estabelecidos
2. Adicione observações sobre progresso
3. Crie relações entre componentes

### Durante Review

1. Verifique consistência com contexto armazenado
2. Identifique novos débitos técnicos
3. Atualize status de features

## Comandos Úteis

```bash
# Buscar todas as decisões técnicas
query: "entityType:Decision"

# Buscar débitos de alta prioridade
query: "entityType:Debt AND priority:high"

# Buscar features relacionadas a auth
query: "entityType:Feature AND authentication"
```

## Integração com Memory Bank

O MCP Memory complementa o Memory Bank em arquivos:

- **Memory Bank**: Documentação legível e versionada
- **MCP Memory**: Grafo de conhecimento consultável

Mantenha ambos sincronizados para máxima eficácia.
