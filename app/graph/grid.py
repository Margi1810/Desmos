import math

class grid:
    def __init__(self, x_min=-50, x_max=50, y_min=-50, y_max=50, grid_spacing=1):
        if grid_spacing <= 0 or not math.isfinite(grid_spacing):
            raise ValueError("grid_spacing must be a positive finite number")
        if x_min >= x_max or y_min >= y_max:
            raise ValueError("Minimum bounds must be smaller than maximum bounds")
        self.x_min, self.x_max = x_min, x_max
        self.y_min, self.y_max = y_min, y_max
        self.grid_spacing = grid_spacing
        self.visible = True

    def get_vertical_lines(self):
        start = math.ceil(self.x_min / self.grid_spacing)
        end = math.floor(self.x_max / self.grid_spacing)
        return [i * self.grid_spacing for i in range(start, end + 1)]

    def get_horizontal_lines(self):
        start = math.ceil(self.y_min / self.grid_spacing)
        end = math.floor(self.y_max / self.grid_spacing)
        return [i * self.grid_spacing for i in range(start, end + 1)]

    def update_viewport(self, viewport):
        self.x_min, self.x_max = viewport.x_min, viewport.x_max
        self.y_min, self.y_max = viewport.y_min, viewport.y_max

    def draw(self, ax):
        if not self.visible:
            return
        ax.set_xticks(self.get_vertical_lines())
        ax.set_yticks(self.get_horizontal_lines())
        ax.grid(True, which="major", linewidth=0.5, alpha=0.35)
