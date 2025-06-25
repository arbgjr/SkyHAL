# Débitos Técnicos - DevContainer

## TD002 - DevContainer Incompatível com Configuração de Montagem SSH no Windows/WSL2

- **Data Identificado**: 2025-06-24
- **Identificado Por**: @arbgjr
- **Componente(s) Afetado(s)**: DevContainer, Configurações de Desenvolvimento
- **Descrição do Débito**: O DevContainer tinha problemas de configuração que impediam o funcionamento correto em ambientes Windows/WSL2, principalmente relacionados à montagem de volumes SSH e configurações de permissão. A implementação não considerava as especificidades do Windows.
- **Motivo da Decisão Atual**: Precisava de uma solução imediata para permitir o desenvolvimento em todos os ambientes.
- **Impacto Potencial/Riscos**: Desenvolvedores usando Windows não conseguiam utilizar o DevContainer, fragmentando o ambiente de desenvolvimento e potencialmente causando problemas de "funciona na minha máquina".
- **Sugestão de Solução Ideal**: Implementar e testar uma configuração mais robusta usando Dockerfile personalizado em vez de imagem pré-construída, com melhor tratamento de permissões e compatibilidade cross-platform.
- **Prioridade Estimada**: Alta
- **Status**: Resolvido
- **Issue/Task Relacionada**: N/A
- **Data de Resolução**: 2025-06-24
- **Notas Adicionais**: A solução implementada resolve o problema, mas deve-se considerar em versões futuras a criação de um Dockerfile personalizado para controle total sobre o ambiente.

---
