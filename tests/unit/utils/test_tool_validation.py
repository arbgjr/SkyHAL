"""Testes unitários para src/utils/tool_validation.py."""

from src.utils import tool_validation


def test_analyze_tool_results_pass():
    security = {"score": 0.95, "passed": True}
    test = {"performance_score": 0.9, "passed": True}
    result, issues, recommendations = tool_validation.analyze_tool_results(
        security, test
    )
    assert result.value == "passed"
    assert issues == []
    assert "A ferramenta passou em todos os testes" in recommendations[0]


def test_analyze_tool_results_fail_security():
    security = {
        "score": 0.2,
        "passed": False,
        "issues": [{"description": "Falha de segurança crítica", "severity": "high"}],
    }
    test = {"performance_score": 0.9, "passed": True}
    result, issues, recommendations = tool_validation.analyze_tool_results(
        security, test
    )
    assert result.value == "failed_security"
    assert any("segurança" in i.get("description", "").lower() for i in issues)


def test_analyze_tool_results_fail_performance():
    security = {"score": 0.95, "passed": True}
    test = {
        "performance_score": 0.2,
        "passed": False,
        "performance_issues": [{"description": "Performance insuficiente"}],
    }
    result, issues, recommendations = tool_validation.analyze_tool_results(
        security, test
    )
    assert result.value == "failed_performance"
    assert any("performance" in i.get("description", "").lower() for i in issues)


def test_analyze_tool_results_fail_both():
    security = {
        "score": 0.1,
        "passed": False,
        "issues": [{"description": "Falha de segurança crítica", "severity": "high"}],
    }
    test = {
        "performance_score": 0.1,
        "passed": False,
        "performance_issues": [{"description": "Performance insuficiente"}],
    }
    result, issues, recommendations = tool_validation.analyze_tool_results(
        security, test
    )
    assert result.value == "failed_security"
    assert len(issues) >= 2
