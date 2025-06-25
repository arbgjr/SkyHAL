# Especificações Técnicas - Artefatos Auto-Extensão MCP

Este documento descreve os artefatos específicos necessários para implementação do sistema de auto-extensão do SkyHAL.

## 1. Sistema de Análise de Capacidades

**Arquivo:** `src/domain/auto_extension/capability_analyzer.py`

### Descrição
Implementa o analisador de capacidades responsável por identificar limitações no sistema atual e recomendar áreas para melhoria através da criação de novas tools.

### Conteúdo

```python
from dataclasses import dataclass
from typing import List, Dict, Any, Optional
from enum import Enum

class CapabilityType(Enum):
    DATA_PROCESSING = "data_processing"
    TEXT_GENERATION = "text_generation"
    CODE_ANALYSIS = "code_analysis"
    EXTERNAL_INTEGRATION = "external_integration"
    REASONING = "reasoning"

@dataclass
class CapabilityGap:
    """Representa uma lacuna identificada nas capacidades atuais."""
    capability_type: CapabilityType
    description: str
    severity: float  # 0.0 a 1.0
    frequency: float  # 0.0 a 1.0
    examples: List[str]
    potential_solutions: List[str]

class CapabilityAnalyzer:
    """Analisador de capacidades do sistema."""

    def __init__(self, metrics_provider, feedback_provider):
        self.metrics_provider = metrics_provider
        self.feedback_provider = feedback_provider
        self.logger = setup_logger(__name__)

    async def analyze_capabilities(self) -> List[CapabilityGap]:
        """Analisa capacidades atuais e identifica lacunas."""
        try:
            metrics = await self.metrics_provider.get_performance_metrics()
            feedback = await self.feedback_provider.get_recent_feedback()

            # Análise de métricas e feedback
            gaps = self._identify_gaps(metrics, feedback)

            self.logger.info(
                "capability_analysis_completed",
                gaps_found=len(gaps),
                severity_avg=sum(gap.severity for gap in gaps) / len(gaps) if gaps else 0
            )

            return gaps
        except Exception as e:
            self.logger.error("capability_analysis_failed", exc_info=e)
            raise
```

### Interfaces Relacionadas
- `MetricsProvider`: Fornece métricas de desempenho do sistema
- `FeedbackProvider`: Fornece feedback de usuários sobre limitações

### Instructions Relacionadas
- `python-mcp.instructions.md`: Estrutura de classes e tratamento de erros
- `observabilidade.instructions.md`: Instrumentação com logs estruturados

## 2. Gerador de Tools

**Arquivo:** `src/domain/auto_extension/tool_generator.py`

### Descrição
Implementa o gerador de novas tools baseado em especificações derivadas das lacunas de capacidade identificadas.

### Conteúdo

```python
from dataclasses import dataclass
from typing import Dict, Any, List, Optional
import uuid
from datetime import datetime

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

class ToolGenerator:
    """Gerador de novas tools baseado em especificações."""

    def __init__(self, template_provider, code_generator, security_validator):
        self.template_provider = template_provider
        self.code_generator = code_generator
        self.security_validator = security_validator
        self.logger = setup_logger(__name__)

    async def generate_tool(self, spec: ToolSpec) -> GeneratedTool:
        """Gera uma nova tool baseada na especificação."""
        try:
            # Validar especificação
            self._validate_spec(spec)

            # Obter template
            template = await self.template_provider.get_template(spec.template_id)

            # Gerar código
            code = await self.code_generator.generate(template, spec)

            # Validar segurança
            validation_results = await self.security_validator.validate(code, spec)

            # Criar tool
            tool = GeneratedTool(
                tool_id=str(uuid.uuid4()),
                name=spec.name,
                code=code,
                spec=spec,
                validation_results=validation_results,
                version="1.0.0",
                created_at=datetime.utcnow().isoformat()
            )

            self.logger.info(
                "tool_generated",
                tool_id=tool.tool_id,
                name=tool.name,
                validation_status="success" if validation_results["passed"] else "failed"
            )

            return tool
        except Exception as e:
            self.logger.error("tool_generation_failed", spec_name=spec.name, exc_info=e)
            raise
```

