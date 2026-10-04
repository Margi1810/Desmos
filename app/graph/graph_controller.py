"""
GraphController acts as the mediator between GraphState, Viewport, and GraphView.
"""

from typing import Optional, Tuple
from app.models.graph_state import GraphState
from app.graph.viewport import Viewport
from app.graph.graph_view import GraphView
from app.utils.constants import ZOOM_IN_FACTOR, ZOOM_OUT_FACTOR


class GraphController:
    """Coordinates business logic and rendering between models and view."""

    def __init__(self, state: GraphState, viewport: Viewport) -> None:
        self.state = state
        self.viewport = viewport
        self.view: Optional[GraphView] = None

        # Subscribe to model and viewport changes
        self.state.add_listener(self.request_redraw)
        self.viewport.add_listener(self.request_redraw)

    def attach_view(self, view: GraphView) -> None:
        """Attach the Matplotlib graph view frame."""
        self.view = view
        self.request_redraw()

    def request_redraw(self) -> None:
        """Trigger view rendering if view is attached."""
        if self.view is not None:
            self.view.render(
                functions=self.state.functions,
                viewport=self.viewport,
                show_grid=self.state.show_grid,
                show_axes=self.state.show_axes,
            )

    def handle_pan(self, dx: float, dy: float) -> None:
        """Handle mouse drag pan in data space."""
        self.viewport.pan(dx, dy)

    def handle_zoom(self, factor: float, center: Optional[Tuple[float, float]] = None) -> None:
        """Handle mouse wheel or toolbar zoom."""
        if factor < 1.0:
            self.viewport.zoom_in(factor, center)
        else:
            self.viewport.zoom_out(factor, center)

    def zoom_in(self) -> None:
        """Toolbar Zoom In."""
        self.viewport.zoom_in(ZOOM_IN_FACTOR)

    def zoom_out(self) -> None:
        """Toolbar Zoom Out."""
        self.viewport.zoom_out(ZOOM_OUT_FACTOR)

    def reset_view(self) -> None:
        """Toolbar Reset View to standard range [-10, 10]."""
        self.viewport.reset()

    def toggle_grid(self) -> bool:
        """Toggle grid visibility."""
        return self.state.toggle_grid()

    def toggle_axes(self) -> bool:
        """Toggle coordinate axes."""
        return self.state.toggle_axes()
