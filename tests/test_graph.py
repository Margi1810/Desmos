import unittest
from app.graph.graph import Graph
from app.graph.viewport import viewport
from app.graph.coordinates import coordinates

class GraphTests(unittest.TestCase):
    def test_add_and_clear(self):
        graph = Graph()
        equation = graph.add_equation("y=x^2")
        self.assertIsNone(equation.error)
        self.assertTrue(equation.points)
        graph.clear_equations()
        self.assertEqual(graph.equations, [])

    def test_bad_expression(self):
        graph = Graph()
        equation = graph.add_equation("import os")
        self.assertIsNotNone(equation.error)
        self.assertEqual(equation.points, [])

    def test_zoom_and_pan(self):
        view = viewport(-10, 10, -5, 5)
        view.zoom(0.5)
        self.assertEqual(view.get_bounds(), (-5.0, 5.0, -2.5, 2.5))
        view.pan(1, 2)
        self.assertEqual(view.get_bounds(), (-4.0, 6.0, -0.5, 4.5))

    def test_coordinate_conversion(self):
        view = viewport(-1, 1, -1, 1)
        point = coordinates(0, 0)
        self.assertEqual(point.to_screen(view, 100, 100), (50, 50))
        restored = coordinates.from_screen(50, 50, view, 100, 100)
        self.assertAlmostEqual(restored.x, 0)
        self.assertAlmostEqual(restored.y, 0)

if __name__ == "__main__":
    unittest.main()
