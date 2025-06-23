# 📚 Índice das Instruções do Projeto

## 🎯 Arquivo Principal
- **[copilot-instructions.md](../../copilot-instructions.md)** - Instruções principais do GitHub Copilot

## 🔧 Instruções Core
- **[global.instructions.md](global.instructions.md)** - Diretrizes globais obrigatórias
- **[copilot-specific.instructions.md](copilot-specific.instructions.md)** - Instruções específicas para GitHub Copilot

## 📋 Processo e Qualidade
- **[done-ready.instructions.md](done-ready.instructions.md)** - Definições de Ready e Done
- **[code-review.instructions.md](code-review.instructions.md)** - Critérios de revisão de código
- **[documentation.instructions.md](documentation.instructions.md)** - Padrões de documentação

## 🛡️ Segurança e Testes
- **[api-security.instructions.md](api-security.instructions.md)** - Práticas de segurança
- **[test.instructions.md](test.instructions.md)** - Estratégias de teste
- **[test-api.instructions.md](test-api.instructions.md)** - Testes específicos de API

## ✍️ Padronização
- **[commit-message.instructions.md](commit-message.instructions.md)** - Padrões de commit
- **[pull-request.instructions.md](pull-request.instructions.md)** - Templates de PR

## 🧠 Sistema e Contexto
- **[memory-bank.instructions.md](memory-bank.instructions.md)** - Sistema de contexto
- **[troubleshooting.instructions.md](troubleshooting.instructions.md)** - Guia de resolução de problemas

## 📊 Rastreamento
- **[tech-debt.instructions.md](tech-debt.instructions.md)** - Registro de débitos técnicos
- **[bugs-founded.instructions.md](bugs-founded.instructions.md)** - Registro de bugs encontrados

## 🎯 Como Usar Este Sistema

### Para Desenvolvedores
1. Comece com `global.instructions.md` para entender princípios fundamentais
2. Consulte `copilot-specific.instructions.md` para otimizar uso do Copilot
3. Use `done-ready.instructions.md` para gerenciar tarefas
4. Aplique `documentation.instructions.md` para documentar adequadamente

### Para GitHub Copilot
- Arquivo principal: `copilot-instructions.md` (raiz do projeto)
- Configurações específicas: `copilot-specific.instructions.md`
- Todos os arquivos são referenciados automaticamente via `settings.json`

### Para Code Review
- Critérios em `code-review.instructions.md`
- Checklist de Done em `done-ready.instructions.md`
- Padrões de segurança em `api-security.instructions.md`

## 🔄 Fluxo de Integração

```
copilot-instructions.md (raiz)
         ↓
   global.instructions.md
         ↓
   ┌─────────────────────┐
   │ Arquivos Específicos │
   └─────────────────────┘
         ↓
   Configuração settings.json
         ↓
   Prompt Files (.github/prompts/)
```

## **Trabalhando com o MCP de Memory e Sequential Thinking**

### **Workflow de Uso**

#### **Início do Dia**
```bash
1. Execute: @workspace #file:.github/prompts/memory-analysis.prompt.md
2. Revise o contexto atual e identifique tarefas
3. Use Sequential Thinking para planejar o dia
```

#### **Durante Desenvolvimento**
```bash
1. Busque padrões: @workspace encontre padrões de [COMPONENTE] #file:.github/prompts/knowledge-search.prompt.md
2. Implemente seguindo padrões encontrados
3. Documente decisões novas
```

#### **Fim do Dia**
```bash
1. Atualize progresso: @workspace #file:.github/prompts/memory-update.prompt.md
2. Documente débitos técnicos encontrados
3. Crie relações entre componentes trabalhados
```

### **Exemplo de Uso Completo**

```markdown
# Exemplo: Implementando Sistema de Autenticação

## 1. Análise Inicial
@workspace analise o contexto de autenticação #file:.github/prompts/memory-analysis.prompt.md

## 2. Planejamento
@workspace planeje a implementação de JWT authentication #file:.github/prompts/sequential-planning.prompt.md

## 3. Busca de Padrões
@workspace encontre padrões de segurança e auth #file:.github/prompts/knowledge-search.prompt.md

## 4. Implementação
[Código seguindo padrões encontrados]

## 5. Documentação
@workspace crie entidades para o novo módulo de auth #file:.github/prompts/entity-management.prompt.md

## 6. Atualização Final
@workspace atualize o memory bank com o progresso #file:.github/prompts/memory-update.prompt.md
```

Todos os arquivos trabalham em conjunto para fornecer uma experiência de desenvolvimento consistente e de alta qualidade.