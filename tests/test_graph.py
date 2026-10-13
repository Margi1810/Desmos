import unittest

from app.graph.viewport import viewport
from app.graph.grid import grid
from app.graph.graph import Graph
from app.graph.coordinates import coordinates
from app.graph.axes import axes


class TestGraph(unittest.TestCase):

    def test_viewport_default_values(self):
        view = viewport()

        self.assertEqual(view.x_min, -50)
        self.assertEqual(view.x_max, 50)
        self.assertEqual(view.y_min, -50)
        self.assertEqual(view.y_max, 50)

    def test_viewport_custom_values(self):
        view = viewport(-10, 10, -5, 5)

        self.assertEqual(view.x_min, -10)
        self.assertEqual(view.x_max, 10)
        self.assertEqual(view.y_min, -5)
        self.assertEqual(view.y_max, 5)

    def test_grid_default_values(self):
        graph_grid = grid()

        self.assertEqual(graph_grid.x_min, -50)
        self.assertEqual(graph_grid.x_max, 50)
        self.assertEqual(graph_grid.y_min, -50)
        self.assertEqual(graph_grid.y_max, 50)
        self.assertEqual(graph_grid.grid_spacing, 1)

    def test_grid_custom_spacing(self):
        graph_grid = grid(-10, 10, -10, 10, 2)

        self.assertEqual(graph_grid.grid_spacing, 2)

    def test_coordinates(self):
        point = coordinates(3, 4)

        self.assertEqual(point.x, 3)
        self.assertEqual(point.y, 4)

    def test_graph_stores_viewport(self):
        view = viewport()
        graph = Graph(view)

        self.assertIs(graph.viewport, view)

    def test_axes_stores_viewport_and_grid(self):
        view = viewport()
        graph_grid = grid()
        graph_axes = axes(view, graph_grid)

        self.assertIs(graph_axes.viewport, view)
        self.assertIs(graph_axes.grid, graph_grid)


if __name__ == "__main__":
    unittest.main()