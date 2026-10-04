"""
ExpressionRow represents a single input item in the expression panel.
"""

from typing import Callable, Optional
import tkinter as tk
from tkinter import colorchooser

from app.models.function_model import FunctionModel
from app.utils.constants import (
    ROW_BG_COLOR,
    ROW_HOVER_COLOR,
    FONT_MAIN,
    FONT_MONO,
    DANGER_BUTTON_COLOR,
)


class ExpressionRow(tk.Frame):
    """Widget for a single function expression input row."""

    def __init__(
        self,
        master: tk.Widget,
        model: FunctionModel,
        on_change: Optional[Callable[[FunctionModel], None]] = None,
        on_delete: Optional[Callable[[str], None]] = None,
        **kwargs,
    ) -> None:
        super().__init__(master, bg=ROW_BG_COLOR, bd=1, relief=tk.SOLID, padx=6, pady=6, **kwargs)

        self.model = model
        self.on_change = on_change
        self.on_delete = on_delete

        self._create_widgets()
        self._sync_with_model()

    def _create_widgets(self) -> None:
        # Visibility & Color Button
        self.visibility_btn = tk.Button(
            self,
            text="●",
            font=("Segoe UI", 13, "bold"),
            fg=self.model.color,
            bg=ROW_BG_COLOR,
            activebackground=ROW_HOVER_COLOR,
            relief=tk.FLAT,
            bd=0,
            width=2,
            cursor="hand2",
            command=self._on_toggle_visibility,
        )
        self.visibility_btn.pack(side=tk.LEFT, padx=(0, 4))
        self.visibility_btn.bind("<Button-3>", self._on_choose_color)

        # Expression Text Entry
        self.entry_var = tk.StringVar(value=self.model.raw_expression)
        self.entry = tk.Entry(
            self,
            textvariable=self.entry_var,
            font=FONT_MONO,
            relief=tk.SOLID,
            bd=1,
            bg="#ffffff",
            fg="#212529",
            highlightthickness=1,
            highlightcolor="#2d70b3",
            highlightbackground="#ced4da",
        )
        self.entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 4), ipady=3)

        # Bind typing and enter events
        self.entry.bind("<KeyRelease>", self._on_text_changed)
        self.entry.bind("<Return>", lambda e: self._on_text_changed())

        # Error / Status Icon
        self.error_lbl = tk.Label(
            self,
            text="",
            font=("Segoe UI", 9),
            fg="#e03131",
            bg=ROW_BG_COLOR,
            width=2,
        )
        self.error_lbl.pack(side=tk.LEFT, padx=(0, 2))

        # Delete Button
        self.delete_btn = tk.Button(
            self,
            text="✕",
            font=("Segoe UI", 10, "bold"),
            fg="#868e96",
            bg=ROW_BG_COLOR,
            activeforeground=DANGER_BUTTON_COLOR,
            activebackground="#ffe3e3",
            relief=tk.FLAT,
            bd=0,
            width=2,
            cursor="hand2",
            command=self._on_delete_clicked,
        )
        self.delete_btn.pack(side=tk.RIGHT)

    def _on_toggle_visibility(self) -> None:
        self.model.toggle_visibility()
        self._update_visibility_ui()
        if self.on_change:
            self.on_change(self.model)

    def _on_choose_color(self, event) -> None:
        """Right click allows choosing custom color."""
        color = colorchooser.askcolor(
            color=self.model.color,
            title="Pick Function Color",
            parent=self.winfo_toplevel(),
        )
        if color and color[1]:
            self.model.set_color(color[1])
            self._update_visibility_ui()
            if self.on_change:
                self.on_change(self.model)

    def _on_text_changed(self, event=None) -> None:
        new_text = self.entry_var.get()
        self.model.update_expression(new_text)
        self._sync_with_model()
        if self.on_change:
            self.on_change(self.model)

    def _on_delete_clicked(self) -> None:
        if self.on_delete:
            self.on_delete(self.model.id)

    def _sync_with_model(self) -> None:
        self._update_visibility_ui()
        if self.model.raw_expression and not self.model.is_valid:
            self.error_lbl.config(text="⚠️")
            self.entry.config(highlightbackground="#fa5252", highlightcolor="#fa5252")
        else:
            self.error_lbl.config(text="")
            self.entry.config(highlightbackground="#ced4da", highlightcolor="#2d70b3")

    def _update_visibility_ui(self) -> None:
        if self.model.visible:
            self.visibility_btn.config(text="●", fg=self.model.color)
        else:
            self.visibility_btn.config(text="○", fg="#adb5bd")

    def focus_entry(self) -> None:
        """Set focus into entry box."""
        self.entry.focus_set()
