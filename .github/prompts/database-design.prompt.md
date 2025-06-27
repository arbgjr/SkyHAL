---
mode: "agent"
description: "Implementar design de banco de dados seguindo melhores práticas."
---

# Design de Banco de Dados

Projete ou refatore estruturas de banco de dados seguindo melhores práticas.

## Padrões Obrigatórios

- Nomenclatura em português/inglês consistente
- Normalização até 3NF mínimo
- Índices para queries frequentes
- Constraints de integridade
- Auditoria (created_at, updated_at, created_by, updated_by)

## Análise de Performance

- Verificar queries N+1
- Otimizar joins complexos
- Implementar paginação adequada
- Considerar particionamento se necessário

## Segurança

- Não expor IDs sequenciais
- Validar permissões a nível de linha
- Implementar soft delete quando apropriado
