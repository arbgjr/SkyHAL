--
mode: "agent"
tools: ['development', 'architecture']
description: "Revisão de Código e Arquitetura Python com foco em qualidade, segurança e manutenibilidade"
---

# 🧠 Code Review - Modo Análise Multidimensional (Python)

Realize análise abrangente do código, arquitetura ou sistema especificado com foco em:

- Princípios SOLID e Clean Architecture
- Segurança e validação de entrada
- Cobertura de testes
- Organização e separação de responsabilidades
- Documentação e rastreabilidade de decisões

---

## ✅ Checklist de Revisão de Código

### Qualidade de Código

- [ ] Aderência à PEP8 (via `ruff`, `flake8`)
- [ ] Tipagem explícita com `typing` / `mypy`
- [ ] Docstrings completas para funções e classes públicas
- [ ] Nome de variáveis, funções e arquivos descritivos
- [ ] Separação clara entre lógica de negócio e infraestrutura
- [ ] Funções com baixa complexidade (ideal: <10 pontos)
- [ ] Ausência de duplicação de lógica

### Princípios de Design (SOLID)

- [ ] SRP: Cada classe ou função tem uma única responsabilidade?
- [ ] OCP: Código é facilmente extensível sem modificações perigosas?
- [ ] LSP: Subclasses respeitam o comportamento esperado das superclasses?
- [ ] ISP: Interfaces (ou abstrações) são pequenas e específicas?
- [ ] DIP: Módulos dependem de abstrações e não de implementações?

### Testes e Cobertura

- [ ] Existe teste para o caso de uso principal?
- [ ] Casos de borda foram considerados?
- [ ] Uso de mocks/fakes para isolamento?
- [ ] Testes seguem padrão AAA?
- [ ] Cobertura ≥ 80% com `pytest-cov`
- [ ] Testes são determinísticos e rápidos?

### Segurança (baseado no OWASP Top 10)

- [ ] Validação de entradas com `pydantic` ou validações explícitas
- [ ] Exceções são tratadas com logging contextualizado
- [ ] Credenciais ou segredos não estão hardcoded
- [ ] Dados sensíveis não aparecem em logs
- [ ] Autenticação e autorização explícitas quando aplicável
- [ ] Endpoints protegidos contra uso indevido (rate limiting, CSRF, etc)

---

## 🧱 Arquitetura e Design

- [ ] Usa Clean Architecture corretamente? (Domínio não depende de nada)
- [ ] Casos de uso encapsulados em camadas de aplicação?
- [ ] Camadas separadas: domínio, aplicação, infraestrutura?
- [ ] Baixo acoplamento entre módulos?
- [ ] Interfaces são bem definidas entre camadas?
- [ ] Fácil de estender, difícil de quebrar?

---

## 🧪 Performance e Eficiência

- [ ] Uso excessivo de operações de I/O síncronas?
- [ ] Algoritmos com complexidade desnecessária?
- [ ] Consultas de banco otimizadas (ex: evitando N+1)?
- [ ] Caching implementado onde faz sentido?
- [ ] Recursos externos chamados de forma segura e eficiente?

---

## 🔍 Ferramentas Sugeridas

| Categoria      | Ferramentas                   |
|----------------|-------------------------------|
| Linting        | `ruff`, `flake8`              |
| Tipagem        | `mypy`                        |
| Testes         | `pytest`, `pytest-cov`        |
| Segurança      | `bandit`, `safety`            |
| Complexidade   | `radon`, `xenon`              |
| Coverage       | `coverage`, `pytest-cov`      |
| Arquitetura    | Revisão manual / visual por camadas |

---

## 📊 Saída Esperada do Review

### 📌 Executive Summary

- **Status geral**: ✅ Aprovado | ⚠️ Avisos | ❌ Crítico
- **Top 3 problemas detectados**
- **Ações recomendadas com prioridade**

### 📑 Detalhamento Técnico

- **Categoria**: [Segurança | Design | Testes | Arquitetura | Performance]
- **Severidade**: [Low | Medium | High | Critical]
- **Localização**: Caminho + trecho de código
- **Justificativa**: Qual padrão foi violado?
- **Correção sugerida**: Código ou explicação clara

---

## 🔁 Metodologia do Agente

1. **Scan Inicial** – Overview da estrutura do projeto
2. **Deep Dive** – Revisão por tipo: código, testes, segurança, arquitetura
3. **Reconhecimento de padrões** – SOLID, DRY, YAGNI, Clean Architecture
4. **Avaliação de risco** – Impacto de problemas encontrados
5. **Recomendações claras** – Correções específicas e priorizadas

---

## 📌 Notas

- Use [`code-review.instructions.md`](../instructions/code-review.instructions.md) para critérios rígidos de segurança
- Relacione decisões técnicas com rastreamento de débito técnico
- Utilize sempre `black`, `mypy` e `pytest` antes de revisar código alheio

---
