"""
Provedor de logging estruturado usando structlog.

Este módulo configura e fornece um logger estruturado para toda a aplicação,
seguindo as melhores práticas de observabilidade.
"""

import logging
import sys
from pathlib import Path
from typing import Any, Dict, Optional

import structlog
from pythonjsonlogger import jsonlogger


class StructuredLoggingProvider:
    """
    Provedor de logging estruturado usando structlog.

    Configura logging estruturado com saída JSON para produção
    e formato legível para desenvolvimento.
    """

    def __init__(self, config: Dict[str, Any]):
        """
        Inicializa o provedor de logging.

        Args:
            config: Configuração do logging contendo level, format, etc.
        """
        self.config = config
        self._is_configured = False

    def configure(self) -> None:
        """Configura o logging estruturado."""
        if self._is_configured:
            return

        # Configurar nível de log
        log_level = getattr(logging, self.config.get("level", "INFO").upper())

        # Configurar processadores do structlog
        processors = [
            structlog.contextvars.merge_contextvars,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.add_log_level,
            structlog.processors.StackInfoRenderer(),
            structlog.dev.set_exc_info,
        ]

        # Adicionar processador específico baseado no formato
        if self.config.get("format") == "json":
            processors.append(structlog.processors.JSONRenderer())
        else:
            processors.append(structlog.dev.ConsoleRenderer(colors=True))

        # Configurar structlog
        structlog.configure(
            processors=processors,
            wrapper_class=structlog.make_filtering_bound_logger(log_level),
            context_class=dict,
            logger_factory=structlog.PrintLoggerFactory(),
            cache_logger_on_first_use=True,
        )

        # Configurar logging padrão do Python
        self._configure_standard_logging(log_level)

        self._is_configured = True

    def _configure_standard_logging(self, log_level: int) -> None:
        """
        Configura o logging padrão do Python para trabalhar com structlog.

        Args:
            log_level: Nível de log a ser configurado.
        """
        # Configurar handler baseado no formato
        if self.config.get("format") == "json":
            formatter = jsonlogger.JsonFormatter(
                fmt="%(asctime)s %(name)s %(levelname)s %(message)s"
            )
        else:
            formatter = logging.Formatter(
                fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S",
            )

        # Configurar handler de saída
        if self.config.get("output") == "file":
            log_file = Path(self.config.get("file_path", "logs/application.log"))
            log_file.parent.mkdir(parents=True, exist_ok=True)
            handler: logging.Handler = logging.FileHandler(log_file)
        else:
            handler = logging.StreamHandler(sys.stdout)

        handler.setFormatter(formatter)
        handler.setLevel(log_level)

        # Configurar logger raiz
        root_logger = logging.getLogger()
        root_logger.setLevel(log_level)
        root_logger.handlers.clear()
        root_logger.addHandler(handler)

        # Configurar loggers específicos
        self._configure_specific_loggers()

    def _configure_specific_loggers(self) -> None:
        """Configura loggers específicos de bibliotecas."""
        # Reduzir verbosidade de bibliotecas externas
        logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
        logging.getLogger("opentelemetry").setLevel(logging.WARNING)

    def get_logger(self, name: Optional[str] = None) -> Any:
        """
        Obtém um logger estruturado.

        Args:
            name: Nome do logger. Se None, usa o nome do módulo chamador.

        Returns:
            Logger estruturado configurado.
        """
        if not self._is_configured:
            self.configure()

        return structlog.get_logger(name)

    def bind_context(self, **kwargs: Any) -> Any:
        """
        Cria um logger com contexto fixo.

        Args:
            **kwargs: Contexto a ser vinculado ao logger.

        Returns:
            Logger com contexto vinculado.
        """
        logger = self.get_logger()
        return logger.bind(**kwargs)
