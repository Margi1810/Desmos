# PyDesmos 📈

A clean, modular, and beginner-friendly Python desktop clone of the core graphing calculator experience inspired by Desmos.

Built with Python, Tkinter, Matplotlib, NumPy, and SymPy.

---

## 🌟 Features

- 📐 **Mathematical Function Graphing**: Plot single or multiple mathematical functions `y = f(x)` simultaneously.
- 🎨 **Dynamic Color Palette & Styling**: Distinct colors for every expression with live visibility toggles.
- 🔍 **Interactive Viewport Controls**:
  - Pan freely by dragging the canvas with your mouse.
  - Zoom in / Zoom out smoothly with mouse scroll wheel or toolbar buttons.
  - One-click **Reset View** to default bounds `[-10, 10]`.
- 🔲 **Grid & Axes Toggles**: Easily toggle Cartesian grid lines and coordinate axes on or off.
- 🧠 **Smart Math Parser**:
  - Handles explicit and implicit equations (e.g. `y = x^2`, `sin(x)`, `2x + 1`, `3sin(x)`, `(x+1)(x-1)`).
  - Power notation support: both `x^2` and `x**2`.
  - Trigonometric, logarithmic, exponential, and algebraic functions: `sin`, `cos`, `tan`, `sqrt`, `abs`, `exp`, `log`, `ln`, `pi`, `e`.
- ⚠️ **Graceful Error Handling & Asymptote Handling**: Real-time syntax validation, visual error indicators, and asymptote masking (preventing vertical artifact lines across discontinuities).
- 🧩 **Modular Architecture**: Clean separation of UI, math parsing, evaluation, graphing, models, and utilities.

---

## 🏗️ Project Architecture

```text
PyDesmos/
│
├── README.md
├── requirements.txt
├── .gitignore
├── LICENSE
│
├── main.py                    # Application entry point
│
├── app/
│   ├── __init__.py
│   ├── application.py         # Application controller & coordinator
│   │
│   ├── ui/                    # UI Layer (Tkinter)
│   │   ├── __init__.py
│   │   ├── main_window.py     # Main window frame & layout
│   │   ├── expression_panel.py# Expression sidebar & manager
│   │   ├── expression_row.py  # Individual expression row widget
│   │   ├── toolbar.py         # Graph action toolbar
│   │   └── dialogs.py         # Help & info dialogs
│   │
│   ├── graph/                 # Graphing Layer (Matplotlib)
│   │   ├── __init__.py
│   │   ├── graph_view.py      # Matplotlib canvas renderer
│   │   ├── graph_controller.py# UI <-> Graph interaction bridge
│   │   └── viewport.py        # Coordinate range & zoom/pan logic
│   │
│   ├── math/                  # Math Engine (SymPy + NumPy)
│   │   ├── __init__.py
│   │   ├── expression.py      # Expression data wrapper
│   │   ├── parser.py          # SymPy expression parser & sanitizer
│   │   └── evaluator.py       # NumPy numerical vector evaluator
│   │
│   ├── models/                # Data Models
│   │   ├── __init__.py
│   │   ├── function_model.py  # Function data representation
│   │   └── graph_state.py     # Global graph state container
│   │
│   └── utils/                 # Utilities
│       ├── __init__.py
│       ├── constants.py       # Application constants & theme tokens
│       └── validators.py      # Syntax & input validators
│
├── tests/                     # Unit Tests (pytest)
│   ├── __init__.py
│   ├── test_parser.py
│   ├── test_evaluator.py
│   ├── test_function_model.py
│   └── test_viewport.py
│
└── docs/                      # Documentation
    ├── architecture.md
    └── features.md
```

---

## 🚀 Quick Start

### 1. Prerequisites

Make sure you have Python 3.9+ installed on your system.

### 2. Installation

Clone the repository and install the dependencies:

```bash
git clone https://github.com/margijayswal/PyDesmos.git
cd PyDesmos
pip install -r requirements.txt
```

### 3. Run the Application

```bash
python main.py
```

### 4. Run Unit Tests

```bash
pytest
```

---

## ⌨️ Mathematical Syntax & Examples

| Function / Expression | Input Syntax |
|---|---|
| Quadratic | `y = x^2` or `x**2` |
| Polynomial | `x^3 - 3*x + 1` |
| Implicit multiplication | `2x + 1` or `(x - 2)(x + 2)` |
| Trigonometric | `sin(x)`, `cos(2x)`, `tan(x)` |
| Square Root | `sqrt(x)` or `sqrt(x + 4)` |
| Exponential | `exp(x)` or `e^x` |
| Natural Logarithm | `ln(x)` or `log(x)` |
| Absolute Value | `abs(x)` or `|x|` |
| Rational Function | `1 / x` |

---

## 🔮 Future Improvements

- [ ] Sliders for dynamic constants (e.g. `y = a*x^2 + b`)
- [ ] Point plotting `(x, y)` and table of values
- [ ] Intersection finder and derivative visualization
- [ ] Export graph as PNG / SVG
- [ ] Dark theme support

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
