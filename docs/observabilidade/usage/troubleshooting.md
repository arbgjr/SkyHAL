# 🔧 Guia de Troubleshooting - Observabilidade

## 🎯 Visão Geral

Este guia ajuda a diagnosticar e resolver problemas comuns na stack de observabilidade do SkyHAL.

## 🚨 Problemas Comuns

### 1. Stack não Inicia

#### Sintomas
- `docker-compose up` falha
- Serviços não respondem nas portas esperadas
- Logs de erro na inicialização

#### Diagnóstico

```bash
# Verificar status do Docker
docker info

# Verificar portas em uso
netstat -tlnp | grep -E "(3000|9090|16686|3100|4317|4318)"

# Verificar logs dos containers
docker-compose logs
```

#### Soluções

**Porta já em uso:**
```bash
# Encontrar processo usando a porta
sudo lsof -i :3000  # Substitua pela porta problemática

# Parar processo ou mudar porta no docker-compose.yml
```

**Volumes com problemas:**
```bash
# Remover volumes corrompidos
docker-compose down -v
docker volume prune

# Recriar stack
docker-compose up -d
```

**Problemas de memória:**
```bash
# Verificar uso de memória
docker stats

# Aumentar recursos no Docker Desktop
# Ou adicionar limites no docker-compose.yml
```

### 2. Métricas não Aparecem no Prometheus

#### Sintomas
- Grafana mostra "No data"
- Prometheus não encontra targets
- Endpoint `/metrics` não responde

#### Diagnóstico

```bash
# Verificar se aplicação está expondo métricas
curl http://localhost:8000/metrics

# Verificar targets no Prometheus
# Acesse http://localhost:9090/targets

# Verificar configuração do Prometheus
docker exec skyhal-prometheus cat /etc/prometheus/prometheus.yml
```

#### Soluções

**Aplicação não expõe métricas:**
```python
# Verificar se middleware está configurado no app.py
from src.infrastructure.observability import ObservabilityMiddleware

app.add_middleware(ObservabilityMiddleware)
```

**Target não acessível:**
```yaml
# Ajustar configuração no prometheus.yml
scrape_configs:
  - job_name: 'skyhal-api'
    static_configs:
      - targets: ['host.docker.internal:8000']  # Para Docker Desktop
      # ou
      - targets: ['172.17.0.1:8000']  # Para Linux
```

**Firewall/Network:**
```bash
# Verificar conectividade
docker exec skyhal-prometheus wget -qO- http://host.docker.internal:8000/metrics

# Verificar network do Docker
docker network ls
docker network inspect skyhal-observability
```

### 3. Traces não Aparecem no Jaeger

#### Sintomas
- Jaeger UI não mostra traces
- Aplicação não envia traces
- OTEL Collector com problemas

#### Diagnóstico

```bash
# Verificar se Jaeger está recebendo dados
curl http://localhost:16686/api/services

# Verificar logs do OTEL Collector
docker-compose logs otel-collector

# Verificar configuração OpenTelemetry na aplicação
```

#### Soluções

**Configuração OpenTelemetry:**
```python
# Verificar se tracing está configurado
from src.infrastructure.observability import setup_observability

logging_provider, metrics_provider, tracing_provider = setup_observability()
```

**OTEL Collector não recebe dados:**
```yaml
# Verificar configuração em otel-collector-config.yml
receivers:
  otlp:
    protocols:
      grpc:
        endpoint: 0.0.0.0:4317
      http:
        endpoint: 0.0.0.0:4318

exporters:
  jaeger:
    endpoint: jaeger:14250
    tls:
      insecure: true
```

**Sampling muito baixo:**
```python
# Ajustar sampling rate no tracing provider
# Em src/infrastructure/observability/providers/tracing_provider.py
from opentelemetry.sdk.trace.sampling import TraceIdRatioBased

tracer_provider.add_span_processor(
    BatchSpanProcessor(
        JaegerExporter(
            endpoint="http://localhost:14268/api/traces",
        ),
        # Aumentar para desenvolvimento
        max_export_batch_size=100,
        export_timeout_millis=30000,
    )
)
```

### 4. Logs não Aparecem no Loki/Grafana

#### Sintomas
- Grafana Explore não mostra logs
- Loki retorna vazio
- Promtail não coleta logs

#### Diagnóstico

```bash
# Verificar se Loki está recebendo dados
curl http://localhost:3100/loki/api/v1/label

# Verificar logs do Promtail
docker-compose logs promtail

# Verificar se aplicação está gerando logs
```

#### Soluções

**Promtail não encontra logs:**
```yaml
# Ajustar caminhos no promtail-config.yml
scrape_configs:
  - job_name: skyhal-logs
    static_configs:
      - targets:
          - localhost
        labels:
          job: skyhal-api
          __path__: /var/log/skyhal/*.log  # Ajustar caminho
```

**Logs não estruturados:**
```python
# Verificar se logging está configurado corretamente
from src.infrastructure.observability import get_observability_providers

logging_provider, _, _ = get_observability_providers()
logger = logging_provider.get_logger("component")

# Logs devem ser JSON estruturados
logger.info("Mensagem", field1="value1", field2="value2")
```

### 5. Dashboards não Carregam

