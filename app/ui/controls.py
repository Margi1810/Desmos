import tkinter as tk


class Controls:
    def __init__(self, parent):
        self.frame = tk.Frame(parent)
        self.frame.pack(side=tk.BOTTOM, fill=tk.X)

        self.plot_button = tk.Button(
            self.frame,
            text="Plot"
        )
        self.plot_button.pack(padx=10, pady=10)