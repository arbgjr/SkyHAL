# Mecanismos de Rollback e Quotas – Auto-Extensão MCP

## Rollback

- Toda tool gerada é versionada no `ToolRegistry`.
- Rollback pode ser feito para qualquer versão anterior via API ou CLI administrativa.
- Logs de rollback são registrados para auditoria.

### Exemplo de uso

```python
# Rollback para versão anterior
tool_registry.rollback("tool_name", "1.0.0")
```

## Quotas

- Limite de ferramentas geradas por sessão (`maxToolsPerSession`)
- Limite de complexidade (`maxToolComplexity`)
- Limite de uso de recursos no sandbox
- Quotas configuráveis em `config/observability.yaml` e via API

### Exemplo de configuração

```yaml
skyhal:
  maxToolsPerSession: 5
  maxToolComplexity: 100
  sandboxTimeout: 30000
```

## Referências

- `src/domain/auto_extension/capability_analyzer.py`
- `src/domain/auto_extension/tool_generator.py`
- `src/domain/auto_extension/security_sandbox.py`
