# 🚀 Observabilidade SkyHAL – Guia Rápido

## 1. Subindo a Stack de Observabilidade

> Pré-requisito: Docker em ambiente WSL (Windows) ou Linux nativo

```powershell
cd infra/grafana
pwsh ./scripts/setup.ps1
```

Acesse:

- Grafana: <http://localhost:3000> (admin/admin123)
- Prometheus: <http://localhost:9090>
- Jaeger: <http://localhost:16686>
- Loki: <http://localhost:3100>

## 2. Validando Instrumentação

- Gere tráfego: `curl http://localhost:8000/health` e `curl http://localhost:8000/metrics`
- Veja logs: `docker-compose logs skyhal-api`
- Veja traces: acesse Jaeger e busque por `skyhal-api`

## 3. Exemplos de Instrumentação

- [Guia para Desenvolvedores](./usage/developers.md)
- [Exemplos de Código](./examples/code-instrumentation.md)

## 4. Troubleshooting

- [Guia de Troubleshooting](./usage/troubleshooting.md)

---

Consulte o [README de Observabilidade](./README.md) para detalhes avançados.
