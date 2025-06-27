# DevContainer Linux - SkyHAL

## Status

- DevContainer funcional para desenvolvimento em Linux e Windows/WSL2
- Inclui .NET 8, Node.js 20, Docker DinD, PowerShell, Python 3.11 com Poetry e utilitários CLI
- Documentação de uso adicionada ao README.md e documentação completa em docs/devcontainer-setup.md
- Script de diagnóstico (.scripts/diagnose-devcontainer.ps1) para resolução de problemas

## Critérios de Aceitação Atendidos

- Ambiente pronto para uso no VS Code (extensão Dev Containers)
- Instruções claras para desenvolvedores em Windows/WSL2 e Linux
- Solução para problemas de montagem de volumes SSH
- Ferramenta de diagnóstico automatizada

## Referências

- Issue: [#1](https://github.com/arbgjr/SkyHAL/issues/1)
- Planejamento: memory-bank/planejamento-mvp.md
- Tech Debt: .github/instructions/devcontainer-tech-debt.md

## Observações

- Testado em Ubuntu 22.04 LTS (WSL2) e nativamente
- Configuração aprimorada para diferentes ambientes
- Corrigido problema de montagem SSH para Windows
- Adicionado modo de compatibilidade para diferentes shells
