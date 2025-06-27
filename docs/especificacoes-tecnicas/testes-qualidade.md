# Qualidade e Testes – Auto-Extensão MCP

## Cobertura de Testes

- Cobertura mínima exigida: **≥ 80%** (unitários e integração)
- Ferramentas: `pytest`, `pytest-cov`, `pytest-mock`
- Relatórios de cobertura gerados automaticamente em cada build

## Testes de Performance e Carga

- Testes de performance para componentes críticos (geração, validação, sandbox)
- Ferramentas sugeridas: `pytest-benchmark`, `locust`, `k6`
- Métricas monitoradas: tempo de resposta, throughput, uso de recursos

## Testes de Rollback, Limites e Falhas de Sandbox

- Casos de rollback validados via API e CLI
- Testes de limites de recursos e falhas forçadas no sandbox
- Logs e métricas validados para cada cenário

## Integração com Sistema Principal

- Testes de integração automatizados para todos os fluxos core
- Ambiente de testes dedicado com stack de observabilidade ativa

## Exemplo de Execução

```bash
# Executar todos os testes e gerar relatório de cobertura
poetry run pytest --cov=src --cov-report=term-missing
```

## Referências

- `tests/unit/` e `tests/integration/`
- `docs/observabilidade/examples/`
- `docs/observabilidade/quickstart.md`
