import importlib.util
import os
from typing import Any

import structlog

logger = structlog.get_logger()


def expand_and_register_tool(code: str, tool_name: str, target_dir: str) -> Any:
    """
    Salva o código Python em disco, importa e registra a nova tool.

    Args:
        code (str): Código fonte Python gerado.
        tool_name (str): Nome da tool/módulo.
        target_dir (str): Caminho relativo do diretório de destino.

    Returns:
        Any: Referência à tool importada.
    Raises:
        Exception: Em caso de erro de escrita ou importação.
    """
    # 1. Validação
    if not tool_name.isidentifier():
        logger.error("invalid_tool_name", tool_name=tool_name)
        raise ValueError("Nome de tool inválido")
    file_path = os.path.join(target_dir, f"{tool_name}.py")
    if os.path.exists(file_path):
        logger.error("tool_already_exists", tool_name=tool_name, file_path=file_path)
        raise FileExistsError(f"Tool {tool_name} já existe")

    # 2. Salvar arquivo
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(code)
        logger.info("tool_saved", tool_name=tool_name, file_path=file_path)
    except Exception as e:
        logger.error("tool_save_failed", tool_name=tool_name, error=str(e))
        raise

    # 3. Importação dinâmica
    try:
        spec = importlib.util.spec_from_file_location(tool_name, file_path)
        if spec is None or spec.loader is None:
            logger.error("import_spec_failed", tool_name=tool_name, file_path=file_path)
            raise ImportError(f"Não foi possível criar spec para {tool_name}")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        logger.info("tool_imported", tool_name=tool_name)
    except Exception as e:
        logger.error("tool_import_failed", tool_name=tool_name, error=str(e))
        raise

    # 4. Registro (exemplo: adicionar ao registry global)
    try:
        from src.utils.tool_registry import register_tool

        register_tool(tool_name, module)
        logger.info("tool_registered", tool_name=tool_name)
    except Exception as e:
        logger.error("tool_registry_failed", tool_name=tool_name, error=str(e))
        raise

    return module
