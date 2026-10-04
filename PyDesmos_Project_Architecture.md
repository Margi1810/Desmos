# PyDesmos — Python Desmos Clone

## 1. Project Overview

**Project name:** PyDesmos

**Goal:** Build a beginner-friendly Python clone of the core graphing experience of Desmos.

The project should be organized into small modules so that:
- `main.py` stays simple.
- Graphing logic is separated from the user interface.
- Mathematical expression handling is separated from plotting.
- New features can be added without rewriting the whole project.
- The GitHub repository looks clean and professional.

### Initial Features

The first version should support:

- Plotting mathematical functions such as `y = x^2`
- Multiple equations/functions
- Zoom in and zoom out
- Pan the graph
- X and Y axes
- Grid
- Function colors
- Show/hide individual expressions
- Basic expression validation
- Clear/reset graph

### Future Features

Possible future additions:

- Points such as `(2, 3)`
- Sliders
- Derivatives
- Intersections
- Tables
- Trigonometric functions
- Implicit equations
- Better expression parsing
- Save/load graphs
- Dark mode
- Desmos-like expression panel
- Keyboard shortcuts

---

# 2. Recommended Technology

Use Python for the complete project.

### Main libraries

- **Python 3**
- **NumPy** — numerical calculations
- **Matplotlib** — graph rendering
- **Tkinter** — desktop GUI
- **SymPy** — mathematical expression parsing and symbolic calculations
- **pytest** — testing

### Why this combination?

```text
Tkinter
   |
   v
User Interface
   |
   v
Expression Manager
   |
   v
Math Engine
   |
   v
Graph Engine
   |
   v
Matplotlib
```

Keep each responsibility separate.

---

# 3. Final Project Architecture

```text
PyDesmos/
│
├── README.md
├── requirements.txt
├── .gitignore
├── LICENSE
│
├── main.py
│
├── app/
│   ├── __init__.py
│   ├── application.py
│   │
│   ├── ui/
│   │   ├── __init__.py
│   │   ├── main_window.py
│   │   ├── expression_panel.py
│   │   ├── expression_row.py
│   │   ├── toolbar.py
│   │   └── dialogs.py
│   │
│   ├── graph/
│   │   ├── __init__.py
│   │   ├── graph_view.py
│   │   ├── graph_controller.py
│   │   └── viewport.py
│   │
│   ├── math/
│   │   ├── __init__.py
│   │   ├── expression.py
│   │   ├── parser.py
│   │   └── evaluator.py
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── function_model.py
│   │   └── graph_state.py
│   │
│   └── utils/
│       ├── __init__.py
│       ├── constants.py
│       └── validators.py
│
├── tests/
│   ├── __init__.py
│   ├── test_parser.py
│   ├── test_evaluator.py
│   ├── test_function_model.py
│   └── test_viewport.py
│
└── docs/
    ├── architecture.md
    └── features.md
```

---

# 4. What Each File Does

## Root Files

### `main.py`

The entry point of the application.

It should remain very small.

Example responsibility:

```python
from app.application import Application

if __name__ == "__main__":
    app = Application()
    app.run()
```

Do NOT put graphing logic here.

---

### `requirements.txt`

Contains project dependencies.

Example:

```text
numpy
matplotlib
sympy
pytest
```

Tkinter is normally included with standard Python installations on Windows.

---

### `.gitignore`

Prevents unnecessary files from being uploaded to GitHub.

Example:

```text
__pycache__/
*.pyc
.pytest_cache/
.venv/
venv/
.env
.vscode/
```

---

### `README.md`

The main GitHub documentation.

It should contain:

- Project description
- Features
- Screenshots
- Installation
- How to run
- Project architecture
- Technologies used
- Future improvements

---

# 5. Application Layer

## `app/application.py`

Controls the complete application.

Responsibilities:

```text
Start application
       |
       v
Create main window
       |
       v
Initialize graph
       |
       v
Connect UI and graph logic
```

