"""Equation-entry panel for the Desmos-style desktop application."""
import tkinter as tk
from tkinter import ttk, messagebox

class EquationPanel(ttk.Frame):
    def __init__(self, parent, graph, on_change=None):
        super().__init__(parent, padding=8)
        self.graph = graph
        self.on_change = on_change
        self.expression = tk.StringVar()
        ttk.Label(self, text="Equation (e.g. y = sin(x))").pack(anchor="w")
        entry = ttk.Entry(self, textvariable=self.expression)
        entry.pack(fill="x", pady=(4, 6))
        entry.bind("<Return>", lambda _event: self.add_equation())
        ttk.Button(self, text="Plot equation", command=self.add_equation).pack(fill="x")
        self.listbox = tk.Listbox(self, height=10, exportselection=False)
        self.listbox.pack(fill="both", expand=True, pady=8)
        ttk.Button(self, text="Remove selected", command=self.remove_selected).pack(fill="x")
        ttk.Button(self, text="Clear all", command=self.clear_equations).pack(fill="x", pady=(4, 0))
        self.status = ttk.Label(self, text="", wraplength=220)
        self.status.pack(fill="x", pady=(8, 0))

    def add_equation(self):
        expression = self.expression.get().strip()
        if not expression:
            self.status.configure(text="Enter an equation first.")
            return
        equation = self.graph.add_equation(expression)
        if equation.error:
            self.status.configure(text=equation.error)
            self.graph.remove_equation(equation)
            return
        self.listbox.insert(tk.END, equation.expression)
        self.expression.set("")
        self.status.configure(text=f"Plotted: {equation.expression}")
        if self.on_change:
            self.on_change()

    def remove_selected(self):
        selected = self.listbox.curselection()
        if not selected:
            return
        index = selected[0]
        if index < len(self.graph.equations):
            self.graph.remove_equation(self.graph.equations[index])
        self.listbox.delete(index)
        if self.on_change:
            self.on_change()

    def clear_equations(self):
        self.graph.clear_equations()
        self.listbox.delete(0, tk.END)
        self.status.configure(text="All equations cleared.")
        if self.on_change:
            self.on_change()
