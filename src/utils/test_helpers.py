"""
Funções utilitárias para testes automatizados e scripts de onboarding.
"""
import os
import shutil
import subprocess  # nosec


def command_exists(command: str) -> bool:
    """
    Verifica se um comando existe no sistema.

    Segurança: só use com comandos conhecidos e confiáveis.
    Não use com entrada de usuário sem validação.
    """
    # Usa shutil.which para evitar execução direta
    return shutil.which(command) is not None


def run_script(script_path: str) -> int:
    """
    Executa um script PowerShell e retorna o código de saída.

    Segurança: só use com caminhos de script conhecidos e confiáveis.
    Não use com entrada de usuário sem validação.
    """
    # Garante que o caminho é absoluto e o arquivo existe
    abs_path = os.path.abspath(script_path)
    if not os.path.isfile(abs_path):
        return -1
    try:
        result = subprocess.run(
            ["pwsh", "-File", abs_path], capture_output=True, shell=False  # nosec
        )
        return result.returncode
    except Exception:
        return -1
