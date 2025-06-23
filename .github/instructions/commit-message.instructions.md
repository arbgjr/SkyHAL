---
applyTo: "**"
---
# ✍️ Mensagens de Commit

## Formato
```
<tipo>[escopo]: <descrição>

[corpo opcional]

[rodapé opcional]
```

## 1. Cabeçalho (Obrigatório)

**Tipos:**
- `feat`: Nova funcionalidade
- `fix`: Correção de bug
- `refactor`: Reestruturação sem mudança funcional
- `style`: Formatação, espaços, etc.
- `test`: Adição/correção de testes
- `docs`: Alterações na documentação
- `build`: Sistema de build/dependências
- `ci`: Scripts de CI
- `chore`: Sem alteração no código fonte
- `perf`: Melhoria de performance

**Escopo:**
- Área do código afetada: `usuarios`, `auth`, `kafka`, `api-core`, etc.

**Descrição:**
- Concisa (≤ 50 caracteres)
- Imperativo presente ("adicionar" não "adicionado")
- Sem capitalizar primeira letra
- Sem ponto final

## 2. Corpo (Opcional)
- Contexto adicional (o "porquê")
- Separado do cabeçalho por linha em branco
- Máximo 72 caracteres por linha

## 3. Rodapé (Opcional)
- Para Breaking Changes: `BREAKING CHANGE: descrição...`
- Para Issues: `Refs: AB#12345`, `Closes: #42`

## Exemplos

**Simples:**
```
feat(usuarios): adicionar endpoint para consulta por CPF
fix(auth): corrigir parsing da data no token JWT
```

**Com corpo:**
```
feat(auth): implementar autenticação JWT

Utiliza tokens JWT Bearer para proteger endpoints.
Validação em cada requisição.
```

**Com Breaking Change:**
```
refactor(api): alterar formato de resposta de erro

BREAKING CHANGE: Estrutura de resposta para erros mudou.
Refs: AB#78910
```