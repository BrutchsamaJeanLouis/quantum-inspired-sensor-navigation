"""
Tests for the TimelinePlayer deterministic scrubbing contract.

Contract under test:
  For a fixed (factory, seed), the state at tick N is reproducible:
  * fast-forward (seek to N live) and rewind (re-seed + re-step N) must
    produce identical world + swarm state.
  * seeking back and forth to the same tick yields identical state.
"""

import os
import sys

import numpy as np
import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from src.core.agents import AgentSwarm
from src.core.timeline import TimelinePlayer
from main import setup_maze_world, setup_world


def _factory():
    world = setup_maze_world()
    swarm = AgentSwarm(world, population=10, spawn_mode='corner')
    return world, swarm


def _fingerprint(player: TimelinePlayer):
    """Full observable state -> hashable tuple."""
    world = player.world
    swarm = player.swarm
    agents = (
        (a.x, a.y, a.alive, a.steps_taken, round(a.energy, 6))
        for a in swarm.agents
    )
    return (
        player.tick,
        float(np.round(world.grid).sum()),
        float(np.round(world.pilot_wave, 6).sum()),
        float(np.round(world.coherence, 6).sum()),
        tuple(agents),
    )


def test_forward_step_advances_tick():
    p = TimelinePlayer(_factory, seed=1)
    assert p.tick == 0
    p.step(5)
    assert p.tick == 5
    p.step(0)
    assert p.tick == 5


def test_seek_forward_is_live_steps():
    """Forward seek must equal simply stepping the live sim."""
    p1 = TimelinePlayer(_factory, seed=2)
    p1.step(10)
    p1.seek(25)
    # independent: step a second instance to 25 the same way
    p2 = TimelinePlayer(_factory, seed=2)
    p2.step(25)
    assert _fingerprint(p1) == _fingerprint(p2)


def test_rewind_reproduces_earlier_state():
    """Rewinding to tick N must equal the state that was live at tick N."""
    p = TimelinePlayer(_factory, seed=3)
    p.step(30)
    snap_30 = _fingerprint(p)

    p.seek(10)  # rewind: re-seed + re-step 10
    snap_10 = _fingerprint(p)

    p2 = TimelinePlayer(_factory, seed=3)
    p2.step(10)
    assert _fingerprint(p2) == snap_10

    # forward again must land exactly back on the earlier snapshot
    p.seek(30)
    assert _fingerprint(p) == snap_30


def test_seek_back_and_forth_stable():
    p = TimelinePlayer(_factory, seed=4)
    p.step(20)
    s20 = _fingerprint(p)
    p.seek(5)
    p.seek(20)
    assert _fingerprint(p) == s20
    p.seek(0)
    p2 = TimelinePlayer(_factory, seed=4)
    assert _fingerprint(p) == _fingerprint(p2)


def test_negative_seek_clamps_to_zero():
    p = TimelinePlayer(_factory, seed=5)
    p.step(5)
    assert p.seek(-3) == 0
    assert p.tick == 0


def test_negative_step_raises():
    p = TimelinePlayer(_factory, seed=5)
    with pytest.raises(ValueError):
        p.step(-1)


def test_stats_shape():
    p = TimelinePlayer(_factory, seed=6)
    p.step(3)
    s = p.stats()
    assert set(s) == {"tick", "seed", "alive", "population", "avg_steps"}
    assert s["tick"] == 3
    assert s["population"] == 10


def test_default_scenario_factory():
    world = setup_world()
    swarm = AgentSwarm(world, population=8, spawn_mode='random')
    def f():
        w = setup_world()
        return w, AgentSwarm(w, 8, 'random')

    p = TimelinePlayer(f, seed=7)
    p.seek(15)
    assert p.tick == 15
    p.seek(4)
    assert p.tick == 4
