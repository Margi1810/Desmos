import tkinter as tk


class EquationPanel:
    def __init__(self, parent):
        self.frame = tk.Frame(parent)
        self.frame.pack(side=tk.LEFT, fill=tk.Y)

        self.entry = tk.Entry(self.frame)
        self.entry.pack(padx=10, pady=10)

    def get_expression(self):
        return self.entry.get()