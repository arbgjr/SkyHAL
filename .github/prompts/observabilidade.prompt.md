---
mode: "agent"
---
# Prompt de Observabilidade para GitHub Copilot

## Contexto
Este prompt orienta o Copilot a atuar como engenheiro sênior de software especializado em observabilidade para projetos .NET (Clean Architecture, microserviços, Kafka, SQL Server, Redis, Vault).

## Instruções para o Copilot

1. **Ferramentas recomendadas:**
   - Métricas: OpenTelemetry + Prometheus
   - Tracing: OpenTelemetry + Jaeger
   - Logs: Serilog (JSON) + Loki
   - Visualização: Grafana

2. **Dependências NuGet sugeridas:**
   - OpenTelemetry.Extensions.Hosting
   - OpenTelemetry.Instrumentation.AspNetCore
   - OpenTelemetry.Instrumentation.Http
   - OpenTelemetry.Exporter.Prometheus.AspNetCore
   - OpenTelemetry.Exporter.Jaeger
   - Serilog.Sinks.Grafana.Loki

3. **Exemplos obrigatórios:**
   - Configuração de OpenTelemetry para métricas, traces e logs
   - Instrumentação RED (Rate, Errors, Duration) em endpoints
   - Logging estruturado em JSON com trace_id

4. **Padronização:**
   - Nomenclatura de métricas: `servico_operacao_requests_total`, `servico_operacao_errors_total`, `servico_operacao_duration_seconds`
   - Spans: nome do serviço + operação, incluir atributos `mensagem_id`, `usuario`, `status`
   - Instrumentar: todos endpoints HTTP, chamadas a banco/mensageria, operações críticas
   - Logs sempre em JSON, incluir `trace_id` e `span_id`, nunca logar dados sensíveis
   - Correlacionar logs, métricas e traces via `trace_id`

5. **Guia de referência:**
   - Consulte sempre `docs/observabilidade/Padrões_de_Observabilidade.md` para exemplos e padrões atualizados.

---

## Exemplo de uso
- "Implemente instrumentação RED neste endpoint seguindo os padrões do projeto."
- "Configure logging estruturado com Serilog e Loki, incluindo trace_id."
- "Adicione métricas customizadas usando OpenTelemetry."
