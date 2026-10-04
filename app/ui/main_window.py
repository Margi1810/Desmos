"""
MainWindow defines the top-level PyDesmos GUI layout and subcomponent wiring.
"""

from typing import Optional
import tkinter as tk
from tkinter import ttk

from app.models.graph_state import GraphState
from app.graph.viewport import Viewport
from app.graph.graph_controller import GraphController
from app.graph.graph_view import GraphView
from app.ui.expression_panel import ExpressionPanel
from app.ui.toolbar import Toolbar
from app.utils.constants import (
    APP_TITLE,
    APP_WIDTH,
    APP_HEIGHT,
    APP_MIN_WIDTH,
    APP_MIN_HEIGHT,
    TOOLBAR_BG_COLOR,
    FONT_MAIN,
)


class MainWindow:
    """Main application window layout manager."""

    def __init__(
        self,
        root: tk.Tk,
        state: GraphState,
        viewport: Viewport,
        controller: GraphController,
    ) -> None:
        self.root = root
        self.state = state
        self.viewport = viewport
        self.controller = controller

        self._configure_window()
        self._build_layout()

    def _configure_window(self) -> None:
        """Set window title, sizing, and theme."""
        self.root.title(APP_TITLE)
        self.root.geometry(f"{APP_WIDTH}x{APP_HEIGHT}")
        self.root.minsize(APP_MIN_WIDTH, APP_MIN_HEIGHT)
        self.root.configure(bg="#ffffff")

    def _build_layout(self) -> None:
        """Assemble top toolbar, sidebar, graph view, and status bar."""
        # 1. Top Toolbar
        self.toolbar = Toolbar(
            self.root,
            on_zoom_in=self.controller.zoom_in,
            on_zoom_out=self.controller.zoom_out,
            on_reset_view=self.controller.reset_view,
            on_toggle_grid=self.controller.toggle_grid,
            on_toggle_axes=self.controller.toggle_axes,
            on_add_preset=self._handle_add_preset,
        )
        self.toolbar.pack(side=tk.TOP, fill=tk.X)

        # 2. Status Bar at bottom
        self.status_bar = tk.Frame(self.root, bg=TOOLBAR_BG_COLOR, bd=1, relief=tk.SUNKEN, padx=8, pady=3)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

        self.coord_label = tk.Label(
            self.status_bar,
            text="Coordinates: (x: 0.00, y: 0.00)",
            font=("Consolas", 9),
            bg=TOOLBAR_BG_COLOR,
            fg="#495057",
        )
        self.coord_label.pack(side=tk.LEFT)

        self.zoom_label = tk.Label(
            self.status_bar,
            text="X-Range: [-10.0, 10.0]  Y-Range: [-10.0, 10.0]",
            font=("Consolas", 9),
            bg=TOOLBAR_BG_COLOR,
            fg="#495057",
        )
        self.zoom_label.pack(side=tk.RIGHT)

        # 3. Main Center Split Container (Sidebar + Graph Canvas)
        self.center_pane = tk.PanedWindow(self.root, orient=tk.HORIZONTAL, bg="#dee2e6", sashwidth=4)
        self.center_pane.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Left: Expression Panel (Sidebar)
        self.expression_panel = ExpressionPanel(
            self.center_pane,
            state=self.state,
            on_expression_change=self.controller.request_redraw,
            width=320,
        )
        self.center_pane.add(self.expression_panel, minsize=260, width=320)

        # Right: Graph View (Matplotlib Canvas)
        self.graph_view = GraphView(
            self.center_pane,
            on_pan=self.controller.handle_pan,
            on_zoom=self.controller.handle_zoom,
            on_cursor_move=self._update_cursor_coords,
        )
        self.center_pane.add(self.graph_view, minsize=400)

        # Connect graph view to controller
        self.controller.attach_view(self.graph_view)

        # Listen to viewport changes to update status label
        self.viewport.add_listener(self._update_viewport_status)
        self._update_viewport_status()

    def _update_cursor_coords(self, x: float, y: float) -> None:
        self.coord_label.config(text=f"Coordinates: (x: {x:+.3f}, y: {y:+.3f})")

    def _update_viewport_status(self) -> None:
        x_min, x_max = self.viewport.get_x_range()
        y_min, y_max = self.viewport.get_y_range()
        self.zoom_label.config(text=f"X: [{x_min:+.2f}, {x_max:+.2f}]  Y: [{y_min:+.2f}, {y_max:+.2f}]")

    def _handle_add_preset(self, preset_expr: str) -> None:
        self.expression_panel.add_new_expression(preset_expr)
        self.controller.request_redraw()
