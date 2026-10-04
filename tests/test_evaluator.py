"""
Unit tests for the numerical expression evaluator.
"""

import numpy as np
import sympy
from app.math.evaluator import ExpressionEvaluator
from app.math.expression import MathExpression


def test_evaluate_polynomial():
    x = sympy.Symbol("x")
    evaluator = ExpressionEvaluator(x**2)
    x_vals = np.array([-2.0, -1.0, 0.0, 1.0, 2.0])
    y_vals = evaluator.evaluate(x_vals)
    expected = np.array([4.0, 1.0, 0.0, 1.0, 4.0])
    np.testing.assert_allclose(y_vals, expected)


def test_evaluate_constant():
    evaluator = ExpressionEvaluator(sympy.Integer(5))
    x_vals = np.array([-1.0, 0.0, 1.0])
    y_vals = evaluator.evaluate(x_vals)
    np.testing.assert_allclose(y_vals, np.array([5.0, 5.0, 5.0]))


def test_evaluate_with_nans():
    x = sympy.Symbol("x")
    evaluator = ExpressionEvaluator(sympy.sqrt(x))
    x_vals = np.array([-4.0, -1.0, 0.0, 4.0])
    y_vals = evaluator.evaluate(x_vals)
    assert np.isnan(y_vals[0])
    assert np.isnan(y_vals[1])
    assert y_vals[2] == 0.0
    assert y_vals[3] == 2.0


def test_math_expression_wrapper():
    expr = MathExpression("y = x^2 - 4")
    assert expr.is_valid is True
    x_vals = np.array([2.0, -2.0])
    y_vals = expr.evaluate(x_vals)
    np.testing.assert_allclose(y_vals, np.array([0.0, 0.0]))


def test_invalid_math_expression():
    expr = MathExpression("invalid syntax ((")
    assert expr.is_valid is False
    assert expr.error_message != ""
    x_vals = np.array([1.0, 2.0])
    y_vals = expr.evaluate(x_vals)
    assert np.all(np.isnan(y_vals))
