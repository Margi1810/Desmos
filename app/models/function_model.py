"""
FunctionModel represents an individual mathematical function in the calculator.
"""

import uuid
from typing import Optional
import numpy as np

from app.math.expression import MathExpression
from app.utils.constants import DEFAULT_FUNCTION_COLOR


class FunctionModel:
    """Represents a single plotted mathematical expression with visual properties."""

    def __init__(
        self,
        raw_expression: str = "",
        color: str = DEFAULT_FUNCTION_COLOR,
        visible: bool = True,
        model_id: Optional[str] = None,
    ) -> None:
        self.id: str = model_id or str(uuid.uuid4())
        self.raw_expression: str = raw_expression
        self.color: str = color
        self.visible: bool = visible
        self.math_expr: Optional[MathExpression] = None

        if raw_expression:
            self.update_expression(raw_expression)

    def update_expression(self, expr_text: str) -> None:
        """Update the mathematical expression and re-parse."""
        self.raw_expression = expr_text
        if expr_text.strip():
            self.math_expr = MathExpression(expr_text)
        else:
            self.math_expr = None

    def toggle_visibility(self) -> bool:
        """Toggle graph visibility and return new state."""
        self.visible = not self.visible
        return self.visible

    def set_color(self, color: str) -> None:
        """Set the plot color for this function."""
        self.color = color

    @property
    def is_valid(self) -> bool:
        """Check if the function expression is valid."""
        return self.math_expr is not None and self.math_expr.is_valid

    @property
    def error_message(self) -> str:
        """Return the parse or validation error message, if any."""
        if self.math_expr is not None:
            return self.math_expr.error_message
        return ""

    def evaluate(self, x_values: np.ndarray, y_min: float = -10.0, y_max: float = 10.0) -> np.ndarray:
        """Evaluate the function across an array of x values."""
        if not self.visible or not self.is_valid or self.math_expr is None:
            return np.full_like(x_values, np.nan, dtype=float)
        return self.math_expr.evaluate(x_values, y_min, y_max)

    def __repr__(self) -> str:
        return f"<FunctionModel id={self.id[:6]} expr='{self.raw_expression}' visible={self.visible} color={self.color}>"