It should coordinate components rather than perform mathematical calculations itself.

---

# 6. UI Layer

The UI layer contains everything the user sees and interacts with.

```text
app/ui/
```

## `main_window.py`

Creates the main application window.

Possible layout:

```text
+------------------------------------------------------+
|                  PyDesmos                            |
+----------------------+-------------------------------+
| Expression Panel    |                               |
|                      |                               |
| y = x^2              |          GRAPH               |
| y = sin(x)           |                               |
| y = 2*x + 1          |                               |
|                      |                               |
| [+ Add Expression]   |                               |
|                      |                               |
+----------------------+-------------------------------+
| Reset | Zoom + | Zoom - | Grid | Axes               |
+------------------------------------------------------+
```

---

## `expression_panel.py`

Manages the list of expressions.

Responsibilities:

- Add expression
- Remove expression
- Update expression
- Show/hide expression
- Store expression rows

Example:

```text
Expression Panel
      |
      +-- Expression Row 1
      |
      +-- Expression Row 2
      |
      +-- Expression Row 3
```

---

## `expression_row.py`

Represents one expression.

Example:

```text
[●] y = x^2                    [X]
```

It can contain:

- Visibility button
- Expression input
- Color indicator
- Delete button

---

## `toolbar.py`

Contains graph controls.

Possible buttons:

```text
+ Zoom In
- Zoom Out
Reset
Grid
Axes
```

---

## `dialogs.py`

Optional file for popups and error messages.

Examples:

```text
Invalid expression
Unable to plot function
Save graph
Load graph
```

---

# 7. Graph Layer

```text
app/graph/
```

This layer handles graph visualization.

## `graph_view.py`

Responsible for displaying the graph.

Use Matplotlib here.

Responsibilities:

- Draw graph
- Draw axes
- Draw grid
- Plot functions
- Refresh graph

It should NOT parse raw user input.

---

## `graph_controller.py`

Connects the UI and graph view.

Example:

```text
User enters:

y = x^2

        |
        v

Expression Panel
        |
        v

Graph Controller
        |
        v

Math Engine
        |
        v

Graph View
        |
        v

Matplotlib
```

This is the main coordination layer for graph-related actions.

---

## `viewport.py`

Controls the visible graph area.

For example:

```text
x_min
x_max
y_min
y_max
```

Responsibilities:

- Zoom
- Pan
- Reset view
- Change visible coordinate range

Example:

```python
viewport.zoom_in()
viewport.zoom_out()
viewport.reset()
```

Keeping viewport logic separate makes the project easier to understand.

---

# 8. Math Layer

```text
app/math/
```

This is one of the most important parts.

## `expression.py`

Represents a mathematical expression.

Example:

```text
y = x^2
```

Possible information stored:

```text
original expression
parsed expression
variable
color
visibility
```

---

## `parser.py`

Converts user input into a form that the math engine can understand.

Example:

```text
User input:

y = x^2 + 2*x + 1

        |
        v

Parser

        |
        v

x^2 + 2*x + 1
```

SymPy can be used here.

The parser should handle:

- `y = x^2`
- `y = sin(x)`
- `y = 2*x + 1`

and reject invalid expressions.

---

## `evaluator.py`

Evaluates the parsed expression for numerical x-values.

Example:

```text
Expression:

x^2

x = 2

2^2 = 4
```

For graphing, the evaluator should work with NumPy arrays when possible.

---

# 9. Model Layer

```text
app/models/
```

Models store application data.

## `function_model.py`

Represents one function.

Example:

```python
FunctionModel(
    expression="x^2",
    color="blue",
    visible=True
)
```

Possible attributes:

```text
expression
color
visible
```

---

## `graph_state.py`

Stores the current state of the graph.

Example:

```text
Functions:
    x^2
    sin(x)
    2*x + 1

Viewport:
    x_min = -10
    x_max = 10
    y_min = -10
    y_max = 10

Grid:
    enabled

Axes:
    enabled
```

