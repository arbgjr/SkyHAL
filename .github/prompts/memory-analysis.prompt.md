# Análise de Memória com MCP

Analise o contexto atual do projeto usando a ferramenta MCP memory.

## Instruções

Use a ferramenta `mcp_memory` para:

1. Listar todas as entidades armazenadas no knowledge graph
2. Identificar relações entre componentes do projeto
3. Buscar padrões e insights no contexto armazenado

## Processo

1. Execute `mcp_memory_read_graph` para obter o estado atual
2. Use `mcp_memory_search_nodes` para buscar informações específicas sobre:
   - Arquitetura do projeto
   - Decisões técnicas
   - Padrões implementados
   - Débitos técnicos

## Output Esperado

Forneça um relatório estruturado com:

- **Contexto Atual**: Estado do Memory Bank
- **Insights**: Padrões identificados
- **Recomendações**: Próximos passos baseados na análise
- **Gaps**: Informações faltantes que precisam ser documentadas

## Exemplo de Uso

```
@workspace analise o contexto do projeto usando #file:.github/prompts/memory-analysis.prompt.md
```
