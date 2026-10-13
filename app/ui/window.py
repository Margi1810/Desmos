import tkinter as tk

from .equation_panel import EquationPanel
from .controls import Controls


class Window:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Desmos Clone")
        self.root.geometry("1000x700")

        self.equation_panel = EquationPanel(self.root)
        self.controls = Controls(self.root)

    def run(self):
        self.root.mainloop()