This prevents graph state from being scattered across multiple files.

---

# 10. Utility Layer

```text
app/utils/
```

## `constants.py`

Store fixed values.

Example:

```python
DEFAULT_X_MIN = -10
DEFAULT_X_MAX = 10
DEFAULT_Y_MIN = -10
DEFAULT_Y_MAX = 10

DEFAULT_FUNCTION_COLOR = "blue"
```

---

## `validators.py`

Contains input validation.

Examples:

```text
Is expression empty?
Is expression valid?
Does expression contain unsupported syntax?
```

This keeps validation code out of the UI.

---

# 11. Data Flow

The most important architecture to understand is:

```text
                USER
                  |
                  v
        +-------------------+
        |   Tkinter UI      |
        +-------------------+
                  |
                  v
        +-------------------+
        | Graph Controller  |
        +-------------------+
             |         |
             v         v
       Math Engine   Graph State
             |
             v
        SymPy / NumPy
             |
             v
        Graph Controller
             |
             v
        +-------------------+
        |  Graph View       |
        |   Matplotlib      |
        +-------------------+
                  |
                  v
                GRAPH
```

---

# 12. Example: Plotting `y = x²`

The complete flow should be:

```text
1. User types:

   y = x^2

2. Expression Row receives input.

3. Parser removes the `y =` part.

4. Parser converts:

   x^2

   into a SymPy expression.

5. Evaluator receives x-values.

6. Evaluator calculates y-values.

7. Graph Controller sends x and y values to Graph View.

8. Graph View plots the function using Matplotlib.

9. User sees:

             |
          *  |
        *    |
      *      |
-----*-------*---------
             |
```

---

# 13. Recommended Development Order

Do NOT create the entire project at once.

Build it in stages.

## Stage 1 — Basic Graph

Create only:

```text
main.py
app/
    application.py
    graph/
        graph_view.py
```

Goal:

```text
Open application
       |
       v
Display graph
```

Then manually plot:

```python
y = x**2
```

---

# Stage 2 — Math Engine

Add:

```text
math/
    expression.py
    parser.py
    evaluator.py
```

Goal:

User enters:

```text
x^2
```

and the program plots it.

---

# Stage 3 — Expression Panel

Add:

```text
ui/
    expression_panel.py
    expression_row.py
```

Now the user can enter:

```text
x^2
sin(x)
2*x + 1
```

---

# Stage 4 — Multiple Functions

The graph should support:

```text
x^2
sin(x)
2*x
```

at the same time.

Each function should have:

```text
expression
color
visibility
```

---

# Stage 5 — Zoom and Pan

Implement:

```text
Zoom In
Zoom Out
Pan
Reset
```

Put this logic inside:

```text
graph/viewport.py
```

Do not put it inside `main.py`.

---

# Stage 6 — Better UI

Create:

```text
toolbar.py
dialogs.py
```

Improve the application layout.

---

# Stage 7 — Validation

Handle cases such as:

```text
Empty expression
Invalid expression
Invalid mathematical syntax
Division by zero
Unsupported input
```

---

# Stage 8 — Testing

Create:

```text
tests/
```

Test the math engine first.

Examples:

```text
test x^2
test 2*x + 1
test sin(x)
test invalid expression
```

---

# 14. Suggested GitHub Repository Structure

Your GitHub repository should look like:

```text
PyDesmos
│
├── README.md
├── LICENSE
├── .gitignore
├── requirements.txt
│
├── main.py
│
├── app/
│   ├── __init__.py
│   ├── application.py
│   │
│   ├── ui/
│   ├── graph/
│   ├── math/
│   ├── models/
│   └── utils/
│
├── tests/
│
└── docs/
```

Do not upload:

```text
__pycache__
.venv
.pytest_cache
temporary files
personal files
```

---

# 15. Git Workflow

Use Git regularly instead of uploading everything at the end.

Example:

```bash
git init
git add .
git commit -m "Initial project structure"
```

After implementing the basic graph:

