"""Validador de Tools.

Este módulo implementa o validador de tools geradas,
testando-as em ambiente sandbox antes da integração ao sistema.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List

import structlog
from opentelemetry import trace
from prometheus_client import Counter, Histogram

from .tool_generator import GeneratedTool

# Configuração do logger
logger = structlog.get_logger(__name__)
tracer = trace.get_tracer(__name__)

# Métricas Prometheus para validação de tools
tool_validations_total = Counter(
    "auto_extension_tool_validations_total",
    "Total de validações de ferramentas",
    ["result"],
)
tool_validation_latency_seconds = Histogram(
    "auto_extension_tool_validation_latency_seconds",
    "Tempo de validação de ferramentas",
)
tool_validation_errors_total = Counter(
    "auto_extension_tool_validation_errors_total",
    "Total de erros na validação de ferramentas",
)


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

    @tool_validation_latency_seconds.time()
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

            with tracer.start_as_current_span("auto_extension.validate_tool") as span:
                # Análise de segurança
                with tracer.start_as_current_span("security_analysis") as sec_span:
                    sec_span.set_attribute("tool_id", tool.tool_id)
                    security_results = await self.security_analyzer.analyze(tool.code)

                # Preparar sandbox
                self.logger.info("criando_ambiente_sandbox", tool_id=tool.tool_id)
                sandbox = await self.sandbox_provider.create_sandbox()

                # Executar testes
                with tracer.start_as_current_span("test_execution") as test_span:
                    test_span.set_attribute("tool_id", tool.tool_id)
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
                tool_validations_total.labels(result=result.value).inc()
                return report
        except Exception as e:
            tool_validation_errors_total.inc()
            self.logger.error("falha_validacao", tool_id=tool.tool_id, exc_info=e)
            with tracer.start_as_current_span(
                "auto_extension.validate_tool.error"
            ) as span:
                span.record_exception(e)
            tool_validations_total.labels(result="error").inc()
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

    # Função utilitária centralizada em src/utils/tool_validation.py
    # Substitui a lógica duplicada anterior.
    def _analyze_results(
        self, security_results: Dict[str, Any], test_results: Dict[str, Any]
    ) -> tuple:
        """Analisa os resultados de segurança e testes usando utilitário centralizado."""
        from src.utils.tool_validation import analyze_tool_results

        return analyze_tool_results(security_results, test_results)
