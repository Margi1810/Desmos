from .validator import validate_expression

def parse_expression(expression):
    if not isinstance(expression, str):
        raise TypeError("Expression must be text")
    expression = expression.strip()
    if not expression:
        raise ValueError("Expression cannot be empty")
    if "=" in expression:
        if expression.count("=") != 1:
            raise ValueError("Only one equals sign is supported")
        left, right = expression.split("=", 1)
        # This project currently graphs functions of x (y = expression).
        if left.strip() not in ("y", "f(x)"):
            raise ValueError("Only equations of the form y = expression are supported")
        expression = right.strip()
    expression = expression.strip()
    if not validate_expression(expression):
        raise ValueError("Invalid or unsupported mathematical expression")
    return expression
