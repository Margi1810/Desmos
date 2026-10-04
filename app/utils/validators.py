"""
Input validators and sanitizers for mathematical expressions.
"""

import re
from typing import Tuple


def sanitize_expression_string(expr_str: str) -> str:
    """
    Sanitize and normalize user mathematical input into a standard Python/SymPy format.

    Examples:
        'y = x^2' -> 'x**2'
        'f(x) = 2x + 1' -> '2*x + 1'
        '3sin(x)' -> '3*sin(x)'
        '|x - 2|' -> 'abs(x - 2)'
        '(x+1)(x-1)' -> '(x+1)*(x-1)'
    """
    if not expr_str:
        return ""

    text = expr_str.strip()

    # Remove leading 'y =' or 'y=' or 'f(x) =' or 'g(x) =' (case-insensitive)
    text = re.sub(r"^(?:y|[a-zA-Z]\([a-zA-Z]\))\s*=\s*", "", text, flags=re.IGNORECASE)

    # Convert absolute value bars |...| to abs(...)
    # Match patterns like |expr|
    text = re.sub(r"\|([^|]+)\|", r"abs(\1)", text)

    # Convert ^ to **
    text = text.replace("^", "**")

    # Insert explicit multiplication for implicit multiplication cases:
    # 1. Number followed by variable or function name: '2x' -> '2*x', '3sin(x)' -> '3*sin(x)'
    text = re.sub(r"(\d+)([a-zA-Z_]\w*)", r"\1*\2", text)

    # 2. Number followed by open parenthesis: '2(x+1)' -> '2*(x+1)'
    text = re.sub(r"(\d+)\s*\(", r"\1*(", text)

    # 3. Variable followed by open parenthesis (if not a recognized function name)
    # Recognized functions: sin, cos, tan, sec, csc, cot, asin, acos, atan, sinh, cosh, tanh,
    # sqrt, exp, log, ln, abs, floor, ceil
    known_funcs = {
        "sin", "cos", "tan", "sec", "csc", "cot",
        "asin", "acos", "atan", "arcsin", "arccos", "arctan",
        "sinh", "cosh", "tanh", "sqrt", "exp", "log", "ln", "abs",
        "floor", "ceil", "rad", "deg"
    }

    # Handle parenthesis multiplication: ')( ' -> ')*('
    text = re.sub(r"\)\s*\(", r")*(", text)

    # Handle variable/closing parenthesis followed by variable: ')x' -> ')*x', 'x x' -> 'x*x'
    text = re.sub(r"\)\s*([a-zA-Z_]\w*)", r")*\1", text)

    # Replace 'ln(' with 'log(' for standard SymPy compatibility
    text = re.sub(r"\bln\(", "log(", text)

    return text.strip()


def validate_expression_syntax(expr_str: str) -> Tuple[bool, str]:
    """
    Check if the expression string has balanced parentheses and non-empty content.

    Returns:
        (is_valid, error_message)
    """
    if not expr_str or not expr_str.strip():
        return False, "Expression cannot be empty."

    # Check parenthesis balance
    stack = []
    pairs = {")": "(", "}": "{", "]": "["}
    for char in expr_str:
        if char in "({[":
            stack.append(char)
        elif char in ")}]":
            if not stack or stack[-1] != pairs[char]:
                return False, f"Mismatched closing bracket '{char}'."
            stack.pop()

    if stack:
        return False, f"Unclosed bracket '{stack[-1]}'."

    # Check for invalid consecutive operators (e.g., '++', '**' is fine, '/*')
    if re.search(r"[/+*-]{3,}", expr_str):
        return False, "Invalid operator sequence."

    return True, ""
