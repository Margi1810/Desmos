"""Safe evaluation of supported mathematical expressions."""
import math
import operator

def preprocess_expression(expression):
    """Normalize a user-entered mathematical expression."""
    expression = str(expression).strip().replace("^", "**")
    return expression

def _safe_eval_node(node, variables):
    import ast
    if isinstance(node, ast.Expression):
        return _safe_eval_node(node.body, variables)
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value
    if isinstance(node, ast.Name):
        if node.id in variables:
            return variables[node.id]
        raise ValueError(f"Unknown name: {node.id}")
    if isinstance(node, ast.BinOp):
        operations = {ast.Add: operator.add, ast.Sub: operator.sub,
                      ast.Mult: operator.mul, ast.Div: operator.truediv,
                      ast.FloorDiv: operator.floordiv, ast.Mod: operator.mod,
                      ast.Pow: operator.pow}
        op = operations.get(type(node.op))
        if op is None:
            raise ValueError("Unsupported operator")
        left = _safe_eval_node(node.left, variables)
        right = _safe_eval_node(node.right, variables)
        if isinstance(node.op, ast.Pow) and abs(right) > 1000:
            raise ValueError("Exponent is too large")
        return op(left, right)
    if isinstance(node, ast.UnaryOp):
        if isinstance(node.op, ast.UAdd):
            return +_safe_eval_node(node.operand, variables)
        if isinstance(node.op, ast.USub):
            return -_safe_eval_node(node.operand, variables)
        raise ValueError("Unsupported unary operator")
    if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
        fn = variables.get(node.func.id)
        if not callable(fn):
            raise ValueError("Unsupported function")
        if node.keywords:
            raise ValueError("Keyword arguments are not supported")
        return fn(*[_safe_eval_node(arg, variables) for arg in node.args])
    raise ValueError("Unsupported expression")

def evaluate_expression(expression, x):
    """Evaluate an expression for a particular x; return an error string if invalid."""
    try:
        import ast
        from ..parser.validator import validate_expression
        expression = preprocess_expression(expression)
        if not validate_expression(expression):
            return "Error evaluating expression: invalid or unsupported expression"
        variables = {name: value for name, value in vars(math).items()
                     if not name.startswith("_")}
        variables.update({"x": x, "abs": abs, "round": round, "min": min, "max": max})
        return _safe_eval_node(ast.parse(expression, mode="eval"), variables)
    except Exception as e:
        return f"Error evaluating expression: {e}"

def generate_points(expression, x_values):
    points = []
    for x in x_values:
        y = evaluate_expression(expression, x)
        if isinstance(y, (int, float)) and not isinstance(y, bool) and math.isfinite(y):
            points.append((x, y))
    return points
