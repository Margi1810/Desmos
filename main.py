"""
PyDesmos - Main Application Entry Point

A clean, modular Python graphing calculator inspired by Desmos.
"""

import sys
import os

# Ensure the project root is in sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.application import Application


def main() -> None:
    """Launch the PyDesmos application."""
    app = Application()
    app.run()


if __name__ == "__main__":
    main()
