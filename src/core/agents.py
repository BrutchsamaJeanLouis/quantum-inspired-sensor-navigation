"""
Module: src.core.agents.py
Depends on:
  - numpy
  - src.core.toy_world (ToyWorld)
  - src.core.quantum_world (QuantumInspiredWorld)

Bio-Inspired Navigation Agents
Phase 4: NanoAgent class for world navigation

Agents sense the guidance field, decide actions based on local coherence,
and trigger collapse when moving. This creates emergent exploration patterns.
"""

import numpy as np
from typing import Tuple, Union, Optional, List
from .toy_world import ToyWorld
from .quantum_world import QuantumInspiredWorld


class NanoAgent:
    """
    Bio-inspired agent that navigates using quantum-inspired world fields.

    The agent senses local guidance field, blends classical gradient descent
    with quantum-inspired sampling based on local coherence, and triggers
    field collapse when moving (Penrose-inspired observation effect).

    Attributes:
        x (int): Current X position
        y (int): Current Y position
        world (ToyWorld or QuantumInspiredWorld): World the agent navigates
        energy (float): Remaining energy (agent dies at 0)
        sense_radius (int): Radius of local sensing (default: 2, gives 5x5 patch)
        coherence_threshold (float): Threshold for quantum vs classical decision
        movement_cost (float): Energy cost per movement step
        alive (bool): Whether agent is still alive
        trail (List[Tuple[int, int]]): Movement history
    """

    def __init__(
        self,
        x: int,
        y: int,
        world: Union[ToyWorld, QuantumInspiredWorld],
        energy: float = 100.0,
        sense_radius: int = 2,
        coherence_threshold: float = 0.7,
        movement_cost: float = 1.0,
        max_trail_length: int = 100,
    ):
        """
        Initialize agent at position (x, y).

        Args:
            x: Starting X coordinate
            y: Starting Y coordinate
            world: World to navigate
            energy: Initial energy (default: 100)
            sense_radius: Sensing radius (default: 2, gives 5x5 patch)
            coherence_threshold: Use quantum move if coherence > threshold
            movement_cost: Energy cost per step (default: 1.0)
            max_trail_length: Maximum trail history length
        """
        self.x = x % world.size
        self.y = y % world.size
        self.world = world
        self.energy = energy
        self.sense_radius = sense_radius
        self.coherence_threshold = coherence_threshold
        self.movement_cost = movement_cost
        self.max_trail_length = max_trail_length
        self.alive = True
        self.trail: List[Tuple[int, int]] = [(self.x, self.y)]
        self.x_traj: List[int] = [self.x]
        self.y_traj: List[int] = [self.y]
        self.steps_taken = 0
        self.energy_source_cooldown: List[int] = [0] * len(world.energy_sources)
        self.in_dead_end = False
        self.dead_end_position: Optional[Tuple[int, int]] = None
        self.dead_end_escapes = 0

    def sense_environment(self) -> np.ndarray:
        """
        Query local guidance field patch.

        Returns:
            2D array of guidance field values in sensing radius
        """
        # Use guidance field if quantum world, else potential field
        if hasattr(self.world, 'get_guidance_field'):
            field = self.world.get_guidance_field()
        else:
            field = self.world.grid

        x_min = max(0, self.x - self.sense_radius)
        x_max = min(self.world.size - 1, self.x + self.sense_radius)
        y_min = max(0, self.y - self.sense_radius)
        y_max = min(self.world.size - 1, self.y + self.sense_radius)

        return field[x_min:x_max+1, y_min:y_max+1].copy()

    def decide_action(self) -> Tuple[int, int]:
        """
        Decide next movement direction.

        Uses classical gradient descent (steepest ascent) or quantum-inspired
        Boltzmann sampling based on local coherence.

        Returns:
            (dx, dy) movement direction
        """
        patch = self.sense_environment()

        # Get local coherence (quantum world only).
        # A zero-coupling world has no quantum channel, so its agents must
        # decide classically (the coupling ablation relies on this).
        use_quantum = False
        if hasattr(self.world, 'get_coherence_at'):
            coherence = self.world.get_coherence_at(self.x, self.y)
            quantum_available = getattr(self.world, 'quantum_coupling', 1.0) > 0
            use_quantum = (coherence > self.coherence_threshold
                          and quantum_available)

        if use_quantum:
            dx, dy = self._quantum_move(patch)
        else:
            dx, dy = self._classical_move(patch)

        return dx, dy

    def _classical_move(self, patch: np.ndarray) -> Tuple[int, int]:
        """
        Classical gradient descent: move toward steepest ascent.

        With world.classical_epsilon > 0 (epsilon-greedy control baseline),
        a uniform random step from the same action set is taken with
        probability epsilon — a stochastic classical baseline for
        comparison against quantum Boltzmann sampling.

        Args:
            patch: Local guidance field patch

        Returns:
            (dx, dy) toward highest value
        """
        eps = float(getattr(self.world, 'classical_epsilon', 0.0))
        if eps > 0.0 and np.random.uniform() < eps:
            flat_idx = int(np.random.randint(patch.size))
            gx, gy = np.unravel_index(flat_idx, patch.shape)
            return int(gx - self.sense_radius), int(gy - self.sense_radius)

        # Find argmax
        max_idx = np.argmax(patch)
        max_x, max_y = np.unravel_index(max_idx, patch.shape)

        # Center of patch is at (sense_radius, sense_radius)
        dx = int(max_x - self.sense_radius)
        dy = int(max_y - self.sense_radius)

        return dx, dy

    def _quantum_move(self, patch: np.ndarray) -> Tuple[int, int]:
        """
        Quantum-inspired Boltzmann sampling.

        Samples movement direction probabilistically based on field values,
        allowing exploration beyond pure gradient descent.

        Args:
            patch: Local guidance field patch

        Returns:
            (dx, dy) sampled direction
        """
        # Softmax-like distribution (Boltzmann)
        # Subtract max for numerical stability
        patch_centered = patch - np.max(patch)

        # Exponentiate (avoid overflow)
        probs = np.exp(patch_centered)

        # Normalize
        total = np.sum(probs)
        if total < 1e-10:
            # Uniform if all equal
            probs = np.ones_like(probs) / probs.size
        else:
            probs = probs / total

        # Sample
        flat_idx = np.random.choice(len(probs.flatten()), p=probs.flatten())
        sample_x, sample_y = np.unravel_index(flat_idx, probs.shape)

        dx = int(sample_x - self.sense_radius)
        dy = int(sample_y - self.sense_radius)

        return dx, dy

    def step(self) -> bool:
        """
        Take one step: decide, move, collapse, update energy.

        Returns:
            True if agent survived, False if died
        """
        if not self.alive:
            return False

        # Decide direction
        dx, dy = self.decide_action()

        # Move (wrap around edges on a torus, clamp on a closed boundary)
        if getattr(self.world, 'torus', True):
            new_x = (self.x + dx) % self.world.size
            new_y = (self.y + dy) % self.world.size
        else:
            new_x = max(0, min(self.world.size - 1, self.x + dx))
            new_y = max(0, min(self.world.size - 1, self.y + dy))

        # Trigger collapse (quantum world only)
        if hasattr(self.world, 'collapse_field'):
            self.world.collapse_field(self.x, self.y, radius=3)

        # Update position
        self.x = new_x
        self.y = new_y
        self.x_traj.append(self.x)
        self.y_traj.append(self.y)
        self.steps_taken += 1

        # Update trail
        self.trail.append((self.x, self.y))
        if len(self.trail) > self.max_trail_length:
            self.trail = self.trail[-self.max_trail_length:]

        # Energy cost
        self.energy -= self.movement_cost

        # Check energy source collision
        self._check_energy_sources()

        # Check death
        if self.energy <= 0:
            self.alive = False

        return self.alive

    def _check_energy_sources(self) -> None:
        """Check if agent is on an energy source and recharge (with cooldown)."""
        for i, (ex, ey, strength) in enumerate(self.world.energy_sources):
            if i >= len(self.energy_source_cooldown):
                break
            if self.energy_source_cooldown[i] > 0:
                self.energy_source_cooldown[i] -= 1
                continue
            dist = np.sqrt((self.x - ex)**2 + (self.y - ey)**2)
            if dist < 3:  # Within radius of energy source
                self.energy += strength
                self.energy_source_cooldown[i] = 50  # Cooldown steps before next pickup

    def check_dead_end_status(self, window: int = 20, stuck_threshold: int = 5) -> bool:
        """
        Check if agent is currently stuck in a dead end.

        Dead end = agent revisiting same small area repeatedly without
        making progress. Returns True if currently in dead end state.

        Args:
            window: Number of recent positions to analyze
            stuck_threshold: Max unique positions before not considered stuck

        Returns:
            True if agent appears stuck in dead end
        """
        if len(self.trail) < window:
            return False

        recent = self.trail[-window:]
        unique_positions = set(recent)

        # Check if stuck: few unique positions in recent history
        is_stuck = len(unique_positions) < stuck_threshold

        # Check if near a local minimum (gradient points inward)
        near_obstacle = self._near_obstacle_boundary()

        was_in_dead_end = self.in_dead_end
        self.in_dead_end = is_stuck and near_obstacle

        # Count escape: was stuck, now not stuck
        if was_in_dead_end and not self.in_dead_end:
            self.dead_end_escapes += 1
            self.dead_end_position = None
        elif self.in_dead_end and self.dead_end_position is None:
            self.dead_end_position = (self.x, self.y)

        return self.in_dead_end

    def _near_obstacle_boundary(self, margin: int = 4) -> bool:
        """Check if agent is near an obstacle boundary (potential dead end wall)."""
        for ox, oy, radius in self.world.obstacles:
            dist = np.sqrt((self.x - ox)**2 + (self.y - oy)**2)
            if radius < dist < radius + margin:
                return True
        return False

    def get_position(self) -> Tuple[int, int]:
        """Get current position."""
        return self.x, self.y

    def get_state(self) -> dict:
        """
        Get agent state.

        Returns:
            Dictionary with agent state information
        """
        return {
            'x': self.x,
            'y': self.y,
            'energy': self.energy,
            'alive': self.alive,
            'steps_taken': self.steps_taken,
            'trail_length': len(self.trail),
            'in_dead_end': self.in_dead_end,
            'dead_end_escapes': self.dead_end_escapes,
        }


