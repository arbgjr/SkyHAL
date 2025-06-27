---
applyTo: "**"
---
# Instruções Específicas para GitHub Copilot

## Tom e Estilo de Resposta

- Evitar desculpas excessivas ou linguagem muito formal
- Ser direto e factual, focando na solução
- Quando questionar decisões, responder com fatos e alternativas
- Evitar hipérboles, manter foco pragmático na tarefa

## Formato de Código

- Sempre especificar o nome do arquivo onde o código deve ser colocado
- Quebrar código em módulos e componentes reutilizáveis
- Incluir importações e dependências necessárias
- Adicionar comentários explicativos para lógica complexa

## Tratamento de Erros

- Sempre incluir tratamento de exceções
- Validar entradas de usuário
- Implementar logging adequado
- Retornar códigos de erro apropriados para APIs

## Testes

- Gerar testes automaticamente para novo código
- Seguir padrão AAA (Arrange-Act-Assert)
- Incluir casos de teste para cenários de erro
- Mockar dependências externas

## Segurança

- Validar todas as entradas
- Não incluir segredos no código
- Aplicar princípio de menor privilégio
- Implementar autenticação e autorização adequadas
