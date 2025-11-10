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
        self.pilot_wave = np.zeros((size, size), dtype=np.float32)
        self.coherence = np.ones((size, size), dtype=np.float32)

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

        # Compute potential for each grid cell
        for x in range(self.size):
            for y in range(self.size):
                potential = 0.0

                # Attraction to energy sources (1/r potential)
                for ex, ey, strength in self.energy_sources:
                    dist = np.sqrt((x - ex)**2 + (y - ey)**2) + 1e-5
                    potential += strength / dist

                # Repulsion from obstacles (negative 1/r potential)
                for ox, oy, radius in self.obstacles:
                    dist = np.sqrt((x - ox)**2 + (y - oy)**2) + 1e-5
                    if dist < radius:
                        potential -= 10.0 / dist

                self.grid[x, y] = potential

    def update_pilot_wave(self, dt: float = 0.1) -> None:
        """
        Update the pilot wave field using diffusion.

        Args:
            dt: Time step for diffusion
        """
        # Laplacian (diffusion) - spreads influence
        laplacian = (
            np.roll(self.pilot_wave, 1, axis=0) +
            np.roll(self.pilot_wave, -1, axis=0) +
            np.roll(self.pilot_wave, 1, axis=1) +
            np.roll(self.pilot_wave, -1, axis=1) -
            4 * self.pilot_wave
        )
        self.pilot_wave += dt * laplacian

        # Couple to energy sources (pilot wave "guides" toward energy)
        for ex, ey, strength in self.energy_sources:
            self.pilot_wave[ex, ey] += strength * dt

    def collapse_field(self, x: int, y: int, radius: int = 3) -> None:
        """
        Collapse the field around a point (Penrose-inspired).

        Args:
            x: X coordinate of the observation point
            y: Y coordinate of the observation point
            radius: Radius of influence for collapse
        """
        for dx in range(-radius, radius + 1):
            for dy in range(-radius, radius + 1):
                nx, ny = (x + dx) % self.size, (y + dy) % self.size
                dist = np.sqrt(dx**2 + dy**2)
                if dist < radius:
                    # Collapse reduces coherence, sharpens pilot wave
                    self.coherence[nx, ny] *= 0.9
                    self.pilot_wave[nx, ny] *= 1.1

    def get_guidance_field(self) -> np.ndarray:
        """
        Get the combined classical and quantum guidance field.

        Returns:
            Combined guidance field as a numpy array
        """
        return self.grid + 0.3 * self.pilot_wave  # Tunable coupling

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
