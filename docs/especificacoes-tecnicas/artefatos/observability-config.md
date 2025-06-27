# Especificação Técnica: Configuração de Observabilidade

## 📁 Artefato

**Caminho:** `config/observability.yaml`

## 🎯 Objetivo

Criar arquivos de configuração centralizados para todos os componentes de observabilidade, permitindo configuração flexível de logging, métricas, tracing e exportadores por ambiente (dev, staging, prod).

## 📚 Instruções Relacionadas

- **observabilidade.instructions.md** - Padrões de configuração e nomenclatura
- **python-mcp.instructions.md** - Padrões de configuração em projetos Python
- **api-security.instructions.md** - Não expor dados sensíveis em configurações

## 🎨 Prompts Relacionados

- **observabilidade.prompt.md** - Configuração de OpenTelemetry
- **clean-architecture.prompt.md** - Organização de configurações

## 🎯 Chat Mode Recomendado

- **arquiteto.chatmode.md** - Para definição de padrões de configuração

## 🏗️ Estrutura de Arquivos

```
config/
├── observability.yaml           # Configuração principal
├── environments/
│   ├── development.yaml        # Configurações de desenvolvimento
│   ├── staging.yaml            # Configurações de staging
│   └── production.yaml         # Configurações de produção
└── exporters/
    ├── prometheus.yaml         # Configuração Prometheus
    ├── jaeger.yaml            # Configuração Jaeger
    └── loki.yaml              # Configuração Loki
```

## 🛠️ Implementação de Configurações

### 1. Configuração Principal (`config/observability.yaml`)

```yaml
# Configuração principal de observabilidade
observability:
  service:
    name: "skyhal-api"
    version: "0.1.0"
    environment: "${ENVIRONMENT:development}"
    instance_id: "${HOSTNAME:localhost}"

  # Configuração de Logging
  logging:
    level: "${LOG_LEVEL:INFO}"
    format: "json"
    structured: true
    include_trace_info: true
    sanitize_sensitive_data: true

    fields:
      service_name: "${SERVICE_NAME:skyhal-api}"
      service_version: "${SERVICE_VERSION:0.1.0}"
      environment: "${ENVIRONMENT:development}"

    sensitive_fields:
      - password
      - token
      - secret
      - key
      - authorization
      - x-api-key

  # Configuração de Métricas
  metrics:
    enabled: true
    prefix: "skyhal"

    # Métricas RED (Rate, Errors, Duration)
    red_metrics:
      enabled: true
      request_counter: "http_requests_total"
      error_counter: "http_errors_total"
      duration_histogram: "http_request_duration_seconds"

    # Métricas customizadas
    custom_metrics:
      enabled: true
      business_metrics: true
      system_metrics: true

    # Configuração de Labels
    default_labels:
      service: "${SERVICE_NAME:skyhal-api}"
      version: "${SERVICE_VERSION:0.1.0}"
      environment: "${ENVIRONMENT:development}"

  # Configuração de Tracing
  tracing:
    enabled: true
    sampling_ratio: "${TRACING_SAMPLING_RATIO:0.1}"

    # Instrumentações automáticas
    auto_instrumentation:
      fastapi: true
      sqlalchemy: true
      requests: true
      logging: true

    # Configuração de Spans
    span_config:
      max_attributes: 128
      max_events: 128
      max_links: 128
      attribute_value_length_limit: 512

    # Recursos incluídos
    resource_attributes:
      service.name: "${SERVICE_NAME:skyhal-api}"
      service.version: "${SERVICE_VERSION:0.1.0}"
      service.environment: "${ENVIRONMENT:development}"
      service.instance.id: "${HOSTNAME:localhost}"

  # Configuração de Exportadores
  exporters:
    prometheus:
      enabled: true
      port: "${PROMETHEUS_PORT:8000}"
      path: "/metrics"
      include_target_info: true

    jaeger:
      enabled: true
      endpoint: "${JAEGER_ENDPOINT:http://localhost:14268/api/traces}"
      timeout: 30
      compression: "gzip"

    otlp:
      enabled: false
      endpoint: "${OTLP_ENDPOINT:http://localhost:4317}"
      insecure: true
      timeout: 30

    loki:
      enabled: false
      endpoint: "${LOKI_ENDPOINT:http://localhost:3100/loki/api/v1/push}"
      tenant_id: "${LOKI_TENANT_ID:}"

  # Configuração de Health Checks
  health_checks:
    enabled: true
    endpoint: "/health"
    detailed_endpoint: "/health/detailed"

    checks:
      - name: "observability_stack"
        enabled: true
      - name: "metrics_exporter"
        enabled: true
      - name: "tracing_exporter"
        enabled: true
```

### 2. Configuração de Desenvolvimento (`config/environments/development.yaml`)

```yaml
# Configurações específicas para desenvolvimento
observability:
  logging:
    level: "DEBUG"

  metrics:
    red_metrics:
      enabled: true
    custom_metrics:
      business_metrics: false  # Desabilitado em dev
      system_metrics: true

  tracing:
    sampling_ratio: 1.0  # 100% sampling em dev

  exporters:
    prometheus:
      enabled: true
      port: 8000

    jaeger:
      enabled: true
      endpoint: "http://localhost:14268/api/traces"

    otlp:
      enabled: false

    loki:
      enabled: false

# Configurações de infraestrutura local
infrastructure:
  jaeger:
    ui_port: 16686
    collector_port: 14268

  prometheus:
    ui_port: 9090
    scrape_interval: "15s"

  grafana:
    ui_port: 3000
    admin_user: "admin"
    admin_password: "admin"
```

### 3. Configuração de Produção (`config/environments/production.yaml`)

