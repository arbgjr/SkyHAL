# Lint script para Windows (PowerShell)
param()
Write-Host "Executando lint (ruff, flake8, black)..."

# Ruff
poetry run ruff check --fix src tests
if ($LASTEXITCODE -ne 0) { exit 1 }

# Flake8
poetry run flake8 src tests
if ($LASTEXITCODE -ne 0) { exit 1 }

# Black (apenas checagem)
poetry run black --check --fix src tests
if ($LASTEXITCODE -ne 0) { exit 1 }

Write-Host "Lint finalizado com sucesso."
exit 0
