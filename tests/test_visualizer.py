"""Tests for interactive controls: click-to-add and the coupling slider."""
import os
import sys

os.environ.setdefault('SDL_VIDEODRIVER', 'dummy')

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pygame  # noqa: E402

from src.core import QuantumInspiredWorld  # noqa: E402
from src.visualization import WorldVisualizer  # noqa: E402


def make_viz(world=None, size=400):
    if world is None:
        world = QuantumInspiredWorld(size=64, quantum_coupling=0.3)
        world.add_energy_source(32, 32, 100.0)
        world.add_obstacle(10, 10, 5.0)
        world.compute_potential_field()
    return world, WorldVisualizer(world, window_size=size)


def make_event(etype, **props):
    return pygame.event.Event(etype, props)


def test_slider_click_sets_coupling():
    world, v = make_viz()
    mid = v.coupling_slider_rect.center
    v._handle_mouse_down(make_event(pygame.MOUSEBUTTONDOWN, pos=mid, button=1, buttons=(1, 0, 0)))
    assert abs(world.quantum_coupling - 0.5) < 0.02
    assert v._coupling_dragging is True


def test_slider_edges_map_to_zero_and_one():
    world, v = make_viz()
    v._set_coupling_from_x(v.coupling_slider_rect.left)
    assert world.quantum_coupling == 0.0
    v._set_coupling_from_x(v.coupling_slider_rect.right)
    assert world.quantum_coupling == 1.0


def test_slider_drag_updates_coupling():
    world, v = make_viz()
    v._handle_mouse_down(make_event(pygame.MOUSEBUTTONDOWN,
                                   pos=v.coupling_slider_rect.center, button=1, buttons=(1, 0, 0)))
    left = v.coupling_slider_rect.left + 10
    v._handle_mouse_motion(make_event(pygame.MOUSEMOTION, pos=(left, v.coupling_slider_rect.centery),
                                     buttons=(1, 0, 0)))
    assert world.quantum_coupling < 0.1
    v._coupling_dragging = False


def test_left_click_in_field_adds_energy():
    world, v = make_viz()
    before = len(world.energy_sources)
    v._handle_mouse_down(make_event(pygame.MOUSEBUTTONDOWN, pos=(50, 300), button=1, buttons=(1, 0, 0)))
    assert len(world.energy_sources) == before + 1


def test_right_click_in_field_adds_obstacle():
    world, v = make_viz()
    before = len(world.obstacles)
    v._handle_mouse_down(make_event(pygame.MOUSEBUTTONDOWN, pos=(50, 300), button=3, buttons=(0, 0, 1)))
    assert len(world.obstacles) == before + 1


def test_slider_click_does_not_add_energy():
    world, v = make_viz()
    before = len(world.energy_sources)
    mid = v.coupling_slider_rect.center
    v._handle_mouse_down(make_event(pygame.MOUSEBUTTONDOWN, pos=mid, button=1, buttons=(1, 0, 0)))
    assert len(world.energy_sources) == before


def test_key_mapping_no_double_r():
    """K_r was bound to BOTH reset and coupling+ (dead branch); now L/U adjust."""
    import inspect
    src = inspect.getsource(WorldVisualizer.run)
    assert src.count('pygame.K_r') == 1, "K_r must be bound exactly once (reset)"
    assert 'pygame.K_u' in src, "K_u must adjust coupling up"


def test_render_draws_slider():
    world, v = make_viz()
    world.quantum_coupling = 0.5
    v.render()
    px = v.screen.get_at((v.coupling_slider_rect.left + 5,
                          v.coupling_slider_rect.centery))
    # blue fill (0, 140, 255)
    assert px[0] < 30 and px[2] > 220
