"""Validador de Tools.

Este módulo implementa o validador de tools geradas,
testando-as em ambiente sandbox antes da integração ao sistema.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List

import structlog
from opentelemetry import trace

from .tool_generator import GeneratedTool

# Configuração do logger
logger = structlog.get_logger(__name__)
tracer = trace.get_tracer(__name__)


class ValidationResult(Enum):
    """Possíveis resultados da validação de uma tool."""

    PASSED = "passed"
    FAILED_SECURITY = "failed_security"
    FAILED_FUNCTIONALITY = "failed_functionality"
    FAILED_PERFORMANCE = "failed_performance"
    FAILED_COMPATIBILITY = "failed_compatibility"


@dataclass
class ValidationReport:
    """Relatório detalhado da validação de uma tool."""

    tool_id: str
    result: ValidationResult
    security_score: float  # 0.0 a 1.0
    performance_score: float  # 0.0 a 1.0
    test_results: Dict[str, Any]
    issues: List[Dict[str, Any]]
    recommendations: List[str]


class ToolValidator:
    """Validador de tools geradas."""

    def __init__(self, sandbox_provider, security_analyzer, test_runner):
        """Inicializa o validador de tools.

        Args:
            sandbox_provider: Provedor de ambientes sandbox para execução segura
            security_analyzer: Analisador de segurança para código gerado
            test_runner: Executor de testes para validar funcionalidade
        """
        self.sandbox_provider = sandbox_provider
        self.security_analyzer = security_analyzer
        self.test_runner = test_runner
        self.logger = logger.bind(component="ToolValidator")

    @tracer.start_as_current_span("validate_tool")
    async def validate_tool(self, tool: GeneratedTool) -> ValidationReport:
        """Valida uma tool gerada em ambiente sandbox.

        Args:
            tool: Tool gerada a ser validada

        Returns:
            Relatório detalhado da validação

        Raises:
            Exception: Se ocorrer um erro durante a validação
        """
        sandbox = None
        try:
            self.logger.info(
                "iniciando_validacao", tool_id=tool.tool_id, tool_name=tool.name
            )

            # Análise de segurança
            with tracer.start_as_current_span("security_analysis") as span:
                span.set_attribute("tool_id", tool.tool_id)
                security_results = await self.security_analyzer.analyze(tool.code)

            # Preparar sandbox
            self.logger.info("criando_ambiente_sandbox", tool_id=tool.tool_id)
            sandbox = await self.sandbox_provider.create_sandbox()

            # Executar testes
            with tracer.start_as_current_span("test_execution") as span:
                span.set_attribute("tool_id", tool.tool_id)
                test_results = await self.test_runner.run_tests(sandbox, tool)

            # Análise dos resultados
            result, issues, recommendations = self._analyze_results(
                security_results, test_results
            )

            # Criar relatório
            report = ValidationReport(
                tool_id=tool.tool_id,
                result=result,
                security_score=security_results.get("score", 0.0),
                performance_score=test_results.get("performance_score", 0.0),
                test_results=test_results,
                issues=issues,
                recommendations=recommendations,
            )

            self.logger.info(
                "validacao_concluida",
                tool_id=tool.tool_id,
                result=result.value,
                security_score=security_results.get("score", 0.0),
                issues_count=len(issues),
            )

            return report
        except Exception as e:
            self.logger.error("falha_validacao", tool_id=tool.tool_id, exc_info=e)
            raise
        finally:
            # Limpar sandbox
            if sandbox:
                try:
                    await self.sandbox_provider.destroy_sandbox(sandbox)
                    self.logger.info("sandbox_destruido", tool_id=tool.tool_id)
                except Exception as e:
                    self.logger.warning(
                        "falha_destruir_sandbox", tool_id=tool.tool_id, error=str(e)
                    )

    def _analyze_results(
        self, security_results: Dict[str, Any], test_results: Dict[str, Any]
    ) -> tuple:
        """Analisa os resultados de segurança e testes.

        Args:
            security_results: Resultados da análise de segurança
            test_results: Resultados dos testes de funcionalidade

        Returns:
            Uma tupla contendo (resultado, problemas, recomendações)
        """
        issues = []
        recommendations = []

        # Verificar problemas de segurança
        security_score = security_results.get("score", 0.0)
        security_issues = security_results.get("issues", [])

        if security_score < 0.7:
            # Falha por segurança insuficiente
            result = ValidationResult.FAILED_SECURITY
            issues.extend(security_issues)

            for issue in security_issues:
                if issue.get("severity", "") == "high":
                    recommendations.append(
                        f"Corrigir vulnerabilidade crítica: {issue.get('description', '')}"
                    )

        # Verificar problemas funcionais
        elif not test_results.get("all_passed", False):
            # Falha por funcionalidade incorreta
            result = ValidationResult.FAILED_FUNCTIONALITY

            # Adicionar testes que falharam
            failed_tests = test_results.get("failed_tests", [])
            for test in failed_tests:
                issues.append(
                    {
                        "type": "test_failure",
                        "test_name": test.get("name", "unknown"),
                        "description": test.get("message", "Teste falhou"),
                        "severity": "medium",
                    }
                )

                recommendations.append(
                    f"Corrigir falha no teste '{test.get('name', 'unknown')}': "
                    f"{test.get('message', 'Sem detalhes')}"
                )

        # Verificar problemas de desempenho
        elif test_results.get("performance_score", 1.0) < 0.5:
            # Falha por desempenho insuficiente
            result = ValidationResult.FAILED_PERFORMANCE

            # Adicionar problemas de desempenho
            performance_issues = test_results.get("performance_issues", [])
            issues.extend(performance_issues)

            for issue in performance_issues:
                recommendations.append(
                    f"Melhorar desempenho: {issue.get('description', '')}"
                )

        # Verificar problemas de compatibilidade
        elif not test_results.get("compatibility_passed", True):
            # Falha por problemas de compatibilidade
            result = ValidationResult.FAILED_COMPATIBILITY

            # Adicionar problemas de compatibilidade
            compat_issues = test_results.get("compatibility_issues", [])
            issues.extend(compat_issues)

            for issue in compat_issues:
                recommendations.append(
                    f"Resolver problema de compatibilidade: "
                    f"{issue.get('description', '')}"
                )

        # Se passou em todas as verificações
        else:
            result = ValidationResult.PASSED

            # Adicionar recomendações gerais para melhoria
            if security_score < 0.9:
                recommendations.append(
                    "Considerar melhorias de segurança para pontuação mais alta"
                )

            if test_results.get("performance_score", 1.0) < 0.8:
                recommendations.append("Avaliar otimizações de desempenho")

        return result, issues, recommendations
