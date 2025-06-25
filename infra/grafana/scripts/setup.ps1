# PowerShell Script para configuração da stack de observabilidade

Write-Host "🚀 Configurando Stack de Observabilidade SkyHAL..." -ForegroundColor Green
Write-Host "================================================="

# Verificar se Docker está rodando
try {
    docker info | Out-Null
} catch {
    Write-Host "❌ Docker não está rodando. Por favor, inicie o Docker primeiro." -ForegroundColor Red
    exit 1
}

# Criar volumes se não existirem
Write-Host "📦 Criando volumes Docker..." -ForegroundColor Yellow
$volumes = @(
    "skyhal-prometheus-data",
    "skyhal-grafana-data",
    "skyhal-loki-data",
    "skyhal-jaeger-data"
)

foreach ($volume in $volumes) {
    try {
        docker volume create $volume 2>$null
        Write-Host "✅ Volume $volume criado/verificado" -ForegroundColor Green
    } catch {
        # Volume já existe, ok
    }
}

# Verificar se já existe uma stack rodando
$runningServices = docker-compose ps --filter "status=running" -q
if ($runningServices) {
    $response = Read-Host "⚠️  Stack já está rodando. Deseja reiniciar? (y/N)"
    if ($response -match "^[Yy]$") {
        Write-Host "🔄 Parando stack atual..." -ForegroundColor Yellow
        docker-compose down
    } else {
        Write-Host "✅ Mantendo stack atual." -ForegroundColor Green
        exit 0
    }
}

# Subir a stack
Write-Host "🔧 Iniciando stack de observabilidade..." -ForegroundColor Yellow
docker-compose up -d

# Aguardar serviços ficarem prontos
Write-Host "⏳ Aguardando serviços ficarem prontos..." -ForegroundColor Yellow
Start-Sleep -Seconds 30

# Verificar saúde dos serviços
Write-Host "🔍 Verificando saúde dos serviços..." -ForegroundColor Yellow

$services = @{
    "prometheus" = 9090
    "grafana" = 3000
    "jaeger" = 16686
    "loki" = 3100
    "otel-collector" = 8888
}

foreach ($service in $services.GetEnumerator()) {
    $name = $service.Key
    $port = $service.Value

    try {
        $response = Invoke-WebRequest -Uri "http://localhost:$port" -UseBasicParsing -TimeoutSec 5
        Write-Host "✅ $name está rodando (porta $port)" -ForegroundColor Green
    } catch {
        Write-Host "❌ $name não responde (porta $port)" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "🎉 Stack de observabilidade configurada!" -ForegroundColor Green
Write-Host "================================================="
Write-Host "📊 Grafana:    http://localhost:3000 (admin/admin123)" -ForegroundColor Cyan
Write-Host "📈 Prometheus: http://localhost:9090" -ForegroundColor Cyan
Write-Host "🔍 Jaeger:     http://localhost:16686" -ForegroundColor Cyan
Write-Host "📝 Loki:       http://localhost:3100" -ForegroundColor Cyan
Write-Host "🔧 OTEL:       http://localhost:8888" -ForegroundColor Cyan
Write-Host ""
Write-Host "💡 Para parar a stack: docker-compose down" -ForegroundColor Yellow
Write-Host "💡 Para ver logs: docker-compose logs -f [service]" -ForegroundColor Yellow