#### Sintomas
- Dashboards vazios ou com erro
- Datasources não funcionam
- Grafana não conecta com Prometheus/Jaeger

#### Diagnóstico

```bash
# Verificar datasources no Grafana
curl -u admin:admin123 http://localhost:3000/api/datasources

# Verificar logs do Grafana
docker-compose logs grafana

# Testar conexão manual
curl http://localhost:9090/api/v1/query?query=up
```

#### Soluções

**Datasources não provisionados:**
```bash
# Verificar arquivos de provisionamento
ls -la infra/grafana/provisioning/datasources/

# Reiniciar Grafana
docker-compose restart grafana
```

**URLs incorretas:**
```yaml
# Corrigir URLs nos datasources
# Em provisioning/datasources/prometheus.yml
datasources:
  - name: Prometheus
    type: prometheus
    url: http://prometheus:9090  # Nome do serviço no Docker
```

## 🔍 Debugging Avançado

### Logs Detalhados

**Aumentar verbosidade:**
```bash
# Adicionar variáveis de ambiente no docker-compose.yml
environment:
  - LOG_LEVEL=DEBUG
  - OTEL_LOG_LEVEL=DEBUG
```

**Logs específicos:**
```bash
# OTEL Collector
docker-compose logs -f otel-collector

# Prometheus
docker-compose logs -f prometheus

# Grafana
docker-compose logs -f grafana
```

### Network Debugging

```bash
# Verificar conectividade entre containers
docker exec skyhal-prometheus ping grafana
docker exec skyhal-grafana ping prometheus

# Verificar DNS resolution
docker exec skyhal-prometheus nslookup grafana
```

### Performance Issues

**Memória insuficiente:**
```yaml
# Adicionar limites no docker-compose.yml
services:
  prometheus:
    deploy:
      resources:
        limits:
          memory: 1G
        reservations:
          memory: 512M
```

**Disco cheio:**
```bash
# Verificar uso de disco dos volumes
docker system df -v

# Limpar dados antigos
docker volume rm $(docker volume ls -q --filter dangling=true)
```

## 🛠️ Ferramentas de Debug

### Scripts Úteis

**Health Check Completo:**
```bash
#!/bin/bash
# health-check.sh

services=(
    "prometheus:9090:/-/healthy"
    "grafana:3000:/api/health"
    "jaeger:16686:/"
    "loki:3100:/ready"
    "otel-collector:8888:/metrics"
)

for service in "${services[@]}"; do
    name=$(echo "$service" | cut -d: -f1)
    port=$(echo "$service" | cut -d: -f2)
    path=$(echo "$service" | cut -d: -f3)

    if curl -f -s "http://localhost:$port$path" >/dev/null; then
        echo "✅ $name healthy"
    else
        echo "❌ $name unhealthy"
    fi
done
```

**Teste de Métricas:**
```bash
# test-metrics.sh
echo "🧪 Testando métricas..."

# Gerar tráfego
for i in {1..10}; do
    curl -s http://localhost:8000/health >/dev/null
    sleep 1
done

# Verificar métricas
curl -s http://localhost:8000/metrics | grep http_requests_total
```

### Queries de Debug

**Prometheus:**
```promql
# Verificar se targets estão up
up

# Métricas da aplicação
{__name__=~"http_.*"}

# Rate de todas as métricas
rate({__name__=~".*"}[5m])
```

**Loki:**
```logql
# Todos os logs
{job="skyhal-api"}

# Logs de erro
{job="skyhal-api"} |= "ERROR"

# Logs com trace específico
{job="skyhal-api"} | json | trace_id="abc123"
```

## 📋 Checklist de Troubleshooting

### Quando algo não funciona:

1. **Verificar serviços básicos:**
   - [ ] Docker está rodando
   - [ ] Todos os containers estão up
   - [ ] Portas não estão em conflito

2. **Verificar conectividade:**
   - [ ] Aplicação responde em localhost:8000
   - [ ] Prometheus acessa aplicação
   - [ ] Grafana acessa Prometheus

3. **Verificar configurações:**
   - [ ] Arquivos de configuração estão corretos
   - [ ] Provisionamento funcionou
   - [ ] Datasources estão configurados

4. **Verificar dados:**
   - [ ] Aplicação está gerando métricas/logs/traces
   - [ ] Coletores estão recebendo dados
   - [ ] Dados chegam aos backends

5. **Verificar visualização:**
   - [ ] Dashboards carregam
   - [ ] Queries retornam dados
   - [ ] Alertas funcionam

## 🆘 Quando Pedir Ajuda

Se os passos acima não resolverem:

1. **Colete informações:**
   ```bash
   # Salvar logs
   docker-compose logs > observability-logs.txt

   # Salvar configurações
   tar -czf configs.tar.gz infra/grafana/

   # Salvar status
   docker-compose ps > services-status.txt
   ```

2. **Documente o problema:**
   - O que você estava tentando fazer
   - O que aconteceu vs. o que deveria acontecer
   - Passos para reproduzir
   - Logs relevantes

3. **Teste em ambiente limpo:**
   ```bash
   # Reset completo
   docker-compose down -v
   docker system prune -f
   docker-compose up -d
   ```
