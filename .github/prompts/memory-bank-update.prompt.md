---
mode: "agent"
description: "Implementar atualização do Memory Bank com foco em melhorias contínuas."
---

# Atualização do Memory Bank

Execute uma atualização completa do Memory Bank seguindo [memory-bank.instructions.md](../instructions/memory-bank.instructions.md).

## Processo de Atualização

### 1. Análise do Estado Atual

- Revisar `activeContext.md` para foco atual
- Verificar `progress.md` para status das funcionalidades
- Analisar mudanças recentes no código

### 2. Identificação de Mudanças

- Novos padrões arquiteturais descobertos
- Decisões técnicas importantes tomadas
- Funcionalidades implementadas ou modificadas
- Problemas resolvidos ou identificados

### 3. Atualização Hierárquica

Atualizar arquivos na ordem de prioridade:

#### Alta Prioridade (Sempre atualizar)

- **activeContext.md**: Foco atual e próximos passos
- **progress.md**: Status e funcionalidades completas

#### Média Prioridade (Se houver mudanças significativas)

- **systemPatterns.md**: Novos padrões ou modificações arquiteturais
- **techContext.md**: Mudanças em tecnologias ou configurações

#### Baixa Prioridade (Apenas em mudanças fundamentais)

- **productContext.md**: Mudanças no propósito ou problemas a resolver
- **projectbrief.md**: Apenas para mudanças de escopo fundamental

### 4. Formato de Atualização

```markdown
## [Data] - Atualização do Memory Bank

### Contexto da Atualização

- **Motivação**: Por que foi necessária esta atualização
- **Período**: Timeframe das mudanças sendo documentadas

### Principais Mudanças

1. **Arquitetura**: [Descrever mudanças arquiteturais]
2. **Funcionalidades**: [Funcionalidades adicionadas/modificadas]
3. **Padrões**: [Novos padrões estabelecidos]
4. **Problemas**: [Problemas resolvidos ou identificados]

### Próximos Passos

- [Lista de próximas ações prioritárias]
- [Dependências ou bloqueadores]
- [Decisões pendentes]
```

## Comando para Atualização

Use o comando: **"update memory bank"** para solicitar atualização completa.
