"""
GraphView embeds a Matplotlib Figure in Tkinter to render the Cartesian plane.
"""

from typing import List, Optional, Callable, Tuple
import tkinter as tk
import numpy as np

import matplotlib
matplotlib.use("TkAgg")
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.ticker as ticker

from app.models.function_model import FunctionModel
from app.graph.viewport import Viewport
from app.utils.constants import (
    GRAPH_BG_COLOR,
    GRAPH_GRID_COLOR,
    GRAPH_GRID_MAJOR_COLOR,
    GRAPH_AXIS_COLOR,
    GRAPH_AXIS_WIDTH,
    GRAPH_LINE_WIDTH,
)


class GraphView(tk.Frame):
    """Tkinter frame hosting the interactive Matplotlib graphing canvas."""

    def __init__(
        self,
        master: tk.Widget,
        on_pan: Optional[Callable[[float, float], None]] = None,
        on_zoom: Optional[Callable[[float, Optional[Tuple[float, float]]], None]] = None,
        on_cursor_move: Optional[Callable[[float, float], None]] = None,
        **kwargs,
    ) -> None:
        super().__init__(master, bg=GRAPH_BG_COLOR, **kwargs)

        self.on_pan = on_pan
        self.on_zoom = on_zoom
        self.on_cursor_move = on_cursor_move

        # Mouse interaction states
        self._drag_start_x: Optional[float] = None
        self._drag_start_y: Optional[float] = None
        self._is_dragging: bool = False

        # Create Matplotlib Figure & Axis
        self.figure = Figure(figsize=(7, 6), dpi=100, facecolor=GRAPH_BG_COLOR)
        self.ax = self.figure.add_subplot(111, facecolor=GRAPH_BG_COLOR)

        # Create Tkinter canvas
        self.canvas = FigureCanvasTkAgg(self.figure, master=self)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(fill=tk.BOTH, expand=True)

        self._bind_events()

    def _bind_events(self) -> None:
        """Bind mouse events for interactive pan, zoom, and coordinate tracking."""
        self.canvas.mpl_connect("button_press_event", self._on_button_press)
        self.canvas.mpl_connect("button_release_event", self._on_button_release)
        self.canvas.mpl_connect("motion_notify_event", self._on_motion)
        self.canvas.mpl_connect("scroll_event", self._on_scroll)

    def _on_button_press(self, event) -> None:
        if event.button == 1 and event.xdata is not None and event.ydata is not None:
            self._is_dragging = True
            self._drag_start_x = event.xdata
            self._drag_start_y = event.ydata

    def _on_button_release(self, event) -> None:
        self._is_dragging = False
        self._drag_start_x = None
        self._drag_start_y = None

    def _on_motion(self, event) -> None:
        # Hover coordinate callback
        if event.xdata is not None and event.ydata is not None:
            if self.on_cursor_move:
                self.on_cursor_move(event.xdata, event.ydata)

        # Pan dragging
        if self._is_dragging and event.xdata is not None and event.ydata is not None:
            if self._drag_start_x is not None and self._drag_start_y is not None:
                dx = self._drag_start_x - event.xdata
                dy = self._drag_start_y - event.ydata
                if self.on_pan and (abs(dx) > 1e-7 or abs(dy) > 1e-7):
                    self.on_pan(dx, dy)

    def _on_scroll(self, event) -> None:
        if event.xdata is None or event.ydata is None:
            return

        center = (event.xdata, event.ydata)
        # Scroll up -> zoom in (factor < 1.0), Scroll down -> zoom out (factor > 1.0)
        if event.button == "up":
            zoom_factor = 0.85
        elif event.button == "down":
            zoom_factor = 1.18
        else:
            return

        if self.on_zoom:
            self.on_zoom(zoom_factor, center)

    def render(
        self,
        functions: List[FunctionModel],
        viewport: Viewport,
        show_grid: bool = True,
        show_axes: bool = True,
    ) -> None:
        """Clear and redraw the Cartesian coordinate graph."""
        self.ax.clear()

        x_min, x_max = viewport.get_x_range()
        y_min, y_max = viewport.get_y_range()

        self.ax.set_xlim(x_min, x_max)
        self.ax.set_ylim(y_min, y_max)

        # Configure Grid
        if show_grid:
            self.ax.grid(True, which="major", color=GRAPH_GRID_MAJOR_COLOR, linestyle="-", linewidth=0.7, alpha=0.8)
            self.ax.minorticks_on()
            self.ax.grid(True, which="minor", color=GRAPH_GRID_COLOR, linestyle=":", linewidth=0.5, alpha=0.6)
        else:
            self.ax.grid(False)
            self.ax.minorticks_off()

        # Configure Axes lines
        if show_axes:
            self.ax.axhline(0, color=GRAPH_AXIS_COLOR, linewidth=GRAPH_AXIS_WIDTH, zorder=2)
            self.ax.axvline(0, color=GRAPH_AXIS_COLOR, linewidth=GRAPH_AXIS_WIDTH, zorder=2)
            self.ax.tick_params(axis="both", colors=GRAPH_AXIS_COLOR, labelsize=9)
            for spine in self.ax.spines.values():
                spine.set_color(GRAPH_GRID_MAJOR_COLOR)
        else:
            self.ax.set_xticks([])
            self.ax.set_yticks([])
            for spine in self.ax.spines.values():
                spine.set_visible(False)

        # Plot all active and visible functions
        x_samples = viewport.get_x_samples()

        for func in functions:
            if not func.visible or not func.is_valid:
                continue

            y_samples = func.evaluate(x_samples, y_min=y_min, y_max=y_max)
            self.ax.plot(
                x_samples,
                y_samples,
                color=func.color,
                linewidth=GRAPH_LINE_WIDTH,
                label=func.raw_expression,
                zorder=3,
                solid_capstyle="round",
            )

        self.figure.tight_layout(pad=1.2)
        self.canvas.draw_idle()
