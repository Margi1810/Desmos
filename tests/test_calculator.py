import unittest
from app.calculator.evaluator import evaluate_expression, generate_points
from app.calculator.point_generator import generate_x_values, create_points

class CalculatorTests(unittest.TestCase):
    def test_evaluate(self):
        self.assertAlmostEqual(evaluate_expression("sin(pi/2)", 0), 1)
        self.assertEqual(evaluate_expression("x^2", 3), 9)

    def test_reject_code(self):
        self.assertIsInstance(evaluate_expression("__import__('os')", 0), str)

    def test_points_skip_domain_errors(self):
        points = generate_points("sqrt(x)", [-1, 0, 1])
        self.assertEqual(points, [(0, 0.0), (1, 1.0)])

    def test_x_values(self):
        self.assertEqual(generate_x_values(0, 1, 0.5), [0, 0.5, 1])
        with self.assertRaises(ValueError):
            generate_x_values(0, 1, 0)

    def test_create_points(self):
        self.assertEqual(create_points("x", -1, 1, 1), [(-1, -1), (0, 0), (1, 1)])

if __name__ == "__main__":
    unittest.main()
