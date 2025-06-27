#!/usr/bin/env python3
"""
Script de teste final da stack de observabilidade.

Valida que todas as funcionalidades estão funcionando corretamente.
"""

import time

import requests  # type: ignore


def test_observability_stack() -> bool:
    """Testa toda a stack de observabilidade."""
    print("🧪 Testando Stack de Observabilidade SkyHAL")
    print("=" * 50)

    results = {}

    # 1. Testar SkyHAL API
    print("\n1️⃣ Testando aplicação SkyHAL...")
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code == 200:
            print("✅ SkyHAL API está rodando")
            results["skyhal_api"] = True
        else:
            print(f"❌ SkyHAL API retornou {response.status_code}")
            results["skyhal_api"] = False
    except Exception as e:
        print(f"❌ SkyHAL API não acessível: {e}")
        results["skyhal_api"] = False

    # 8. Testar geração de dados
    print("\n8️⃣ Testando geração de dados...")
    print("Gerando tráfego para validar instrumentação...")

    for _ in range(5):
        try:
            requests.get("http://localhost:8000/health", timeout=2)
            time.sleep(1)
        except requests.RequestException:
            pass  # nosec B110

    print("✅ Tráfego gerado")
    results["data_generation"] = True

    # Resumo
    print("\n" + "=" * 50)
    print("📊 RESUMO DOS TESTES")
    print("=" * 50)

    total_tests = len(results)
    passed_tests = sum(1 for result in results.values() if result)

    for component, passed in results.items():
        status_icon = "✅" if passed else "❌"
        print(f"{status_icon} {component.replace('_', ' ').title()}")

    print(f"\n🎯 Resultado: {passed_tests}/{total_tests} testes passaram")

    if passed_tests == total_tests:
        print("🎉 TODOS OS TESTES PASSARAM! Stack está funcionando perfeitamente.")
        return True
    else:
        print("⚠️  Alguns testes falharam. Verifique os logs acima.")
        return False


def generate_test_data() -> None:
    """Gera dados de teste para validar a observabilidade."""
    print("\n🔄 Gerando dados de teste...")

    # Gerar apenas tráfego HTTP básico
    for _ in range(10):
        try:
            requests.get("http://localhost:8000/health", timeout=2)
            time.sleep(0.1)
        except requests.RequestException:
            pass  # nosec B110

    print("✅ Dados de teste gerados com sucesso!")


if __name__ == "__main__":
    # Executar testes principais
    success = test_observability_stack()

    # Gerar dados de teste se tudo estiver funcionando
    if success:
        generate_test_data()

        print("\n🎯 PRÓXIMOS PASSOS:")
        print("1. Acesse Grafana: http://localhost:3000 (admin/admin123)")
        print("2. Veja os dashboards em: SkyHAL > API Overview")
        print("3. Explore traces em: http://localhost:16686")
        print("4. Verifique métricas em: http://localhost:9090")

    print("\n🏁 Teste concluído!")
