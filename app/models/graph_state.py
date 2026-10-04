"""
GraphState manages the overall state of expressions and display options.
"""

from typing import List, Optional, Callable
from app.models.function_model import FunctionModel
from app.utils.constants import FUNCTION_COLORS


class GraphState:
    """Container for all active functions and global graph display settings."""

    def __init__(self) -> None:
        self.functions: List[FunctionModel] = []
        self.show_grid: bool = True
        self.show_axes: bool = True
        self._color_index: int = 0
        self._listeners: List[Callable[[], None]] = []

    def get_next_color(self) -> str:
        """Get the next color from the curated palette cyclically."""
        color = FUNCTION_COLORS[self._color_index % len(FUNCTION_COLORS)]
        self._color_index += 1
        return color

    def add_function(
        self,
        raw_expression: str = "",
        color: Optional[str] = None,
        visible: bool = True,
    ) -> FunctionModel:
        """Add a new function model to the state."""
        assigned_color = color or self.get_next_color()
        model = FunctionModel(
            raw_expression=raw_expression,
            color=assigned_color,
            visible=visible,
        )
        self.functions.append(model)
        self.notify_listeners()
        return model

    def remove_function(self, model_id: str) -> bool:
        """Remove a function model by its ID."""
        initial_len = len(self.functions)
        self.functions = [f for f in self.functions if f.id != model_id]
        if len(self.functions) != initial_len:
            self.notify_listeners()
            return True
        return False

    def get_function(self, model_id: str) -> Optional[FunctionModel]:
        """Find a function model by ID."""
        for f in self.functions:
            if f.id == model_id:
                return f
        return None

    def clear_all(self) -> None:
        """Clear all function expressions."""
        self.functions.clear()
        self._color_index = 0
        self.notify_listeners()

    def toggle_grid(self) -> bool:
        """Toggle grid visibility."""
        self.show_grid = not self.show_grid
        self.notify_listeners()
        return self.show_grid

    def toggle_axes(self) -> bool:
        """Toggle axes visibility."""
        self.show_axes = not self.show_axes
        self.notify_listeners()
        return self.show_axes

    def add_listener(self, callback: Callable[[], None]) -> None:
        """Register a callback for state changes."""
        if callback not in self._listeners:
            self._listeners.append(callback)

    def remove_listener(self, callback: Callable[[], None]) -> None:
        """Unregister a state change callback."""
        if callback in self._listeners:
            self._listeners.remove(callback)

    def notify_listeners(self) -> None:
        """Notify all registered listeners that state has changed."""
        for callback in self._listeners:
            try:
                callback()
            except Exception:
                pass
