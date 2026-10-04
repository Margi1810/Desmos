"""
Dialog windows and popup alerts for PyDesmos.
"""

import tkinter as tk
from tkinter import messagebox
from app.utils.constants import APP_TITLE, APP_VERSION


def show_error_dialog(parent: tk.Widget, title: str, message: str) -> None:
    """Display an error message box."""
    messagebox.showerror(title, message, parent=parent)


def show_about_dialog(parent: tk.Widget) -> None:
    """Display application About info."""
    about_text = (
        f"{APP_TITLE}\n"
        f"Version: {APP_VERSION}\n\n"
        "A modular, beginner-friendly Python clone of the Desmos graphing calculator.\n\n"
        "Developed with Tkinter, Matplotlib, NumPy, and SymPy.\n"
        "Author: Margi Jayswal\n"
        "License: MIT"
    )
    messagebox.showinfo("About PyDesmos", about_text, parent=parent)


def show_help_dialog(parent: tk.Widget) -> None:
    """Display mathematical syntax cheat sheet and instructions."""
    help_window = tk.Toplevel(parent)
    help_window.title("PyDesmos - Math Syntax & Help")
    help_window.geometry("550x480")
    help_window.resizable(False, False)
    help_window.transient(parent)
    help_window.grab_set()

    # Center dialog on parent
    parent_x = parent.winfo_rootx()
    parent_y = parent.winfo_rooty()
    parent_w = parent.winfo_width()
    parent_h = parent.winfo_height()
    help_window.geometry(f"+{parent_x + (parent_w - 550) // 2}+{parent_y + (parent_h - 480) // 2}")

    frame = tk.Frame(help_window, padx=20, pady=20, bg="#ffffff")
    frame.pack(fill=tk.BOTH, expand=True)

    title_lbl = tk.Label(
        frame,
        text="Supported Mathematical Syntax",
        font=("Segoe UI", 13, "bold"),
        bg="#ffffff",
        fg="#212529",
    )
    title_lbl.pack(anchor="w", pady=(0, 10))

    help_content = (
        "You can enter equations in explicit format (y = ...) or directly as expressions:\n\n"
        "• Basic Operations:  +,  -,  *,  /,  ^  (or **)\n"
        "• Polynomials:        x^2,  2x + 1,  x^3 - 4x\n"
        "• Trigonometry:       sin(x),  cos(x),  tan(x),  sec(x),  csc(x),  cot(x)\n"
        "• Inverse Trig:       asin(x),  acos(x),  atan(x)\n"
        "• Roots & Powers:     sqrt(x),  x^(1/3),  exp(x),  e^x\n"
        "• Logarithms:         ln(x),  log(x)\n"
        "• Absolute Value:     abs(x)  or  |x|\n"
        "• Constants:          pi,  e\n\n"
        "Interactive Graph Controls:\n"
        "• Pan: Click and drag anywhere on the graph.\n"
        "• Zoom: Use the mouse scroll wheel or toolbar [+] and [-] buttons.\n"
        "• Reset: Click 'Reset View' to return to [-10, 10].\n"
        "• Visibility: Click the colored circle next to any expression to toggle it."
    )

    msg_lbl = tk.Label(
        frame,
        text=help_content,
        font=("Segoe UI", 9),
        justify=tk.LEFT,
        bg="#ffffff",
        fg="#343a40",
    )
    msg_lbl.pack(anchor="w", pady=(0, 15))

    btn_close = tk.Button(
        frame,
        text="Got it!",
        font=("Segoe UI", 9, "bold"),
        bg="#2d70b3",
        fg="#ffffff",
        activebackground="#1c538c",
        activeforeground="#ffffff",
        relief=tk.FLAT,
        padx=15,
        pady=5,
        cursor="hand2",
        command=help_window.destroy,
    )
    btn_close.pack(anchor="e")
