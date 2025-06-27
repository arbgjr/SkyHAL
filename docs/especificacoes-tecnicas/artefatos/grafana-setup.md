# Especificação Técnica: Setup do Grafana

## 📁 Artefato

**Caminho:** `infra/grafana/`

## 🎯 Objetivo

Configurar Grafana com dashboards, alertas e datasources para visualização completa da stack de observabilidade, incluindo métricas, logs e traces.

## 📚 Instruções Relacionadas

- **observabilidade.instructions.md** - Padrões de visualização e alertas
- **api-security.instructions.md** - Configurações seguras do Grafana

## 🎨 Prompts Relacionados

- **observabilidade.prompt.md** - Configuração de visualização
- **project-planning.prompt.md** - Estruturação de infraestrutura

## 🎯 Chat Mode Recomendado

- **arquiteto.chatmode.md** - Para definição de arquitetura de monitoramento

## 🏗️ Estrutura de Arquivos

```text
infra/grafana/
├── docker-compose.yml              # Orquestração da stack
├── provisioning/
│   ├── datasources/
│   │   ├── prometheus.yml         # Configuração Prometheus
│   │   ├── jaeger.yml             # Configuração Jaeger
│   │   └── loki.yml               # Configuração Loki
│   ├── dashboards/
│   │   ├── dashboard.yml          # Provisionamento de dashboards
│   │   └── skyhal/
│   │       ├── api-overview.json  # Dashboard geral da API
│   │       ├── red-metrics.json   # Dashboard métricas RED
│   │       ├── traces.json        # Dashboard de traces
│   │       └── system.json        # Dashboard do sistema
│   └── alerting/
│       ├── alerts.yml             # Regras de alerta
│       └── notification.yml       # Canais de notificação
├── config/
│   ├── grafana.ini               # Configuração principal
│   └── ldap.toml                 # Configuração LDAP (se necessário)
└── scripts/
    ├── setup.sh                 # Script de configuração inicial
    └── backup-dashboards.sh     # Script de backup
```

## 🛠️ Implementação da Infraestrutura

### 1. Docker Compose (`infra/grafana/docker-compose.yml`)

```yaml
version: '3.8'

services:
  # Prometheus - Métricas
  prometheus:
    image: prom/prometheus:v2.45.0
    container_name: skyhal-prometheus
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus/prometheus.yml:/etc/prometheus/prometheus.yml
      - ./prometheus/rules:/etc/prometheus/rules
      - prometheus_data:/prometheus
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.path=/prometheus'
      - '--web.console.libraries=/etc/prometheus/console_libraries'
      - '--web.console.templates=/etc/prometheus/consoles'
      - '--storage.tsdb.retention.time=30d'
      - '--web.enable-lifecycle'
    networks:
      - observability

  # Jaeger - Traces
  jaeger:
    image: jaegertracing/all-in-one:1.49
    container_name: skyhal-jaeger
    ports:
      - "16686:16686"  # UI
      - "14268:14268"  # HTTP collector
      - "14250:14250"  # gRPC collector
    environment:
      - COLLECTOR_OTLP_ENABLED=true
      - SPAN_STORAGE_TYPE=memory
    networks:
      - observability

  # Loki - Logs
  loki:
    image: grafana/loki:2.8.0
    container_name: skyhal-loki
    ports:
      - "3100:3100"
    volumes:
      - ./loki/loki-config.yml:/etc/loki/local-config.yaml
      - loki_data:/loki
    command: -config.file=/etc/loki/local-config.yaml
    networks:
      - observability

  # Promtail - Coletor de logs
  promtail:
    image: grafana/promtail:2.8.0
    container_name: skyhal-promtail
    volumes:
      - ./promtail/promtail-config.yml:/etc/promtail/config.yml
      - /var/log:/var/log:ro
      - /var/lib/docker/containers:/var/lib/docker/containers:ro
    command: -config.file=/etc/promtail/config.yml
    networks:
      - observability

  # Grafana - Visualização
  grafana:
    image: grafana/grafana:10.0.0
    container_name: skyhal-grafana
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_USER=admin
      - GF_SECURITY_ADMIN_PASSWORD=${GRAFANA_ADMIN_PASSWORD:-admin}
      - GF_USERS_ALLOW_SIGN_UP=false
      - GF_INSTALL_PLUGINS=grafana-piechart-panel
    volumes:
      - ./grafana/config/grafana.ini:/etc/grafana/grafana.ini
      - ./grafana/provisioning:/etc/grafana/provisioning
      - grafana_data:/var/lib/grafana
    networks:
      - observability
    depends_on:
      - prometheus
      - jaeger
      - loki

volumes:
  prometheus_data:
  loki_data:
  grafana_data:

networks:
  observability:
    driver: bridge
```

