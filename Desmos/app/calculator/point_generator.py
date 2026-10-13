from .evaluator import generate_points

def generate_x_values(x_min, x_max, step):
    if step <= 0:
        raise ValueError("step must be greater than zero")
    if x_min > x_max:
        raise ValueError("x_min must be less than or equal to x_max")
    x_values = []
    x = x_min
    while x <= x_max + step * 1e-9:
        x_values.append(round(x, 10))
        x += step
    return x_values

def create_points(expression, x_min, x_max, step):
    x_values = generate_x_values(x_min, x_max, step)
    return generate_points(expression, x_values)
