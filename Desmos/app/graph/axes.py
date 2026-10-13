class axes:
    def __init__(self, viewport, grid):
        self.viewport = viewport
        self.grid = grid
        self.visible = True

    def draw(self, ax):
        if not self.visible:
            return
        ax.axhline(y=0, color="black", linewidth=1)
        ax.axvline(x=0, color="black", linewidth=1)
        ax.set_xlim(self.viewport.x_min, self.viewport.x_max)
        ax.set_ylim(self.viewport.y_min, self.viewport.y_max)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)

    def update_viewport(self, viewport):
        self.viewport = viewport
        if self.grid:
            self.grid.update_viewport(viewport)