### 2. Configuração Prometheus (`infra/grafana/prometheus/prometheus.yml`)

```yaml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

rule_files:
  - "rules/*.yml"

alerting:
  alertmanagers:
    - static_configs:
        - targets:
          # - alertmanager:9093

scrape_configs:
  # SkyHAL API
  - job_name: 'skyhal-api'
    static_configs:
      - targets: ['host.docker.internal:8000']
    metrics_path: '/metrics'
    scrape_interval: 5s

    metric_relabel_configs:
      # Manter apenas métricas relevantes
      - source_labels: [__name__]
        regex: 'skyhal_.*|app_.*|http_.*|process_.*|python_.*'
        action: keep

  # Prometheus self-monitoring
  - job_name: 'prometheus'
    static_configs:
      - targets: ['localhost:9090']

  # Node Exporter (se disponível)
  - job_name: 'node'
    static_configs:
      - targets: ['node-exporter:9100']
    scrape_interval: 15s
```

### 3. Datasources Grafana (`infra/grafana/provisioning/datasources/`)

#### Prometheus (`prometheus.yml`)
```yaml
apiVersion: 1

datasources:
  - name: Prometheus
    type: prometheus
    access: proxy
    url: http://prometheus:9090
    isDefault: true
    editable: true
    jsonData:
      httpMethod: POST
      queryTimeout: 60s
      timeInterval: 15s
```

#### Jaeger (`jaeger.yml`)
```yaml
apiVersion: 1

datasources:
  - name: Jaeger
    type: jaeger
    access: proxy
    url: http://jaeger:16686
    editable: true
    jsonData:
      tracesToLogsV2:
        datasourceUid: 'loki'
        spanStartTimeShift: '-1h'
        spanEndTimeShift: '1h'
        tags: ['trace_id']
```

#### Loki (`loki.yml`)
```yaml
apiVersion: 1

datasources:
  - name: Loki
    type: loki
    access: proxy
    url: http://loki:3100
    editable: true
    jsonData:
      derivedFields:
        - datasourceUid: jaeger
          matcherRegex: "trace_id=(\\w+)"
          name: TraceID
          url: "$${__value.raw}"
          urlDisplayLabel: "View Trace"
```

### 4. Dashboard Principal (`infra/grafana/provisioning/dashboards/skyhal/api-overview.json`)

