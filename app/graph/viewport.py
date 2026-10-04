"""
Viewport manages coordinate boundaries, zoom levels, panning, and sample generation.
"""

from typing import Tuple, Optional, Callable, List
import numpy as np

from app.utils.constants import (
    DEFAULT_X_MIN,
    DEFAULT_X_MAX,
    DEFAULT_Y_MIN,
    DEFAULT_Y_MAX,
    NUM_SAMPLES,
    ZOOM_IN_FACTOR,
    ZOOM_OUT_FACTOR,
)


class Viewport:
    """Manages the visible region of the Cartesian coordinate plane."""

    def __init__(
        self,
        x_min: float = DEFAULT_X_MIN,
        x_max: float = DEFAULT_X_MAX,
        y_min: float = DEFAULT_Y_MIN,
        y_max: float = DEFAULT_Y_MAX,
    ) -> None:
        self.default_x_min = float(x_min)
        self.default_x_max = float(x_max)
        self.default_y_min = float(y_min)
        self.default_y_max = float(y_max)

        self.x_min: float = self.default_x_min
        self.x_max: float = self.default_x_max
        self.y_min: float = self.default_y_min
        self.y_max: float = self.default_y_max

        self._listeners: List[Callable[[], None]] = []

    def reset(self) -> None:
        """Reset viewport bounds back to defaults."""
        self.set_bounds(
            self.default_x_min,
            self.default_x_max,
            self.default_y_min,
            self.default_y_max,
        )

    def set_bounds(self, x_min: float, x_max: float, y_min: float, y_max: float) -> None:
        """Set explicit viewport boundaries."""
        if x_min >= x_max or y_min >= y_max:
            return

        self.x_min = float(x_min)
        self.x_max = float(x_max)
        self.y_min = float(y_min)
        self.y_max = float(y_max)
        self.notify_listeners()

    def zoom_in(self, factor: float = ZOOM_IN_FACTOR, center: Optional[Tuple[float, float]] = None) -> None:
        """
        Zoom into the graph around an optional center point (cx, cy).
        """
        self._apply_zoom(factor, center)

    def zoom_out(self, factor: float = ZOOM_OUT_FACTOR, center: Optional[Tuple[float, float]] = None) -> None:
        """
        Zoom out of the graph around an optional center point (cx, cy).
        """
        self._apply_zoom(factor, center)

    def _apply_zoom(self, factor: float, center: Optional[Tuple[float, float]] = None) -> None:
        if factor <= 0:
            return

        cx = center[0] if center is not None else (self.x_min + self.x_max) / 2.0
        cy = center[1] if center is not None else (self.y_min + self.y_max) / 2.0

        x_span = (self.x_max - self.x_min) * factor
        y_span = (self.y_max - self.y_min) * factor

        # Prevent zooming to infinitesimal or infinite scales
        if x_span < 1e-10 or x_span > 1e12 or y_span < 1e-10 or y_span > 1e12:
            return

        # Proportions of center in current view
        cur_x_span = self.x_max - self.x_min
        cur_y_span = self.y_max - self.y_min
        rx = (cx - self.x_min) / cur_x_span
        ry = (cy - self.y_min) / cur_y_span

        new_x_min = cx - rx * x_span
        new_x_max = new_x_min + x_span
        new_y_min = cy - ry * y_span
        new_y_max = new_y_min + y_span

        self.set_bounds(new_x_min, new_x_max, new_y_min, new_y_max)

    def pan(self, dx: float, dy: float) -> None:
        """
        Pan the viewport by delta values in data coordinate space.
        """
        self.x_min += dx
        self.x_max += dx
        self.y_min += dy
        self.y_max += dy
        self.notify_listeners()

    def get_x_samples(self, num_points: int = NUM_SAMPLES) -> np.ndarray:
        """Generate linearly spaced array of x sample points across current viewport."""
        return np.linspace(self.x_min, self.x_max, max(100, num_points))

    def get_x_range(self) -> Tuple[float, float]:
        """Return (x_min, x_max)."""
        return self.x_min, self.x_max

    def get_y_range(self) -> Tuple[float, float]:
        """Return (y_min, y_max)."""
        return self.y_min, self.y_max

    def add_listener(self, callback: Callable[[], None]) -> None:
        """Register a callback for viewport updates."""
        if callback not in self._listeners:
            self._listeners.append(callback)

    def remove_listener(self, callback: Callable[[], None]) -> None:
        """Unregister a viewport update callback."""
        if callback in self._listeners:
            self._listeners.remove(callback)

    def notify_listeners(self) -> None:
        """Trigger update callbacks."""
        for callback in self._listeners:
            try:
                callback()
            except Exception:
                pass