### Interfaces Relacionadas
- `TemplateProvider`: Fornece templates para diferentes tipos de tools
- `CodeGenerator`: Gera código com base em templates e especificações
- `SecurityValidator`: Realiza verificações de segurança no código gerado

### Instructions Relacionadas
- `python-mcp.instructions.md`: Estrutura de dados e tratamento de erros
- `api-security.instructions.md`: Validação de segurança

## 3. Validador de Tools

**Arquivo:** `src/domain/auto_extension/tool_validator.py`

### Descrição
Implementa o validador que testa as tools geradas em ambiente sandbox antes da integração ao sistema.

### Conteúdo

```python
from dataclasses import dataclass
from typing import Dict, Any, List, Optional
from enum import Enum

class ValidationResult(Enum):
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
        self.sandbox_provider = sandbox_provider
        self.security_analyzer = security_analyzer
        self.test_runner = test_runner
        self.logger = setup_logger(__name__)

    async def validate_tool(self, tool: GeneratedTool) -> ValidationReport:
        """Valida uma tool gerada em ambiente sandbox."""
        try:
            # Análise de segurança
            security_results = await self.security_analyzer.analyze(tool.code)

            # Preparar sandbox
            sandbox = await self.sandbox_provider.create_sandbox()

            # Executar testes
            with tracer.start_as_current_span("tool_validation_tests") as span:
                span.set_attribute("tool_id", tool.tool_id)
                test_results = await self.test_runner.run_tests(sandbox, tool)

            # Análise dos resultados
            result, issues, recommendations = self._analyze_results(security_results, test_results)

            # Criar relatório
            report = ValidationReport(
                tool_id=tool.tool_id,
                result=result,
                security_score=security_results["score"],
                performance_score=test_results.get("performance_score", 0.0),
                test_results=test_results,
                issues=issues,
                recommendations=recommendations
            )

            self.logger.info(
                "tool_validation_completed",
                tool_id=tool.tool_id,
                result=result.value,
                security_score=security_results["score"],
                issues_count=len(issues)
            )

            return report
        except Exception as e:
            self.logger.error("tool_validation_failed", tool_id=tool.tool_id, exc_info=e)
            raise
        finally:
            # Limpar sandbox
            await self.sandbox_provider.destroy_sandbox(sandbox)
```

### Interfaces Relacionadas
- `SandboxProvider`: Cria ambientes sandbox isolados
- `SecurityAnalyzer`: Analisa código para vulnerabilidades
- `TestRunner`: Executa testes de validação em tools

### Instructions Relacionadas
- `test.instructions.md`: Práticas de testes e validação
- `api-security.instructions.md`: Verificação de segurança

## 4. Sistema de Auto-Aprendizado

**Arquivo:** `src/domain/auto_extension/learning_system.py`

### Descrição
Implementa o sistema de aprendizado baseado no uso e feedback das tools criadas.

### Conteúdo

