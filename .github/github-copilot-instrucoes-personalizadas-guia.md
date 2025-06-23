# Guia de Instruções Personalizadas para GitHub Copilot

Este guia abrangente explica como usar arquivos de instruções personalizadas com o GitHub Copilot para melhorar a qualidade do código, aplicar padrões de equipe e aumentar a produtividade.

## Índice

1. [Introdução](#introdução)
2. [Tipos de Arquivos de Instruções Personalizadas](#tipos-de-arquivos-de-instruções-personalizadas)
   - [.github/copilot-instructions.md](#githubcopilot-instructionsmd)
   - [Arquivos .instructions.md](#arquivos-instructionsmd)
   - [Arquivos .prompt.md](#arquivos-promptmd)
3. [Configurações do VS Code para GitHub Copilot](#configurações-do-vs-code-para-github-copilot)
4. [Boas Práticas e Exemplos](#boas-práticas-e-exemplos)
5. [Referências e Recursos Adicionais](#referências-e-recursos-adicionais)

## Introdução

O GitHub Copilot pode fornecer respostas melhor alinhadas com as práticas da sua equipe, padrões de codificação e requisitos do projeto quando recebe o contexto apropriado. Em vez de repetidamente fornecer este contexto em cada prompt, você pode criar arquivos que adicionam automaticamente estas informações às suas interações com o Copilot.

As instruções personalizadas ajudam o Copilot a entender:
- Seu estilo e convenções de codificação
- Estrutura e arquitetura do projeto
- Bibliotecas ou frameworks específicos que você está usando
- Melhores práticas e padrões da equipe

## Tipos de Arquivos de Instruções Personalizadas

### .github/copilot-instructions.md

Este é um arquivo de instruções para todo o repositório que se aplica a todas as conversas com o GitHub Copilot relacionadas ao seu repositório.

#### Propósito
- Estabelece padrões e práticas globais de codificação
- Aplica-se automaticamente a todas as interações com o Copilot no repositório
- Garante consistência entre membros da equipe

#### Configuração
1. Crie uma pasta `.github` na raiz do seu repositório (se não existir)
2. Adicione um arquivo chamado `copilot-instructions.md` dentro desta pasta
3. Escreva suas instruções no formato Markdown

#### Exemplo de Conteúdo
```markdown
# Padrões de Codificação

## Geral
- Use camelCase para nomes de variáveis e funções
- Use PascalCase para nomes de classes
- Use nomes de variáveis significativos que descrevam seu propósito
- Mantenha funções pequenas e focadas em uma única tarefa
- Comente lógica complexa, mas deixe código limpo falar por si mesmo

## JavaScript/TypeScript
- Use aspas duplas para strings
- Use ponto e vírgula ao final das declarações
- Prefira const em vez de let quando as variáveis não serão reatribuídas
- Use async/await para código assíncrono em vez de promises

## Testes
- Escreva testes unitários para toda lógica de negócios
- Use Jest para testes
- Siga o padrão AAA (Arrange, Act, Assert)

## Tratamento de Erros
- Use blocos try/catch para tratamento de erros
- Prefira tipos de erro específicos em vez de genéricos
- Registre erros com informações de contexto
```

#### Como Funciona
- O Copilot inclui automaticamente estas instruções no contexto para cada solicitação de chat
- As instruções não são visíveis diretamente no chat, mas influenciam as respostas do Copilot
- Você pode verificar se as instruções foram usadas verificando a lista de Referências em uma resposta

### Arquivos .instructions.md

Estes são arquivos de instruções específicos para tarefas que podem ser configurados para serem incluídos para arquivos ou pastas específicas.

#### Propósito
- Criar instruções direcionadas para tarefas ou tipos de arquivos específicos
- Controle mais granular comparado às instruções para todo o repositório
- Aplicar diferentes padrões a diferentes partes do seu código

#### Configuração
1. Crie arquivos `.instructions.md` em diretórios relevantes
2. Adicione os metadados `applyTo` no topo do arquivo para especificar a quais arquivos se aplica
3. Configure o VS Code para usar arquivos de instruções (configurações abordadas mais adiante)

#### Exemplo de Conteúdo
```markdown
---
applyTo: "src/components/**"
---
# Padrões para Componentes React

## Estrutura
- Use componentes funcionais com hooks
- Organize importações: React primeiro, depois hooks, depois componentes, depois estilos
- Extraia lógica de UI complexa para hooks personalizados
- Use prop-types ou interfaces TypeScript para todas as props

## Gerenciamento de Estado
- Use useState para estado local do componente
- Use useContext para estado compartilhado entre componentes
- Evite prop drilling

## Estilização
- Use módulos CSS para estilização de componentes
- Siga a convenção de nomenclatura BEM
- Mantenha estilos específicos de componentes junto ao componente
```

### Arquivos .prompt.md

Arquivos de prompt permitem que você salve instruções de prompts comuns em arquivos Markdown que você pode reutilizar em conversas.

#### Propósito
- Armazenar templates de prompts reutilizáveis
- Incluir contexto que você frequentemente precisa
- Compartilhar prompts comuns com sua equipe

#### Configuração
1. Habilite arquivos de prompt nas configurações do VS Code
2. Crie arquivos com extensão `.prompt.md`
3. Armazene-os em uma pasta designada (comumente `.github/prompts`)

#### Exemplo de Conteúdo
```markdown
# Gerador de Componente de Formulário React

Seu objetivo é gerar um novo componente de formulário React.

Requisitos:
- Use Formik para gerenciamento de estado do formulário
- Use Yup para validação
- Inclua validação de campos
- Mostre erros de validação abaixo de cada campo
- Suporte os seguintes tipos de campo: texto, email, senha, select, checkbox
- Crie um layout responsivo

O componente deve:
1. Aceitar um objeto de configuração para campos
2. Gerenciar o envio do formulário
3. Mostrar estado de carregamento durante o envio
4. Mostrar mensagens de sucesso/erro após o envio
```

#### Como Usar
1. No Chat do Copilot, clique no ícone Anexar Contexto (clipe de papel)
2. Escolha "Prompt..." e selecione seu arquivo de prompt
3. Opcionalmente adicione detalhes específicos para sua solicitação atual
4. Envie o prompt de chat

## Configurações do VS Code para GitHub Copilot

Você pode personalizar o comportamento do Copilot através das configurações do VS Code. Aqui estão as principais configurações:

### Configurações Gerais
```json
{
  "github.copilot.enable": true,
  "github.copilot.editor.enableCodeActions": true,
  "github.copilot.renameSuggestions.triggerAutomatically": true,
  "chat.commandCenter.enabled": true,
  "github.copilot.chat.followUps": true
}
```

### Configurações de Arquivos de Instruções
```json
{
  "chat.promptFiles": true,
  "chat.promptFilesLocations": [
    ".github/prompts"
  ]
}
```

### Instruções Personalizadas por Tarefa
```json
{
  "github.copilot.chat.codeGeneration.instructions": [
    {
      "text": "Siga nossos padrões de codificação incluindo tratamento adequado de erros, logging e cobertura de testes."
    },
    {
      "file": "./docs/coding-standards.md"
    }
  ],
  "github.copilot.chat.testGeneration.instructions": [
    {
      "text": "Gere testes usando Jest. Inclua o caminho feliz, casos extremos e cenários de erro."
    }
  ],
  "github.copilot.chat.codeReview.instructions": [
    {
      "text": "Revise o código para problemas de desempenho, vulnerabilidades de segurança e aderência aos nossos padrões de codificação."
    }
  ],
  "github.copilot.chat.commitMessageGeneration.instructions": [
    {
      "text": "Siga o formato de commits convencionais. Seja descritivo sobre o que mudou e por quê."
    }
  ],
  "github.copilot.chat.pullRequestDescriptionGeneration.instructions": [
    {
      "text": "Inclua contexto, alterações feitas, testes realizados e quaisquer problemas pendentes."
    }
  ]
}
```

## Boas Práticas e Exemplos

### Boas Práticas Gerais

1. **Mantenha instruções concisas e específicas**
   - Foque em regras concretas em vez de preferências vagas
   - Evite instruções excessivamente complexas ou longas

2. **Comece com regras de alta prioridade**
   - Coloque as diretrizes mais importantes primeiro
   - Agrupe instruções relacionadas

3. **Evite instruções que não funcionarão**
   Estes tipos de instruções geralmente não funcionam bem:
   - Referências a recursos externos
   - Instruções sobre tom ou estilo de respostas
   - Solicitações para tamanhos específicos ou formatos de resposta

4. **Verifique se as instruções estão funcionando**
   - Verifique referências de resposta para ver se seus arquivos de instrução estão sendo usados
   - Teste com prompts simples para confirmar que as instruções estão sendo aplicadas

### Exemplo: Padrões de Codificação para uma Equipe

```markdown
# Padrões de Codificação da Equipe

## Convenções de Nomenclatura
- Use camelCase para variáveis e funções
- Use PascalCase para classes e componentes
- Use UPPER_SNAKE_CASE para constantes
- Prefixe métodos privados com underscore
- Use nomes descritivos que explicam o propósito

## Diretrizes JavaScript
- Use recursos ES6+ onde apropriado
- Prefira const sobre let, evite var
- Use arrow functions para callbacks
- Use template literals em vez de concatenação de strings
- Use desestruturação para objetos e arrays

## Diretrizes React
- Use componentes funcionais com hooks
- Extraia lógica reutilizável para hooks personalizados
- Mantenha componentes pequenos e focados
- Use prop-types ou TypeScript para verificação de tipo
- Siga o padrão de componente apresentacional/container

## Testes
- Escreva testes para toda lógica de negócios
- Teste componentes para renderização e interações adequadas
- Use mocks para dependências externas
- Nomeie testes descritivamente usando o formato "should..."
```

### Exemplo: Regras SonarQube como Instruções

```markdown
# Regras SonarQube

## Code Smells
- Mantenha complexidade ciclomática abaixo de 15
- Mantenha comprimento da função abaixo de 60 linhas
- Evite blocos de código duplicados
- Limite parâmetros para 5 por função
- Remova variáveis e importações não utilizadas

## Bugs
- Sempre verifique null antes de acessar propriedades
- Não reatribua parâmetros
- Feche recursos em blocos finally
- Não capture exceções genéricas
- Não use valores de ponto flutuante em comparações de igualdade

## Segurança
- Valide todas as entradas do usuário
- Não hardcode credenciais
- Use consultas parametrizadas para acesso ao banco de dados
- Não registre informações sensíveis em logs
- Use protocolos de comunicação seguros
```

## Referências e Recursos Adicionais

1. [Documentação do GitHub Copilot](https://docs.github.com/en/copilot/customizing-copilot/adding-repository-custom-instructions-for-github-copilot)
2. [Guia de Instruções Personalizadas do VS Code](https://code.visualstudio.com/blogs/2025/03/26/custom-instructions)
3. [Formato de Instruções do Copilot](https://copilot-instructions.md/)
4. [Como Usar copilot-instructions.md](https://medium.com/@a.shtaigmann/how-to-use-copilot-instructions-md-to-improve-github-copilot-suggestions-fcd71b7f787f)
5. [Dominando Instruções Personalizadas do GitHub Copilot](https://medium.com/@anil.goyal0057/mastering-github-copilot-custom-instructions-with-github-copilot-instructions-md-f353e5abf2b1)
6. [Regras para Melhor Geração de Código](https://www.reddit.com/r/vibecoding/comments/1l0ynlv/rules_i_give_claude_to_get_better_code_curious/)
7. [Economize Horas com Instruções Personalizadas](https://www.linkedin.com/pulse/save-hours-giving-github-copilot-custom-instructions-code-raymon-s-j4tke/)
8. [Referência de Configurações do VS Code para Copilot](https://code.visualstudio.com/docs/copilot/reference/copilot-settings)

---

Este guia destina-se a ajudá-lo a aproveitar melhor o GitHub Copilot em seu fluxo de trabalho de desenvolvimento. Ao usar arquivos de instruções personalizadas adequadamente, você pode melhorar significativamente a qualidade e relevância das sugestões do Copilot enquanto aplica padrões de codificação em sua equipe.
