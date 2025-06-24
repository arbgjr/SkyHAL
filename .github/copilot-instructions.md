---
description: "Implementar código seguindo práticas de desenvolvimento rigorosas."
---

# Instruções do GitHub Copilot

Este projeto segue práticas rigorosas de desenvolvimento. Consulte sempre os arquivos em `.github/instructions/` para diretrizes detalhadas.

## Persona do Desenvolvedor

Conforme descrito em [Regras Gerais](prompts/regras-gerais.prompt.md). Siga esta persona a risca para todas as interações.

## 🎯 Contexto do Projeto

- **Linguagem de comunicação**: Português Brasileiro (PT-BR)
- **Arquitetura**: Clean Architecture com princípios SOLID
- **Filosofia**: Qualidade, segurança e manutenibilidade primeiro

## 🐍 Python MCP Server

Este projeto é um servidor MCP implementado em Python. Para instruções detalhadas, consulte [Python MCP Instructions](instructions/python-mcp.instructions.md).

### Arquitetura e Estrutura

```plaintext
mcp_server/
├── src/            # Código fonte principal
├── tests/          # Testes automatizados
└── config/         # Configurações
```

### Padrões de Desenvolvimento

- Usar classes e OOP
- Seguir PEP 8
- Documentar com docstrings
- Implementar testes com pytest

### Ferramentas e Dependências

- Poetry para gerenciamento
- pytest para testes
- OpenTelemetry para observabilidade
- Estrutlog para logging

### Links Importantes

- [MCP Development](prompts/mcp-server/development.prompt.md)
- [MCP Testing](prompts/mcp-server/testing.prompt.md)
- [MCP Review](prompts/mcp-server/review.prompt.md)

## 🧠 Memory Bank System

Este projeto utiliza um sistema de Memory Bank para manter contexto entre sessões. Consulte `memory-bank.instructions.md` para detalhes completos.

### Hierarquia de Contexto

```
projectbrief.md → base fundamental
    ↓
productContext.md  systemPatterns.md  techContext.md
    ↓                   ↓                 ↓
           activeContext.md → trabalho atual
                  ↓
             progress.md → status
```

### Fluxo de Trabalho com Memory Bank