```python
from dataclasses import dataclass
from typing import Dict, Any, List, Optional
import time

@dataclass
class ToolUsageMetrics:
    """Métricas de uso de uma tool."""
    tool_id: str
    invocation_count: int
    success_rate: float
    average_execution_time: float
    error_types: Dict[str, int]
    user_ratings: List[float]
    last_used_at: float

@dataclass
class LearningInsight:
    """Insight gerado pelo sistema de aprendizado."""
    tool_id: str
    suggested_improvements: List[str]
    parameter_adjustments: Dict[str, Any]
    usage_patterns: Dict[str, Any]
    performance_bottlenecks: List[str]

class LearningSystem:
    """Sistema de auto-aprendizado baseado em uso de tools."""

    def __init__(self, metrics_collector, pattern_analyzer):
        self.metrics_collector = metrics_collector
        self.pattern_analyzer = pattern_analyzer
        self.logger = setup_logger(__name__)

    async def analyze_tool_usage(self, tool_id: str) -> LearningInsight:
        """Analisa o uso de uma tool e gera insights."""
        try:
            # Coletar métricas de uso
            with tracer.start_as_current_span("collect_tool_metrics") as span:
                span.set_attribute("tool_id", tool_id)
                metrics = await self.metrics_collector.get_tool_metrics(tool_id)

            # Identificar padrões
            usage_patterns = await self.pattern_analyzer.identify_patterns(metrics)

            # Gerar sugestões de melhoria
            suggestions = self._generate_suggestions(metrics, usage_patterns)

            # Calcular ajustes de parâmetros
            parameter_adjustments = self._calculate_parameter_adjustments(metrics, usage_patterns)

            # Identificar gargalos de performance
            bottlenecks = self._identify_bottlenecks(metrics)

            # Criar insight
            insight = LearningInsight(
                tool_id=tool_id,
                suggested_improvements=suggestions,
                parameter_adjustments=parameter_adjustments,
                usage_patterns=usage_patterns,
                performance_bottlenecks=bottlenecks
            )

            self.logger.info(
                "tool_learning_analysis_completed",
                tool_id=tool_id,
                suggestions_count=len(suggestions),
                bottlenecks_count=len(bottlenecks)
            )

            return insight
        except Exception as e:
            self.logger.error("tool_learning_analysis_failed", tool_id=tool_id, exc_info=e)
            raise
```

### Interfaces Relacionadas
- `MetricsCollector`: Coleta métricas de uso de tools
- `PatternAnalyzer`: Analisa padrões em métricas de uso

### Instructions Relacionadas
- `python-mcp.instructions.md`: Estrutura de dados e tratamento de erros
- `observabilidade.instructions.md`: Integração com métricas

## 5. Sandbox de Segurança

**Arquivo:** `src/infrastructure/auto_extension/sandbox/memory_sandbox.py`

### Descrição
Implementa um ambiente sandbox isolado para execução segura de código gerado.

### Conteúdo

```python
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
import asyncio
import resource
import uuid
import time

class Sandbox(ABC):
    """Interface para ambientes sandbox de execução."""

    @abstractmethod
    async def initialize(self) -> str:
        """Inicializa o ambiente sandbox e retorna ID."""
        pass

    @abstractmethod
    async def execute(self, sandbox_id: str, code: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Executa código no sandbox com os parâmetros fornecidos."""
        pass

    @abstractmethod
    async def destroy(self, sandbox_id: str) -> None:
        """Destrói o ambiente sandbox."""
        pass

class MemorySandbox(Sandbox):
    """Implementação de sandbox em memória com isolamento de recursos."""

    def __init__(self, permission_manager, resource_limiter):
        self.permission_manager = permission_manager
        self.resource_limiter = resource_limiter
        self.sandboxes = {}
        self.logger = setup_logger(__name__)

    async def initialize(self) -> str:
        """Inicializa um novo sandbox em memória."""
        try:
            sandbox_id = str(uuid.uuid4())

            # Criar ambiente isolado
            self.sandboxes[sandbox_id] = {
                "created_at": time.time(),
                "namespace": {},
                "permissions": self.permission_manager.get_default_permissions(),
                "resources": self.resource_limiter.get_default_limits()
            }

            self.logger.info(
                "sandbox_initialized",
                sandbox_id=sandbox_id
            )

            return sandbox_id
        except Exception as e:
            self.logger.error("sandbox_initialization_failed", exc_info=e)
            raise

    async def execute(self, sandbox_id: str, code: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Executa código no sandbox com isolamento e limites."""
        if sandbox_id not in self.sandboxes:
            raise ValueError(f"Sandbox {sandbox_id} não encontrado")

        sandbox = self.sandboxes[sandbox_id]

        try:
            # Validar permissões
            self.permission_manager.validate_code(code, sandbox["permissions"])

            # Preparar ambiente de execução
            namespace = sandbox["namespace"].copy()
            namespace.update(params)

            # Configurar limites de recursos
            resource.setrlimit(resource.RLIMIT_CPU, (sandbox["resources"]["cpu_seconds"], sandbox["resources"]["cpu_seconds"]))
            resource.setrlimit(resource.RLIMIT_AS, (sandbox["resources"]["memory_bytes"], sandbox["resources"]["memory_bytes"]))

            # Executar com timeout
            with tracer.start_as_current_span("sandbox_execution") as span:
                span.set_attribute("sandbox_id", sandbox_id)

                result = await asyncio.wait_for(
                    self._execute_code(code, namespace),
                    timeout=sandbox["resources"]["timeout_seconds"]
                )

            self.logger.info(
                "sandbox_execution_completed",
                sandbox_id=sandbox_id,
                execution_time=result.get("execution_time", 0)
            )

            return result
        except asyncio.TimeoutError:
            self.logger.warning(
                "sandbox_execution_timeout",
                sandbox_id=sandbox_id
            )
            return {"error": "Execution timeout", "status": "timeout"}
        except Exception as e:
            self.logger.error(
                "sandbox_execution_failed",
                sandbox_id=sandbox_id,
                exc_info=e
            )
            return {"error": str(e), "status": "error"}
```

