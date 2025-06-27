---
applyTo: "**"
---

# 🌟 Diretrizes Globais do Projeto

## 🤖 Instruções Específicas para GitHub Copilot

### Configurações de Resposta

- **Idioma obrigatório**: Português Brasileiro (PT-BR)
- **Tom**: Direto, factual, sem formalidade excessiva
- **Formato**: Sempre especificar nome/localização dos arquivos
- **Explicações**: Justificar decisões técnicas com fatos

### Padrões de Código Obrigatórios

- **Arquitetura**: Clean Architecture com DDD quando aplicável
- **Princípios**: SOLID, KISS, DRY, YAGNI rigorosamente aplicados
- **Nomenclatura**: Descritiva, em português/inglês consistente
- **Modularização**: Componentes pequenos, focados e reutilizáveis

### Qualidade e Segurança

- **Tratamento de Erros**: Sempre incluir try/catch adequado
- **Validação**: Rigorosa em todas as entradas
- **Logging**: Estruturado com níveis apropriados
- **Testes**: Gerar automaticamente para novo código

### Rastreamento Obrigatório

- **Débitos Técnicos**: Documentar em `tech-debt.instructions.md`
- **Bugs**: Registrar em `bugs-founded.instructions.md`
- **Documentação**: Atualizar quando código impactar interfaces

## 🧠 Memory Bank System Integration

### Consulta Obrigatória

Antes de qualquer tarefa significativa:

- [ ] Consultar `activeContext.md` para entender foco atual
- [ ] Verificar `progress.md` para status das funcionalidades
- [ ] Revisar `systemPatterns.md` para padrões estabelecidos
- [ ] Considerar contexto em `techContext.md`

### Fluxo de Trabalho

1. **Plan Mode**: Estratégias de alto nível consultando Memory Bank
2. **Act Mode**: Implementação concreta mantendo consistência
3. **Update Mode**: Documentar mudanças significativas

### Quando Atualizar Memory Bank

- Comando explícito "update memory bank"
- Implementação de nova arquitetura
- Descoberta de novos padrões
- Finalização de funcionalidades importantes
- Resolução de problemas complexos

### Responsabilidades por Arquivo

- **projectbrief.md**: Escopo fundamental (raramente muda)
- **productContext.md**: Propósito e problemas (muda ocasionalmente)
- **systemPatterns.md**: Arquitetura e padrões (muda com evolução)
- **techContext.md**: Tecnologias e configurações (muda com atualizações)
- **activeContext.md**: Foco atual (muda frequentemente)
- **progress.md**: Status e funcionalidades (muda constantemente)

## ✅ Checklist com Memory Bank

### Antes de Iniciar Desenvolvimento

- [ ] Memory Bank consultado para contexto
- [ ] Estratégia alinhada com padrões estabelecidos
- [ ] Próximos passos claros baseados no `activeContext.md`

### Durante Desenvolvimento

- [ ] Implementação consistente com `systemPatterns.md`
- [ ] Tecnologias alinhadas com `techContext.md`
- [ ] Progresso sendo rastreado mentalmente

### Após Desenvolvimento

- [ ] Atualizar Memory Bank se mudanças significativas
- [ ] Documentar novos padrões descobertos
- [ ] Atualizar `progress.md` se funcionalidade completa

## ✅ Checklist Operacional de Conformidade

### Antes de Finalizar Qualquer Código:

- [ ] Aplica princípios SOLID
- [ ] Inclui tratamento de erros robusto
- [ ] Tem validação de entrada adequada
- [ ] É testável e inclui testes
- [ ] Segue padrões de segurança estabelecidos
- [ ] Está bem documentado
- [ ] Especifica nome do arquivo/localização
- [ ] Usa nomenclatura descritiva e consistente
- [ ] É modular e reutilizável
- [ ] Considera performance e escalabilidade

### Rastreamento de Mudanças:

- [ ] Débitos técnicos identificados foram registrados
- [ ] Bugs encontrados foram documentados
- [ ] Documentação foi atualizada se necessário
- [ ] Impacto em outros componentes foi avaliado

### Definições de Ready/Done

Antes de iniciar ou finalizar qualquer tarefa, consulte as definições em [`done-ready.instructions.md`](./done-ready.instructions.md):

- [ ] Tarefa atende critérios de "Ready" antes de iniciar
- [ ] Todas as condições de "Done" são verificadas antes de finalizar
- [ ] Documentação atualizada conforme [`documentation.instructions.md`](./documentation.instructions.md)
- [ ] Instruções específicas do Copilot em [`copilot-specific.instructions.md`](./copilot-specific.instructions.md) foram seguidas

## 🎯 Diretrizes por Tipo de Tarefa

### Geração de Código

- Seguir padrões definidos em arquivos de instruções específicos
- Implementar logging e monitoramento adequados
- Considerar testabilidade desde o design
- Documentar decisões arquiteturais importantes

### Revisão de Código

- Verificar aderência aos padrões SOLID
- Avaliar segurança, performance e manutenibilidade
- Identificar potenciais débitos técnicos
- Sugerir melhorias específicas com exemplos

### Refatoração

- Manter funcionalidade existente
- Melhorar legibilidade e estrutura
- Reduzir complexidade ciclomática
- Preservar compatibilidade de interface

## 📖 Referências Cruzadas

- [Segurança](api-security.instructions.md)
- [Testes](test.instructions.md)
- [Revisão](code-review.instructions.md)
- [Commits](commit-message.instructions.md)
- [Memory Bank](memory-bank.instructions.md)
- [Padrões de documentação](documentation.instructions.md)
- [Definições de pronto e concluído](done-ready.instructions.md)
