# Plano de Implementação: Geração Automática de Código via LLM

## Objetivo

Implementar de forma completa, segura e testável a feature de geração automática de código utilizando LLMs (Large Language Models) no projeto SkyHAL, seguindo Clean Architecture, padrões de segurança e observabilidade.

---

## 1. Infraestrutura e Integração

- [x] Criar módulo Python para integração com provedores LLM (OpenAI, Azure OpenAI, etc.)
  - [x] Implementar client HTTP seguro (requests/httpx)
  - [x] Suporte completo a configuração dinâmica (model, temperatura, etc.) via settings/config central
  - [x] Gerenciamento robusto de quotas, retries e tratamento de erros (aprimorado)
- [x] Orquestrador de geração de código
  - [x] Receber prompt, acionar LLM, validar resposta
  - [x] Dividir prompts grandes (chunking) se necessário
  - [x] Validar sintaxe e semântica do código gerado
- [x] Sanitização e validação de segurança do código gerado
  - [x] Bloquear execuções perigosas/imports proibidos
  - [x] Validar entrada/saída via Pydantic
  - [x] Logging estruturado de todas as interações
- [x] Inserir teste de geração de código via LLM no notebook de testes existente (`notebooks/testes_skyhal_api.ipynb`)

## 2. API/Interface

- [x] Criar endpoint REST (FastAPI) para acionar geração de código
  - [x] Receber prompt, parâmetros e autenticação
  - [x] Retornar status, logs e resultado
- [x] Implementar autenticação, autorização e rate limiting

## 3. Observabilidade

- [x] Instrumentar métricas (OpenTelemetry, Prometheus)
- [x] Logging estruturado (structlog)
- [x] Tracing de requisições e respostas

## 4. Testes

- [x] Testes unitários para client LLM (mock)
- [x] Testes de integração para orquestrador e API
- [x] Testes de segurança (injeção, código malicioso)
- [x] Cobertura mínima 80%

## 5. Documentação

- [x] Guia de uso para desenvolvedores (README, exemplos)
- [x] Documentação de arquitetura (fluxo, dependências)
- [x] Exemplos de prompts
- [x] Exemplos de respostas

## 6. DevOps/Configuração

- [x] Gerenciar segredos de API (env)
- [x] Variáveis de ambiente para endpoint, modelo, limites

## 7. Checklist de Conformidade

- [x] Clean Architecture e SOLID
- [x] Segurança e validação rigorosa
- [x] Testabilidade e cobertura
- [x] Observabilidade e logging
- [x] Documentação atualizada

---

## Entregáveis

- Módulo de integração LLM (src/infrastructure/llm_client.py)
- Orquestrador de geração (src/application/llm_code_orchestrator.py)
- Endpoint REST (src/presentation/api/llm_codegen.py)
- Testes (tests/unit/test_llm_client.py, tests/integration/test_llm_codegen.py)
- Documentação (docs/llm-codegen.md)
- Configuração segura de segredos

---

## Observações

- Seguir rigorosamente as instruções do projeto e este plano.
- Não avançar para etapas seguintes sem validação do responsável.
- Registrar débitos técnicos e bugs encontrados.
- Atualizar documentação e Memory Bank ao final de cada etapa.
