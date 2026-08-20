"""
Unit tests for QuantumInspiredWorld class - Phase 2
"""

import sys
import os
import numpy as np
import pytest

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.core import QuantumInspiredWorld


class TestQuantumInspiredWorld:
    """Test suite for QuantumInspiredWorld quantum dynamics."""

    def test_initialization(self):
        """Test quantum world initialization."""
        world = QuantumInspiredWorld(size=64)
        assert world.size == 64
        assert world.grid.shape == (64, 64)
        assert world.pilot_wave.shape == (64, 64)
        assert world.coherence.shape == (64, 64)
        assert world.quantum_coupling == 0.3
        assert np.all(world.pilot_wave == 0)
        assert np.all(world.coherence == 1)

    def test_custom_parameters(self):
        """Test custom quantum parameters."""
        world = QuantumInspiredWorld(
            size=64,
            quantum_coupling=0.5,
            diffusion_rate=0.2,
            collapse_coherence_decay=0.8,
            collapse_wave_amplify=1.2,
        )
        assert world.quantum_coupling == 0.5
        assert world.diffusion_rate == 0.2
        assert world.collapse_coherence_decay == 0.8
        assert world.collapse_wave_amplify == 1.2

    def test_inherits_classical_behavior(self):
        """Test that quantum world inherits classical ToyWorld behavior."""
        world = QuantumInspiredWorld(size=64)
        world.add_energy_source(32, 32, strength=10.0)
        world.add_obstacle(10, 10, radius=5.0)
        world.compute_potential_field()

        assert world.grid[32, 32] > world.grid[0, 0]
        assert len(world.energy_sources) == 1
        assert len(world.obstacles) == 1

    def test_update_pilot_wave(self):
        """Test pilot wave field update."""
        world = QuantumInspiredWorld(size=64)
        world.add_energy_source(32, 32, strength=10.0)
        world.compute_potential_field()

        # Store initial pilot wave values
        initial_pilot_wave = world.pilot_wave.copy()

        # Update pilot wave
        world.update_pilot_wave(dt=0.1)

        # Pilot wave should have changed
        assert not np.array_equal(world.pilot_wave, initial_pilot_wave)

        # Pilot wave should be non-negative (after diffusion from zero)
        assert np.all(world.pilot_wave >= 0)

    def test_pilot_wave_coupling_to_energy(self):
        """Test pilot wave couples to energy sources."""
        world = QuantumInspiredWorld(size=64)
        world.add_energy_source(32, 32, strength=10.0)
        world.compute_potential_field()

        # Multiple updates should increase pilot wave at energy source
        for _ in range(10):
            world.update_pilot_wave(dt=0.1)

        assert world.pilot_wave[32, 32] > 0

    def test_collapse_field(self):
        """Test field collapse mechanism."""
        world = QuantumInspiredWorld(size=64)
        world.add_energy_source(32, 32, strength=10.0)
        world.compute_potential_field()
        world.update_pilot_wave(dt=0.1)

        # Store initial values
        initial_coherence = world.coherence.copy()
        initial_pilot_wave = world.pilot_wave.copy()

        # Collapse at center
        world.collapse_field(32, 32, radius=3)

        # Coherence should be reduced in the collapsed region
        assert world.coherence[32, 32] < initial_coherence[32, 32]

        # Pilot wave should be increased in the collapsed region
        assert world.pilot_wave[32, 32] > initial_pilot_wave[32, 32]

    def test_collapse_radius(self):
        """Test collapse affects only specified radius."""
        world = QuantumInspiredWorld(size=64)
        world.update_pilot_wave(dt=0.1)

        initial_coherence = world.coherence.copy()

        # Collapse at center with radius 2
        world.collapse_field(32, 32, radius=2)

        # Inside radius should be affected
        assert world.coherence[32, 32] < initial_coherence[32, 32]

        # Outside radius should be unchanged
        assert world.coherence[32, 35] == initial_coherence[32, 35]

    def test_get_guidance_field(self):
        """Test guidance field computation."""
        world = QuantumInspiredWorld(size=64, quantum_coupling=0.3)
        world.add_energy_source(32, 32, strength=10.0)
        world.compute_potential_field()
        world.update_pilot_wave(dt=0.1)

        # Get guidance field
        guidance_field = world.get_guidance_field()

        # Should return a numpy array with same shape
        assert guidance_field.shape == (64, 64)

        # Should be a combination of grid and normalized pilot_wave
        normalized = world.pilot_wave / world.pilot_wave.max()
        expected = world.grid + 0.3 * world.pilot_wave_gain * normalized
        assert np.allclose(guidance_field, expected)

    def test_guidance_field_with_different_coupling(self):
        """Test guidance field respects quantum coupling parameter."""
        world = QuantumInspiredWorld(size=64, quantum_coupling=0.5)
        world.add_energy_source(32, 32, strength=10.0)
        world.compute_potential_field()
        world.update_pilot_wave(dt=0.1)

        guidance = world.get_guidance_field()
        normalized = world.pilot_wave / world.pilot_wave.max()
        expected = world.grid + 0.5 * world.pilot_wave_gain * normalized
        assert np.allclose(guidance, expected)

    def test_guidance_field_pilot_wave_normalization(self):
        """Pilot wave contribution normalized so gain is comparable to grid."""
        world = QuantumInspiredWorld(size=64, quantum_coupling=0.5)
        world.add_energy_source(32, 32, strength=10.0)
        world.compute_potential_field()
        for _ in range(20):
            world.update_pilot_wave(dt=0.1)

        guidance = world.get_guidance_field()
        # Quantum term at the pilot wave max location must equal
        # coupling * gain (normalized pilot wave is 1.0 there)
        pmax_loc = np.unravel_index(np.argmax(world.pilot_wave), world.pilot_wave.shape)
        quantum_term = guidance[pmax_loc] - world.grid[pmax_loc]
        assert abs(quantum_term - world.quantum_coupling * world.pilot_wave_gain) < 1e-3

    def test_guidance_field_zero_pilot_wave(self):
        """Zero pilot wave: guidance field equals classical grid."""
        world = QuantumInspiredWorld(size=32, quantum_coupling=0.3)
        world.add_energy_source(16, 16, strength=10.0)
        world.compute_potential_field()
        assert np.array_equal(world.pilot_wave, np.zeros((32, 32)))
        assert np.allclose(world.get_guidance_field(), world.grid)

    def test_get_coherence_at(self):
        """Test getting coherence at specific coordinates."""
        world = QuantumInspiredWorld(size=64)

        # Default coherence is 1.0
        assert world.get_coherence_at(32, 32) == 1.0

        # Collapse reduces coherence
        world.collapse_field(32, 32, radius=3)
        assert world.get_coherence_at(32, 32) < 1.0

        # Out of bounds returns 0
        assert world.get_coherence_at(-1, 10) == 0.0

    def test_get_state(self):
        """Test getting extended state with quantum fields."""
        world = QuantumInspiredWorld(size=64)
        world.add_energy_source(32, 32, strength=10.0)
        world.compute_potential_field()
        world.update_pilot_wave(dt=0.1)

        state = world.get_state()

        # Classical state
        assert state['size'] == 64
        assert state['num_energy_sources'] == 1

        # Quantum state
        assert 'pilot_wave_range' in state
        assert 'pilot_wave_mean' in state
        assert 'coherence_range' in state
        assert 'coherence_mean' in state
        assert state['quantum_coupling'] == 0.3

    def test_non_local_propagation(self):
        """Test that pilot wave propagates non-locally."""
        world = QuantumInspiredWorld(size=64)
        world.add_energy_source(0, 0, strength=10.0)  # Corner
        world.compute_potential_field()

        # Update pilot wave multiple times
        for _ in range(20):
            world.update_pilot_wave(dt=0.1)

        # Opposite corner should have non-zero pilot wave (non-local effect)
        opposite_corner = world.pilot_wave[63, 63]
        assert opposite_corner > 0
