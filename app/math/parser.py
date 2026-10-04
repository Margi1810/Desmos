"""
Mathematical expression parser for PyDesmos using SymPy.
"""

from typing import Any, Set
import sympy
from sympy.parsing.sympy_parser import (
    parse_expr,
    standard_transformations,
    implicit_multiplication_application,
    convert_xor,
)

from app.utils.validators import sanitize_expression_string, validate_expression_syntax


class ExpressionParseError(Exception):
    """Raised when an expression cannot be parsed into a valid mathematical function."""
    pass


class ExpressionParser:
    """Parses raw user input strings into SymPy symbolic expressions."""

    ALLOWED_SYMBOLS: Set[str] = {"x", "pi", "e", "E"}

    TRANSFORMATIONS = standard_transformations + (
        implicit_multiplication_application,
        convert_xor,
    )

    @classmethod
    def parse(cls, expr_text: str) -> sympy.Expr:
        """
        Parse a mathematical expression string into a SymPy expression in terms of 'x'.

        Args:
            expr_text: Raw input string from the user (e.g. 'y = x^2', 'sin(x)', '2x+1')

        Returns:
            SymPy Expr object.

        Raises:
            ExpressionParseError: If syntax is invalid, contains undefined variables, etc.
        """
        if not expr_text or not expr_text.strip():
            raise ExpressionParseError("Expression is empty.")

        # Step 1: Pre-validation
        is_valid, error_msg = validate_expression_syntax(expr_text)
        if not is_valid:
            raise ExpressionParseError(error_msg)

        # Step 2: Sanitization
        clean_text = sanitize_expression_string(expr_text)
        if not clean_text:
            raise ExpressionParseError("Expression contains no mathematical content.")

        # Step 3: SymPy parsing
        try:
            # Provide local math constants and variable x
            x = sympy.Symbol("x")
            local_dict = {
                "x": x,
                "pi": sympy.pi,
                "e": sympy.E,
                "E": sympy.E,
                "sin": sympy.sin,
                "cos": sympy.cos,
                "tan": sympy.tan,
                "sec": sympy.sec,
                "csc": sympy.csc,
                "cot": sympy.cot,
                "asin": sympy.asin,
                "acos": sympy.acos,
                "atan": sympy.atan,
                "arcsin": sympy.asin,
                "arccos": sympy.acos,
                "arctan": sympy.atan,
                "sinh": sympy.sinh,
                "cosh": sympy.cosh,
                "tanh": sympy.tanh,
                "sqrt": sympy.sqrt,
                "exp": sympy.exp,
                "log": sympy.log,
                "ln": sympy.log,
                "abs": sympy.Abs,
            }

            parsed = parse_expr(
                clean_text,
                local_dict=local_dict,
                transformations=cls.TRANSFORMATIONS,
                evaluate=True,
            )

        except Exception as e:
            raise ExpressionParseError(f"Syntax error: {str(e)}")

        # Step 4: Validate free symbols (only 'x' is allowed as variable)
        free_symbols = {sym.name for sym in parsed.free_symbols}
        unknown_symbols = free_symbols - {"x"}
        if unknown_symbols:
            symbols_str = ", ".join(sorted(unknown_symbols))
            raise ExpressionParseError(
                f"Unknown variable(s): {symbols_str}. Only 'x' is supported."
            )

        return parsed
