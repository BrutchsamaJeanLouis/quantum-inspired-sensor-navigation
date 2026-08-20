"""
Unit tests for agents module - Phase 4
"""

import sys
import os
import numpy as np
import pytest

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.core import ToyWorld, QuantumInspiredWorld, NanoAgent, AgentSwarm


class TestNanoAgent:
    """Test suite for NanoAgent bio-inspired navigation."""

    def test_initialization(self):
        """Test agent initialization."""
        world = ToyWorld(size=64)
        agent = NanoAgent(10, 10, world)

        assert agent.x == 10
        assert agent.y == 10
        assert agent.energy == 100.0
        assert agent.alive is True
        assert len(agent.trail) == 1

    def test_initialization_quantum_world(self):
        """Test agent initialization with quantum world."""
        world = QuantumInspiredWorld(size=64)
        agent = NanoAgent(10, 10, world)

        assert agent.world is world
        assert agent.coherence_threshold == 0.7

    def test_position_wrapping(self):
        """Test that position wraps around world edges."""
        world = ToyWorld(size=64)
        agent = NanoAgent(70, 70, world)  # Out of bounds

        assert agent.x == 6
        assert agent.y == 6

    def test_sense_environment(self):
        """Test local field sensing."""
        world = ToyWorld(size=64)
        world.add_energy_source(32, 32, strength=10.0)
        world.compute_potential_field()

        agent = NanoAgent(30, 30, world)
        patch = agent.sense_environment()

        assert patch.shape == (5, 5)  # sense_radius=2 gives 5x5

    def test_sense_environment_quantum(self):
        """Test sensing uses guidance field for quantum world."""
        world = QuantumInspiredWorld(size=64)
        world.add_energy_source(32, 32, strength=10.0)
        world.compute_potential_field()
        world.update_pilot_wave(dt=0.1)

        agent = NanoAgent(30, 30, world)
        patch = agent.sense_environment()

        assert patch.shape == (5, 5)

    def test_classical_move_toward_energy(self):
        """Test classical move goes toward energy source."""
        world = ToyWorld(size=64)
        world.add_energy_source(50, 32, strength=100.0)
        world.compute_potential_field()

        agent = NanoAgent(40, 32, world)
        dx, dy = agent._classical_move(agent.sense_environment())

        # Should move right (positive x) toward source
        assert dx >= 0

    def test_step_moves_agent(self):
        """Test that step changes position."""
        world = ToyWorld(size=64)
        world.add_energy_source(50, 32, strength=100.0)
        world.compute_potential_field()

        agent = NanoAgent(40, 32, world)
        agent.step()

        assert agent.steps_taken == 1
        assert len(agent.trail) == 2

    def test_step_costs_energy(self):
        """Test that step costs energy."""
        world = ToyWorld(size=64)
        agent = NanoAgent(10, 10, world, energy=100.0, movement_cost=1.0)

        agent.step()
        assert agent.energy == 99.0

    def test_agent_dies_at_zero_energy(self):
        """Test agent dies when energy reaches 0."""
        world = ToyWorld(size=64)
        agent = NanoAgent(10, 10, world, energy=5.0, movement_cost=1.0)

        for _ in range(5):
            agent.step()

        assert agent.alive is False

    def test_energy_source_recharge(self):
        """Test agent recharges at energy source."""
        world = ToyWorld(size=64)
        world.add_energy_source(10, 10, strength=10.0)
        world.compute_potential_field()

        agent = NanoAgent(10, 10, world, energy=10.0)
        initial_energy = agent.energy

        # Move around and back to source
        agent.step()
        agent.step()

        # Energy should have increased if near source
        assert agent.energy >= initial_energy - 2

    def test_collapse_on_step(self):
        """Test agent triggers collapse in quantum world."""
        world = QuantumInspiredWorld(size=64)
        initial_coherence = world.coherence.copy()

        agent = NanoAgent(32, 32, world)
        agent.step()

        # Coherence should be reduced around old position
        assert world.coherence[32, 32] < initial_coherence[32, 32]

    def test_get_state(self):
        """Test agent state reporting."""
        world = ToyWorld(size=64)
        agent = NanoAgent(10, 10, world)
        agent.step()

        state = agent.get_state()
        assert state['x'] == agent.x
        assert state['y'] == agent.y
        assert state['alive'] is True
        assert state['steps_taken'] == 1


