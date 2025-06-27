FROM mcr.microsoft.com/devcontainers/dotnet:8.0

RUN apt-get update && \
    apt-get install -y python3 python3-pip python3-venv pipx && \
    pipx install poetry && \
    rm -rf /var/lib/apt/lists/*

RUN useradd -m -s /bin/bash vscode || true
USER vscode
ENV PATH="/home/vscode/.local/bin:$PATH"
CMD ["sleep", "infinity"]
