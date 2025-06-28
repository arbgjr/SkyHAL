"""
Registry global de tools expandidas dinamicamente.
"""

_tools = {}


def register_tool(name: str, module: object) -> None:
    """Registra uma tool dinâmica pelo nome."""
    _tools[name] = module


def get_tool(name: str) -> object:
    """Recupera uma tool dinâmica pelo nome."""
    return _tools.get(name)