### Interfaces Relacionadas
- `PermissionManager`: Gerencia permissões para execução de código
- `ResourceLimiter`: Define limites de recursos para execução

### Instructions Relacionadas
- `api-security.instructions.md`: Práticas de segurança
- `python-mcp.instructions.md`: Tratamento de erros e exceções

## 6. Observabilidade para Auto-Extensão

**Arquivo:** `src/infrastructure/observability/auto_extension_metrics.py`

### Descrição
Implementa métricas específicas para monitoramento do sistema de auto-extensão.

### Conteúdo

```python
from typing import Dict, Any
from prometheus_client import Counter, Histogram, Gauge
from opentelemetry import trace
from opentelemetry.trace import Status, StatusCode
from functools import wraps
import time
import hashlib

# Métricas para sistema de auto-extensão
tools_generated = Counter(
    "skyhal_auto_extension_tools_generated_total",
    "Total de tools geradas pelo sistema de auto-extensão",
    ["status", "type"]
)

generation_time = Histogram(
    "skyhal_auto_extension_generation_time_seconds",
    "Tempo para gerar uma nova tool",
    ["type"]
)

validation_success_rate = Gauge(
    "skyhal_auto_extension_validation_success_rate",
    "Taxa de sucesso na validação de tools",
    ["type"]
)

sandbox_executions = Counter(
    "skyhal_auto_extension_sandbox_executions_total",
    "Total de execuções em ambiente sandbox",
    ["status", "resource_limit"]
)

class AutoExtensionObservability:
    """Configuração de observabilidade para o sistema de auto-extensão."""

    def __init__(self):
        self.tracer = trace.get_tracer(__name__)
        self.logger = setup_logger(__name__)

    def trace_capability_analysis(self, func):
        """Decorator para tracing de análise de capacidades."""
        @wraps(func)
        async def wrapper(*args, **kwargs):
            with self.tracer.start_as_current_span("capability_analysis") as span:
                try:
                    start_time = time.time()
                    result = await func(*args, **kwargs)

                    # Adicionar atributos ao span
                    span.set_attribute("gaps_found", len(result))
                    span.set_attribute("analysis_time_seconds", time.time() - start_time)
                    span.set_status(Status(StatusCode.OK))

                    return result
                except Exception as e:
                    span.set_status(Status(StatusCode.ERROR))
                    span.record_exception(e)
                    raise
        return wrapper

    def trace_tool_generation(self, func):
        """Decorator para tracing de geração de tools."""
        @wraps(func)
        async def wrapper(*args, **kwargs):
            with self.tracer.start_as_current_span("tool_generation") as span:
                try:
                    spec = kwargs.get("spec") or args[1]  # Assumindo que spec é segundo argumento
                    span.set_attribute("tool_name", spec.name)
                    span.set_attribute("template_id", spec.template_id)

                    start_time = time.time()
                    tool = await func(*args, **kwargs)
                    elapsed = time.time() - start_time

                    # Registrar métricas
                    tools_generated.labels(
                        status="success",
                        type=spec.template_id
                    ).inc()

                    generation_time.labels(
                        type=spec.template_id
                    ).observe(elapsed)

                    # Atualizar span
                    span.set_attribute("tool_id", tool.tool_id)
                    span.set_attribute("generation_time_seconds", elapsed)
                    span.set_status(Status(StatusCode.OK))

                    return tool
                except Exception as e:
                    tools_generated.labels(
                        status="error",
                        type=kwargs.get("spec", {}).get("template_id", "unknown")
                    ).inc()

                    span.set_status(Status(StatusCode.ERROR))
                    span.record_exception(e)
                    raise
        return wrapper
```

