---
mode: 'edit'
description: 'Realiza uma revisão completa de segurança no código'
---

# Revisão de Segurança

Faça uma análise completa de segurança do código selecionado seguindo os padrões.

## Checklist de Segurança

### Autenticação & Autorização
- [ ] Verificar implementação de autenticação adequada
- [ ] Validar controles de autorização (RBAC/ABAC)
- [ ] Analisar gerenciamento de sessões
- [ ] Verificar expiração de tokens/sessões

### Validação de Input
- [ ] Verificar sanitização de todos os inputs
- [ ] Validar proteção contra SQL injection
- [ ] Analisar proteção contra XSS
- [ ] Verificar validação server-side

### Gestão de Dados Sensíveis
- [ ] Verificar se credentials não estão hardcoded
- [ ] Analisar proteção de dados PII
- [ ] Verificar criptografia adequada
- [ ] Validar políticas de logs (sem dados sensíveis)

### Configurações de Segurança
- [ ] Verificar headers de segurança
- [ ] Analisar configurações de CORS
- [ ] Verificar rate limiting
- [ ] Validar configurações de cookies

### Dependências
- [ ] Verificar vulnerabilidades em dependências
- [ ] Analisar versões desatualizadas
- [ ] Validar supply chain security

## Output Esperado
1. **Vulnerabilidades Críticas**: Issues que precisam ser corrigidos imediatamente
2. **Vulnerabilidades Altas**: Issues importantes para próxima release
3. **Melhorias de Segurança**: Sugestões para hardening
4. **Code Fixes**: Exemplos de código corrigido
5. **Prevention**: Como evitar issues similares no futuro
