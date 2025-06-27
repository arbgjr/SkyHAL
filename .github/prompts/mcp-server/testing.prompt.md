---
mode: "agent"
description: "Implementar e executar testes para servidor MCP"
tools: ['codebase', 'extensions', 'findTestFiles', 'githubRepo', 'problems', 'runCommands', 'runTasks', 'runTests', 'search', 'searchResults', 'terminalLastCommand', 'terminalSelection', 'testFailure', 'usages', 'time', 'get_current_time', 'sequentialthinking', 'filesystem', 'read_file', 'read_multiple_files', 'memory', 'everything', 'longRunningOperation', 'github', 'add_issue_comment', 'create_issue', 'get_issue', 'list_issues', 'search_issues', 'update_pull_request_branch', 'metamcp', 'intruder', 'chroma']
---

# Testes MCP

## 🎯 Objetivo
Garantir qualidade e confiabilidade do servidor MCP através de testes automatizados.

## 📋 Tipos de Teste

### Unitários
- Funções isoladas
- Comportamentos específicos
- Mocking de dependências

### Integração
- Fluxos completos
- Interação entre componentes
- Cenários reais

### Performance
- Tempo de resposta
- Uso de recursos
- Comportamento sob carga

## 🛠️ Ferramentas
- pytest para execução
- pytest-cov para cobertura
- pytest-asyncio para testes assíncronos
- pytest-mock para mocking

## 📚 Referências
- [Python MCP Instructions](../instructions/python-mcp.instructions.md)
- [Test Instructions](../instructions/test.instructions.md)

## ✅ Checklist

Antes de finalizar:
- [ ] Testes unitários completos
- [ ] Testes de integração
- [ ] Cobertura adequada
- [ ] Documentação atualizada
- [ ] CI/CD configurado
