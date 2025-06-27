---
applyTo: "**"
---

# Memory Bank System

O Memory Bank mantém contexto entre sessões em arquivos Markdown organizados hierarquicamente.

## Hierarquia e Fluxo

```
projectbrief.md → base fundamental
    ↓
productContext.md  systemPatterns.md  techContext.md
    ↓                   ↓                 ↓
           activeContext.md → trabalho atual
                  ↓
             progress.md → status
```

- Informações fluem de cima para baixo
- Arquivos superiores informam os inferiores
- Conflitos resolvidos priorizando níveis superiores

## Arquivos Principais

1. **projectbrief.md**

   - Requisitos e objetivos fundamentais
   - Fonte de verdade para o escopo

2. **productContext.md**

   - Propósito do projeto
   - Problemas a resolver
   - Experiência do usuário desejada

3. **systemPatterns.md**

   - Arquitetura
   - Decisões técnicas
   - Padrões de design
   - Relacionamentos entre componentes

4. **techContext.md**

   - Tecnologias usadas
   - Configurações
   - Dependências

5. **activeContext.md**

   - Foco atual
   - Mudanças recentes
   - Próximos passos
   - Decisões ativas

6. **progress.md**
   - Funcionalidades completas
   - Pendências
   - Status atual
   - Problemas conhecidos

## Fluxo de Trabalho

1. **Iniciar**: Consultar Memory Bank para contexto
2. **Planejar**: Plan Mode (// mode: plan)
   - Estratégias de alto nível
   - Divisão de tarefas
   - Priorização
3. **Executar**: Act Mode (// mode: act)
   - Implementação concreta
   - Geração de código
   - Testes
4. **Atualizar**: Documentar mudanças no Memory Bank

## Atualizações

Atualizar quando:

- Descobrir novos padrões
- Implementar mudanças significativas
- Receber comando **update memory bank**
- Precisar esclarecer contexto

**Importante**: Em caso de **update memory bank**, revisar TODOS os arquivos, com foco em activeContext.md e progress.md.

## 🔗 Integração com Ferramentas de Desenvolvimento

### GitHub Copilot

O Memory Bank está integrado ao GitHub Copilot através de:

- **Instruções automáticas**: Configuradas no `settings.json`
- **Prompt files específicos**: Para atualização e consulta
- **Comandos de controle**: "update memory bank" para atualizações

### VS Code Tasks

- **Consultar Memory Bank**: Visualizar status atual
- **Verificar Integração**: Validar referências nos arquivos
- **Update Memory Bank**: Lembrete para usar comando do Copilot

### Pull Requests

Checklist automático verifica:

- Consistência com padrões do Memory Bank
- Necessidade de atualização após mudanças
- Impacto no contexto do projeto

### Code Review

Revisores devem verificar:

- Alinhamento com `systemPatterns.md`
- Consistência com `activeContext.md`
- Necessidade de atualização do Memory Bank

## 🎯 Comandos Específicos

### Para Desenvolvedores

```bash
# Consultar status do Memory Bank
code-copilot: "analyze current context using memory bank"

# Solicitar atualização
code-copilot: "update memory bank"

# Planejar com contexto
code-copilot: "plan next steps using memory bank context"

# Verificar consistência
code-copilot: "verify code consistency with memory bank patterns"
```

### Para GitHub Copilot

O sistema responde automaticamente aos comandos:

- **"update memory bank"**: Executa atualização completa
- **"// mode: plan"**: Entra em modo de planejamento
- **"// mode: act"**: Entra em modo de implementação
- **"analyze context"**: Analisa contexto atual

## 📊 Métricas de Uso

### Indicadores de Saúde

- **Frequência de atualização**: Memory Bank atualizado semanalmente
- **Consistência**: Código alinhado com padrões documentados
- **Contexto perdido**: Mínimo de informações não capturadas

### Sinais de Problema

- Memory Bank não atualizado por > 2 semanas
- Código divergindo de padrões estabelecidos
- Desenvolvedores não consultando contexto
- Decisões importantes não documentadas
