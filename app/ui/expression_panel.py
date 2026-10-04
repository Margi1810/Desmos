"""
ExpressionPanel manages the list of expression rows and controls to add or clear them.
"""

from typing import Dict, Optional, Callable
import tkinter as tk
from tkinter import ttk

from app.models.graph_state import GraphState
from app.models.function_model import FunctionModel
from app.ui.expression_row import ExpressionRow
from app.utils.constants import (
    PANEL_BG_COLOR,
    FONT_TITLE,
    FONT_MAIN,
    PRIMARY_BUTTON_COLOR,
    PRIMARY_BUTTON_TEXT,
)


class ExpressionPanel(tk.Frame):
    """Sidebar panel for managing mathematical expressions."""

    def __init__(
        self,
        master: tk.Widget,
        state: GraphState,
        on_expression_change: Optional[Callable[[], None]] = None,
        **kwargs,
    ) -> None:
        super().__init__(master, bg=PANEL_BG_COLOR, bd=1, relief=tk.SOLID, **kwargs)

        self.state = state
        self.on_expression_change = on_expression_change
        self.rows: Dict[str, ExpressionRow] = {}

        self._create_widgets()
        self.refresh_rows()

    def _create_widgets(self) -> None:
        # Header frame
        header_frame = tk.Frame(self, bg=PANEL_BG_COLOR, padx=12, pady=10)
        header_frame.pack(side=tk.TOP, fill=tk.X)

        title_lbl = tk.Label(
            header_frame,
            text="Expressions",
            font=FONT_TITLE,
            bg=PANEL_BG_COLOR,
            fg="#212529",
        )
        title_lbl.pack(side=tk.LEFT)

        clear_btn = tk.Button(
            header_frame,
            text="Clear All",
            font=("Segoe UI", 8),
            bg="#f1f3f5",
            fg="#868e96",
            activebackground="#ffe3e3",
            activeforeground="#e03131",
            relief=tk.FLAT,
            bd=0,
            padx=6,
            pady=2,
            cursor="hand2",
            command=self._on_clear_all,
        )
        clear_btn.pack(side=tk.RIGHT)

        # Scrollable Canvas for rows
        self.canvas_container = tk.Frame(self, bg=PANEL_BG_COLOR)
        self.canvas_container.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=6)

        self.canvas = tk.Canvas(self.canvas_container, bg=PANEL_BG_COLOR, highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self.canvas_container, orient=tk.VERTICAL, command=self.canvas.yview)
        self.rows_frame = tk.Frame(self.canvas, bg=PANEL_BG_COLOR)

        self.rows_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")),
        )
        self.canvas_window = self.canvas.create_window((0, 0), window=self.rows_frame, anchor="nw")
        self.canvas.configure(xscrollcommand=None, yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Resize rows frame with canvas width
        self.canvas.bind(
            "<Configure>",
            lambda e: self.canvas.itemconfig(self.canvas_window, width=e.width),
        )

        # Bottom Add Button
        bottom_frame = tk.Frame(self, bg=PANEL_BG_COLOR, padx=12, pady=10)
        bottom_frame.pack(side=tk.BOTTOM, fill=tk.X)

        add_btn = tk.Button(
            bottom_frame,
            text="➕  Add Expression",
            font=FONT_MAIN,
            bg=PRIMARY_BUTTON_COLOR,
            fg=PRIMARY_BUTTON_TEXT,
            activebackground="#1c538c",
            activeforeground="#ffffff",
            relief=tk.FLAT,
            padx=12,
            pady=6,
            cursor="hand2",
            command=self.add_new_expression,
        )
        add_btn.pack(fill=tk.X)

    def refresh_rows(self) -> None:
        """Synchronize UI rows with the models in GraphState."""
        # Clear existing row widgets
        for row in self.rows.values():
            row.destroy()
        self.rows.clear()

        # Build rows for each model
        for model in self.state.functions:
            self._create_row_widget(model)

    def _create_row_widget(self, model: FunctionModel) -> ExpressionRow:
        row = ExpressionRow(
            self.rows_frame,
            model=model,
            on_change=self._on_row_changed,
            on_delete=self._on_row_deleted,
        )
        row.pack(fill=tk.X, pady=3, padx=2)
        self.rows[model.id] = row
        return row

    def add_new_expression(self, expr_text: str = "") -> FunctionModel:
        """Add a new expression row and focus it."""
        model = self.state.add_function(raw_expression=expr_text)
        row = self._create_row_widget(model)
        row.focus_entry()
        if self.on_expression_change:
            self.on_expression_change()
        return model

    def _on_row_changed(self, model: FunctionModel) -> None:
        self.state.notify_listeners()
        if self.on_expression_change:
            self.on_expression_change()

    def _on_row_deleted(self, model_id: str) -> None:
        if model_id in self.rows:
            self.rows[model_id].destroy()
            del self.rows[model_id]
        self.state.remove_function(model_id)
        if self.on_expression_change:
            self.on_expression_change()

    def _on_clear_all(self) -> None:
        for row in self.rows.values():
            row.destroy()
        self.rows.clear()
        self.state.clear_all()
        # Add one blank expression row for a nice user experience
        self.add_new_expression("")