```json
{
  "dashboard": {
    "id": null,
    "title": "SkyHAL API - Overview",
    "tags": ["skyhal", "api", "overview"],
    "timezone": "browser",
    "panels": [
      {
        "id": 1,
        "title": "Request Rate",
        "type": "stat",
        "targets": [
          {
            "expr": "sum(rate(app_http_requests_total[5m]))",
            "legendFormat": "Requests/sec"
          }
        ],
        "fieldConfig": {
          "defaults": {
            "color": {"mode": "palette-classic"},
            "unit": "reqps"
          }
        },
        "gridPos": {"h": 8, "w": 6, "x": 0, "y": 0}
      },
      {
        "id": 2,
        "title": "Error Rate",
        "type": "stat",
        "targets": [
          {
            "expr": "sum(rate(app_http_requests_total{status=\"error\"}[5m])) / sum(rate(app_http_requests_total[5m])) * 100",
            "legendFormat": "Error %"
          }
        ],
        "fieldConfig": {
          "defaults": {
            "color": {"mode": "palette-classic"},
            "unit": "percent",
            "thresholds": {
              "steps": [
                {"color": "green", "value": null},
                {"color": "yellow", "value": 1},
                {"color": "red", "value": 5}
              ]
            }
          }
        },
        "gridPos": {"h": 8, "w": 6, "x": 6, "y": 0}
      },
      {
        "id": 3,
        "title": "Response Time (95th percentile)",
        "type": "stat",
        "targets": [
          {
            "expr": "histogram_quantile(0.95, sum(rate(app_http_request_duration_seconds_bucket[5m])) by (le))",
            "legendFormat": "P95 Latency"
          }
        ],
        "fieldConfig": {
          "defaults": {
            "color": {"mode": "palette-classic"},
            "unit": "s",
            "thresholds": {
              "steps": [
                {"color": "green", "value": null},
                {"color": "yellow", "value": 0.1},
                {"color": "red", "value": 0.5}
              ]
            }
          }
        },
        "gridPos": {"h": 8, "w": 6, "x": 12, "y": 0}
      },
      {
        "id": 4,
        "title": "Active Requests",
        "type": "stat",
        "targets": [
          {
            "expr": "sum(app_http_requests_total) - sum(app_http_requests_total offset 1m)",
            "legendFormat": "Active"
          }
        ],
        "gridPos": {"h": 8, "w": 6, "x": 18, "y": 0}
      },
      {
        "id": 5,
        "title": "Request Rate by Endpoint",
        "type": "graph",
        "targets": [
          {
            "expr": "sum(rate(app_http_requests_total[5m])) by (path)",
            "legendFormat": "{{path}}"
          }
        ],
        "gridPos": {"h": 8, "w": 12, "x": 0, "y": 8}
      },
      {
        "id": 6,
        "title": "Response Time Distribution",
        "type": "graph",
        "targets": [
          {
            "expr": "histogram_quantile(0.50, sum(rate(app_http_request_duration_seconds_bucket[5m])) by (le))",
            "legendFormat": "P50"
          },
          {
            "expr": "histogram_quantile(0.95, sum(rate(app_http_request_duration_seconds_bucket[5m])) by (le))",
            "legendFormat": "P95"
          },
          {
            "expr": "histogram_quantile(0.99, sum(rate(app_http_request_duration_seconds_bucket[5m])) by (le))",
            "legendFormat": "P99"
          }
        ],
        "gridPos": {"h": 8, "w": 12, "x": 12, "y": 8}
      }
    ],
    "time": {"from": "now-1h", "to": "now"},
    "refresh": "5s"
  }
}
```

### 5. Regras de Alerta (`infra/grafana/provisioning/alerting/alerts.yml`)

```yaml
groups:
  - name: skyhal-api-alerts
    rules:
      - alert: HighErrorRate
        expr: sum(rate(app_http_requests_total{status="error"}[5m])) / sum(rate(app_http_requests_total[5m])) > 0.05
        for: 2m
        labels:
          severity: warning
          service: skyhal-api
        annotations:
          summary: "High error rate detected"
          description: "Error rate is {{ $value | humanizePercentage }} for the last 5 minutes"

      - alert: HighLatency
        expr: histogram_quantile(0.95, sum(rate(app_http_request_duration_seconds_bucket[5m])) by (le)) > 0.5
        for: 2m
        labels:
          severity: warning
          service: skyhal-api
        annotations:
          summary: "High latency detected"
          description: "95th percentile latency is {{ $value }}s for the last 5 minutes"

      - alert: ServiceDown
        expr: up{job="skyhal-api"} == 0
        for: 1m
        labels:
          severity: critical
          service: skyhal-api
        annotations:
          summary: "SkyHAL API is down"
          description: "SkyHAL API has been down for more than 1 minute"

      - alert: LowAvailability
        expr: (sum(rate(app_http_requests_total{status!="error"}[5m])) / sum(rate(app_http_requests_total[5m]))) < 0.99
        for: 5m
        labels:
          severity: critical
          service: skyhal-api
        annotations:
          summary: "Low availability detected"
          description: "Availability is {{ $value | humanizePercentage }} for the last 5 minutes"
```

