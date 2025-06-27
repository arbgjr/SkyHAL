"""
Funções utilitárias para análise de resultados de validação de tools.
Extraído de ToolValidator para centralização e reuso.
"""
from typing import Any, Dict, List, Tuple

from src.domain.auto_extension.tool_validator import ValidationResult


def analyze_tool_results(
    security_results: Dict[str, Any], test_results: Dict[str, Any]
) -> Tuple[ValidationResult, List[Dict[str, Any]], List[str]]:
    """
    Analisa os resultados de segurança e testes de uma tool.
    Args:
        security_results: Resultados da análise de segurança
        test_results: Resultados dos testes de funcionalidade
    Returns:
        Uma tupla contendo (resultado, problemas, recomendações)
    """
    issues = []
    recommendations = []
    security_score = security_results.get("score", 0.0)
    security_issues = security_results.get("issues", [])
    # Falha de segurança tem prioridade, mas acumula issues de performance se houver
    performance_issues = test_results.get("performance_issues", [])
    failed_tests = test_results.get("failed_tests", [])
    compat_issues = test_results.get("compatibility_issues", [])
    has_failed_tests = bool(failed_tests)
    has_performance_fail = test_results.get("performance_score", 1.0) < 0.5
    has_compat_fail = not test_results.get("compatibility_passed", True)

    if security_score < 0.7:
        result = ValidationResult.FAILED_SECURITY
        issues.extend(security_issues)
        # Acumula issues de performance se também houver falha de performance
        if has_performance_fail:
            issues.extend(performance_issues)
        for issue in security_issues:
            if issue.get("severity", "") == "high":
                recommendations.append(
                    f"Corrigir vulnerabilidade crítica: {issue.get('description', '')}"
                )
        for issue in performance_issues:
            recommendations.append(
                f"Melhorar desempenho: {issue.get('description', '')}"
            )
    elif has_performance_fail:
        result = ValidationResult.FAILED_PERFORMANCE
        issues.extend(performance_issues)
        for issue in performance_issues:
            recommendations.append(
                f"Melhorar desempenho: {issue.get('description', '')}"
            )
    elif has_failed_tests:
        result = ValidationResult.FAILED_FUNCTIONALITY
        for test in failed_tests:
            issues.append(
                {
                    "type": "test_failure",
                    "test_name": test.get("name", "unknown"),
                    "description": test.get(
                        "message", test.get("error", "Teste falhou")
                    ),
                    "severity": "medium",
                }
            )
            recommendations.append(
                f"Corrigir falha no teste '{test.get('name', 'unknown')}': "
                f"{test.get('message', test.get('error', 'Sem detalhes'))}"
            )
    elif has_compat_fail:
        result = ValidationResult.FAILED_COMPATIBILITY
        issues.extend(compat_issues)
        for issue in compat_issues:
            recommendations.append(
                f"Resolver problema de compatibilidade: "
                f"{issue.get('description', '')}"
            )
    else:
        result = ValidationResult.PASSED
        recommendations.append("A ferramenta passou em todos os testes e validações.")
        if security_score < 0.9:
            recommendations.append(
                "Considerar melhorias de segurança para pontuação mais alta"
            )
        if test_results.get("performance_score", 1.0) < 0.8:
            recommendations.append("Avaliar otimizações de desempenho")
    return result, issues, recommendations
