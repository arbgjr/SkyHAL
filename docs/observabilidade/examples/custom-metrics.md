# Exemplos de Métricas Customizadas – Observabilidade SkyHAL

## Criando um Counter Customizado

```python
_, metrics_provider, _ = get_observability_providers()
metrics_provider.increment_counter(
    "custom_event_total",
    labels={"event_type": "auto_extension"}
)
```

## Criando um Gauge

```python
metrics_provider.set_gauge("active_sessions", 5)
```

## Criando um Histogram

```python
metrics_provider.observe_histogram(
    "tool_execution_duration_seconds",
    value=0.42,
    labels={"tool": "capability_analyzer"}
)
```

## Referências

- [Guia para Desenvolvedores](../usage/developers.md)
- [README Observabilidade](../README.md)
