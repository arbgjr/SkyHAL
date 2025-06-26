---
mode: 'agent'
tools: ['memory-system', 'reasoning-tools']
description: 'Análise de experimento com memória'
---

# Análise de Experimento

Com base no experimento que acabou de executar:

1. **Recuperar contexto**: `#memory_search "experimentos {tipo}"`
2. **Analisar resultados**: `#thinking_start comparação com hipótese`
3. **Registrar descobertas**:
   - `#memory_create_entities` nome="Experimento-{data}"
   - `#memory_create_observations` resultado e insights
4. **Conectar conhecimento**: `#memory_create_relations` com experimentos relacionados
5. **Planejar próximos passos**: `#thinking_analyze próximas direções`

Formate como: **Hipótese → Método → Resultado → Insight → Próximo Passo**
