---
mode: "agent"
description: "Implementar planejamento de projeto seguindo [memory-bank.instructions.md](../instructions/memory-bank.instructions.md)."
---

# Planejamento de Projeto

Execute planejamento usando Plan Mode seguindo [memory-bank.instructions.md](../instructions/memory-bank.instructions.md).

## Plan Mode (// mode: plan)

### 1. Análise do Contexto

Consultar Memory Bank para entender:

- **Objetivos**: Conforme `projectbrief.md` e `productContext.md`
- **Arquitetura**: Padrões estabelecidos em `systemPatterns.md`
- **Estado atual**: Progresso em `progress.md`
- **Foco ativo**: Trabalho atual em `activeContext.md`

### 2. Estratégia de Alto Nível

- Definir abordagem geral
- Identificar componentes principais
- Estabelecer ordem de implementação
- Considerar dependências e riscos

### 3. Divisão de Tarefas

- Quebrar trabalho em tarefas menores
- Priorizar baseado em valor e dependências
- Estimar esforço necessário
- Identificar recursos requeridos

### 4. Documentação da Estratégia

```markdown
# Plano: [Nome da Iniciativa]

## Contexto

- **Baseado em**: [Arquivos do Memory Bank consultados]
- **Objetivo**: [O que queremos alcançar]
- **Escopo**: [O que está incluído/excluído]

## Estratégia

1. **Fase 1**: [Primeira fase]
2. **Fase 2**: [Segunda fase]
3. **Fase 3**: [Terceira fase]

## Tarefas Prioritárias

- [ ] [Tarefa 1] - [Estimativa]
- [ ] [Tarefa 2] - [Estimativa]
- [ ] [Tarefa 3] - [Estimativa]

## Dependências

- [Dependência externa 1]
- [Dependência interna 2]

## Riscos

- [Risco 1] - [Mitigação]
- [Risco 2] - [Mitigação]
```

## Transição para Act Mode

Após planejamento, use Act Mode (// mode: act) para implementação.
