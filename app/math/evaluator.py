"""
Vectorized numerical expression evaluator for PyDesmos using NumPy.
"""

from typing import Callable, Optional
import numpy as np
import sympy


class ExpressionEvaluator:
    """Evaluates SymPy expressions over NumPy arrays safely."""

    def __init__(self, sympy_expr: sympy.Expr) -> None:
        self.sympy_expr = sympy_expr
        self._compiled_fn: Optional[Callable] = None
        self._compile()

    def _compile(self) -> None:
        """Compile SymPy expression to a high-speed vectorized NumPy function."""
        x = sympy.Symbol("x")
        # Custom modules dict to ensure smooth NumPy evaluations
        custom_modules = [
            {
                "log": np.log,
                "ln": np.log,
                "sin": np.sin,
                "cos": np.cos,
                "tan": np.tan,
                "sqrt": np.sqrt,
                "exp": np.exp,
                "Abs": np.abs,
                "abs": np.abs,
            },
            "numpy",
        ]
        self._compiled_fn = sympy.lambdify(x, self.sympy_expr, modules=custom_modules)

    def evaluate(self, x_values: np.ndarray) -> np.ndarray:
        """
        Safely evaluate the expression over an array of x values.

        Returns:
            np.ndarray of floats (with NaNs for undefined points).
        """
        if self._compiled_fn is None:
            return np.full_like(x_values, np.nan, dtype=float)

        try:
            # Suppress runtime warnings for division by zero or invalid sqrt values
            with np.errstate(all="ignore"):
                y_values = self._compiled_fn(x_values)

            # If the expression was constant (e.g., y = 4), lambdify returns a scalar number
            if np.isscalar(y_values) or not isinstance(y_values, np.ndarray):
                y_values = np.full_like(x_values, float(y_values), dtype=float)
            else:
                y_values = np.asarray(y_values, dtype=float)
                # If shapes don't match, broadcast
                if y_values.shape != x_values.shape:
                    y_values = np.broadcast_to(y_values, x_values.shape).copy()

            # Replace infinite values or complex conversions with NaN
            y_values[~np.isfinite(y_values)] = np.nan

            return y_values

        except Exception:
            # Fallback for piecewise or evaluation failures
            result = np.full_like(x_values, np.nan, dtype=float)
            for i, x_val in enumerate(x_values):
                try:
                    val = float(self.sympy_expr.evalf(subs={sympy.Symbol("x"): x_val}))
                    if np.isfinite(val):
                        result[i] = val
                except Exception:
                    pass
            return result

    @staticmethod
    def filter_discontinuities(
        y_values: np.ndarray, y_min: float, y_max: float, threshold_factor: float = 10.0
    ) -> np.ndarray:
        """
        Insert NaNs where extreme derivative jumps occur (e.g., tan(x), 1/x asymptotes)
        so matplotlib does not connect vertical lines across asymptotes.
        """
        y_clean = y_values.copy()
        y_span = abs(y_max - y_min)
        max_jump = y_span * threshold_factor

        diffs = np.abs(np.diff(y_clean))
        # Find indices where jump is huge and crosses opposite signs
        huge_jumps = np.where(diffs > max_jump)[0]

        for idx in huge_jumps:
            # If values on either side have opposite sign or one is near vertical
            if idx + 1 < len(y_clean):
                if y_clean[idx] * y_clean[idx + 1] < 0 or abs(y_clean[idx]) > y_span:
                    y_clean[idx + 1] = np.nan

        return y_clean
