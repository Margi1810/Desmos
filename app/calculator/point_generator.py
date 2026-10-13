"""Sampling utilities for graphing functions."""
import math
from .evaluator import generate_points

def generate_x_values(x_min, x_max, step):
    if not all(math.isfinite(v) for v in (x_min, x_max, step)):
        raise ValueError("bounds and step must be finite numbers")
    if step <= 0:
        raise ValueError("step must be greater than zero")
    if x_min > x_max:
        raise ValueError("x_min must be less than or equal to x_max")
    count = int(math.floor((x_max - x_min) / step + 1e-10))
    if count > 1_000_000:
        raise ValueError("Too many sample points; increase the step size")
    return [round(x_min + i * step, 10) for i in range(count + 1)]

def create_points(expression, x_min, x_max, step):
    x_values = generate_x_values(x_min, x_max, step)
    return generate_points(expression, x_values)
