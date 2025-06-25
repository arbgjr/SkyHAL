# Correlação de Logs e Traces – Observabilidade SkyHAL

## Exemplo de Log com Trace ID

```python
logger.info(
    "Processando solicitação",
    user_id="12345",
    request_id="req-789",
    operation="user_profile_update"
)
# O trace_id é automaticamente incluído pelo middleware
```

## Exemplo de Trace Customizado

```python
with tracing_provider.create_span("user_profile_update") as span:
    span.set_attribute("user_id", "12345")
    # ... lógica ...
```

## Dica

- Use o trace_id nos logs para rastrear requisições ponta a ponta no Grafana/Jaeger.

## Referências

- [Guia para Desenvolvedores](../usage/developers.md)
- [README Observabilidade](../README.md)
