"""Small UI helpers kept separate from the graphing logic."""
import tkinter as tk
from tkinter import ttk

def create_button(parent, text, command, **kwargs):
    """Create and return a themed button."""
    return ttk.Button(parent, text=text, command=command, **kwargs)

def create_entry(parent, textvariable=None, **kwargs):
    """Create and return a themed text entry."""
    return ttk.Entry(parent, textvariable=textvariable, **kwargs)
