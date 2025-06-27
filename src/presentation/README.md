# 🖥️ Presentation Layer

## Propósito

Esta camada é responsável pela interface com usuários e sistemas externos.

## Princípios

- Define APIs e interfaces de usuário
- Gerencia apresentação de dados
- Trata validação de entrada
- Gerencia autenticação/autorização

## Estrutura

```plaintext
presentation/
├── api/           # Endpoints da API
├── middlewares/   # Middlewares da aplicação
├── schemas/       # Esquemas de validação
└── responses/     # Formatos de resposta
```

## Regras

1. Depende apenas da camada de aplicação
2. Valida todas as entradas
3. Formata todas as saídas
4. Gerencia estado da sessão
