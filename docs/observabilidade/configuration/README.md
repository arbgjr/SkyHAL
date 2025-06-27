# Configuração de Observabilidade – SkyHAL

## Estrutura de Arquivos

```
config/
├── observability.yaml           # Configuração principal
├── environments/
│   ├── development.yaml        # Configurações de desenvolvimento
│   ├── staging.yaml            # Configurações de staging
│   └── production.yaml         # Configurações de produção
└── exporters/
    ├── prometheus.yaml         # Configuração Prometheus
    ├── jaeger.yaml             # Configuração Jaeger
    └── loki.yaml               # Configuração Loki
```

## Exemplos de Configuração

Veja exemplos completos em:

- [observability-config.md](../../especificacoes-tecnicas/artefatos/observability-config.md)

## Parâmetros Principais

- `service.name`, `service.version`, `environment`: Identificação do serviço
- `logging`: Nível, formato, campos sensíveis
- `metrics`: RED, customizadas, labels
- `tracing`: Sampling, auto-instrumentação, atributos
- `exporters`: Prometheus, Jaeger, Loki

## Referências

- [README Observabilidade](../README.md)
- [Guia para Devs](../usage/developers.md)
