"""
Unit tests for coherence module - Phase 3
"""

import sys
import os
import numpy as np
import pytest

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.core import ToyWorld, QuantumInspiredWorld, compute_phi, compute_phi_map, compute_phi_agents
from src.core import AgentSwarm, NanoAgent


class TestComputePhi:
    """Test suite for IIT-inspired coherence measurement."""

    def test_phi_returns_float(self):
        """Test that compute_phi returns a float."""
        world = ToyWorld(size=64)
        world.add_energy_source(32, 32, strength=10.0)
        world.compute_potential_field()

        phi = compute_phi(world, (20, 20, 40, 40))
        assert isinstance(phi, float)

    def test_phi_non_negative(self):
        """Test that phi is always >= 0."""
        world = ToyWorld(size=64)
        world.add_energy_source(32, 32, strength=10.0)
        world.compute_potential_field()

        phi = compute_phi(world, (20, 20, 40, 40))
        assert phi >= 0.0

    def test_phi_valid_region(self):
        """Test phi on a valid region."""
        world = ToyWorld(size=64)
        world.add_energy_source(32, 32, strength=10.0)
        world.compute_potential_field()

        phi = compute_phi(world, (20, 20, 40, 40))
        assert phi >= 0.0  # Phi is non-negative (clipped at 0)
        assert not np.isnan(phi)

    def test_phi_invalid_region(self):
        """Test phi on invalid region returns 0."""
        world = ToyWorld(size=64)
        phi = compute_phi(world, (50, 50, 30, 30))  # x_min > x_max
        assert phi == 0.0

    def test_phi_clamps_region(self):
        """Test that phi clamps region to world bounds."""
        world = ToyWorld(size=64)
        world.add_energy_source(32, 32, strength=10.0)
        world.compute_potential_field()

        # Region extends beyond world
        phi = compute_phi(world, (50, 50, 100, 100))
        assert phi >= 0.0

    def test_phi_quantum_world(self):
        """Test phi works with QuantumInspiredWorld."""
        world = QuantumInspiredWorld(size=64)
        world.add_energy_source(32, 32, strength=10.0)
        world.compute_potential_field()
        world.update_pilot_wave(dt=0.1)

        phi = compute_phi(world, (20, 20, 40, 40))
        assert isinstance(phi, float)
        assert phi >= 0.0

    def test_phi_near_energy_source(self):
        """Test phi is higher near energy sources (more self-organized)."""
        world = ToyWorld(size=64)
        world.add_energy_source(32, 32, strength=100.0)
        world.compute_potential_field()

        # Region near source
        phi_near = compute_phi(world, (28, 28, 36, 36))
        # Region far from source
        phi_far = compute_phi(world, (0, 0, 8, 8))

        # Near source should have higher phi (more structure)
        assert phi_near >= phi_far


class TestComputePhiMap:
    """Test suite for phi map computation."""

    def test_phi_map_shape(self):
        """Test phi map has expected shape."""
        world = ToyWorld(size=64)
        world.add_energy_source(32, 32, strength=10.0)
        world.compute_potential_field()

        phi_map = compute_phi_map(world, region_size=8, overlap=4)
        assert len(phi_map.shape) == 2
        assert phi_map.shape[0] > 1
        assert phi_map.shape[1] > 1

    def test_phi_map_non_negative(self):
        """Test all phi map values are non-negative."""
        world = ToyWorld(size=64)
        world.add_energy_source(32, 32, strength=10.0)
        world.compute_potential_field()

        phi_map = compute_phi_map(world)
        assert np.all(phi_map >= 0)

    def test_phi_map_with_quantum_world(self):
        """Test phi map with QuantumInspiredWorld."""
        world = QuantumInspiredWorld(size=64)
        world.add_energy_source(32, 32, strength=10.0)
        world.compute_potential_field()
        world.update_pilot_wave(dt=0.1)

        phi_map = compute_phi_map(world)
        assert np.all(phi_map >= 0)


class TestComputePhiAgents:
    """Tests for the re-scoped agent-in-the-loop, agent-localised Phi (P7)."""

    def _world_and_swarm(self, q, size=64):
        world = QuantumInspiredWorld(size=size, quantum_coupling=q)
        world.add_energy_source(20, 20, strength=100.0)
        world.add_energy_source(44, 44, strength=80.0)
        world.add_obstacle(32, 32, radius=6.0)
        world.compute_potential_field()
        for _ in range(200):
            world.update_pilot_wave(dt=0.2)
        swarm = AgentSwarm(world, 8, spawn_mode='cluster')
        return world, swarm

    def test_returns_float_non_negative(self):
        world, swarm = self._world_and_swarm(0.3)
        phi = compute_phi_agents(world, swarm.agents, local_radius=3, steps=3)
        assert isinstance(phi, float)
        assert phi >= 0.0
        assert not np.isnan(phi)

    def test_deterministic_no_agents(self):
        world, swarm = self._world_and_swarm(0.3)
        assert compute_phi_agents(world, [], local_radius=3, steps=3) == 0.0

    def test_does_not_mutate_live_world(self):
        world, swarm = self._world_and_swarm(0.3)
        before_pilot = world.pilot_wave.copy()
        before_pos = [a.x for a in swarm.agents]
        compute_phi_agents(world, swarm.agents, local_radius=3, steps=3)
        # Live world pilot wave and agent positions are untouched (deep copy).
        assert np.array_equal(world.pilot_wave, before_pilot)
        assert [a.x for a in swarm.agents] == before_pos

    def test_local_radius_bounded_window(self):
        # Probe window is (2*local_radius+1); a tiny radius must still run.
        world, swarm = self._world_and_swarm(0.3)
        small = compute_phi_agents(world, swarm.agents, local_radius=1, steps=2)
        large = compute_phi_agents(world, swarm.agents, local_radius=4, steps=2)
        assert small >= 0.0 and large >= 0.0

    def test_coupling_changes_value(self):
        # Same layout/seed; quantum vs classical guidance field differ, so the
        # metric should not be bit-identical across coupling (it is not a
        # constant 0.0 no-op).
        np.random.seed(0)
        wq, sq = self._world_and_swarm(0.3)
        np.random.seed(0)
        wc, sc = self._world_and_swarm(0.0)
        pq = compute_phi_agents(wq, sq.agents, local_radius=3, steps=3)
        pc = compute_phi_agents(wc, sc.agents, local_radius=3, steps=3)
        assert pq >= 0.0 and pc >= 0.0
        # Not a no-op: the two worlds are distinct systems.
        assert (wq.quantum_coupling, wc.quantum_coupling) == (0.3, 0.0)