class AgentSwarm:
    """
    Manages a swarm of NanoAgents.

    Provides batch operations for simulation and analysis.
    """

    def __init__(
        self,
        world: Union[ToyWorld, QuantumInspiredWorld],
        population: int = 20,
        spawn_mode: str = 'random',
    ):
        """
        Initialize agent swarm.

        Args:
            world: World to populate
            population: Number of agents
            spawn_mode: 'random', 'corner', or 'cluster'
        """
        self.world = world
        self.agents: List[NanoAgent] = []
        self._spawn_agents(population, spawn_mode)

    def _spawn_agents(self, population: int, mode: str) -> None:
        """Spawn agents in specified pattern."""
        size = self.world.size

        if mode == 'random':
            for _ in range(population):
                x = np.random.randint(0, size)
                y = np.random.randint(0, size)
                self.agents.append(NanoAgent(x, y, self.world))

        elif mode == 'corner':
            for i in range(population):
                x = i % 10
                y = i // 10
                self.agents.append(NanoAgent(x, y, self.world))

        elif mode == 'cluster':
            cx, cy = size // 2, size // 2
            for _ in range(population):
                x = cx + np.random.randint(-5, 6)
                y = cy + np.random.randint(-5, 6)
                self.agents.append(NanoAgent(x, y, self.world))

    def step_all(self) -> int:
        """
        Step all alive agents.

        Returns:
            Number of agents that survived
        """
        survivors = 0
        for agent in self.agents:
            if agent.alive:
                if agent.step():
                    survivors += 1
        return survivors

    def get_alive_agents(self) -> List[NanoAgent]:
        """Get list of alive agents."""
        return [a for a in self.agents if a.alive]

    def get_stats(self) -> dict:
        """
        Get swarm statistics.

        Returns:
            Dictionary with swarm stats
        """
        alive = self.get_alive_agents()
        if not alive:
            return {
                'total': len(self.agents),
                'alive': 0,
                'dead': len(self.agents),
                'avg_energy': 0,
                'avg_steps': 0,
            }

        return {
            'total': len(self.agents),
            'alive': len(alive),
            'dead': len(self.agents) - len(alive),
            'avg_energy': np.mean([a.energy for a in alive]),
            'avg_steps': np.mean([a.steps_taken for a in alive]),
            'max_steps': max(a.steps_taken for a in alive),
        }
