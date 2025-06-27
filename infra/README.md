# 🏗️ Infraestrutura SkyHAL

## 📋 Visão Geral

Este diretório contém toda a infraestrutura como código do projeto SkyHAL, incluindo a stack completa de observabilidade.

## 📁 Estrutura

```text
infra/
├── README.md                    # Este arquivo
└── grafana/                     # Stack de Observabilidade ✅ COMPLETA
    ├── docker-compose.yml       # Orquestração completa
    ├── config/
    │   └── grafana.ini          # Configuração do Grafana
    ├── provisioning/            # Provisionamento automático
    │   ├── datasources/         # Datasources (Prometheus, Jaeger, Loki)
    │   └── dashboards/          # Dashboards automáticos
    │       └── skyhal/          # API Overview + RED Metrics
    ├── prometheus/              # Configuração Prometheus
    ├── loki/                    # Configuração Loki
    ├── promtail/                # Configuração Promtail
    ├── otel/                    # OpenTelemetry Collector
    └── scripts/                 # Scripts de setup (Windows + Linux)
```

## 🚀 Quick Start

### ⚠️ Pré-requisito Importante

**Docker só funciona em ambiente WSL.** Certifique-se de estar executando em WSL antes de iniciar a stack.

### Iniciar Stack Completa

**Windows (WSL):**
```powershell
cd infra/grafana
.\scripts\setup.ps1
```

**Linux/macOS:**
```bash
cd infra/grafana
chmod +x scripts/setup.sh
./scripts/setup.sh
```

## 🌐 Serviços Disponíveis

| Serviço | URL | Descrição |
|---------|-----|-----------|
| **Grafana** | http://localhost:3000 | Dashboards (admin/admin123) |
| **Prometheus** | http://localhost:9090 | Métricas |
| **Jaeger** | http://localhost:16686 | Traces |
| **Loki** | http://localhost:3100 | Logs |

## 📚 Documentação

- [Documentação Completa](../docs/observabilidade/README.md)
- [Guia para Desenvolvedores](../docs/observabilidade/usage/developers.md)

**⚡ Stack implementada conforme Issue #10 - Todas as funcionalidades operacionais!**
