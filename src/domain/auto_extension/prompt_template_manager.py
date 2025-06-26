"""
PromptTemplateManager: gerenciamento centralizado de prompts para geração de código e especificação.
Permite versionamento, customização por provider/modelo e integração com providers LLM/template.
Atende à especificação técnica em docs/especificacoes-tecnicas/llm-auto-extensao.md.
"""
from typing import Dict, Optional


class PromptTemplateManager:
    def get_template(self, provider: str, tipo: str = "code") -> dict:
        """
        Alias retrocompatível para get_prompt (usado por alguns providers).
        Sempre retorna dict com chave 'code_template'.
        """
        prompt = self.get_prompt(provider, tipo)
        if isinstance(prompt, dict):
            return prompt
        return {"code_template": prompt or "# Código gerado por template não definido"}

    def __init__(self, templates: Optional[Dict[str, Dict[str, str]]] = None):
        """
        templates: dict no formato {provider: {tipo: prompt}}
        Exemplo: {"openai": {"code": "...", "spec": "..."}}
        """
        self.templates = templates or {}

    def get_prompt(self, provider: str, tipo: str = "code") -> str:
        """
        Retorna o prompt para o provider e tipo (code/spec).
        """
        return self.templates.get(provider, {}).get(tipo, "")

    def set_prompt(self, provider: str, tipo: str, prompt: str) -> None:
        """
        Seta o prompt para o provider e tipo (code/spec).
        """
        if provider not in self.templates:
            self.templates[provider] = {}
        self.templates[provider][tipo] = prompt

    def list_providers(self) -> list[str]:
        """
        Retorna os providers disponíveis.
        """
        return list(self.templates.keys())

    def list_prompts(self, provider: str) -> list[str]:
        """
        Lista os prompts para o provider.
        """
        return list(self.templates.get(provider, {}).keys())
