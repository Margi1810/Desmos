class Equation:
    def __init__(self, expression):
        self.expression = expression
        self.points = []
        self.error = None
        self.visible = True

    def set_points(self, points):
        self.points = list(points)
        self.error = None

    def set_error(self, error):
        self.error = str(error)
        self.points = []

    def __repr__(self):
        return f"Equation(expression={self.expression!r})"
