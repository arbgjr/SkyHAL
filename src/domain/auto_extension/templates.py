# src/domain/auto_extension/templates.py
# Templates Python para geração de código dinâmico

templates = {
    "python_func": {
        "code": (
            "def {name}({params}):\n"
            '    """{description}\n\n'
            "    Gerado automaticamente pelo SkyHAL.\n"
            '    """\n'
            "    # TODO: implementar lógica\n"
            "    pass\n"
        )
    }
}


def get_template(template_id: str = "python_func") -> dict:
    return templates.get(template_id, templates["python_func"])
