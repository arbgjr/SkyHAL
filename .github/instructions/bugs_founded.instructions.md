# Registro de Bugs Encontrados

Este documento rastreia os bugs identificados no projeto, mesmo que já tenham sido corrigidos.

---

## Formato de Registro

Para cada bug, utilize o seguinte formato:

```
### [ID_BUG] - Título Descritivo do Bug

- **Data Identificado**: YYYY-MM-DD
- **Identificado Por**: @username
- **Componente(s) Afetado(s)**: (ex: Módulo de Login, API de Produtos, Frontend Carrinho)
- **Gravidade**: (Crítica, Alta, Média, Baixa)
- **Prioridade**: (Urgente, Alta, Média, Baixa)
- **Status**: (Novo, Em Análise, Em Correção, Corrigido, Fechado, Reaberto, Adiado)

**Descrição do Bug**:
(Detalhe o comportamento inesperado. Seja o mais específico possível.)

**Passos para Reproduzir**:
1. (Passo 1)
2. (Passo 2)
3. (Passo 3)
... (Comportamento observado vs. Comportamento esperado)

**Ambiente (se aplicável)**:
- Navegador/Versão:
- Sistema Operacional:
- Versão do Software:
- Dados específicos usados:

**Impacto do Bug**:
(Qual o impacto no usuário, no sistema ou no negócio?)

**Solução Aplicada (se corrigido)**:
(Descreva a correção implementada.)

- **Data da Correção**: YYYY-MM-DD
- **Corrigido Por**: @username
- **Commit/PR da Correção**: (Link para o commit ou Pull Request)

**Causa Raiz (opcional, se conhecida)**:
(Uma breve análise da causa raiz do bug.)

**Notas Adicionais**:
(Qualquer outra informação relevante, screenshots, logs, etc.)

---
```

## Bugs Registrados

### Exemplo: BUG001 - Botão de Login Não Responde em Navegadores Específicos

- **Data Identificado**: 2025-05-15
- **Identificado Por**: @tester_jane
- **Componente(s) Afetado(s)**: Módulo de Login, Interface do Usuário
- **Gravidade**: Alta
- **Prioridade**: Urgente
- **Status**: Corrigido

**Descrição do Bug**:
O botão "Entrar" na página de login não dispara nenhuma ação quando clicado nos navegadores Safari (versão X.Y) e Edge (versão A.B). Em outros navegadores como Chrome e Firefox, funciona como esperado.

**Passos para Reproduzir**:

1. Abrir a página de login (`/login`) no Safari vX.Y ou Edge vA.B.
2. Preencher o email e senha com credenciais válidas.
3. Clicar no botão "Entrar".
4. **Comportamento Observado**: Nada acontece. Nenhuma requisição de rede é disparada, nenhum erro no console.
5. **Comportamento Esperado**: O usuário deve ser autenticado e redirecionado para o dashboard.

**Ambiente (se aplicável)**:

- Navegador/Versão: Safari vX.Y, Microsoft Edge vA.B
- Sistema Operacional: macOS Sonoma (para Safari), Windows 11 (para Edge)

**Impacto do Bug**:
Usuários dos navegadores afetados não conseguem acessar o sistema, bloqueando completamente o uso da plataforma para eles.

**Solução Aplicada (se corrigido)**:
Foi identificado um problema de compatibilidade com um polyfill de JavaScript que não estava sendo carregado corretamente nesses navegadores. O script de carregamento do polyfill foi ajustado para garantir a execução antes do código de login.

- **Data da Correção**: 2025-05-15
- **Corrigido Por**: @dev_john
- **Commit/PR da Correção**: [Link para PR #123](https://github.com/SU-AIOFFICE/Demo/pull/123)

**Causa Raiz (opcional, se conhecida)**:
Carregamento assíncrono de dependências críticas não estava garantindo a ordem de execução correta em todos os navegadores.

**Notas Adicionais**:
Testes de compatibilidade cross-browser foram reforçados para a funcionalidade de login.

---

_(Adicione novos bugs abaixo desta linha, seguindo o formato)_
