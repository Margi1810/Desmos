"""
Application constants and styling tokens for PyDesmos.
"""

# Application Metadata
APP_TITLE = "PyDesmos - Graphing Calculator"
APP_VERSION = "1.0.0"
APP_WIDTH = 1100
APP_HEIGHT = 700
APP_MIN_WIDTH = 800
APP_MIN_HEIGHT = 500

# Viewport Defaults
DEFAULT_X_MIN = -10.0
DEFAULT_X_MAX = 10.0
DEFAULT_Y_MIN = -10.0
DEFAULT_Y_MAX = 10.0
NUM_SAMPLES = 1200
ZOOM_IN_FACTOR = 0.8
ZOOM_OUT_FACTOR = 1.25

# Color Palette for Functions (Curated Desmos-like vibrant colors)
FUNCTION_COLORS = [
    "#c74440",  # Red
    "#2d70b3",  # Blue
    "#388c46",  # Green
    "#6042a6",  # Purple
    "#fa7e19",  # Orange
    "#000000",  # Black
    "#008080",  # Teal
    "#d83c74",  # Magenta
]

DEFAULT_FUNCTION_COLOR = FUNCTION_COLORS[0]

# UI Styling
PANEL_BG_COLOR = "#f8f9fa"
PANEL_BORDER_COLOR = "#dee2e6"
TOOLBAR_BG_COLOR = "#f1f3f5"
ROW_BG_COLOR = "#ffffff"
ROW_HOVER_COLOR = "#f8f9fa"
PRIMARY_BUTTON_COLOR = "#2d70b3"
PRIMARY_BUTTON_TEXT = "#ffffff"
DANGER_BUTTON_COLOR = "#e03131"
FONT_FAMILY = "Segoe UI" if "win" in __import__("sys").platform else "Helvetica"
FONT_MAIN = (FONT_FAMILY, 10)
FONT_BOLD = (FONT_FAMILY, 10, "bold")
FONT_TITLE = (FONT_FAMILY, 12, "bold")
FONT_MONO = ("Consolas" if "win" in __import__("sys").platform else "Courier", 11)

# Graph Viewport Rendering Settings
GRAPH_BG_COLOR = "#ffffff"
GRAPH_GRID_COLOR = "#e9ecef"
GRAPH_GRID_MAJOR_COLOR = "#ced4da"
GRAPH_AXIS_COLOR = "#495057"
GRAPH_AXIS_WIDTH = 1.5
GRAPH_LINE_WIDTH = 2.0