### 6. Scripts de Setup (`infra/grafana/scripts/setup.sh`)

```bash
#!/bin/bash
set -e

echo "🚀 Configurando stack de observabilidade SkyHAL..."

# Verifica se Docker está rodando
if ! docker info >/dev/null 2>&1; then
    echo "❌ Docker não está rodando. Por favor, inicie o Docker primeiro."
    exit 1
fi

# Cria diretórios necessários
echo "📁 Criando diretórios..."
mkdir -p prometheus/rules
mkdir -p loki/data
mkdir -p grafana/data

# Define permissões
echo "🔐 Configurando permissões..."
sudo chown -R 472:472 grafana/data  # UID/GID do Grafana
sudo chown -R 10001:10001 loki/data  # UID/GID do Loki

# Cria arquivo .env se não existir
if [ ! -f .env ]; then
    echo "📝 Criando arquivo .env..."
    cat > .env << EOF
GRAFANA_ADMIN_PASSWORD=admin123
ENVIRONMENT=development
EOF
fi

# Inicia serviços
echo "🏃 Iniciando serviços..."
docker-compose up -d

# Aguarda serviços iniciarem
echo "⏳ Aguardando serviços iniciarem..."
sleep 30

# Verifica se serviços estão rodando
echo "🔍 Verificando status dos serviços..."
docker-compose ps

echo "✅ Setup concluído!"
echo ""
echo "🌐 URLs dos serviços:"
echo "  - Grafana: http://localhost:3000 (admin/admin123)"
echo "  - Prometheus: http://localhost:9090"
echo "  - Jaeger: http://localhost:16686"
echo "  - Loki: http://localhost:3100"
echo ""
echo "📊 Para visualizar dashboards:"
echo "  1. Acesse Grafana em http://localhost:3000"
echo "  2. Faça login com admin/admin123"
echo "  3. Navegue para Dashboards > SkyHAL"
```

## 📋 Recursos Implementados

### Dashboards Disponíveis

1. **API Overview** - Visão geral da API com métricas RED
2. **RED Metrics** - Dashboard específico para Rate, Errors, Duration
3. **Traces** - Visualização de traces distribuídos
4. **System** - Métricas de sistema e infraestrutura

### Alertas Configurados

1. **High Error Rate** - Taxa de erro > 5%
2. **High Latency** - P95 > 500ms
3. **Service Down** - Serviço indisponível
4. **Low Availability** - Disponibilidade < 99%

### Datasources Integrados

- **Prometheus** - Para métricas
- **Jaeger** - Para traces
- **Loki** - Para logs
- **Correlação** - Links automáticos entre traces e logs

## ✅ Checklist de Implementação

- [ ] Criar docker-compose.yml com stack completa
- [ ] Configurar datasources do Grafana
- [ ] Implementar dashboards básicos
- [ ] Configurar regras de alerta
- [ ] Criar scripts de setup e manutenção
- [ ] Configurar backup de dashboards
- [ ] Documentar URLs e credenciais
- [ ] Testar alertas e notificações
- [ ] Configurar rotação de logs e retenção
- [ ] Validar correlação entre datasources

## 🔗 Dependências de Outros Artefatos

- **observability-infrastructure.md** - Exporta métricas e traces
- **observability-middleware.md** - Gera dados para visualização
- **observability-config.md** - Configura exportadores

## 📝 Notas Técnicas

- Stack completa roda em containers Docker
- Grafana provisioning automático de dashboards
- Alertas podem ser integrados com Slack/email
- Backup automático de configurações
- Suporte a ambiente de desenvolvimento e produção
