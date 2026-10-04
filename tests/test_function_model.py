"""
Unit tests for FunctionModel and GraphState.
"""

import numpy as np
from app.models.function_model import FunctionModel
from app.models.graph_state import GraphState


def test_function_model_initialization():
    model = FunctionModel(raw_expression="y = 2*x + 3", color="#ff0000")
    assert model.is_valid is True
    assert model.color == "#ff0000"
    assert model.visible is True

    x_vals = np.array([0.0, 1.0])
    y_vals = model.evaluate(x_vals)
    np.testing.assert_allclose(y_vals, np.array([3.0, 5.0]))


def test_function_model_visibility():
    model = FunctionModel(raw_expression="y = x", visible=True)
    assert model.visible is True

    model.toggle_visibility()
    assert model.visible is False

    # When hidden, evaluation returns NaNs
    x_vals = np.array([1.0, 2.0])
    y_vals = model.evaluate(x_vals)
    assert np.all(np.isnan(y_vals))


def test_graph_state_management():
    state = GraphState()
    assert len(state.functions) == 0

    f1 = state.add_function("y = x^2")
    f2 = state.add_function("y = sin(x)")
    assert len(state.functions) == 2

    # Verify colors are distinct
    assert f1.color != f2.color

    # Remove function
    removed = state.remove_function(f1.id)
    assert removed is True
    assert len(state.functions) == 1
    assert state.get_function(f1.id) is None
    assert state.get_function(f2.id) == f2

    # Clear all
    state.clear_all()
    assert len(state.functions) == 0
