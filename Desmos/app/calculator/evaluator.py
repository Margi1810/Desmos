import math

def preprocess_expression(expression):
    """Normalize a user-entered mathematical expression."""
    expression = str(expression).replace(" ", "")
    expression = expression.replace("^", "**")
    return expression

def evaluate_expression(expression, x):
    """Evaluate an expression for a particular x; return an error string if invalid."""
    try:
        expression = preprocess_expression(expression)
        variables = {name: value for name, value in vars(math).items() if not name.startswith("_")}
        variables.update({"x": x, "abs": abs, "round": round, "min": min, "max": max})
        # Keep evaluation away from built-ins and permit only known math names.
        return eval(expression, {"__builtins__": {}}, variables)
    except Exception as e:
        return f"Error evaluating expression: {e}"

def generate_points(expression, x_values):
    points = []
    for x in x_values:
        y = evaluate_expression(expression, x)
        if isinstance(y, (int, float)) and math.isfinite(y):
            points.append((x, y))
    return points
