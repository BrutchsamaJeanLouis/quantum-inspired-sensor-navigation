"""
Module: src.core.coherence.py
Depends on:
  - numpy
  - src.core.toy_world (ToyWorld)
  - src.core.quantum_world (QuantumInspiredWorld)

IIT-Inspired Coherence Measurement
Phase 3: Phi (Φ) calculation for world regions

This module implements a simplified Integrated Information Theory (IIT)
coherence metric for measuring self-organization in world regions.

High Φ regions: self-organized (maintain structure despite environment)
Low Φ regions: externally-driven (passive response)
"""

import numpy as np
from typing import Tuple, Union
from .toy_world import ToyWorld


def compute_phi(
    world: Union[ToyWorld, 'QuantumInspiredWorld'],
    region: Tuple[int, int, int, int],
    steps: int = 5,
) -> float:
    """
    Compute IIT-inspired Φ (phi) for a world region.

    Φ measures how self-organized a region is versus how much it's driven
    by external forces. High Φ indicates self-organization; low Φ indicates
    passive response to environment.

    Args:
        world: ToyWorld or QuantumInspiredWorld instance
        region: (x_min, y_min, x_max, y_max) bounding box of region
        steps: Number of forward simulation steps for prediction (default: 5)

    Returns:
        Phi value: max(0, internal_correlation - external_correlation)
        Higher values = more self-organized
    """
    x_min, y_min, x_max, y_max = region

    # Clamp region to world bounds
    x_min = max(0, x_min)
    y_min = max(0, y_min)
    x_max = min(world.size - 1, x_max)
    y_max = min(world.size - 1, y_max)

    if x_min >= x_max or y_min >= y_max:
        return 0.0

    # Use clamped region
    clamped_region = (x_min, y_min, x_max, y_max)

    # Sample initial state of the region
    t0_internal = world.grid[x_min:x_max+1, y_min:y_max+1].copy()

    # Sample boundary (external) state
    boundary = _get_boundary(world, clamped_region)

    # Simulate forward to get t1 state
    t1_internal = _simulate_forward(world, region, steps)

    # Compute internal correlation: how well t0 predicts t1
    internal_corr = _correlation(t0_internal.flatten(), t1_internal.flatten())

    # Compute external correlation: how well boundary predicts t1
    external_corr = _correlation(boundary.flatten(), t1_internal.flatten())

    # Phi = internal self-prediction minus external drive
    phi = max(0.0, internal_corr - external_corr)

    return float(phi)


def compute_phi_map(
    world: Union[ToyWorld, 'QuantumInspiredWorld'],
    region_size: int = 8,
    overlap: int = 4,
) -> np.ndarray:
    """
    Compute Φ map for the entire world using sliding window.

    Args:
        world: ToyWorld or QuantumInspiredWorld instance
        region_size: Size of sliding window (default: 8)
        overlap: Overlap between windows (default: 4)

    Returns:
        2D array of Φ values (coarser resolution than world grid)
    """
    stride = region_size - overlap
    x_steps = (world.size - 1) // stride + 1
    y_steps = (world.size - 1) // stride + 1

    phi_map = np.zeros((x_steps, y_steps), dtype=np.float32)

    for i in range(x_steps):
        for j in range(y_steps):
            x_min = i * stride
            y_min = j * stride
            x_max = min(x_min + region_size - 1, world.size - 1)
            y_max = min(y_min + region_size - 1, world.size - 1)

            phi_map[i, j] = compute_phi(world, (x_min, y_min, x_max, y_max))

    return phi_map


def _get_boundary(world: ToyWorld, region: Tuple[int, int, int, int]) -> np.ndarray:
    """
    Extract boundary cells surrounding a region.

    Args:
        world: World instance
        region: (x_min, y_min, x_max, y_max)

    Returns:
        2D array of boundary values (same shape as region, interior = 0)
    """
    x_min, y_min, x_max, y_max = region
    boundary = np.zeros((x_max - x_min + 1, y_max - y_min + 1), dtype=np.float32)

    # Top row
    boundary[0, :] = world.grid[x_min, y_min:y_max+1]
    # Bottom row
    boundary[-1, :] = world.grid[x_max, y_min:y_max+1]
    # Left column
    boundary[:, 0] = world.grid[x_min:x_max+1, y_min]
    # Right column
    boundary[:, -1] = world.grid[x_min:x_max+1, y_max]

    return boundary


def _simulate_forward(
    world: Union[ToyWorld, 'QuantumInspiredWorld'],
    region: Tuple[int, int, int, int],
    steps: int,
) -> np.ndarray:
    """
    Simulate world forward and return region state.

    For QuantumInspiredWorld, includes pilot wave dynamics.
    For ToyWorld, recomputes potential field each step.

    Args:
        world: World instance
        region: (x_min, y_min, x_max, y_max)
        steps: Number of steps to simulate

    Returns:
        Region state after simulation
    """
    x_min, y_min, x_max, y_max = region

    # Check if quantum world
    has_pilot_wave = hasattr(world, 'pilot_wave')

    for _ in range(steps):
        # Recompute potential field (simulates dynamics)
        world.compute_potential_field()

        # Update pilot wave if quantum world
        if has_pilot_wave:
            world.update_pilot_wave()

    # Return guidance field if quantum, else potential field
    if has_pilot_wave:
        return world.get_guidance_field()[x_min:x_max+1, y_min:y_max+1].copy()
    else:
        return world.grid[x_min:x_max+1, y_min:y_max+1].copy()


def _correlation(x: np.ndarray, y: np.ndarray) -> float:
    """
    Compute Pearson correlation coefficient between two arrays.

    Args:
        x: First array
        y: Second array

    Returns:
        Correlation coefficient in [-1, 1], or 0 if undefined
    """
    # Handle edge cases
    if len(x) != len(y) or len(x) < 2:
        return 0.0

    # Standardize
    x_mean = np.mean(x)
    y_mean = np.mean(y)
    x_std = np.std(x)
    y_std = np.std(y)

    if x_std < 1e-10 or y_std < 1e-10:
        return 0.0

    # Pearson correlation
    corr = np.mean((x - x_mean) * (y - y_mean)) / (x_std * y_std)
    return float(np.clip(corr, -1.0, 1.0))
