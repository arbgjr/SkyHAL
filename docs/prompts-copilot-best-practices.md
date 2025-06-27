# Melhores Práticas para Uso do GitHub Copilot como Agente de Tarefas

> **Arquivo de apoio para governança de prompts e instruções internas**

---

## 1. Escopo Claro das Issues/Prompts
- Descreva claramente o problema ou tarefa.
- Inclua critérios de aceite objetivos (ex: "deve conter testes unitários").
- Indique explicitamente quais arquivos ou áreas do projeto devem ser alterados.
- Pense na issue como um prompt para IA: seja direto, evite ambiguidades.

## 2. Tipos de Tarefas Recomendadas para Copilot
- Correção de bugs pontuais.
- Ajustes em interface de usuário.
- Melhoria de cobertura de testes.
- Atualização de documentação.
- Refino de acessibilidade.
- Endereçamento de débito técnico simples.

**Evite delegar ao Copilot:**
- Refatorações amplas e complexas.
- Mudanças que exigem conhecimento profundo de domínio ou dependências cruzadas.
- Tarefas críticas de produção, segurança ou privacidade.
- Issues com requisitos vagos ou abertos.

## 3. Iteração via Pull Request
- Trate o Copilot como um colaborador: revise o PR, comente melhorias ou ajustes.
- Prefira agrupar comentários em uma revisão única ("Start a review") para maior eficiência.
- O Copilot responde apenas a comentários de usuários com permissão de escrita.

## 4. Instruções Customizadas no Repositório
- Mantenha um arquivo `.github/copilot-instructions.md` com padrões, fluxos e exemplos do projeto.
- Detalhe comandos de build, teste e validação.
- Explique a estrutura do repositório e convenções de código.
- Exemplo de tópicos:
  - Fluxo de desenvolvimento (build, test, lint, CI)
  - Estrutura de pastas e responsabilidades
  - Padrões de injeção de dependência
  - Regras para documentação e testes

## 5. Pré-instalação de Dependências
- Use um arquivo `copilot-setup-steps.yml` para garantir que dependências essenciais estejam disponíveis no ambiente do Copilot.
- Isso acelera e aumenta a confiabilidade das execuções automáticas.

## 6. Uso do Model Context Protocol (MCP)
- Considere integrar ferramentas MCP para ampliar as capacidades do Copilot, especialmente para automação e contexto avançado.

## 7. Referências e Links Úteis
- [Best practices for using Copilot to work on tasks (GitHub Docs)](https://docs.github.com/en/enterprise-cloud@latest/copilot/using-github-copilot/coding-agent/best-practices-for-using-copilot-to-work-on-tasks)
- [Customizing Copilot with repository instructions](https://docs.github.com/en/enterprise-cloud@latest/copilot/customizing-copilot/adding-repository-custom-instructions-for-github-copilot)
- [Model Context Protocol (MCP)](https://docs.github.com/en/enterprise-cloud@latest/copilot/using-github-copilot/coding-agent/extending-copilot-coding-agent-with-mcp)

---

**Dica:**
Sempre revise e atualize as instruções internas conforme o projeto evolui. Prompts bem definidos e governança clara aumentam a produtividade e a qualidade das entregas automatizadas.