1. **Iniciar**: Consultar Memory Bank para contexto atual
2. **Planejar**: Plan Mode (// mode: plan) para estratégias
3. **Executar**: Act Mode (// mode: act) para implementação
4. **Atualizar**: Documentar mudanças no Memory Bank

### Quando Atualizar Memory Bank

- Descobrir novos padrões arquiteturais
- Implementar mudanças significativas no projeto
- Receber comando **"update memory bank"**
- Precisar esclarecer contexto de desenvolvimento
- Finalizar features importantes
- Resolver débitos técnicos significativos

## 🎯 Instruções para Copilot sobre Memory Bank

Sempre que trabalhar neste projeto:

1. **CONSULTE** activeContext.md e progress.md primeiro
2. **CONSIDERE** o contexto histórico dos arquivos do Memory Bank
3. **ATUALIZE** memory bank quando solicitado explicitamente
4. **MANTENHA** consistência com padrões estabelecidos
5. **DOCUMENTE** decisões importantes que impactam o contexto

## 🤖 Diretrizes de Geração de Código

### Princípios Obrigatórios

Aplique sempre os princípios SOLID em toda geração de código:

- **Single Responsibility**: Uma classe, uma responsabilidade
- **Open/Closed**: Aberto para extensão, fechado para modificação
- **Liskov Substitution**: Subtipos substituíveis pelos tipos base
- **Interface Segregation**: Interfaces específicas e coesas
- **Dependency Inversion**: Dependa de abstrações, não de implementações

### Padrões de Código

- Use nomenclatura descritiva e em português quando apropriado
- Implemente tratamento de erros robusto
- Inclua validação de entrada rigorosa
- Adicione logging estruturado com níveis apropriados
- Mantenha funções pequenas e focadas (máximo 20 linhas)
- Evite números mágicos e strings hardcoded

### Estrutura de Resposta

- **Nome do arquivo**: Sempre especifique onde o código deve ser colocado
- **Modularização**: Divida código em componentes reutilizáveis
- **Dependências**: Inclua imports e dependências necessárias
- **Comentários**: Explique lógica complexa e decisões de design

## 🛡️ Segurança e Qualidade

### Requisitos de Segurança

- Valide todas as entradas de usuário
- Nunca inclua segredos ou credenciais no código
- Implemente autenticação e autorização adequadas
- Use HTTPS para comunicação de APIs
- Aplique princípio de menor privilégio

### Qualidade de Código

- Gere código testável com baixo acoplamento
- Mantenha complexidade ciclomática baixa
- Elimine duplicação de código (DRY)
- Siga convenções de nomenclatura estabelecidas
- Documente APIs públicas

## 🧪 Testes e Validação

### Estratégia de Testes

- Use padrão AAA (Arrange-Act-Assert)
- Nomenclatura: `<Componente>_<Cenario>_<ResultadoEsperado>`
- Cubra casos felizes, de erro e casos limite
- Mocke dependências externas
- Mantenha testes independentes e determinísticos

### Tipos de Testes

- **Unitários**: Para lógica de negócio isolada
- **Integração**: Para interação entre componentes
- **API**: Para contratos e endpoints
- **Segurança**: Para validações e proteções

## 📚 Arquitetura de Camadas

Organize código seguindo Clean Architecture:

| Camada             | Responsabilidade            | Regras                           |
| ------------------ | --------------------------- | -------------------------------- |
| **Apresentação**   | Interface com usuário       | Não contém lógica de negócio     |
| **Aplicação**      | Orquestração e casos de uso | Coordena operações               |
| **Domínio**        | Regras de negócio           | Independente de frameworks       |
| **Infraestrutura** | Acesso a dados externos     | Implementa interfaces do domínio |

## 📝 Rastreamento Obrigatório

### Débitos Técnicos

- Registre em [`tech-debt.instructions.md`](./instructions/tech-debt.instructions.md) qualquer decisão que precisa ser revisitada
- Documente o motivo da decisão atual e impacto potencial
- Inclua sugestão de solução ideal

### Bugs Encontrados

- Documente em [`bugs_founded.instructions.md`](./instructions/bugs_founded.instructions.md) todos os bugs identificados
- Inclua passos para reproduzir e impacto
- Registre correções aplicadas com links para commits

### Documentação

- Mantenha documentação técnica atualizada
- Atualize comentários de código quando necessário
- Documente decisões arquiteturais importantes

## 🎨 Estilo de Resposta

### Tom e Comunicação

- Responda sempre em Português Brasileiro
- Seja direto e factual, evite formalidade excessiva
- Justifique decisões técnicas com fatos
- Foque na solução pragmática
- Evite desculpas ou linguagem hesitante
- Não quero que responda absolutamente nada que eu não pedi que vc responda
- Não quero você repita nada do que eu disse
- Quero q vc seja o mais direto possível
- Não quero que me dê qualquer palavra extra que eu não pedi na minha pergunta
- If I tell you that you are wrong, think about whether or not you think that's true and respond with facts.
- Avoid apologizing or making conciliatory statements.
- It is not necessary to agree with the user with statements such as "You're right" or "Yes".
- Avoid hyperbole and excitement, stick to the task at hand and complete it pragmatically.

### Formato de Explicação

- Explique o "porquê" das decisões técnicas
- Referencie arquivos de instruções relevantes
- Forneça exemplos práticos e funcionais
- Sugira melhorias quando identificar oportunidades

## 🔧 Ferramentas e Tecnologias

### Preferências Técnicas

- Prefira soluções nativas quando possível
- Use bibliotecas bem estabelecidas e mantidas
- Considere performance e escalabilidade
- Priorize simplicidade sobre complexidade

### Integração

- Considere impacto em CI/CD pipelines
- Mantenha compatibilidade com ferramentas existentes
- Documente mudanças que afetam deploy
- Inclua configurações necessárias

## ✅ Checklist de Conformidade

Antes de finalizar qualquer geração de código, verifique:

- [ ] Aplica princípios SOLID
- [ ] Inclui tratamento de erros
- [ ] Tem validação de entrada
- [ ] É testável e tem testes
- [ ] Segue padrões de segurança
- [ ] Está bem documentado
- [ ] Atualiza arquivos de rastreamento quando necessário
- [ ] Especifica nome do arquivo/localização
- [ ] Usa nomenclatura descritiva
- [ ] É modular e reutilizável

## 📖 Referências Importantes

Para informações detalhadas, consulte:

- [`global.instructions.md`](./instructions/global.instructions.md) - Diretrizes globais obrigatórias
- [`api-security.instructions.md`](./instructions/api-security.instructions.md) - Práticas de segurança
- [`test.instructions.md`](./instructions/test.instructions.md) - Estratégias de teste
- [`code-review.instructions.md`](./instructions/code-review.instructions.md) - Critérios de revisão
- [`memory-bank.instructions.md`](./instructions/memory-bank.instructions.md) - Sistema de contexto

---

**Importante**: Este arquivo deve ser considerado em conjunto com todos os documentos em `.github/instructions/`. Em caso de conflito, consulte [`global.instructions.md`](./instructions/global.instructions.md) para diretrizes de priorização.