class TestAgentSwarm:
    """Test suite for AgentSwarm management."""

    def test_initialization(self):
        """Test swarm initialization."""
        world = ToyWorld(size=64)
        swarm = AgentSwarm(world, population=10)

        assert len(swarm.agents) == 10

    def test_random_spawn(self):
        """Test random spawn mode."""
        world = ToyWorld(size=64)
        swarm = AgentSwarm(world, population=10, spawn_mode='random')

        positions = [(a.x, a.y) for a in swarm.agents]
        assert len(positions) == 10

    def test_corner_spawn(self):
        """Test corner spawn mode."""
        world = ToyWorld(size=64)
        swarm = AgentSwarm(world, population=10, spawn_mode='corner')

        # All should be near (0, 0)
        for agent in swarm.agents:
            assert agent.x < 10
            assert agent.y < 10

    def test_cluster_spawn(self):
        """Test cluster spawn mode."""
        world = ToyWorld(size=64)
        swarm = AgentSwarm(world, population=10, spawn_mode='cluster')

        # All should be near center
        for agent in swarm.agents:
            assert 25 < agent.x < 39
            assert 25 < agent.y < 39

    def test_step_all(self):
        """Test stepping all agents."""
        world = ToyWorld(size=64)
        world.add_energy_source(32, 32, strength=10.0)
        world.compute_potential_field()

        swarm = AgentSwarm(world, population=5)
        survivors = swarm.step_all()

        assert survivors == 5  # All should survive one step

    def test_get_alive_agents(self):
        """Test getting alive agents."""
        world = ToyWorld(size=64)
        swarm = AgentSwarm(world, population=5)

        alive = swarm.get_alive_agents()
        assert len(alive) == 5

    def test_get_stats(self):
        """Test swarm statistics."""
        world = ToyWorld(size=64)
        swarm = AgentSwarm(world, population=5)

        stats = swarm.get_stats()
        assert stats['total'] == 5
        assert stats['alive'] == 5
        assert stats['dead'] == 0


class TestZeroCouplingClassicalBehavior:
    """A zero-coupling quantum world must run classical (deterministic
    argmax) decision-making, not Boltzmann sampling. This is what makes
    the coupling ablation a meaningful classical baseline."""

    def test_zero_coupling_uses_classical_move(self):
        """q=0 agents move exactly where the guidance-field argmax points,
        repeated over many trials (no sampling noise)."""
        world = QuantumInspiredWorld(size=64, quantum_coupling=0.0)
        world.add_energy_source(40, 40, strength=100.0)
        world.compute_potential_field()
        agent = NanoAgent(10, 10, world)
        patch = agent.sense_environment()
        max_idx = np.argmax(patch)
        expected_dx = int(np.unravel_index(max_idx, patch.shape)[0]
                          - agent.sense_radius)
        expected_dy = int(np.unravel_index(max_idx, patch.shape)[1]
                          - agent.sense_radius)
        for _ in range(20):
            dx, dy = agent.decide_action()
            assert (dx, dy) == (expected_dx, expected_dy)

    def test_positive_coupling_can_sample_stochastically(self):
        """q>0 agents may deviate from pure argmax (Boltzmann sampling)
        when coherence is high."""
        world = QuantumInspiredWorld(size=64, quantum_coupling=0.5)
        world.add_energy_source(40, 40, strength=100.0)
        world.compute_potential_field()
        for _ in range(100):
            world.update_pilot_wave(dt=0.1)
        agent = NanoAgent(10, 10, world)
        patch = agent.sense_environment()
        max_idx = np.argmax(patch)
        argmax_dx = int(np.unravel_index(max_idx, patch.shape)[0]
                        - agent.sense_radius)
        argmax_dy = int(np.unravel_index(max_idx, patch.shape)[1]
                        - agent.sense_radius)
        moves = {agent.decide_action() for _ in range(300)}
        # Sampling must include the argmax and produce >1 distinct move
        assert (argmax_dx, argmax_dy) in moves
        assert len(moves) > 1


class TestEpsilonGreedyClassicalControl:
    """Stochastic classical baseline: world.classical_epsilon makes
    classical decision steps uniform-random with probability epsilon."""

    def test_high_epsilon_moves_stochastically(self):
        world = QuantumInspiredWorld(
            size=64, quantum_coupling=0.0, classical_epsilon=0.99)
        world.add_energy_source(40, 40, strength=100.0)
        world.compute_potential_field()
        agent = NanoAgent(10, 10, world)
        moves = {agent.decide_action() for _ in range(200)}
        assert len(moves) > 5

    def test_zero_epsilon_is_deterministic(self):
        world = QuantumInspiredWorld(
            size=64, quantum_coupling=0.0, classical_epsilon=0.0)
        world.add_energy_source(40, 40, strength=100.0)
        world.compute_potential_field()
        agent = NanoAgent(10, 10, world)
        moves = {agent.decide_action() for _ in range(200)}
        assert len(moves) == 1


class TestXTrajectory:
    def test_traj_records_every_step(self):
        world = ToyWorld(32)
        world.add_energy_source(20, 20, strength=50.0)
        world.compute_potential_field()
        agent = NanoAgent(5, 5, world)
        for _ in range(10):
            agent.step()
        assert len(agent.x_traj) == 11
        assert agent.x_traj[-1] == agent.x
