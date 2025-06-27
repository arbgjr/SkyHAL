"""
Entidades para autoextensão LLM/Template/Hybrid.
"""
from typing import Any, Dict, List, Optional

from pydantic import BaseModel


class ToolSpec(BaseModel):
    """Especificação de ferramenta para geração automática."""

    name: str
    description: str
    parameters: Optional[List[Dict[str, Any]]] = None
    return_type: Optional[str] = None
    template_id: Optional[str] = None
    security_level: Optional[str] = None
    resource_requirements: Optional[Dict[str, Any]] = None
