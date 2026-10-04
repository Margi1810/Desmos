"""
Unit tests for the expression parser.
"""

import pytest
import sympy
from app.math.parser import ExpressionParser, ExpressionParseError
from app.utils.validators import sanitize_expression_string, validate_expression_syntax


def test_sanitize_expression():
    assert sanitize_expression_string("y = x^2") == "x**2"
    assert sanitize_expression_string("f(x) = 2x + 1") == "2*x + 1"
    assert sanitize_expression_string("3sin(x)") == "3*sin(x)"
    assert sanitize_expression_string("|x - 3|") == "abs(x - 3)"
    assert sanitize_expression_string("(x+1)(x-1)") == "(x+1)*(x-1)"
    assert sanitize_expression_string("ln(x)") == "log(x)"


def test_validate_syntax():
    valid, _ = validate_expression_syntax("sin(x) + cos(x)")
    assert valid is True

    valid, err = validate_expression_syntax("((x + 1)")
    assert valid is False
    assert "Unclosed bracket" in err

    valid, err = validate_expression_syntax("x + 1)")
    assert valid is False
    assert "Mismatched closing bracket" in err

    valid, err = validate_expression_syntax("")
    assert valid is False


def test_parse_polynomial():
    expr = ExpressionParser.parse("y = x^2 + 2*x + 1")
    x = sympy.Symbol("x")
    expected = x**2 + 2*x + 1
    assert sympy.simplify(expr - expected) == 0


def test_parse_trigonometric():
    expr = ExpressionParser.parse("sin(x) + cos(2x)")
    x = sympy.Symbol("x")
    expected = sympy.sin(x) + sympy.cos(2*x)
    assert sympy.simplify(expr - expected) == 0


def test_parse_implicit_multiplication():
    expr = ExpressionParser.parse("2x(x+1)")
    x = sympy.Symbol("x")
    expected = 2 * x * (x + 1)
    assert sympy.simplify(expr - expected) == 0


def test_parse_unknown_variable_fails():
    with pytest.raises(ExpressionParseError) as excinfo:
        ExpressionParser.parse("y = a*x + b")
    assert "Unknown variable" in str(excinfo.value)


def test_parse_invalid_syntax_fails():
    with pytest.raises(ExpressionParseError):
        ExpressionParser.parse("x + * 2")
