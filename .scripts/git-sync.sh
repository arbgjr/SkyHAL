#!/bin/bash
# Script: .scripts/git-sync.sh
# Equivalente Bash para git-sync.ps1
# Requisitos: GITHUB_USERNAME, GITHUB_PAT, GIT_COMMIT_MSG_FILE

set -e

# Função para saída de erro estruturada
error_exit() {
  echo "{\"level\":\"Error\",\"msg\":\"$1\"}" >&2
  exit 1
}

# Checagem de variáveis de ambiente obrigatórias
if [[ -z "$GITHUB_USERNAME" || -z "$GITHUB_PAT" ]]; then
  error_exit "Variáveis de ambiente GITHUB_USERNAME e/ou GITHUB_PAT não definidas."
fi

if [[ -z "$GIT_COMMIT_MSG_FILE" ]]; then
  error_exit "Variável de ambiente GIT_COMMIT_MSG_FILE não definida."
fi

if [[ ! -f "$GIT_COMMIT_MSG_FILE" ]]; then
  error_exit "Arquivo de mensagem de commit não encontrado: $GIT_COMMIT_MSG_FILE"
fi

msg=$(cat "$GIT_COMMIT_MSG_FILE")
if [[ -z "${msg// /}" ]]; then
  error_exit "Arquivo de mensagem de commit está vazio: $GIT_COMMIT_MSG_FILE"
fi

# Localizar git
if ! command -v git >/dev/null 2>&1; then
  error_exit "git não encontrado no PATH."
fi
GIT_BIN=$(command -v git)

# Configurar usuário/email se não estiverem setados
if ! $GIT_BIN config user.name >/dev/null 2>&1; then
  $GIT_BIN config user.name "$GITHUB_USERNAME"
  echo '{"level":"Info","msg":"git user.name configurado."}'
fi
if ! $GIT_BIN config user.email >/dev/null 2>&1; then
  $GIT_BIN config user.email "$GITHUB_USERNAME@users.noreply.github.com"
  echo '{"level":"Info","msg":"git user.email configurado."}'
fi

# Adicionar arquivos alterados
$GIT_BIN add -A
if [[ $? -ne 0 ]]; then
  error_exit "Falha ao adicionar arquivos ao git."
fi

# Commitar
$GIT_BIN commit -F "$GIT_COMMIT_MSG_FILE"
if [[ $? -ne 0 ]]; then
  error_exit "Falha ao realizar commit. Nenhuma alteração detectada?"
fi

echo '{"level":"Info","msg":"Commit realizado com sucesso."}'

# Pull remoto (merge automático)
$GIT_BIN pull --rebase
if [[ $? -ne 0 ]]; then
  error_exit "Falha ao fazer pull do repositório remoto."
fi

echo '{"level":"Info","msg":"Pull remoto realizado com sucesso."}'

# Push autenticado
remote_url=$($GIT_BIN remote get-url origin)
if [[ "$remote_url" =~ ^https:// ]]; then
  # Substitui https:// por https://usuario:token@
  auth_url=$(echo "$remote_url" | sed "s#https://#https://$GITHUB_USERNAME:$GITHUB_PAT@#")
else
  error_exit "URL do remote não é HTTPS. Push seguro não suportado."
fi

$GIT_BIN push "$auth_url" HEAD
if [[ $? -ne 0 ]]; then
  error_exit "Falha ao fazer push para o repositório remoto."
fi

echo '{"level":"Info","msg":"Push realizado com sucesso. Sincronização completa."}'
