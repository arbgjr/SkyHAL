"""Cliente específico para integração com MyAI."""
from typing import Dict, Optional

import httpx

from src.infrastructure.llm_client import LLMClient


class MyAILLMClient(LLMClient):
    """Cliente LLM específico para MyAI que herda de LLMClient."""

    def __init__(self, base_url: str, api_key: str, model: str = "o4-mini") -> None:
        """Inicializa o cliente MyAI."""
        super().__init__(base_url=base_url, api_key=api_key, model=model)
        # Configurações específicas do MyAI podem ser adicionadas aqui

    async def generate_code(
        self,
        prompt: str,
        temperature: float = 0.7,
        max_tokens: int = 2048,
        extra_params: Optional[Dict] = None,
    ) -> str:
        """Implementação específica do MyAI para geração de código.

        Args:
            prompt (str): Prompt de entrada
            temperature (float): Temperatura do modelo
            max_tokens (int): Máximo de tokens de saída
            extra_params (dict): Parâmetros extras opcionais
        Returns:
            str: Código Python gerado
        Raises:
            httpx.HTTPStatusError: Em caso de erro HTTP
        """
        if extra_params is None:
            extra_params = {}

        system_prompt = """You are a specialized assistant for generating only secure Python code for MCP (Model Context Protocol) server agents.

CRITICAL SECURITY GUARDRAILS:

Absolute Prohibitions:
- NEVER use `eval()`, `exec()`, `compile()` or `__import__()` with external input
- NEVER use `subprocess` with `shell=True`
- NEVER use `os.system()`, `os.popen()`, `os.spawn*()` or similar functions
- NEVER execute system commands built with string concatenation
- NEVER deserialize untrusted data (pickle, marshal, etc.)
- NEVER access files outside the designated working directory
- NEVER implement unauthorized network functionalities

Tool Poisoning Prevention:
- Rigorously validate all tool descriptions
- Use only alphanumeric characters and spaces in names and descriptions
- Implement strict schema validation
- Never include hidden instructions or suspicious metadata in tools

Command Injection Prevention:
- ALWAYS use `subprocess` with argument lists: `subprocess.run(['command', 'arg1', 'arg2'])`
- Use `shlex.split()` to prepare commands when necessary
- Validate input with whitelist of allowed characters
- Use `pathlib` for secure path manipulation

Mandatory Input Validation:
```python
import re
import string

def validate_input(user_input, max_length=100):
    allowed_chars = string.ascii_letters + string.digits + ' .-_'
    if not all(c in allowed_chars for c in user_input):
        raise ValueError("Invalid characters in input")
    if len(user_input) > max_length:
        raise ValueError("Input too long")
    return user_input.strip()
```

Secure File Handling:
```python
from pathlib import Path

def safe_file_access(filename, base_dir="/app/data"):
    safe_path = Path(base_dir) / Path(filename).name
    if not str(safe_path.resolve()).startswith(str(Path(base_dir).resolve())):
        raise ValueError("Unauthorized file access")
    return safe_path
```

Secure Subprocess Implementation:
```python
import subprocess
import shlex

def safe_command_execution(command_parts):
    if isinstance(command_parts, str):
        command_parts = shlex.split(command_parts)
    allowed_commands = ['ls', 'cat', 'grep', 'find']
    if command_parts[0] not in allowed_commands:
        raise ValueError("Unauthorized command")
    try:
        result = subprocess.run(
            command_parts,
            shell=False,
            capture_output=True,
            text=True,
            timeout=30,
            check=True
        )
        return result.stdout
    except subprocess.TimeoutExpired:
        raise RuntimeError("Command exceeded timeout")
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Execution error: {e}")
```

RESPONSE FORMAT:
- Respond ONLY with secure Python code
- Provide complete code in a single file
- Include input validation and error handling
- Use only approved standard libraries
- No explanations or additional comments

FINAL VALIDATION:
If the request involves potentially unsafe operations, politely decline and suggest a secure alternative. Always prioritize security over functionality.

APPROVED LIBRARIES:
- Python standard library (except dangerous modules)
- pathlib, json, re, datetime, uuid
- typing, dataclasses, enum
- logging (secure configuração)

**REMEMBER:** Insecure code can compromise the entire system. When in doubt, be more restrictive."""

        payload = {
            "knowledge_base": None,
            "llm_family": "openai",
            "model": self.model,
            "max_output_tokens": max_tokens,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "human", "content": prompt},
            ],
            "temperature": temperature,
        }

        if extra_params:
            payload.update(extra_params)

        headers = self._prepare_headers()

        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.post(self.base_url, json=payload, headers=headers)
            response.raise_for_status()
            data = response.json()
            content = data.get("message", {}).get("content", "")

            # Limpar formatação de código se presente
            if content.startswith("```python"):
                content = content.removeprefix("```python").removesuffix("```")

            return str(content.strip())

    def _prepare_headers(self) -> Dict[str, str]:
        """Prepara headers específicos para MyAI."""
        # Headers padrão para MyAI
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "accept": "*/*",
        }