### Instructions Relacionadas
- `observabilidade.instructions.md`: Padrões de métricas e traces
- `python-mcp.instructions.md`: Tratamento de erros e estrutura

## 7. API para Auto-Extensão

**Arquivo:** `src/presentation/api/routers/auto_extension.py`

### Descrição
Implementa os endpoints de API para interação com o sistema de auto-extensão.

### Conteúdo

```python
from fastapi import APIRouter, Depends, HTTPException, Body
from typing import List, Dict, Any
from pydantic import BaseModel, Field

# Modelos de dados
class CapabilityGapResponse(BaseModel):
    capability_type: str
    description: str
    severity: float
    frequency: float
    examples: List[str]
    potential_solutions: List[str]

class ToolSpecRequest(BaseModel):
    name: str = Field(..., description="Nome da tool")
    description: str = Field(..., description="Descrição da funcionalidade")
    parameters: Dict[str, Any] = Field(..., description="Parâmetros de entrada")
    return_type: str = Field(..., description="Tipo de retorno")
    template_id: str = Field(..., description="ID do template a ser usado")

class ToolResponse(BaseModel):
    tool_id: str
    name: str
    description: str
    version: str
    created_at: str
    status: str

# Router
router = APIRouter(
    prefix="/auto-extension",
    tags=["auto-extension"],
    responses={404: {"description": "Não encontrado"}},
)

@router.get("/capabilities/gaps", response_model=List[CapabilityGapResponse])
async def get_capability_gaps(
    service: CapabilityAnalysisService = Depends(get_capability_analysis_service)
):
    """Retorna as lacunas de capacidade identificadas no sistema."""
    try:
        gaps = await service.analyze_capabilities()

        return [
            CapabilityGapResponse(
                capability_type=gap.capability_type.value,
                description=gap.description,
                severity=gap.severity,
                frequency=gap.frequency,
                examples=gap.examples,
                potential_solutions=gap.potential_solutions
            )
            for gap in gaps
        ]
    except Exception as e:
        logger.error("Error getting capability gaps", exc_info=e)
        raise HTTPException(
            status_code=500,
            detail="Erro ao analisar capacidades do sistema"
        )

@router.post("/tools", response_model=ToolResponse)
async def generate_tool(
    spec: ToolSpecRequest = Body(...),
    service: ToolGenerationService = Depends(get_tool_generation_service)
):
    """Gera uma nova tool baseada na especificação fornecida."""
    try:
        # Converter para domínio
        domain_spec = ToolSpec(
            name=spec.name,
            description=spec.description,
            parameters=spec.parameters,
            return_type=spec.return_type,
            template_id=spec.template_id,
            security_level="standard",  # Default
            resource_requirements={"memory_mb": 512, "timeout_seconds": 30}  # Default
        )

        # Gerar tool
        tool = await service.generate_tool(domain_spec)

        # Converter resposta
        return ToolResponse(
            tool_id=tool.tool_id,
            name=tool.name,
            description=tool.spec.description,
            version=tool.version,
            created_at=tool.created_at,
            status="ready" if tool.validation_results.get("passed", False) else "failed"
        )
    except Exception as e:
        logger.error("Error generating tool", exc_info=e)
        raise HTTPException(
            status_code=500,
            detail="Erro ao gerar nova ferramenta"
        )
```

