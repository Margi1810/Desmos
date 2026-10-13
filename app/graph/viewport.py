import math

class viewport:
    def __init__(self, x_min=-50, x_max=50, y_min=-50, y_max=50):
        self.x_min = x_min
        self.x_max = x_max
        self.y_min = y_min
        self.y_max = y_max
        self._validate_bounds()

    def _validate_bounds(self):
        if not all(math.isfinite(v) for v in (self.x_min, self.x_max, self.y_min, self.y_max)):
            raise ValueError("Viewport bounds must be finite numbers")
        if self.x_min >= self.x_max or self.y_min >= self.y_max:
            raise ValueError("Minimum bounds must be smaller than maximum bounds")

    def zoom(self, factor, center_x=None, center_y=None):
        """factor < 1 zooms in; factor > 1 zooms out."""
        if not math.isfinite(factor) or factor <= 0:
            raise ValueError("factor must be a positive finite number")
        cx = (self.x_min + self.x_max) / 2 if center_x is None else center_x
        cy = (self.y_min + self.y_max) / 2 if center_y is None else center_y
        if not math.isfinite(cx) or not math.isfinite(cy):
            raise ValueError("zoom center must be finite")
        half_x = (self.x_max - self.x_min) * factor / 2
        half_y = (self.y_max - self.y_min) * factor / 2
        self.x_min, self.x_max = cx - half_x, cx + half_x
        self.y_min, self.y_max = cy - half_y, cy + half_y
        self._validate_bounds()

    def zoom_in(self, factor=0.8):
        self.zoom(factor)

    def zoom_out(self, factor=1.25):
        self.zoom(factor)

    def pan(self, dx=0, dy=0):
        if not math.isfinite(dx) or not math.isfinite(dy):
            raise ValueError("pan offsets must be finite numbers")
        self.x_min += dx
        self.x_max += dx
        self.y_min += dy
        self.y_max += dy

    def reset(self, x_min=-50, x_max=50, y_min=-50, y_max=50):
        old = self.get_bounds()
        self.x_min, self.x_max, self.y_min, self.y_max = x_min, x_max, y_min, y_max
        try:
            self._validate_bounds()
        except ValueError:
            self.x_min, self.x_max, self.y_min, self.y_max = old
            raise

    def get_bounds(self):
        return self.x_min, self.x_max, self.y_min, self.y_max
