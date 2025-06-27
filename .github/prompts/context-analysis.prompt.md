---
mode: "agent"
description: "Implementar análise de contexto do projeto usando o Memory Bank System."
---

# Análise de Contexto do Projeto

Analise o contexto atual do projeto usando o Memory Bank System definido em [memory-bank.instructions.md](../instructions/memory-bank.instructions.md).

## Análise Requerida

### 1. Contexto Atual

- **Foco ativo**: O que está sendo trabalhado agora
- **Progresso**: Status das funcionalidades principais
- **Padrões**: Arquitetura e padrões estabelecidos
- **Tecnologias**: Stack técnico e configurações

### 2. Análise de Consistência

- Código atual está alinhado com padrões do Memory Bank?
- Há divergências entre implementação e documentação?
- Novos padrões emergiram que precisam ser documentados?

### 3. Identificação de Gaps

- Funcionalidades documentadas mas não implementadas
- Implementações não documentadas no Memory Bank
- Decisões técnicas não capturadas
- Contexto perdido que precisa ser recuperado

### 4. Recomendações

- Atualizações necessárias no Memory Bank
- Alinhamentos entre código e documentação
- Próximos passos recomendados

## Saída Esperada

```markdown
# Análise de Contexto - [Data]

## Status Atual

- **Foco**: [Descrição do foco atual]
- **Progresso**: [Resumo do progresso]
- **Último Update**: [Data da última atualização do Memory Bank]

## Consistência

- ✅ Alinhamentos identificados
- ⚠️ Divergências encontradas
- ❌ Problemas críticos

## Recomendações

1. [Ação prioritária 1]
2. [Ação prioritária 2]
3. [Atualização do Memory Bank necessária?]
```
