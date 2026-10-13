"""Tkinter application window with an embedded Matplotlib graph."""
import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from ..graph.graph import Graph
from .equation_panel import EquationPanel

class DesmosWindow:
    def __init__(self, root=None):
        self.root = root or tk.Tk()
        self.root.title("Desmos - Function Grapher")
        self.root.geometry("1000x650")
        self.graph = Graph()
        self._build_ui()
        self.redraw()

    def _build_ui(self):
        container = ttk.Frame(self.root, padding=8)
        container.pack(fill="both", expand=True)
        container.columnconfigure(1, weight=1)
        container.rowconfigure(0, weight=1)
        self.panel = EquationPanel(container, self.graph, self.redraw)
        self.panel.grid(row=0, column=0, sticky="nsw", padx=(0, 8))
        plot_frame = ttk.Frame(container)
        plot_frame.grid(row=0, column=1, sticky="nsew")
        self.figure = Figure(figsize=(7, 5), dpi=100)
        self.axes = self.figure.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.figure, master=plot_frame)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)
        NavigationToolbar2Tk(self.canvas, plot_frame).update()
        buttons = ttk.Frame(plot_frame)
        buttons.pack(fill="x")
        ttk.Button(buttons, text="Zoom in", command=self.zoom_in).pack(side="left")
        ttk.Button(buttons, text="Zoom out", command=self.zoom_out).pack(side="left", padx=4)
        ttk.Button(buttons, text="Reset view", command=self.reset_view).pack(side="left")

    def redraw(self):
        self.axes.clear()
        self.graph.draw(self.axes)
        self.canvas.draw_idle()

    def zoom_in(self):
        self.graph.zoom_in()
        self.redraw()

    def zoom_out(self):
        self.graph.zoom_out()
        self.redraw()

    def reset_view(self):
        self.graph.viewport.reset(-10, 10, -10, 10)
        self.graph._update_components()
        self.redraw()

    def run(self):
        self.root.mainloop()
