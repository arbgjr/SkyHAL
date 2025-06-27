# 🐳 DevContainer: Configuração e Solução de Problemas

## 📋 Requisitos

Para usar o DevContainer do SkyHAL, você precisa dos seguintes itens:

- **Windows**
  - [WSL2](https://docs.microsoft.com/pt-br/windows/wsl/install) **instalado e configurado**
  - [Docker Desktop](https://www.docker.com/products/docker-desktop/) configurado para usar WSL2
  - [Visual Studio Code](https://code.visualstudio.com/download)
  - Extensão [Remote - Containers](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)

- **Linux**
  - Docker [instalado nativamente](https://docs.docker.com/engine/install/)
  - [Visual Studio Code](https://code.visualstudio.com/download)
  - Extensão [Remote - Containers](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)

> ⚠️ **IMPORTANTE**: No Windows, o DevContainer **somente funciona através do WSL2**, não diretamente no Windows.

## 🚀 Passo a Passo

### Windows com WSL2

1. **Configure o WSL2**

   ```powershell
   # No PowerShell com privilégios administrativos
   wsl --install
   # Reinicie o computador após a instalação
   ```

2. **Instale o Docker Desktop**
   - [Baixe o Docker Desktop](https://www.docker.com/products/docker-desktop/)
   - Durante a instalação, garanta que a opção "Use WSL 2 instead of Hyper-V" esteja marcada
   - Após instalação, verifique nas configurações do Docker Desktop se a integração com WSL2 está habilitada

3. **Configure seu projeto no WSL**

   ```bash
   # No terminal WSL
   cd ~
   git clone https://github.com/arbgjr/SkyHAL.git
   cd SkyHAL
   code .
   ```

4. **Abra no DevContainer**
   - Quando o VS Code abrir, você verá uma notificação sugerindo reabrir o projeto no container
   - Clique em "Reopen in Container"
   - Alternativamente, use Ctrl+Shift+P e digite "Remote-Containers: Reopen in Container"

### Linux Nativo

1. **Instale o Docker**

   ```bash
   # Ubuntu/Debian
   sudo apt update
   sudo apt install docker.io
   sudo systemctl enable --now docker
   sudo usermod -aG docker $USER
   # Logout e login novamente para aplicar as mudanças de grupo
   ```

2. **Clone o repositório**

   ```bash
   git clone https://github.com/arbgjr/SkyHAL.git
   cd SkyHAL
   code .
   ```

3. **Abra no DevContainer**
   - Quando o VS Code abrir, você verá uma notificação sugerindo reabrir o projeto no container
   - Clique em "Reopen in Container"
   - Alternativamente, use Ctrl+Shift+P e digite "Remote-Containers: Reopen in Container"

## 🔍 Solucionando Problemas Comuns

### Docker não está disponível

**Problema**: Mensagem "Docker is not installed or not running"

**Solução**:

- **Windows**: Verifique se o Docker Desktop está em execução
- **Linux**: Execute `sudo systemctl status docker` para verificar o status do serviço
- Em ambos os casos, confirme com `docker info` no terminal

### Erro de montagem dos volumes

**Problema**: Erros relacionados a permissão ou montagem de volumes

**Solução**:

1. Verifique se o diretório `.ssh` existe no seu usuário

   ```bash
   # Windows/WSL
   ls -la ~/ | grep .ssh

   # Windows (PowerShell)
   Test-Path ~\.ssh
   ```

2. Se necessário, crie o diretório:

   ```bash
   mkdir -p ~/.ssh
   chmod 700 ~/.ssh
   ```

### Erros ao construir o container

**Problema**: O DevContainer falha durante a construção

**Solução**:

1. Limpe os contêineres e imagens antigos do Docker:

   ```bash
   docker system prune -a
   ```

2. Aumente os recursos atribuídos ao Docker:
   - **Windows**: Nas configurações do Docker Desktop, aumente a memória e CPUs
   - **Linux**: Verifique os limites do sistema com `ulimit -a`

### WSL consumindo muito espaço

**Problema**: O WSL está consumindo muito espaço no seu disco C:

**Solução**:

1. Limpe arquivos temporários no WSL:

   ```bash
   sudo apt clean
   docker system prune -a
   ```

2. Considere [mover a instalação do WSL para outro disco](https://docs.microsoft.com/pt-br/windows/wsl/disk-space)

## 🔄 Reconstruindo o Container

Se você precisar reconstruir o container completamente:

1. No VS Code, pressione Ctrl+Shift+P
2. Digite e selecione "Remote-Containers: Rebuild Container"
3. Aguarde a reconstrução completa

## � Ferramenta de Diagnóstico

O projeto inclui uma ferramenta de diagnóstico para ajudar a identificar e resolver problemas com o DevContainer:

```powershell
# No PowerShell ou terminal WSL
pwsh .scripts/diagnose-devcontainer.ps1
```

Esta ferramenta verifica:

- Status do WSL (apenas no Windows)
- Instalação e execução do Docker
- Instalação do VS Code e extensões necessárias
- Configurações do DevContainer
- Diretório SSH
- Fornece recomendações específicas para seu ambiente

Execute esta ferramenta sempre que encontrar problemas com o DevContainer.

## �📚 Referências

- [Documentação oficial do Dev Containers](https://code.visualstudio.com/docs/remote/containers)
- [Documentação do Docker](https://docs.docker.com/)
- [Documentação do WSL](https://docs.microsoft.com/pt-br/windows/wsl/)
- [Configuração do Docker com WSL2](https://docs.docker.com/desktop/windows/wsl/)
