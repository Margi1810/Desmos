# Architecture

- `app/parser/` validates expressions and parses `y = ...` / `f(x) = ...`-style inputs (currently the supported left sides are `y` and `f(x)`).
- `app/calculator/` safely evaluates supported math expressions and samples x-values.
- `app/models/` stores equation and point data.
- `app/graph/` manages the viewport, grid, axes, and Matplotlib rendering.
- `app/ui/` contains the Tkinter equation panel and application window.
- `main.py` is the desktop application entry point.

Run from the `Desmos` directory with `python main.py`. A graphical desktop environment is required.
