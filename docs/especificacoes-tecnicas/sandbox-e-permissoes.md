# Modelo de Sandbox e Permissões – Auto-Extensão MCP

## Visão Geral

O sandbox de segurança do SkyHAL isola a execução de código gerado, limitando recursos, acessos e operações permitidas. O modelo segue princípios de menor privilégio, defesa em profundidade e auditabilidade total.

## Componentes

- **SecuritySandbox**: Classe principal de isolamento (ver `src/domain/auto_extension/security_sandbox.py`)
- **ResourceMonitor**: Monitora uso de CPU, memória, IO
- **CodeAnalyzer**: Analisa código para vulnerabilidades

## Permissões e Restrições

- APIs restritas: acesso a sistema de arquivos, rede, comandos shell bloqueados
- Endpoints de rede permitidos: apenas whitelisted
- Limites de recursos: CPU, memória, IO configuráveis
- Timeout de execução: padrão 1s, customizável
- Auditoria: todos os eventos registrados em log estruturado

## Fluxo de Execução

1. Código recebido é analisado pelo `CodeAnalyzer`
2. Se seguro, ambiente é criado (`create_environment`)
3. Execução ocorre sob monitoramento de recursos
4. Limites violados ou vulnerabilidades detectadas → execução abortada
5. Logs e métricas gerados para cada execução

## Exemplo de Configuração

```yaml
sandbox:
  cpu_percent: 80.0
  memory_mb: 500
  io_operations: 100
  timeout_ms: 1000
  allowed_endpoints:
    - "api.trusted.com"
```

## Referências

- `src/domain/auto_extension/security_sandbox.py`
- `docs/observabilidade/examples/log-correlation.md`
- `docs/observabilidade/README.md`
