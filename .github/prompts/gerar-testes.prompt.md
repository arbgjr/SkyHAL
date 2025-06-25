---
mode: 'agent'
tools: ['testing']
description: 'Gera suite completa de testes seguindo padrões'
---

# Gerador de Testes

Crie uma suite completa de testes para o código fornecido seguindo os padrões.

## Tipos de Testes a Gerar

### Unit Tests
- Teste cada função/método isoladamente
- Mock todas as dependências externas
- Teste casos felizes e edge cases
- Teste cenários de erro
- Use padrão AAA (Arrange, Act, Assert)

### Integration Tests
- Teste interações entre componentes
- Teste fluxos de dados end-to-end
- Valide contratos de API
- Teste configurações reais

### Snapshot Tests (se aplicável)
- Para componentes UI
- Para outputs de formatação
- Para estruturas de dados complexas

## Configuração de Testes
- Configure ambiente de testes apropriado
- Setup e teardown adequados
- Mocks e fixtures necessários
- Utilities de teste customizados

## Estrutura de Arquivos
```
${fileBasename}.test.${fileExtension}
__tests__/
  ├── unit/
  ├── integration/
  ├── fixtures/
  └── helpers/
```

## Padrões de Nomenclatura
- `describe()`: Nome da classe/função sendo testada
- `it()`: "should [behavior] when [condition]"
- Test files: `*.test.ts` ou `*.spec.ts`

## Coverage Requirements
- Mínimo 80% code coverage
- 100% coverage para lógica crítica de negócio
- Teste todos os branches condicionais
- Teste todos os error paths

## Ferramentas Sugeridas
- **Jest/Vitest**: Test runner principal
- **Testing Library**: Para testes de componentes
- **MSW**: Para mock de APIs
- **Playwright**: Para testes E2E quando necessário
