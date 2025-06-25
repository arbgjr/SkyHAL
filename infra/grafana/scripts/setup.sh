#!/bin/bash
# Script de configuração inicial da stack de observabilidade

set -e

echo "🚀 Configurando Stack de Observabilidade SkyHAL..."
echo "================================================="

# Verificar se Docker está rodando
if ! docker info >/dev/null 2>&1; then
    echo "❌ Docker não está rodando. Por favor, inicie o Docker primeiro."
    exit 1
fi

# Criar volumes se não existirem
echo "📦 Criando volumes Docker..."
docker volume create skyhal-prometheus-data 2>/dev/null || true
docker volume create skyhal-grafana-data 2>/dev/null || true
docker volume create skyhal-loki-data 2>/dev/null || true
docker volume create skyhal-jaeger-data 2>/dev/null || true

# Verificar se já existe uma stack rodando
if docker-compose ps | grep -q "Up"; then
    echo "⚠️  Stack já está rodando. Deseja reiniciar? (y/N)"
    read -r response
    if [[ "$response" =~ ^[Yy]$ ]]; then
        echo "🔄 Parando stack atual..."
        docker-compose down
    else
        echo "✅ Mantendo stack atual."
        exit 0
    fi
fi

# Subir a stack
echo "🔧 Iniciando stack de observabilidade..."
docker-compose up -d

# Aguardar serviços ficarem prontos
echo "⏳ Aguardando serviços ficarem prontos..."
sleep 30

# Verificar saúde dos serviços
echo "🔍 Verificando saúde dos serviços..."

services=(
    "prometheus:9090"
    "grafana:3000"
    "jaeger:16686"
    "loki:3100"
    "otel-collector:8888"
)

for service in "${services[@]}"; do
    name=$(echo "$service" | cut -d: -f1)
    port=$(echo "$service" | cut -d: -f2)

    if curl -f -s "http://localhost:$port" >/dev/null 2>&1; then
        echo "✅ $name está rodando (porta $port)"
    else
        echo "❌ $name não responde (porta $port)"
    fi
done

echo ""
echo "🎉 Stack de observabilidade configurada!"
echo "================================================="
echo "📊 Grafana:    http://localhost:3000 (admin/admin123)"
echo "📈 Prometheus: http://localhost:9090"
echo "🔍 Jaeger:     http://localhost:16686"
echo "📝 Loki:       http://localhost:3100"
echo "🔧 OTEL:       http://localhost:8888"
echo ""
echo "💡 Para parar a stack: docker-compose down"
echo "💡 Para ver logs: docker-compose logs -f [service]"
