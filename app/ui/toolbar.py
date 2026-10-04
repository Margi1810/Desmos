"""
Toolbar widget containing interactive graph controls and quick presets.
"""

from typing import Callable, Optional
import tkinter as tk
from tkinter import ttk

from app.utils.constants import (
    TOOLBAR_BG_COLOR,
    FONT_MAIN,
    FONT_BOLD,
    PRIMARY_BUTTON_COLOR,
    PRIMARY_BUTTON_TEXT,
)
from app.ui.dialogs import show_help_dialog, show_about_dialog


class Toolbar(tk.Frame):
    """Toolbar providing Zoom, Pan, Grid/Axes toggles, Presets, and Help."""

    def __init__(
        self,
        master: tk.Widget,
        on_zoom_in: Optional[Callable[[], None]] = None,
        on_zoom_out: Optional[Callable[[], None]] = None,
        on_reset_view: Optional[Callable[[], None]] = None,
        on_toggle_grid: Optional[Callable[[], bool]] = None,
        on_toggle_axes: Optional[Callable[[], bool]] = None,
        on_add_preset: Optional[Callable[[str], None]] = None,
        **kwargs,
    ) -> None:
        super().__init__(master, bg=TOOLBAR_BG_COLOR, bd=1, relief=tk.SOLID, padx=8, pady=6, **kwargs)

        self.on_zoom_in = on_zoom_in
        self.on_zoom_out = on_zoom_out
        self.on_reset_view = on_reset_view
        self.on_toggle_grid = on_toggle_grid
        self.on_toggle_axes = on_toggle_axes
        self.on_add_preset = on_add_preset

        self._create_widgets()

    def _create_widgets(self) -> None:
        # Left cluster: Viewport Navigation Buttons
        btn_zoom_in = tk.Button(
            self,
            text="🔍 Zoom +",
            font=FONT_MAIN,
            bg="#ffffff",
            fg="#212529",
            activebackground="#e9ecef",
            relief=tk.RAISED,
            bd=1,
            padx=8,
            pady=3,
            cursor="hand2",
            command=self._handle_zoom_in,
        )
        btn_zoom_in.pack(side=tk.LEFT, padx=3)

        btn_zoom_out = tk.Button(
            self,
            text="🔍 Zoom -",
            font=FONT_MAIN,
            bg="#ffffff",
            fg="#212529",
            activebackground="#e9ecef",
            relief=tk.RAISED,
            bd=1,
            padx=8,
            pady=3,
            cursor="hand2",
            command=self._handle_zoom_out,
        )
        btn_zoom_out.pack(side=tk.LEFT, padx=3)

        btn_reset = tk.Button(
            self,
            text="⟲ Reset View",
            font=FONT_MAIN,
            bg="#ffffff",
            fg="#212529",
            activebackground="#e9ecef",
            relief=tk.RAISED,
            bd=1,
            padx=8,
            pady=3,
            cursor="hand2",
            command=self._handle_reset,
        )
        btn_reset.pack(side=tk.LEFT, padx=3)

        # Separator
        sep1 = ttk.Separator(self, orient=tk.VERTICAL)
        sep1.pack(side=tk.LEFT, fill=tk.Y, padx=8, pady=2)

        # Middle cluster: Toggles
        self.grid_btn = tk.Button(
            self,
            text="⊞ Grid: ON",
            font=FONT_MAIN,
            bg="#e7f5ff",
            fg="#1971c2",
            activebackground="#d0ebff",
            relief=tk.RAISED,
            bd=1,
            padx=8,
            pady=3,
            cursor="hand2",
            command=self._handle_toggle_grid,
        )
        self.grid_btn.pack(side=tk.LEFT, padx=3)

        self.axes_btn = tk.Button(
            self,
            text="✛ Axes: ON",
            font=FONT_MAIN,
            bg="#e7f5ff",
            fg="#1971c2",
            activebackground="#d0ebff",
            relief=tk.RAISED,
            bd=1,
            padx=8,
            pady=3,
            cursor="hand2",
            command=self._handle_toggle_axes,
        )
        self.axes_btn.pack(side=tk.LEFT, padx=3)

        # Separator
        sep2 = ttk.Separator(self, orient=tk.VERTICAL)
        sep2.pack(side=tk.LEFT, fill=tk.Y, padx=8, pady=2)

        # Preset Examples Dropdown
        preset_lbl = tk.Label(self, text="Presets:", font=FONT_MAIN, bg=TOOLBAR_BG_COLOR, fg="#495057")
        preset_lbl.pack(side=tk.LEFT, padx=(4, 2))

        self.preset_combo = ttk.Combobox(
            self,
            values=[
                "y = x^2",
                "y = sin(x)",
                "y = cos(x)",
                "y = tan(x)",
                "y = 1 / x",
                "y = sqrt(x)",
                "y = abs(x)",
                "y = x^3 - 3*x",
                "y = exp(x)",
                "y = 2*x + 1",
            ],
            state="readonly",
            width=14,
        )
        self.preset_combo.pack(side=tk.LEFT, padx=2)
        self.preset_combo.bind("<<ComboboxSelected>>", self._on_preset_selected)

        # Right cluster: Help & About
        btn_about = tk.Button(
            self,
            text="ℹ About",
            font=FONT_MAIN,
            bg="#ffffff",
            fg="#495057",
            activebackground="#e9ecef",
            relief=tk.RAISED,
            bd=1,
            padx=8,
            pady=3,
            cursor="hand2",
            command=lambda: show_about_dialog(self.winfo_toplevel()),
        )
        btn_about.pack(side=tk.RIGHT, padx=3)

        btn_help = tk.Button(
            self,
            text="❓ Help / Syntax",
            font=FONT_MAIN,
            bg="#2d70b3",
            fg="#ffffff",
            activebackground="#1c538c",
            activeforeground="#ffffff",
            relief=tk.RAISED,
            bd=1,
            padx=8,
            pady=3,
            cursor="hand2",
            command=lambda: show_help_dialog(self.winfo_toplevel()),
        )
        btn_help.pack(side=tk.RIGHT, padx=3)

    def _handle_zoom_in(self) -> None:
        if self.on_zoom_in:
            self.on_zoom_in()

    def _handle_zoom_out(self) -> None:
        if self.on_zoom_out:
            self.on_zoom_out()

    def _handle_reset(self) -> None:
        if self.on_reset_view:
            self.on_reset_view()

    def _handle_toggle_grid(self) -> None:
        if self.on_toggle_grid:
            is_on = self.on_toggle_grid()
            if is_on:
                self.grid_btn.config(text="⊞ Grid: ON", bg="#e7f5ff", fg="#1971c2")
            else:
                self.grid_btn.config(text="⊞ Grid: OFF", bg="#f1f3f5", fg="#868e96")

    def _handle_toggle_axes(self) -> None:
        if self.on_toggle_axes:
            is_on = self.on_toggle_axes()
            if is_on:
                self.axes_btn.config(text="✛ Axes: ON", bg="#e7f5ff", fg="#1971c2")
            else:
                self.axes_btn.config(text="✛ Axes: OFF", bg="#f1f3f5", fg="#868e96")

    def _on_preset_selected(self, event) -> None:
        selected = self.preset_combo.get()
        if selected and self.on_add_preset:
            self.on_add_preset(selected)
            self.preset_combo.set("")
