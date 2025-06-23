$envVars = @('Machine', 'User')
foreach ($level in $envVars) {
    [System.Environment]::GetEnvironmentVariables($level).GetEnumerator() | ForEach-Object {
        Set-Item -Path env:$($_.Name) -Value $_.Value
    }
}
#region Variáveis e Pré-Checagens
$usuario = $env:GITHUB_USERNAME
$pat = $env:GITHUB_PAT
$msg = $env:GIT_COMMIT_MSG

if (-not $usuario -or -not $pat) {
    Write-Host ('{"level":"Error","msg":"Variáveis de ambiente GITHUB_USERNAME e/ou GITHUB_PAT não definidas."}')
    exit 1
}

# Tentar localizar o git.exe no PATH
$gitPath = (Get-Command git -ErrorAction SilentlyContinue).Source
if (-not $gitPath) {
    # Possíveis diretórios padrão do Windows
    $possiveis = @(
        "$env:ProgramFiles\Git\cmd\git.exe",
        "$env:ProgramFiles(x86)\Git\cmd\git.exe",
        "$env:UserProfile\scoop\apps\git\current\cmd\git.exe",
        "$env:LocalAppData\Programs\Git\cmd\git.exe"
    )
    foreach ($caminho in $possiveis) {
        if (Test-Path $caminho) {
            $gitPath = $caminho
            Write-Host ("{""level"":""Warning"",""msg"":""Git não estava no PATH, mas foi encontrado em: $gitPath""}")
            break
        }
    }
}
if ($gitPath) {
    Write-Host ("{""level"":""Info"",""msg"":""Git encontrado em: $gitPath""}")
} else {
    Write-Host ('{"level":"Error","msg":"Git não encontrado no PATH nem nos diretórios padrão. Instale o Git e reinicie o VS Code."}')
    exit 1
}

# Verificar se o diretório atual é um repositório Git
if (-not (Test-Path .git)) {
    Write-Host ('{"level":"Error","msg":"Diretório atual não é um repositório Git. Navegue até um repositório válido."}')
    exit 1
}

if (-not $msg) {
    $msg = 'chore(sync): sincronizar alterações locais com remoto via task VS Code'
}

# Construir URL remota usando concatenação para evitar problemas de sintaxe
$remote = "https://" + $usuario + ":" + $pat + "@github.com/arbgjr/SkyHAL.git"
Write-Host ('{"level":"Info","msg":"Iniciando sync local-remoto..."}')
#endregion

#region Preparar Remote
& $gitPath remote set-url origin $remote
if ($LASTEXITCODE -ne 0) {
    Write-Host ('{"level":"Error","msg":"Falha ao configurar remote."}')
    exit 1
}
#endregion

#region Add & Commit
# Verificar se há conflitos não resolvidos antes de tentar commitar
$conflicts = & $gitPath ls-files --unmerged
if ($conflicts) {
    Write-Host ('{"level":"Error","msg":"Existem arquivos em conflito não resolvidos. Resolva os conflitos, faça git add/rm e tente novamente."}')
    exit 1
}

& $gitPath add .
if ($LASTEXITCODE -ne 0) {
    Write-Host ('{"level":"Error","msg":"Falha ao adicionar arquivos ao stage."}')
    exit 1
}

& $gitPath commit -m "$msg"
if ($LASTEXITCODE -eq 0) {
    Write-Host ('{"level":"Info","msg":"Commit realizado com sucesso."}')
} elseif ($LASTEXITCODE -eq 1) {
    Write-Host ('{"level":"Info","msg":"Nada para commitar."}')
} else {
    Write-Host ('{"level":"Error","msg":"Falha ao commitar alterações. Verifique se há conflitos não resolvidos."}')
    exit 1
}

#endregion

#region Pull --rebase
& $gitPath pull $remote main --rebase
if ($LASTEXITCODE -ne 0) {
    Write-Host ('{"level":"Error","msg":"Falha ao fazer pull --rebase."}')
    exit 1
}
Write-Host ('{"level":"Info","msg":"Rebase concluído com sucesso."}')
#endregion

#region Push
& $gitPath push
if ($LASTEXITCODE -ne 0) {
    Write-Host ('{"level":"Error","msg":"Falha ao fazer push para o remoto."}')
    exit 1
}
Write-Host ('{"level":"Info","msg":"Push realizado com sucesso."}')
#endregion

#region Restaurar Remote
& $gitPath remote set-url origin https://github.com/arbgjr/SkyHAL.git
if ($LASTEXITCODE -ne 0) {
    Write-Host ('{"level":"Warning","msg":"Falha ao restaurar remote padrão. Verifique manualmente."}')
} else {
    Write-Host ('{"level":"Info","msg":"Remote restaurado para padrão."}')
}
#endregion