```bash
git add .
git commit -m "Add basic graph rendering"
```

After adding the parser:

```bash
git add .
git commit -m "Add expression parser"
```

After adding multiple functions:

```bash
git add .
git commit -m "Support multiple expressions"
```

After adding zoom:

```bash
git add .
git commit -m "Add graph zoom and viewport controls"
```

Then push to GitHub:

```bash
git branch -M main
git remote add origin YOUR_GITHUB_REPOSITORY_URL
git push -u origin main
```

---

# 16. GitHub README Structure

Your `README.md` should eventually contain:

```text
# PyDesmos

A beginner-friendly Python clone of the core Desmos graphing experience.

## Features

- Function plotting
- Multiple expressions
- Zoom and pan
- Grid and axes
- Expression visibility
- Mathematical expression parsing

## Tech Stack

- Python
- Tkinter
- NumPy
- Matplotlib
- SymPy

## Installation

```bash
git clone YOUR_REPOSITORY_URL
cd PyDesmos
pip install -r requirements.txt
```

## Run

```bash
python main.py
```

## Project Structure

Explain the major folders.

## Screenshots

Add screenshots here.

## Future Improvements

- Sliders
- Tables
- Derivatives
- Intersections
- Save/load graphs
- Dark mode

## Author

Margi Jayswal
```

---

# 17. Important Design Rule

Keep this rule throughout the project:

```text
UI              → handles user interaction
Controller      → connects components
Math            → handles mathematical operations
Graph           → handles visualization
Models          → store data/state
Utils           → common helper code
Tests           → verify behavior
```

Do NOT do this:

```text
main.py
   |
   +-- UI
   +-- parsing
   +-- calculations
   +-- plotting
   +-- zoom
   +-- validation
   +-- file handling
```

That will quickly become messy.

Instead:

```text
main.py
   |
   v
Application
   |
   +---- UI
   |
   +---- Controller
   |
   +---- Math Engine
   |
   +---- Graph Engine
   |
   +---- Models
```

---

# 18. Final Target Architecture

```text
                         PyDesmos
                            |
              +-------------+-------------+
              |                           |
             UI                     Application
              |                           |
              +-------------+-------------+
                            |
                     Graph Controller
                            |
              +-------------+-------------+
              |                           |
         Math Engine                 Graph Engine
              |                           |
        +-----+------+              +-----+------+
        |            |              |            |
      Parser     Evaluator       Viewport     Graph View
        |            |              |            |
        +-----+------+              +-----+------+
              |                           |
            SymPy                       Matplotlib
              |
            NumPy

                         Models
                           |
                  +--------+--------+
                  |                 |
             FunctionModel      GraphState
```

---

# 19. First Version Scope

Do not try to recreate every Desmos feature.

Your **Version 1** should only contain:

```text
✓ Desktop window
✓ Expression input
✓ y = f(x)
✓ Multiple functions
✓ Different colors
✓ Show/hide function
✓ Delete function
✓ X/Y axes
✓ Grid
✓ Zoom
✓ Pan
✓ Reset view
✓ Invalid-expression handling
```

Once this works properly, add advanced features.

---

# 20. Final Goal

The finished project should feel like:

```text
+---------------------------------------------------------+
| PyDesmos                                      _ □ X     |
+-------------------+-------------------------------------+
| Expressions       |                                     |
|                   |                                     |
| ● y = x^2         |                                     |
| ● y = sin(x)      |             GRAPH                   |
| ● y = 2*x + 1     |                                     |
|                   |                  /                  |
| [+] Add           |                /                    |
|                   |              /                      |
|                   |------------/-----------------------  |
|                   |          /                           |
|                   |        /                             |
+-------------------+-------------------------------------+
| Reset | Zoom + | Zoom - | Grid | Axes |                 |
+---------------------------------------------------------+
```

The architecture above is intentionally modular so you can start very small and gradually move toward a more realistic Desmos-like application without turning the codebase into one huge file.
