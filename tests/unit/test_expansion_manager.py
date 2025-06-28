import os
import tempfile

import pytest

from src.application.expansion_manager import expand_and_register_tool
from src.utils import tool_registry


def test_expand_and_register_tool_success(monkeypatch):
    code = "def hello():\n    return 'world'\n"
    tool_name = "tool_test_hello"
    with tempfile.TemporaryDirectory() as tmpdir:
        # Limpa registry antes do teste
        tool_registry._tools.clear()
        module = expand_and_register_tool(code, tool_name, tmpdir)
        assert hasattr(module, "hello")
        assert callable(module.hello)
        assert module.hello() == "world"
        # Verifica registro
        assert tool_registry.get_tool(tool_name) is module
        # Arquivo existe
        assert os.path.exists(os.path.join(tmpdir, f"{tool_name}.py"))


def test_expand_and_register_tool_invalid_name():
    code = "def x(): pass"
    with tempfile.TemporaryDirectory() as tmpdir:
        with pytest.raises(ValueError):
            expand_and_register_tool(code, "123abc", tmpdir)


def test_expand_and_register_tool_conflict():
    code = "def x(): pass"
    tool_name = "tool_conflict"
    with tempfile.TemporaryDirectory() as tmpdir:
        file_path = os.path.join(tmpdir, f"{tool_name}.py")
        with open(file_path, "w") as f:
            f.write("# já existe")
        with pytest.raises(FileExistsError):
            expand_and_register_tool(code, tool_name, tmpdir)


def test_expand_and_register_tool_syntax_error():
    code = "def x(\n"  # erro de sintaxe
    tool_name = "tool_syntax_error"
    with tempfile.TemporaryDirectory() as tmpdir:
        with pytest.raises(SyntaxError):
            expand_and_register_tool(code, tool_name, tmpdir)
