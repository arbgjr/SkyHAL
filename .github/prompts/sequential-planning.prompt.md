---
mode: "agent"
description: "Planejamento sequencial para problemas complexos"
---

# Planejamento Sequencial com MCP

Use a ferramenta `mcp_sequentialthinking` para decompor problemas complexos.

## Contexto Necessário

Antes de começar, garanta que você tem:

- [Memory Bank Context](../../memory-bank/activeContext.md)
- [System Patterns](../../memory-bank/systemPatterns.md)
- Requisitos específicos da tarefa

## Processo de Pensamento Sequencial

### 1. Decomposição do Problema

Use `mcp_sequentialthinking_sequentialthinking` com o seguinte formato:

```
Problema: [DESCRIÇÃO_DO_PROBLEMA]

Passo 1: Análise do contexto atual
- Consultar Memory Bank
- Identificar dependências
- Mapear recursos necessários

Passo 2: Estratégia de solução
- Definir abordagem técnica
- Identificar riscos
- Estabelecer critérios de sucesso

Passo 3: Plano de implementação
- Quebrar em tarefas menores
- Definir ordem de execução
- Estimar esforço

Passo 4: Validação
- Critérios de teste
- Métricas de sucesso
- Pontos de verificação
```

## Integração com Memory Bank

Após o planejamento:

1. Armazene decisões importantes usando `mcp_memory_create_entities`
2. Crie relações entre o plano e features existentes
3. Documente riscos identificados como potenciais débitos técnicos

## Output Esperado

Um plano detalhado e estruturado que pode ser seguido passo a passo, com checkpoints claros de validação.
