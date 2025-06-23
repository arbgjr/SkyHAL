---
mode: "agent"
description: "Implementar tratamento de erros robusto e padronizado."
---

# Tratamento de Erros

Implemente tratamento de erros robusto e padronizado.

## Estratégias por Camada

- **Controllers**: Capturar e transformar em respostas HTTP apropriadas
- **Services**: Lançar exceções específicas de domínio
- **Repositories**: Tratar erros de acesso a dados

## Tipos de Erro

- **ValidationException**: 400 Bad Request
- **NotFoundException**: 404 Not Found
- **UnauthorizedException**: 401 Unauthorized
- **ForbiddenException**: 403 Forbidden
- **ConflictException**: 409 Conflict

## Logging Obrigatório

- Incluir correlationId em todos os logs
- Nunca logar informações sensíveis
- Diferentes níveis por tipo de erro
- Stack trace completa para erros inesperados

Referência: [Troubleshooting Guidelines](../instructions/troubleshooting.instructions.md)
