"""
Application orchestrator initializing models, controller, viewport, and GUI.
"""

import tkinter as tk
from app.models.graph_state import GraphState
from app.graph.viewport import Viewport
from app.graph.graph_controller import GraphController
from app.ui.main_window import MainWindow


class Application:
    """Core PyDesmos Application coordinator."""

    def __init__(self) -> None:
        # Initialize Core Data State
        self.state = GraphState()

        # Add initial starter expressions for great first-run experience
        self.state.add_function("y = x^2")
        self.state.add_function("y = sin(x)")

        # Initialize Viewport & Controller
        self.viewport = Viewport()
        self.controller = GraphController(state=self.state, viewport=self.viewport)

        # Initialize UI Root
        self.root = tk.Tk()
        self.main_window = MainWindow(
            root=self.root,
            state=self.state,
            viewport=self.viewport,
            controller=self.controller,
        )

    def run(self) -> None:
        """Start the application main event loop."""
        self.root.mainloop()
