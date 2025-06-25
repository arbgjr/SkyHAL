#!/usr/bin/env python3
"""
Script de validação das dependências de observabilidade.
"""

import sys
from importlib import import_module

# Lista de pacotes de observabilidade a validar
OBSERVABILITY_PACKAGES = [
    "structlog",
    "opentelemetry",
    "opentelemetry.sdk",
    "opentelemetry.instrumentation",
    "opentelemetry.instrumentation.fastapi",
    "opentelemetry.instrumentation.requests",
    "opentelemetry.instrumentation.sqlalchemy",
    "opentelemetry.instrumentation.logging",
    "opentelemetry.exporter.otlp",
    "opentelemetry.exporter.jaeger",
    "prometheus_client",
    "pythonjsonlogger",
]


def validate_import(package_name: str) -> tuple[bool, str | None]:
    """Valida se um pacote pode ser importado."""
    try:
        import_module(package_name)
        return True, None
    except ImportError as e:
        return False, str(e)


def main() -> int:
    """Executa a validação de todos os pacotes."""
    print("🔍 Validando dependências de observabilidade...")
    print("=" * 60)

    all_valid = True

    for package in OBSERVABILITY_PACKAGES:
        is_valid, error = validate_import(package)

        if is_valid:
            print(f"✅ {package}")
        else:
            print(f"❌ {package} - Erro: {error}")
            all_valid = False

    print("=" * 60)

    if all_valid:
        print(
            "🎉 Todas as dependências de observabilidade foram "
            "instaladas com sucesso!"
        )
        return 0
    else:
        print("⚠️  Algumas dependências falharam na validação.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
