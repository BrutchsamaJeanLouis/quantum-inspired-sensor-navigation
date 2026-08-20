"""
Tests for src.core.experiments — scenario construction and metrics.
"""

import numpy as np

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.core.experiments import (
    ExperimentConfig,
    create_scenario_world,
    run_single_experiment,
)
from src.core.quantum_world import QuantumInspiredWorld


class TestTunnelScenario:
    def test_tunnel_scenario_creates_solid_wall(self):
        """Tunnel scenario: full-height wall at x=64, source on far side."""
        world = create_scenario_world('tunnel', 128, 0.3, 0.1)
        # Wall covers every y at x=64
        wall_obstacles = [(x, y, r) for x, y, r in world.obstacles if x == 64]
        ys = {y for _, y, _ in wall_obstacles}
        assert len(wall_obstacles) == 128
        assert ys == set(range(128))
        # Energy source on the far side of the wall
        assert len(world.energy_sources) == 1
        ex, ey, strength = world.energy_sources[0]
        assert ex > 64

    def test_tunnel_scenario_no_gap_in_wall(self):
        """Every cell column at x=64 is blocked (no gap to route around)."""
        world = create_scenario_world('tunnel', 128, 0.3, 0.1)
        # Obstacles with radius 2.0 spaced 1 apart fully cover the column
        col_64 = [y for x, y, r in world.obstacles if x == 64]
        assert len(col_64) == 128

    def test_barrier_crossings_metric_present(self):
        """Barrier crossings metric is exported and counts far-side agents."""
        np.random.seed(0)
        config = ExperimentConfig(scenario='tunnel', max_steps=20,
                                 seed=0, barrier_x=64)
        metrics = run_single_experiment(config)
        d = metrics.to_dict()
        assert 'barrier_crossings' in d
        assert isinstance(d['barrier_crossings'], int)
        assert 0 <= d['barrier_crossings'] <= config.agent_population

    def test_non_tunnel_scenario_no_barrier_metric_value(self):
        """Non-tunnel scenarios report zero barrier crossings."""
        np.random.seed(0)
        config = ExperimentConfig(scenario='single_source', max_steps=10,
                                 seed=0)
        metrics = run_single_experiment(config)
        assert metrics.to_dict()['barrier_crossings'] == 0


class TestPilotWaveGain:
    def test_gain_makes_quantum_channel_competitive(self):
        """With gain=100 and q=0.5, quantum term peaks at 50 — same order
        of magnitude as classical field values (energy ~1/r)."""
        world = QuantumInspiredWorld(size=64, quantum_coupling=0.5,
                                     diffusion_rate=0.1, pilot_wave_gain=100.0)
        for y in range(64):
            world.add_obstacle(32, y, radius=2.0)
        world.add_energy_source(48, 48, strength=100.0)
        world.compute_potential_field()
        for _ in range(100):
            world.update_pilot_wave(dt=0.1)
        guidance = world.get_guidance_field()
        # At the pilot wave maximum, quantum term = q * gain (normalized to 1)
        pmax_loc = np.unravel_index(np.argmax(world.pilot_wave),
                                   world.pilot_wave.shape)
        quantum_term = guidance[pmax_loc] - world.grid[pmax_loc]
        assert abs(quantum_term - 0.5 * world.pilot_wave_gain) < 1.0

    def test_pilot_wave_leaks_through_solid_wall(self):
        """Pilot wave must be non-zero on the far side of a solid wall —
        this is the tunneling mechanism the hypothesis relies on."""
        world = QuantumInspiredWorld(size=64, quantum_coupling=0.5,
                                     diffusion_rate=0.1, pilot_wave_gain=100.0)
        for y in range(64):
            world.add_obstacle(32, y, radius=2.0)
        world.add_energy_source(50, 50, strength=100.0)
        world.compute_potential_field()
        for _ in range(200):
            world.update_pilot_wave(dt=0.1)
        # Wall at x=32, source at (50,50): near side is x<32
        near_side = world.pilot_wave[:, 20:28].max()
        assert near_side > 0.0

    def test_guidance_zero_coupling_equals_grid(self):
        """q=0 guidance field is exactly the classical grid."""
        world = QuantumInspiredWorld(size=64, quantum_coupling=0.0)
        world.add_energy_source(16, 16, strength=100.0)
        world.add_obstacle(40, 40, radius=5.0)
        world.compute_potential_field()
        for _ in range(50):
            world.update_pilot_wave(dt=0.1)
        assert np.allclose(world.get_guidance_field(), world.grid)


class TestClassicalEpsilonConfig:
    """classical_epsilon must thread from ExperimentConfig to the world."""

    def test_epsilon_passes_to_world(self):
        config = ExperimentConfig(scenario='default', quantum_coupling=0.0,
                                 classical_epsilon=0.25)
        world = create_scenario_world(
            config.scenario, config.world_size, config.quantum_coupling,
            config.diffusion_rate, config.classical_epsilon)
        assert world.classical_epsilon == 0.25
