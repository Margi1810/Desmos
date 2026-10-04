"""
Unit tests for Viewport coordinate math and zoom/pan logic.
"""

from app.graph.viewport import Viewport


def test_viewport_initial_bounds():
    vp = Viewport(-10, 10, -5, 5)
    assert vp.get_x_range() == (-10.0, 10.0)
    assert vp.get_y_range() == (-5.0, 5.0)


def test_viewport_pan():
    vp = Viewport(-10, 10, -10, 10)
    vp.pan(2.0, -3.0)
    assert vp.get_x_range() == (-8.0, 12.0)
    assert vp.get_y_range() == (-13.0, 7.0)


def test_viewport_zoom():
    vp = Viewport(-10, 10, -10, 10)
    # Zoom in by factor 0.5 around origin (0, 0)
    vp.zoom_in(factor=0.5, center=(0.0, 0.0))
    assert vp.get_x_range() == (-5.0, 5.0)
    assert vp.get_y_range() == (-5.0, 5.0)


def test_viewport_reset():
    vp = Viewport(-10, 10, -10, 10)
    vp.pan(5.0, 5.0)
    vp.zoom_in(0.5)
    assert vp.get_x_range() != (-10.0, 10.0)

    vp.reset()
    assert vp.get_x_range() == (-10.0, 10.0)
    assert vp.get_y_range() == (-10.0, 10.0)


def test_viewport_samples_count():
    vp = Viewport(-5, 5, -5, 5)
    samples = vp.get_x_samples(num_points=500)
    assert len(samples) == 500
    assert samples[0] == -5.0
    assert samples[-1] == 5.0
