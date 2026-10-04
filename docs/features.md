# PyDesmos Features & User Guide

PyDesmos provides a desktop graphing experience for 2D Cartesian mathematics.

---

## 1. Core Graphing Features

- **Real-Time Plotting**: Functions are plotted dynamically as you enter equations.
- **Multiple Simultaneous Functions**: Add as many simultaneous equations as you need, each rendered with distinct colors.
- **Interactive Pan & Drag**: Click and drag anywhere on the graph canvas to explore different regions.
- **Centric Zoom**: Zoom in/out using mouse scroll wheel centered at your mouse pointer or via the `Zoom +` / `Zoom -` toolbar buttons.
- **Reset View**: Quickly jump back to the standard `[-10, 10]` Cartesian grid.
- **Visibility Toggle**: Click on the colored circle next to any equation to show or hide the curve without deleting the equation.
- **Color Customization**: Right-click on any equation's color circle to open a full color picker and select a custom color.
- **Live Coordinate Tracker**: Bottom status bar shows the real-time `(x, y)` coordinate under your mouse pointer.
- **Grid & Axes Control**: Toggle the background grid and axis lines on or off.

---

## 2. Supported Mathematical Syntax

### Expressions & Functions
| Category | Examples | Description |
|---|---|---|
| **Explicit Equations** | `y = x^2`, `f(x) = 2x + 1` | `y =` or `f(x) =` prefix is automatically recognized and handled. |
| **Direct Expressions** | `sin(x)`, `x^3 - 3*x` | Direct input without prefix is supported. |
| **Implicit Multiplications** | `2x`, `3sin(x)`, `(x-1)(x+1)` | Automatic expansion to `2*x`, `3*sin(x)`, `(x-1)*(x+1)`. |
| **Powers** | `x^2`, `x**3`, `x^(1/3)` | Both `^` and Python `**` power notations are supported. |
| **Trigonometry** | `sin(x)`, `cos(x)`, `tan(x)` | Standard trigonometric functions. |
| **Reciprocal Trig** | `sec(x)`, `csc(x)`, `cot(x)` | Secant, cosecant, cotangent. |
| **Inverse Trig** | `asin(x)`, `acos(x)`, `atan(x)` | Arc sine, arc cosine, arc tangent. |
| **Hyperbolic** | `sinh(x)`, `cosh(x)`, `tanh(x)` | Hyperbolic functions. |
| **Logarithms** | `ln(x)`, `log(x)` | Natural logarithm. |
| **Exponential & Roots** | `exp(x)`, `e^x`, `sqrt(x)` | Exponential and square root. |
| **Absolute Value** | `abs(x)`, `|x|` | Absolute value brackets or `abs()`. |
| **Constants** | `pi`, `e` | Standard mathematical constants `π` and `e`. |

---

## 3. Discontinuity & Asymptote Handling

PyDesmos automatically detects extreme vertical jumps in asymptotic functions like `y = tan(x)` and `y = 1 / x`, inserting clean breaks in the rendering so you do not see erroneous vertical lines across the graph.

---

## 4. Presets Menu

The toolbar includes a **Presets** dropdown for instant loading of common functions:
- Quadratic: `y = x^2`
- Trigonometric: `y = sin(x)`, `y = cos(x)`, `y = tan(x)`
- Rational: `y = 1 / x`
- Radical: `y = sqrt(x)`
- Absolute Value: `y = abs(x)`
- Cubic: `y = x^3 - 3*x`
- Exponential: `y = exp(x)`
- Linear: `y = 2*x + 1`
