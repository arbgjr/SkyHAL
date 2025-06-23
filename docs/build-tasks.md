# Guia de Uso das Tasks Multiplataforma

Este documento descreve como utilizar as tasks de build, testes, lint e integração com Memory Bank no projeto SkyHAL, garantindo compatibilidade entre Windows e Linux.

## Pré-requisitos
- Scripts `.ps1` (PowerShell) para Windows e `.sh` (Bash) para Linux devem estar presentes em `.scripts/`.
- Permissões de execução para scripts `.sh` no Linux (`chmod +x`).
- PowerShell instalado no Windows.

## Tasks Disponíveis

### 1. Build (cross-platform)
- **Windows:** Executa `.scripts/build.ps1`
- **Linux:** Executa `.scripts/build.sh`

### 2. Testes (cross-platform)
- **Windows:** Executa `.scripts/test.ps1`
- **Linux:** Executa `.scripts/test.sh`

### 3. Lint (cross-platform)
- **Windows:** Executa `.scripts/lint.ps1`
- **Linux:** Executa `.scripts/lint.sh`

### 4. Memory Bank: Consultar Status
- **Windows:** Executa `.scripts/memory-bank-status.ps1`
- **Linux:** Executa `.scripts/memory-bank-status.sh`

## Como Executar

1. Abra o menu de comandos do VS Code (`Ctrl+Shift+P` > `Tasks: Run Task`).
2. Selecione a task desejada.
3. O VS Code executará automaticamente o script correto conforme o sistema operacional.

## Estrutura Recomendada de Scripts

```
.scripts/
  build.ps1
  build.sh
  test.ps1
  test.sh
  lint.ps1
  lint.sh
  memory-bank-status.ps1
  memory-bank-status.sh
```

Cada script deve:
- Retornar código de saída adequado (0 para sucesso, diferente de 0 para erro)
- Exibir logs claros e estruturados
- Validar entradas e dependências

## Observações
- Mantenha os scripts sincronizados em lógica e parâmetros.
- Consulte o Memory Bank para contexto e padrões antes de alterar tasks.
- Documente qualquer ajuste relevante neste arquivo.

---

Dúvidas ou sugestões: consulte o time de arquitetura ou abra um issue.