### Dependências
- FastAPI
- Pydantic para validação de dados

### Instructions Relacionadas
- `api-security.instructions.md`: Validação de entrada
- `python-mcp.instructions.md`: Estrutura de API

## 8. Testes Unitários

**Arquivo:** `tests/unit/domain/auto_extension/test_capability_analyzer.py`

### Descrição
Implementa testes unitários para o analisador de capacidades.

### Conteúdo

```python
import pytest
from unittest.mock import AsyncMock, MagicMock
from src.domain.auto_extension.capability_analyzer import CapabilityAnalyzer, CapabilityGap, CapabilityType

@pytest.fixture
def metrics_provider():
    provider = AsyncMock()
    provider.get_performance_metrics.return_value = {
        "response_times": {
            "data_processing": {"avg": 120, "p95": 350, "p99": 500},
            "text_generation": {"avg": 50, "p95": 150, "p99": 250},
        },
        "error_rates": {
            "data_processing": 0.05,
            "text_generation": 0.02,
        },
        "usage_counts": {
            "data_processing": 1000,
            "text_generation": 500,
        }
    }
    return provider

@pytest.fixture
def feedback_provider():
    provider = AsyncMock()
    provider.get_recent_feedback.return_value = [
        {
            "type": "limitation",
            "area": "data_processing",
            "description": "Não consegue processar arquivos grandes",
            "severity": 0.8,
            "user_id": "user-123",
            "timestamp": "2023-01-01T12:00:00Z"
        },
        {
            "type": "suggestion",
            "area": "text_generation",
            "description": "Melhorar a geração de texto técnico",
            "severity": 0.6,
            "user_id": "user-456",
            "timestamp": "2023-01-02T13:00:00Z"
        }
    ]
    return provider

@pytest.fixture
def analyzer(metrics_provider, feedback_provider):
    analyzer = CapabilityAnalyzer(metrics_provider, feedback_provider)
    # Mock do método privado para simplificar o teste
    analyzer._identify_gaps = MagicMock()
    analyzer._identify_gaps.return_value = [
        CapabilityGap(
            capability_type=CapabilityType.DATA_PROCESSING,
            description="Limitação no processamento de arquivos grandes",
            severity=0.8,
            frequency=0.3,
            examples=["Processamento de CSV com mais de 1GB"],
            potential_solutions=["Implementar processamento em chunks", "Usar streaming"]
        ),
        CapabilityGap(
            capability_type=CapabilityType.TEXT_GENERATION,
            description="Fraco em textos técnicos",
            severity=0.6,
            frequency=0.2,
            examples=["Documentação técnica", "Código com comentários"],
            potential_solutions=["Fine-tuning em corpora técnico", "Uso de exemplares"]
        )
    ]
    return analyzer

@pytest.mark.asyncio
async def test_analyze_capabilities(analyzer, metrics_provider, feedback_provider):
    # Arrange - já feito via fixtures

    # Act
    gaps = await analyzer.analyze_capabilities()

    # Assert
    assert len(gaps) == 2
    assert gaps[0].capability_type == CapabilityType.DATA_PROCESSING
    assert gaps[1].capability_type == CapabilityType.TEXT_GENERATION

    # Verify métricas e feedback foram acessados
    metrics_provider.get_performance_metrics.assert_called_once()
    feedback_provider.get_recent_feedback.assert_called_once()

    # Verify identificação de gaps foi chamada com os args corretos
    analyzer._identify_gaps.assert_called_once()
    metrics, feedback = analyzer._identify_gaps.call_args[0]
    assert metrics == metrics_provider.get_performance_metrics.return_value
    assert feedback == feedback_provider.get_recent_feedback.return_value

@pytest.mark.asyncio
async def test_analyze_capabilities_error_handling(analyzer, metrics_provider):
    # Arrange
    metrics_provider.get_performance_metrics.side_effect = Exception("Falha ao obter métricas")

    # Act/Assert
    with pytest.raises(Exception) as e:
        await analyzer.analyze_capabilities()

    assert "Falha ao obter métricas" in str(e.value)
```

