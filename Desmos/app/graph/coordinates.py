class coordinates:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def to_screen(self, viewport, width, height):
        """Convert mathematical coordinates to pixel coordinates."""
        if width <= 0 or height <= 0:
            raise ValueError("width and height must be positive")
        px = (self.x - viewport.x_min) / (viewport.x_max - viewport.x_min) * width
        py = height - (self.y - viewport.y_min) / (viewport.y_max - viewport.y_min) * height
        return px, py

    @staticmethod
    def from_screen(px, py, viewport, width, height):
        if width <= 0 or height <= 0:
            raise ValueError("width and height must be positive")
        x = viewport.x_min + (px / width) * (viewport.x_max - viewport.x_min)
        y = viewport.y_min + ((height - py) / height) * (viewport.y_max - viewport.y_min)
        return coordinates(x, y)

    def __repr__(self):
        return f"coordinates(x={self.x}, y={self.y})"