```yaml
# Configurações específicas para produção
observability:
  logging:
    level: "INFO"

  metrics:
    red_metrics:
      enabled: true
    custom_metrics:
      business_metrics: true
      system_metrics: true

  tracing:
    sampling_ratio: 0.01  # 1% sampling em produção

  exporters:
    prometheus:
      enabled: true
      port: 8000

    jaeger:
      enabled: true
      endpoint: "${JAEGER_ENDPOINT}"

    otlp:
      enabled: true
      endpoint: "${OTLP_ENDPOINT}"

    loki:
      enabled: true
      endpoint: "${LOKI_ENDPOINT}"
      tenant_id: "${LOKI_TENANT_ID}"

# Configurações de alertas
alerts:
  enabled: true

  rules:
    high_error_rate:
      enabled: true
      threshold: 0.05  # 5% error rate
      duration: "5m"

    high_latency:
      enabled: true
      threshold: 0.5   # 500ms
      percentile: 95
      duration: "2m"

    low_availability:
      enabled: true
      threshold: 0.99  # 99% availability
      duration: "1m"

# Configurações de retenção
retention:
  metrics: "30d"
  traces: "7d"
  logs: "14d"
```

### 4. Configuração Prometheus (`config/exporters/prometheus.yaml`)

```yaml
# Configuração específica do exportador Prometheus
prometheus:
  global:
    scrape_interval: 15s
    evaluation_interval: 15s

  scrape_configs:
    - job_name: 'skyhal-api'
      static_configs:
        - targets: ['localhost:8000']
      metrics_path: '/metrics'
      scrape_interval: 5s

      metric_relabel_configs:
        # Manter apenas métricas relevantes
        - source_labels: [__name__]
          regex: 'skyhal_.*|http_.*|process_.*'
          action: keep

  # Regras de agregação
  rule_files:
    - "rules/*.yml"

  # Configuração de alertas
  alerting:
    alertmanagers:
      - static_configs:
          - targets:
            - alertmanager:9093
```

## 🔧 Classe de Configuração Python

### `src/infrastructure/config/observability_config.py`

```python
from typing import Dict, Any, Optional
import yaml
import os
from pydantic import BaseSettings, Field
from pathlib import Path

class ObservabilityConfig(BaseSettings):
    """Configuração de observabilidade baseada em arquivos YAML."""

    # Configurações do serviço
    service_name: str = Field(default="skyhal-api", env="SERVICE_NAME")
    service_version: str = Field(default="0.1.0", env="SERVICE_VERSION")
    environment: str = Field(default="development", env="ENVIRONMENT")

    # Configurações de logging
    log_level: str = Field(default="INFO", env="LOG_LEVEL")

    # Configurações de tracing
    tracing_sampling_ratio: float = Field(default=0.1, env="TRACING_SAMPLING_RATIO")

    # Configurações de exportadores
    prometheus_port: int = Field(default=8000, env="PROMETHEUS_PORT")
    jaeger_endpoint: str = Field(
        default="http://localhost:14268/api/traces",
        env="JAEGER_ENDPOINT"
    )

    def __init__(self, config_path: Optional[str] = None):
        super().__init__()
        self._config_data = self._load_config(config_path)

    def _load_config(self, config_path: Optional[str] = None) -> Dict[str, Any]:
        """Carrega configuração dos arquivos YAML."""
        if not config_path:
            config_path = Path(__file__).parent.parent.parent.parent / "config"

        config_path = Path(config_path)

        # Carrega configuração principal
        main_config_file = config_path / "observability.yaml"
        with open(main_config_file, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)

        # Carrega configuração específica do ambiente
        env_config_file = config_path / "environments" / f"{self.environment}.yaml"
        if env_config_file.exists():
            with open(env_config_file, 'r', encoding='utf-8') as f:
                env_config = yaml.safe_load(f)
                self._merge_configs(config, env_config)

        return config

    def _merge_configs(self, base: Dict[str, Any], override: Dict[str, Any]) -> None:
        """Merge configurações, priorizando override."""
        for key, value in override.items():
            if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                self._merge_configs(base[key], value)
            else:
                base[key] = value

    def get_config(self, path: str, default: Any = None) -> Any:
        """Obtém configuração usando notação de pontos."""
        keys = path.split('.')
        value = self._config_data

        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return default

        return value

    @property
    def is_metrics_enabled(self) -> bool:
        """Verifica se métricas estão habilitadas."""
        return self.get_config('observability.metrics.enabled', True)

    @property
    def is_tracing_enabled(self) -> bool:
        """Verifica se tracing está habilitado."""
        return self.get_config('observability.tracing.enabled', True)

    @property
    def sensitive_fields(self) -> list:
        """Retorna lista de campos sensíveis."""
        return self.get_config('observability.logging.sensitive_fields', [])
```

## ✅ Checklist de Implementação

- [ ] Criar arquivo de configuração principal `observability.yaml`
- [ ] Criar configurações por ambiente (dev, staging, prod)
- [ ] Criar configurações específicas de exportadores
- [ ] Implementar classe Python para carregamento de configurações
- [ ] Configurar variáveis de ambiente para diferentes ambientes
- [ ] Validar configurações com diferentes cenários
- [ ] Documentar todas as opções de configuração
- [ ] Implementar testes de carregamento de configuração
- [ ] Configurar validação de schema das configurações

## 🔗 Dependências de Outros Artefatos

- **observability-infrastructure.md** - Usa configurações definidas aqui
- **observability-middleware.md** - Aplica configurações de instrumentação
- **grafana-setup.md** - Usa configurações de exportadores

## 📝 Notas Técnicas

- Usar variáveis de ambiente para configurações sensíveis
- Configurações podem ser sobrescritas por ambiente
- Validação de schema garante integridade das configurações
- Suporte a hot-reload para desenvolvimento
- Configurações são centralizadas mas modulares por componente
