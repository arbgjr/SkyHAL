# Exemplos de Instrumentação de Código – Observabilidade SkyHAL

## Logging Estruturado

```python
from src.infrastructure.observability import get_observability_providers
logging_provider, _, _ = get_observability_providers()
logger = logging_provider.get_logger("my_component")
logger.info("Operação concluída", operation="data_sync", duration_ms=150)
```

## Métricas Customizadas

```python
_, metrics_provider, _ = get_observability_providers()
metrics_provider.increment_counter("custom_operations_total", labels={"operation": "data_processing"})
```

## Tracing Customizado

```python
_, _, tracing_provider = get_observability_providers()
with tracing_provider.create_span("custom_operation") as span:
    span.set_attribute("user_id", "12345")
    # ... lógica ...
```

## Referências

- [Guia para Desenvolvedores](../usage/developers.md)
- [README Observabilidade](../README.md)
