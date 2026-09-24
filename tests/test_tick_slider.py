"""Deterministic tests for the bottom tick-slider UI wiring.

These exercise the exact mouse-path an LLM (or a human) drives: clicking /
dragging the bottom slider must map the cursor X to player.seek(tick). The
coupling slider already has tests in test_visualizer.py; this file covers the
tick timeline control added for LLM-driven scrubbing.

A small world keeps each test fast; the seek/rewind determinism itself is
covered in test_timeline.py.
"""
import os
import sys

os.environ.setdefault('SDL_VIDEODRIVER', 'dummy')

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pygame  # noqa: E402

from src.core.agents import AgentSwarm  # noqa: E402
from src.core.quantum_world import QuantumInspiredWorld  # noqa: E402
from src.core.timeline import TimelinePlayer  # noqa: E402
from src.visualization import WorldVisualizer  # noqa: E402


def _tiny_factory():
    """A fast (world, swarm) at t=0 for the timeline player."""
    w = QuantumInspiredWorld(size=32, quantum_coupling=0.5, diffusion_rate=0.15)
    w.add_energy_source(16, 16, strength=100.0)
    w.compute_potential_field()
    s = AgentSwarm(w, population=4, spawn_mode='corner')
    return w, s


def make_event(etype, **props):
    return pygame.event.Event(etype, props)


def make_player_viz(size=400):
    player = TimelinePlayer(factory=_tiny_factory, seed=7)
    viz = WorldVisualizer(player.world, window_size=size, player=player)
    return player, viz


def test_click_tick_slider_seeks_and_arm_drag():
    player, v = make_player_viz()
    player.seek(20)  # start somewhere non-zero
    r = v._tick_slider_rect
    # click at 25% of the track -> seek(0.25 * tick_slider_max)
    x = r.left + r.width // 4
    v._handle_mouse_down(make_event(pygame.MOUSEBUTTONDOWN, pos=(x, r.centery),
                                    button=1, buttons=(1, 0, 0)))
    assert v._tick_dragging is True
    expected = int(round(0.25 * v.tick_slider_max))
    assert player.tick == expected, (player.tick, expected)


def test_drag_tick_slider_updates_tick():
    player, v = make_player_viz()
    player.seek(300)
    r = v._tick_slider_rect
    # grab at 75% then drag to ~left -> tick should drop toward 0
    x75 = r.left + (3 * r.width) // 4
    v._handle_mouse_down(make_event(pygame.MOUSEBUTTONDOWN, pos=(x75, r.centery),
                                    button=1, buttons=(1, 0, 0)))
    v._handle_mouse_motion(make_event(pygame.MOUSEMOTION,
                                      pos=(r.left + 5, r.centery),
                                      buttons=(1, 0, 0)))
    assert player.tick < 20, player.tick
    # release (the run loop clears _tick_dragging on MOUSEBUTTONUP)
    v._tick_dragging = False


def test_set_tick_from_x_edges():
    player, v = make_player_viz()
    r = v._tick_slider_rect
    v._set_tick_from_x(r.left)
    assert player.tick == 0
    v._set_tick_from_x(r.right)
    assert player.tick == v.tick_slider_max


def test_tick_slider_click_does_not_add_energy():
    player, v = make_player_viz()
    before = len(player.world.energy_sources)
    r = v._tick_slider_rect
    v._handle_mouse_down(make_event(pygame.MOUSEBUTTONDOWN, pos=r.center,
                                    button=1, buttons=(1, 0, 0)))
    assert len(player.world.energy_sources) == before


def test_rewind_repoints_visualizer_world():
    """After a rewind seek the visualizer must render the rebuilt world/swarm."""
    player, v = make_player_viz()
    player.seek(40)
    before = id(player.world)
    player.seek(5)  # rewind -> rebuilds a fresh t=0 world
    # _sync_player re-points viz.world to the rebuilt player.world
    v._sync_player()
    assert v.world is player.world
    assert id(player.world) != before
