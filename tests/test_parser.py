
import unittest

from app.parser.parser import parse_expression
from app.parser.validator import validate_expression


class TestParser(unittest.TestCase):

    def test_remove_spaces(self):
        result = parse_expression("  x^2 + 3  ")
        self.assertEqual(result, "x^2 + 3")

    def test_parse_equation(self):
        result = parse_expression("y = x^2 + 3")
        self.assertEqual(result, "x^2 + 3")

    def test_parse_equation_with_spaces(self):
        result = parse_expression(" y = x^2 + 3 ")
        self.assertEqual(result, "x^2 + 3")

    def test_valid_expression(self):
        expression = parse_expression("y = x^2 + 3")
        self.assertTrue(validate_expression(expression))

    def test_invalid_expression(self):
        expression = parse_expression("x +")
        self.assertFalse(validate_expression(expression))


if __name__ == "__main__":
    unittest.main()