"""Gerador de Tools para o sistema de auto-extensão.

Este módulo fornece componentes para geração de novas tools
baseadas em especificações derivadas das lacunas de capacidade identificadas.
"""

import uuid
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict

import structlog
from opentelemetry import trace

# Configuração do logger
logger = structlog.get_logger(__name__)
tracer = trace.get_tracer(__name__)


@dataclass
class ToolSpec:
    """Especificação para geração de uma nova tool."""

    name: str
    description: str
    parameters: Dict[str, Any]
    return_type: str
    template_id: str
    security_level: str
    resource_requirements: Dict[str, Any]


@dataclass
class GeneratedTool:
    """Resultado da geração de uma nova tool."""

    tool_id: str
    name: str
    code: str
    spec: ToolSpec
    validation_results: Dict[str, Any]
    version: str
    created_at: str


class DefaultTemplateProvider:
    """Provedor de templates padrão para uso em testes."""

    async def get_template(self, spec: Any) -> Dict[str, str]:
        """Retorna um template padrão para testes."""
        return {
            "code_template": (
                f"def {spec.name}({', '.join(spec.parameters)}):\n"
                f"    '''\n    {spec.description}\n    '''\n"
                "    # Implementação padrão\n"
                "    return {'result': 'success'}"
            ),
            "type": spec.template_id or "default",
            "version": "1.0.0",
        }


class ToolGenerator:
    """Gerador de novas tools baseado em especificações."""

    def __init__(
        self, template_provider: Any, code_generator: Any, security_validator: Any
    ) -> None:
        """Inicializa o gerador de tools.

        Args:
            template_provider: Provedor de templates para geração de código
            code_generator: Gerador de código baseado em templates e especificações
            security_validator: Validador de segurança para código gerado
        """
        self.template_provider = template_provider
        self.code_generator = code_generator
        self.security_validator = security_validator
        self.logger = logger.bind(component="ToolGenerator")

    @tracer.start_as_current_span("generate_tool")
    async def generate_tool(self, spec: ToolSpec) -> GeneratedTool:
        """Gera uma nova tool baseada na especificação.

        Args:
            spec: Especificação da tool a ser gerada

        Returns:
            A tool gerada com seu código e metadados

        Raises:
            ValueError: Se a especificação for inválida
            Exception: Se ocorrer erro durante a geração
        """
        try:
            # Validar especificação
            self._validate_spec(spec)

            # Obter template
            template = await self.template_provider.get_template(spec.template_id)

            # Gerar código
            self.logger.info(
                "iniciando_geracao_codigo",
                tool_name=spec.name,
                template_id=spec.template_id,
            )

            with tracer.start_as_current_span("code_generation") as span:
                span.set_attribute("tool_name", spec.name)
                span.set_attribute("template_id", spec.template_id)
                code = await self.code_generator.generate(template, spec)

            # Validar segurança
            self.logger.info("iniciando_validacao_seguranca", tool_name=spec.name)

            with tracer.start_as_current_span("security_validation") as span:
                span.set_attribute("tool_name", spec.name)
                validation_results = await self.security_validator.validate(code, spec)

            # Criar tool
            tool_id = str(uuid.uuid4())
            tool = GeneratedTool(
                tool_id=tool_id,
                name=spec.name,
                code=code,
                spec=spec,
                validation_results=validation_results,
                version="1.0.0",
                created_at=datetime.utcnow().isoformat(),
            )

            status = "success" if validation_results.get("passed", False) else "failed"
            self.logger.info(
                "tool_gerada",
                tool_id=tool.tool_id,
                name=tool.name,
                status=status,
                validation_score=validation_results.get("score", 0),
            )

            return tool
        except ValueError as e:
            self.logger.warning(
                "especificacao_invalida", spec_name=spec.name, error=str(e)
            )
            raise
        except Exception as e:
            self.logger.error("falha_geracao_tool", spec_name=spec.name, exc_info=e)
            raise

    def _validate_spec(self, spec: ToolSpec) -> None:
        """Valida a especificação da tool antes da geração.

        Args:
            spec: Especificação a ser validada

        Raises:
            ValueError: Se a especificação for inválida
        """
        # Validar nome
        if not spec.name or not all(c.isalnum() or c == "_" for c in spec.name):
            raise ValueError(
                f"Nome da tool inválido: '{spec.name}'. "
                "Use apenas caracteres alfanuméricos e underscores."
            )

        # Validar descrição
        if not spec.description or len(spec.description) < 10:
            raise ValueError(
                f"Descrição muito curta: '{spec.description}'. "
                "Forneça uma descrição mais detalhada."
            )

        # Validar parâmetros
        if not spec.parameters:
            raise ValueError("A tool deve ter pelo menos um parâmetro.")

        for param_name, param_info in spec.parameters.items():
            if not isinstance(param_info, dict):
                raise ValueError(f"Parâmetro '{param_name}' deve ser um dicionário.")

            if "type" not in param_info:
                raise ValueError(f"Parâmetro '{param_name}' deve ter um tipo.")

        # Validar nível de segurança
        valid_security_levels = ["standard", "elevated", "admin"]
        if spec.security_level not in valid_security_levels:
            raise ValueError(
                f"Nível de segurança '{spec.security_level}' inválido. "
                f"Use um dos seguintes: {', '.join(valid_security_levels)}."
            )

        # Validar requisitos de recursos
        required_resources = ["memory_mb", "timeout_seconds"]
        for resource in required_resources:
            if resource not in spec.resource_requirements:
                raise ValueError(f"Requisito de recurso '{resource}' não especificado.")

            if not isinstance(spec.resource_requirements[resource], (int, float)):
                raise ValueError(
                    f"Requisito de recurso '{resource}' deve ser numérico."
                )

        # Validar limites de recursos
        if spec.resource_requirements.get("memory_mb", 0) > 1024:
            raise ValueError("Requisito de memória não pode exceder 1024MB.")

        if spec.resource_requirements.get("timeout_seconds", 0) > 60:
            raise ValueError("Timeout não pode exceder 60 segundos.")
