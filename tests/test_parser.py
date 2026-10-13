import unittest
from app.parser.parser import parse_expression
from app.parser.validator import validate_expression

class ParserTests(unittest.TestCase):
    def test_parse_prefix(self):
        self.assertEqual(parse_expression(" y = x^2 "), "x^2")
        self.assertEqual(parse_expression("sin(x)"), "sin(x)")

    def test_reject_invalid_equations(self):
        for expression in ("", "x = 2", "y = ", "y = x; import os", "y = __import__('os')"):
            with self.subTest(expression=expression):
                with self.assertRaises((ValueError, TypeError)):
                    parse_expression(expression)

    def test_validator(self):
        self.assertTrue(validate_expression("cos(x) + pi"))
        self.assertFalse(validate_expression("x.__class__"))
        self.assertFalse(validate_expression("open('file')"))

if __name__ == "__main__":
    unittest.main()
