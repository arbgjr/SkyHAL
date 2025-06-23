---
applyTo: "**"
---
# 🛰️ Observabilidade - Padrões e Boas Práticas

## Objetivo
Garantir rastreabilidade ponta a ponta, diagnóstico rápido e confiável, e padronização de sinais (logs, métricas, traces) em todos os microserviços .NET do projeto.

## Ferramentas Obrigatórias
- **Métricas:** OpenTelemetry + Prometheus
- **Tracing:** OpenTelemetry + Jaeger
- **Logs:** Serilog (JSON) + Loki
- **Visualização:** Grafana

## Padrões de Nomenclatura
- **Métricas:**
  - `servico_operacao_requests_total` (ex: `mensagem_entrada_requests_total`)
  - `servico_operacao_errors_total`
  - `servico_operacao_duration_seconds`
- **Spans/Traces:**
  - Nome: Serviço + Operação (ex: `MSG.Mensagem.EntradaIntegracao.ProcessarMensagem`)
  - Atributos obrigatórios: `mensagem_id`, `usuario`, `status`

## Instrumentação Obrigatória
- Todos endpoints HTTP (APIs)
- Chamadas a bancos de dados e mensageria (Kafka, MQ)
- Operações críticas de negócio

## Logging Estruturado
- Sempre em JSON
- Incluir `trace_id` e `span_id` em todos os logs
- Nunca logar dados sensíveis

## Correlacionamento
- O `trace_id` deve estar presente em logs, métricas e traces para rastreabilidade ponta a ponta

## Exemplos
- Métrica: `mensagem_entrada_requests_total{status="success"}`
- Log: `{ "level": "Information", "mensagemId": "123", "trace_id": "..." }`
- Span: `MSG.Mensagem.EntradaIntegracao.ProcessarMensagem`

## Referências
- `docs/observabilidade/Padrões_de_Observabilidade.md`
- Exemplos práticos em `docs/observabilidade/`

---

## Checklist de Observabilidade
- [ ] Instrumentação RED em todos endpoints críticos
- [ ] Logging estruturado com trace_id
- [ ] Métricas customizadas para operações relevantes
- [ ] Correlacionamento entre logs, métricas e traces
- [ ] Não expor dados sensíveis em logs
