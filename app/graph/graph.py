from ..calculator.point_generator import create_points
from ..models.equation import Equation
from ..parser.parser import parse_expression
from .viewport import viewport
from .grid import grid
from .axes import axes

class Graph:
    """Coordinates equation parsing, point generation, and graph rendering."""

    def __init__(self, x_min=-10, x_max=10, y_min=-10, y_max=10, grid_spacing=1):
        self.viewport = viewport(x_min, x_max, y_min, y_max)
        self.grid = grid(x_min, x_max, y_min, y_max, grid_spacing)
        self.axes = axes(self.viewport, self.grid)
        self.equations = []

    def add_equation(self, expression, step=0.1):
        equation = Equation(expression)
        try:
            parsed = parse_expression(expression)
            equation.expression = parsed
            equation.set_points(create_points(parsed, self.viewport.x_min,
                                               self.viewport.x_max, step))
        except (ValueError, TypeError) as error:
            equation.set_error(str(error))
        self.equations.append(equation)
        return equation

    def remove_equation(self, equation):
        if equation in self.equations:
            self.equations.remove(equation)

    def clear_equations(self):
        self.equations.clear()

    def refresh_equation(self, equation, step=0.1):
        parsed = parse_expression(equation.expression)
        points = create_points(parsed, self.viewport.x_min, self.viewport.x_max, step)
        equation.set_points(points)
        return equation.points

    def zoom_in(self, factor=0.8):
        self.viewport.zoom_in(factor)
        self._update_components()

    def zoom_out(self, factor=1.25):
        self.viewport.zoom_out(factor)
        self._update_components()

    def pan(self, dx=0, dy=0):
        self.viewport.pan(dx, dy)
        self._update_components()

    def _update_components(self):
        self.grid.update_viewport(self.viewport)
        self.axes.update_viewport(self.viewport)
        for equation in self.equations:
            try:
                self.refresh_equation(equation)
            except (ValueError, TypeError) as error:
                equation.set_error(str(error))

    def draw(self, ax=None):
        """Draw on a supplied Matplotlib Axes; create one if omitted."""
        import matplotlib.pyplot as plt
        if ax is None:
            _, ax = plt.subplots()
        self.grid.draw(ax)
        self.axes.draw(ax)
        for equation in self.equations:
            if equation.visible and equation.points:
                xs = [point[0] for point in equation.points]
                ys = [point[1] for point in equation.points]
                ax.plot(xs, ys, label=equation.expression)
        if any(e.visible and e.points for e in self.equations):
            ax.legend()
        ax.set_aspect("auto")
        return ax

    def show(self):
        import matplotlib.pyplot as plt
        self.draw()
        plt.show()

# Preserve the lowercase name style used by the existing project.
graph = Graph
