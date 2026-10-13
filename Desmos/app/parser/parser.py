from .validator import validate_expression

def parse_expression(expression):
    expression = expression.strip()
    if "=" in expression:
        left, right = expression.split("=", 1)
        # This project currently graphs functions of x (y = expression).
        if left.strip() not in ("y", "f(x)"):
            raise ValueError("Only equations of the form y = expression are supported")
        expression = right
    expression = expression.strip()
    if not validate_expression(expression):
        raise ValueError("Invalid or unsupported mathematical expression")
    return expression
