---
mode: "agent"
description: "Implementar geração de documentação seguindo melhores práticas."
---

# Geração de Documentação

Gere documentação deste sistema seguindo os padrões definidos em [documentation.instructions.md](../instructions/documentation.instructions.md).

## Tipos de Documentação

### Para Código

- **Comentários**: Explicar "por quê", não "o quê"
- **Docstrings/XMLDocs**: Para classes, métodos e propriedades públicas
- **Exemplos**: Incluir para APIs e funções complexas

### Para APIs

- **Especificação**: OpenAPI/Swagger para REST
- **Endpoints**: Parâmetros, respostas, códigos de erro
- **Exemplos**: Requisições e respostas
- **Autenticação**: Métodos e fluxos detalhados

### Para Usuários

- **Guias**: Passo a passo para funcionalidades
- **FAQ**: Perguntas frequentes
- **Troubleshooting**: Soluções para problemas comuns

## Princípios

1. **Proximidade ao código** - Documentação que se afasta fica desatualizada
2. **Atualização constante** - Durante desenvolvimento, não depois
3. **Linguagem clara** - Frases curtas, evitar jargões
4. **Estrutura consistente** - Templates padronizados
5. **Automação** - Gerar do código quando possível

Consulte o arquivo completo para templates e exemplos específicos.
