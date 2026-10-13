import ast
from ..calculator.evaluator import preprocess_expression

_ALLOWED_FUNCTIONS = {
    "sin", "cos", "tan", "asin", "acos", "atan", "atan2",
    "sinh", "cosh", "tanh", "sqrt", "log", "log10", "log2",
    "exp", "fabs", "floor", "ceil", "degrees", "radians",
    "factorial", "comb", "perm", "abs", "round", "min", "max"
}
_ALLOWED_NAMES = _ALLOWED_FUNCTIONS | {"x", "pi", "e", "tau", "inf"}

def validate_expression(expression):
    """Return True only for syntactically valid, supported math expressions."""
    try:
        expression = preprocess_expression(expression)
        if not expression:
            return False
        tree = ast.parse(expression, mode="eval")
        allowed_nodes = (ast.Expression, ast.Load, ast.Constant, ast.BinOp,
                         ast.UnaryOp, ast.Add, ast.Sub, ast.Mult, ast.Div,
                         ast.FloorDiv, ast.Mod, ast.Pow, ast.UAdd, ast.USub,
                         ast.Call, ast.Name)
        for node in ast.walk(tree):
            if not isinstance(node, allowed_nodes):
                return False
            if isinstance(node, ast.Constant) and not isinstance(node.value, (int, float)):
                return False
            if isinstance(node, ast.Name) and node.id not in _ALLOWED_NAMES:
                return False
            if isinstance(node, ast.Call):
                if not isinstance(node.func, ast.Name) or node.func.id not in _ALLOWED_FUNCTIONS:
                    return False
                if node.keywords:
                    return False
        return True
    except (SyntaxError, TypeError, ValueError):
        return False
