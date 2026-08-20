"""
Module: src\\core\\toy_world.py
Depends on:
  - None (standalone)

Toy Physics Substrate for Quantum-Inspired World Model
Phase 1: Classical potential field simulation

This module implements a minimal 2D physics simulation where agents can
navigate through energy gradients and obstacles.
"""

import numpy as np
from typing import List, Tuple, Optional


class ToyWorld:
    """
    Classical 2D world with potential fields, energy sources, and obstacles.

    This serves as the baseline for quantum-inspired enhancements in later phases.

    Attributes:
        size (int): Grid dimensions (size x size)
        grid (np.ndarray): 2D potential field
        energy_sources (List[Tuple]): List of (x, y, strength) tuples
        obstacles (List[Tuple]): List of (x, y, radius) tuples
    """

    def __init__(self, size: int = 128):
        """
        Initialize the toy world with empty grid.

        Args:
            size: Dimension of the square grid (default: 128x128)
        """
        self.size = size
        self.grid = np.zeros((size, size), dtype=np.float32)
        self.energy_sources: List[Tuple[int, int, float]] = []
        self.obstacles: List[Tuple[int, int, float]] = []

    def add_energy_source(self, x: int, y: int, strength: float = 1.0) -> None:
        """
        Add an energy source (attractor) to the world.

        Args:
            x: X coordinate (0 to size-1)
            y: Y coordinate (0 to size-1)
            strength: Attraction strength (default: 1.0)
        """
        if not (0 <= x < self.size and 0 <= y < self.size):
            raise ValueError(f"Coordinates ({x}, {y}) out of bounds [0, {self.size})")

        self.energy_sources.append((x, y, strength))

    def add_obstacle(self, x: int, y: int, radius: float = 5.0) -> None:
        """
        Add an obstacle (repulsor) to the world.

        Args:
            x: X coordinate (0 to size-1)
            y: Y coordinate (0 to size-1)
            radius: Obstacle radius (default: 5.0)
        """
        if not (0 <= x < self.size and 0 <= y < self.size):
            raise ValueError(f"Coordinates ({x}, {y}) out of bounds [0, {self.size})")

        self.obstacles.append((x, y, radius))

    def compute_potential_field(self) -> None:
        """
        Compute the classical gradient descent field.

        Combines attraction from energy sources and repulsion from obstacles
        to create a potential field that guides agent navigation.

        This is the baseline classical approach that will be enhanced
        with quantum-inspired dynamics in Phase 2.
        """
        # Reset grid
        self.grid.fill(0.0)

        # Create coordinate arrays for vectorized computation
        xx, yy = np.meshgrid(np.arange(self.size), np.arange(self.size), indexing='ij')

        # Attraction to energy sources (1/r potential) — vectorized
        for ex, ey, strength in self.energy_sources:
            dist = np.sqrt((xx - ex)**2 + (yy - ey)**2) + 1e-5
            self.grid += strength / dist

        # Repulsion from obstacles (negative 1/r potential) — vectorized
        for ox, oy, radius in self.obstacles:
            dist = np.sqrt((xx - ox)**2 + (yy - oy)**2) + 1e-5
            mask = dist < radius
            self.grid[mask] -= 10.0 / dist[mask]

    def get_gradient(self, x: int, y: int) -> Tuple[float, float]:
        """
        Get the gradient (direction of steepest ascent) at a position.

        Args:
            x: X coordinate
            y: Y coordinate

        Returns:
            Tuple of (dx, dy) gradient components
        """
        # Use central difference for gradient estimation
        dx = 0.0
        dy = 0.0

        if x > 0 and x < self.size - 1:
            dx = (self.grid[x + 1, y] - self.grid[x - 1, y]) / 2.0

        if y > 0 and y < self.size - 1:
            dy = (self.grid[x, y + 1] - self.grid[x, y - 1]) / 2.0

        return dx, dy

    def get_potential(self, x: int, y: int) -> float:
        """
        Get the potential value at a specific position.

        Args:
            x: X coordinate
            y: Y coordinate

        Returns:
            Potential value at (x, y)
        """
        if not (0 <= x < self.size and 0 <= y < self.size):
            return -np.inf  # Out of bounds is infinitely bad

        return self.grid[x, y]

    def clear(self) -> None:
        """Clear all energy sources and obstacles from the world."""
        self.energy_sources.clear()
        self.obstacles.clear()
        self.grid.fill(0.0)

    def get_state(self) -> dict:
        """
        Get the current state of the world.

        Returns:
            Dictionary containing world state information
        """
        return {
            'size': self.size,
            'num_energy_sources': len(self.energy_sources),
            'num_obstacles': len(self.obstacles),
            'potential_range': (self.grid.min(), self.grid.max()),
            'potential_mean': self.grid.mean()
        }
