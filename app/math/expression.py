"""
MathExpression model wrapping parsing and numerical evaluation.
"""

from typing import Optional
import numpy as np
import sympy

from app.math.parser import ExpressionParser, ExpressionParseError
from app.math.evaluator import ExpressionEvaluator


class MathExpression:
    """Represents a validated, parsed, and evaluatable mathematical expression."""

    def __init__(self, raw_text: str) -> None:
        self.raw_text: str = raw_text
        self.sympy_expr: Optional[sympy.Expr] = None
        self._evaluator: Optional[ExpressionEvaluator] = None
        self.is_valid: bool = False
        self.error_message: str = ""

        self._parse()

    def _parse(self) -> None:
        """Parse raw text and initialize evaluator."""
        if not self.raw_text or not self.raw_text.strip():
            self.is_valid = False
            self.error_message = "Empty expression"
            return

        try:
            self.sympy_expr = ExpressionParser.parse(self.raw_text)
            self._evaluator = ExpressionEvaluator(self.sympy_expr)
            self.is_valid = True
            self.error_message = ""
        except ExpressionParseError as e:
            self.is_valid = False
            self.error_message = str(e)
            self.sympy_expr = None
            self._evaluator = None
        except Exception as e:
            self.is_valid = False
            self.error_message = f"Error: {str(e)}"
            self.sympy_expr = None
            self._evaluator = None

    def evaluate(self, x_values: np.ndarray, y_min: float = -10.0, y_max: float = 10.0) -> np.ndarray:
        """
        Evaluate expression over an array of x values.

        Returns:
            np.ndarray of y values with discontinuities filtered.
        """
        if not self.is_valid or self._evaluator is None:
            return np.full_like(x_values, np.nan, dtype=float)

        raw_y = self._evaluator.evaluate(x_values)
        return ExpressionEvaluator.filter_discontinuities(raw_y, y_min, y_max)

    def to_latex(self) -> str:
        """Return LaTeX representation of the SymPy expression if valid."""
        if self.is_valid and self.sympy_expr is not None:
            return sympy.latex(self.sympy_expr)
        return self.raw_text

    def __repr__(self) -> str:
        return f"MathExpression('{self.raw_text}', valid={self.is_valid})"
