
import unittest

from app.calculator.evaluator import evaluate_expression, generate_points
from app.calculator.point_generator import generate_x_values, create_points


class TestCalculator(unittest.TestCase):

    def test_evaluate_expression(self):
        result = evaluate_expression("x**2", 3)
        self.assertEqual(result, 9)

    def test_evaluate_with_power_symbol(self):
        result = evaluate_expression("x^2", 4)
        self.assertEqual(result, 16)

    def test_evaluate_sine(self):
        result = evaluate_expression("sin(x)", 0)
        self.assertEqual(result, 0)

    def test_generate_x_values(self):
        result = generate_x_values(-2, 2, 1)
        self.assertEqual(result, [-2, -1, 0, 1, 2])

    def test_generate_points(self):
        result = generate_points("x**2", [-2, -1, 0, 1, 2])
        expected = [(-2, 4), (-1, 1), (0, 0), (1, 1), (2, 4)]
        self.assertEqual(result, expected)

    def test_create_points(self):
        result = create_points("x^2", -2, 2, 1)
        expected = [(-2, 4), (-1, 1), (0, 0), (1, 1), (2, 4)]
        self.assertEqual(result, expected)

    def test_invalid_expression(self):
        result = evaluate_expression("x +", 2)
        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()