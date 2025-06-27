---
applyTo: "**"
---

# ✍️ Mensagens de Commit - Padrão Avançado

## 🎯 Para GitHub Copilot: Geração Automática

### Formato Obrigatório

```
<tipo>[escopo opcional]: <descrição>

[corpo opcional - explicar O QUÊ e POR QUÊ]

[rodapé opcional - breaking changes, issues]
```

### Tipos Específicos e Quando Usar

#### **feat** - Nova Funcionalidade

```bash
feat(auth): implementar autenticação JWT com refresh token

- Adiciona middleware de autenticação JWT
- Implementa renovação automática de tokens
- Inclui logout com blacklist de tokens

Refs: #123
```

#### **fix** - Correção de Bug

```bash
fix(api): corrigir vazamento de memória em upload de arquivos

O sistema estava mantendo arquivos em memória após upload.
Implementada limpeza automática usando IDisposable pattern.

Impacto: Reduz uso de memória em 80% em operações de upload.
Closes: #456
```

#### **refactor** - Refatoração

```bash
refactor(services): extrair interface IEmailService

- Move lógica de email para serviço dedicado
- Implementa padrão Dependency Injection
- Melhora testabilidade com mock de IEmailService

BREAKING CHANGE: EmailService agora requer configuração de SMTP
no appsettings.json

Refs: #789
```

#### **perf** - Melhoria de Performance

```bash
perf(database): otimizar queries de relatórios

- Adiciona índices para colunas frequentemente consultadas
- Implementa paginação em listagens grandes
- Reduz tempo de resposta de 2s para 200ms

Impacto: Melhoria de 90% na performance de relatórios.
```

#### **test** - Testes

```bash
test(users): adicionar testes de integração para UserController

- Testa cenários de criação, atualização e exclusão
- Inclui validação de entrada e casos de erro
- Cobertura aumentada de 65% para 85%

Refs: #321
```

#### **docs** - Documentação

```bash
docs(api): atualizar documentação OpenAPI

- Adiciona exemplos de request/response
- Documenta códigos de erro específicos
- Inclui guia de autenticação

Refs: #654
```

### Configuração Automática VS Code

#### **settings.json** - Instruções para Commit:

```json
{
  "github.copilot.chat.commitMessageGeneration.instructions": [
    {
      "text": "Sempre seguir formato convencional: tipo(escopo): descrição"
    },
    {
      "text": "Incluir contexto sobre IMPACTO da mudança"
    },
    {
      "text": "Explicar O QUÊ mudou e POR QUÊ foi necessário"
    },
    {
      "text": "Mencionar breaking changes se houver"
    },
    {
      "text": "Referenciar issues relacionadas com Refs: ou Closes:"
    },
    {
      "file": ".github/instructions/commit-message.instructions.md"
    }
  ]
}
```

### Templates por Tipo de Mudança

#### **Nova Feature Completa:**

```bash
feat(module): implementar [funcionalidade]

Funcionalidades incluídas:
- [Lista específica do que foi adicionado]
- [Integrações implementadas]
- [Validações incluídas]

Impacto técnico:
- [Como afeta arquitetura]
- [Performance esperada]
- [Compatibilidade]

Refs: #[issue-number]
```

#### **Bug Fix Crítico:**

```bash
fix(critical): corrigir [problema específico]

Problema: [Descrição clara do bug]
Causa raiz: [O que estava causando]
Solução: [Como foi resolvido]

Impacto:
- [Usuários afetados]
- [Sistemas corrigidos]
- [Dados preservados]

Closes: #[bug-issue]
```

#### **Refatoração com Breaking Change:**

```bash
refactor(api): reestruturar [componente] para [objetivo]

Motivação: [Por que a refatoração foi necessária]

Mudanças:
- [Lista específica de alterações]
- [Novos padrões implementados]
- [Código removido/movido]

BREAKING CHANGE: [Impacto específico na compatibilidade]
Migração: [Como desenvolvedores devem adaptar]

Refs: #[refactor-issue]
```

### Verificação Automatizada

#### **Git Hook - commit-msg:**

```bash
#!/bin/sh
# .git/hooks/commit-msg

# Verificar formato convencional
if ! grep -qE '^(feat|fix|docs|style|refactor|test|chore|perf|ci|build)(\(.+\))?: .{1,50}' "$1"; then
    echo "❌ Formato de commit inválido!"
    echo "Use: tipo(escopo): descrição"
    echo "Exemplo: feat(auth): implementar login JWT"
    exit 1
fi

# Verificar tamanho da primeira linha
if [ $(head -n1 "$1" | wc -c) -gt 50 ]; then
    echo "❌ Primeira linha muito longa (máximo 50 caracteres)"
    exit 1
fi

echo "✅ Formato de commit válido"
```

### Boas Práticas Específicas

#### **O que INCLUIR:**

- **Impacto no usuário**: Como a mudança afeta funcionalidade
- **Impacto técnico**: Mudanças arquiteturais ou de performance
- **Contexto de negócio**: Por que a mudança foi necessária
- **Breaking changes**: Sempre documentar incompatibilidades

#### **O que EVITAR:**

```bash
# ❌ Muito vago
fix: correção

# ❌ Muito técnico sem contexto
refactor: move UserService to different namespace

# ❌ Sem explicar impacto
feat: add validation

# ✅ Específico com contexto
fix(auth): corrigir timeout em sessões longas

Usuários não eram desconectados após 30min de inatividade.
Ajustado timer para funcionar corretamente com sliding expiration.

Impacto: Melhora segurança e experiência do usuário.
Closes: #234
```

### Integração com Ferramentas

#### **Conventional Changelog:**

```json
// package.json
{
  "scripts": {
    "changelog": "conventional-changelog -p angular -i CHANGELOG.md -s",
    "release": "standard-version"
  }
}
```

#### **Semantic Release:**

```yaml
# .github/workflows/release.yml
- name: Semantic Release
  env:
    GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
  run: npx semantic-release
```

## 🎯 Instruções para Copilot

Ao gerar mensagens de commit:

1. **SEMPRE** usar formato convencional
2. **SEMPRE** incluir contexto sobre impacto
3. **SEMPRE** explicar motivação da mudança
4. **SEMPRE** mencionar breaking changes se houver
5. **CONSIDERAR** impacto no usuário final
6. **REFERENCIAR** issues quando aplicável
7. **MANTER** primeira linha concisa (≤50 caracteres)
8. **DETALHAR** mudanças complexas no corpo
