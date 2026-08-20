"""
Unit tests for ToyWorld class - Phase 1
"""

import sys
import os
import numpy as np
import pytest

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.core import ToyWorld


class TestToyWorld:
    """Test suite for ToyWorld classical physics simulation."""

    def test_initialization(self):
        """Test world initialization."""
        world = ToyWorld(size=64)
        assert world.size == 64
        assert world.grid.shape == (64, 64)
        assert len(world.energy_sources) == 0
        assert len(world.obstacles) == 0

    def test_add_energy_source(self):
        """Test adding energy sources."""
        world = ToyWorld(size=64)
        world.add_energy_source(10, 10, strength=5.0)

        assert len(world.energy_sources) == 1
        assert world.energy_sources[0] == (10, 10, 5.0)

    def test_add_energy_source_out_of_bounds(self):
        """Test that out-of-bounds coordinates raise error."""
        world = ToyWorld(size=64)

        with pytest.raises(ValueError):
            world.add_energy_source(100, 10)

        with pytest.raises(ValueError):
            world.add_energy_source(10, -5)

    def test_add_obstacle(self):
        """Test adding obstacles."""
        world = ToyWorld(size=64)
        world.add_obstacle(20, 20, radius=5.0)

        assert len(world.obstacles) == 1
        assert world.obstacles[0] == (20, 20, 5.0)

    def test_compute_potential_field(self):
        """Test potential field computation."""
        world = ToyWorld(size=64)
        world.add_energy_source(32, 32, strength=10.0)
        world.compute_potential_field()

        # Check that potential is higher near the source
        center_potential = world.grid[32, 32]
        edge_potential = world.grid[0, 0]

        assert center_potential > edge_potential

    def test_potential_field_with_obstacle(self):
        """Test that obstacles create negative potential."""
        world = ToyWorld(size=64)
        world.add_energy_source(50, 50, strength=10.0)
        world.add_obstacle(32, 32, radius=5.0)
        world.compute_potential_field()

        # Check obstacle creates negative/lower potential
        obstacle_center = world.grid[32, 32]
        far_away = world.grid[10, 10]

        # Obstacle should reduce potential
        assert obstacle_center < far_away

    def test_get_gradient(self):
        """Test gradient calculation."""
        world = ToyWorld(size=64)
        world.add_energy_source(50, 32, strength=100.0)
        world.compute_potential_field()

        # Get gradient at a point left of the source
        dx, dy = world.get_gradient(40, 32)

        # Should point toward the source (positive x direction)
        assert dx > 0

    def test_get_potential(self):
        """Test getting potential at specific coordinates."""
        world = ToyWorld(size=64)
        world.add_energy_source(32, 32, strength=10.0)
        world.compute_potential_field()

        potential = world.get_potential(32, 32)
        assert potential > 0

        # Out of bounds should return -inf
        oob_potential = world.get_potential(-1, 10)
        assert oob_potential == -np.inf

    def test_clear(self):
        """Test clearing the world."""
        world = ToyWorld(size=64)
        world.add_energy_source(10, 10)
        world.add_obstacle(20, 20)
        world.compute_potential_field()

        world.clear()

        assert len(world.energy_sources) == 0
        assert len(world.obstacles) == 0
        assert np.all(world.grid == 0)

    def test_get_state(self):
        """Test getting world state."""
        world = ToyWorld(size=64)
        world.add_energy_source(10, 10, strength=5.0)
        world.add_obstacle(20, 20, radius=3.0)
        world.compute_potential_field()

        state = world.get_state()

        assert state['size'] == 64
        assert state['num_energy_sources'] == 1
        assert state['num_obstacles'] == 1
        assert 'potential_range' in state
        assert 'potential_mean' in state

    def test_multiple_energy_sources(self):
        """Test multiple energy sources create combined field."""
        world = ToyWorld(size=64)
        world.add_energy_source(20, 32, strength=10.0)
        world.add_energy_source(40, 32, strength=10.0)
        world.compute_potential_field()

        # Point between sources should have high potential
        midpoint = world.get_potential(30, 32)
        corner = world.get_potential(0, 0)

        assert midpoint > corner