### Instructions Relacionadas
- `test.instructions.md`: Padrões de testes
- `python-mcp.instructions.md`: Estrutura de testes

## 9. Documentação de Uso

**Arquivo:** `docs/auto_extension/usage.md`

### Descrição
Fornece documentação sobre o uso do sistema de auto-extensão.

### Conteúdo

```markdown
# Guia de Uso do Sistema de Auto-Extensão

## Visão Geral

O Sistema de Auto-Extensão permite que o SkyHAL identifique suas próprias limitações e crie novas ferramentas (tools) para superá-las. Este documento explica como utilizar este sistema.

## Fluxo Básico de Uso

1. **Análise de Capacidades**
   - O sistema analisa periodicamente suas capacidades
   - Lacunas são identificadas baseadas em métricas e feedback

2. **Geração de Tools**
   - Para cada lacuna, uma especificação de tool é criada
   - O gerador cria o código da tool baseado na especificação
   - A tool é validada em ambiente sandbox

3. **Integração e Uso**
   - Tools validadas são registradas no sistema
   - As tools podem ser usadas como qualquer outra ferramenta

## API de Uso

### Análise Manual de Capacidades

Você pode iniciar uma análise manual de capacidades:

```bash
curl -X GET "http://api.skyhal.com/auto-extension/capabilities/gaps" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <seu-token>"
```

### Criação Manual de Tool

Você pode criar uma tool manualmente:

```bash
curl -X POST "http://api.skyhal.com/auto-extension/tools" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <seu-token>" \
  -d '{
    "name": "csv_processor",
    "description": "Processa arquivos CSV grandes",
    "parameters": {
      "file_path": {"type": "string", "description": "Caminho para o arquivo CSV"},
      "batch_size": {"type": "integer", "description": "Tamanho do batch para processamento"}
    },
    "return_type": "array",
    "template_id": "data_processor_v1"
  }'
```

## Monitoramento

O sistema possui dashboards específicos no Grafana:

- **Dashboard de Capacidades**: Mostra lacunas identificadas
- **Dashboard de Geração**: Métricas de geração e validação de tools
- **Dashboard de Uso**: Estatísticas de uso das tools geradas

## Troubleshooting

### Problemas Comuns

#### Tool não é gerada

Causas possíveis:
- Especificação incompleta
- Template não encontrado
- Falha na geração de código

Solução:
1. Verifique logs com `tool_generation_failed`
2. Revise a especificação da tool
3. Verifique disponibilidade do template

#### Tool falha na validação

Causas possíveis:
- Problemas de segurança no código
- Falha nos testes automatizados
- Uso excessivo de recursos

Solução:
1. Verifique relatório de validação
2. Revise logs com `tool_validation_failed`
3. Ajuste parâmetros de recursos ou permissões
```

### Instructions Relacionadas
- `documentation.instructions.md`: Padrões de documentação
- `troubleshooting.instructions.md`: Guias de solução de problemas
