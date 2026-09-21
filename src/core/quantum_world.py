"""
Module: src.core.quantum_world.py
Depends on:
  - src.core.toy_world (ToyWorld)

Quantum-Inspired World Model
Phase 2: Pilot waves, collapse mechanics, guidance fields

This module extends the classical ToyWorld with quantum-inspired dynamics:
- Bohmian pilot wave (non-local guidance field)
- Penrose-inspired collapse (observer-triggered decoherence)
- Combined guidance field (classical + quantum)
"""

import numpy as np
from typing import Tuple
from .toy_world import ToyWorld


class QuantumInspiredWorld(ToyWorld):
    """
    Quantum-inspired world extending classical ToyWorld.

    Adds non-local pilot wave dynamics and collapse mechanics inspired by
    Bohmian mechanics and Penrose's objective reduction theory.

    Attributes:
        pilot_wave (np.ndarray): Non-local guidance field (diffusion-based)
        coherence (np.ndarray): Local coherence field (1.0 = fully coherent)
        quantum_coupling (float): Weight of pilot wave in guidance field
        diffusion_rate (float): Rate of pilot wave diffusion
        collapse_coherence_decay (float): Coherence multiplier on collapse
        collapse_wave_amplify (float): Pilot wave multiplier on collapse
    """

    def __init__(
        self,
        size: int = 128,
        quantum_coupling: float = 0.3,
        diffusion_rate: float = 0.1,
        collapse_coherence_decay: float = 0.9,
        collapse_wave_amplify: float = 1.1,
        pilot_wave_gain: float = 3000.0,
        pilot_wave_dissipation: float = 0.9999,
        classical_epsilon: float = 0.0,
        torus: bool = True,
    ):
        """
        Initialize quantum-inspired world.

        Args:
            size: Grid dimension (default: 128x128)
            torus: True = positions wrap at edges (default); False = closed
                boundary, positions clamp at edges (edge wraps become dead
                ends — used to test whether seam-shortcut results are a
                torus artifact).
            quantum_coupling: Weight of pilot wave in guidance field (default: 0.3)
            diffusion_rate: Pilot wave diffusion rate (default: 0.1)
            collapse_coherence_decay: Coherence multiplier on collapse (default: 0.9)
            collapse_wave_amplify: Pilot wave multiplier on collapse (default: 1.1)
            pilot_wave_gain: Scale of the normalized pilot wave contribution so
                the quantum channel is comparable in magnitude to the classical
                field (default: 3000.0)
            pilot_wave_dissipation: Per-step amplitude retention of the pilot
                wave (default: 0.9999). Low dissipation lets the diffusive
                profile propagate non-locally through obstacles.
            classical_epsilon: Epsilon-greedy probability for classical
                (zero-coupling or low-coherence) decision steps (default 0.0
                = deterministic argmax). Used for stochastic classical
                control baselines.
            torus: See above (default True).
        """
        super().__init__(size)
        self.pilot_wave = np.zeros((size, size), dtype=np.float32)
        self.coherence = np.ones((size, size), dtype=np.float32)
        self.quantum_coupling = quantum_coupling
        self.classical_epsilon = classical_epsilon
        self.diffusion_rate = diffusion_rate
        self.pilot_wave_gain = pilot_wave_gain
        self.pilot_wave_dissipation = pilot_wave_dissipation
        self.collapse_coherence_decay = collapse_coherence_decay
        self.collapse_wave_amplify = collapse_wave_amplify
        self.torus = torus

    def update_pilot_wave(self, dt: float = None) -> None:
        """
        Update the pilot wave field using Laplacian diffusion with dissipation.

        The pilot wave spreads influence non-locally via diffusion, creating
        correlations between distant regions. Dissipation prevents unbounded
        growth and keeps the field numerically stable.

        Args:
            dt: Time step (default: diffusion_rate)
        """
        if dt is None:
            dt = self.diffusion_rate

        # Laplacian diffusion - spreads influence to neighbors
        laplacian = (
            np.roll(self.pilot_wave, 1, axis=0) +
            np.roll(self.pilot_wave, -1, axis=0) +
            np.roll(self.pilot_wave, 1, axis=1) +
            np.roll(self.pilot_wave, -1, axis=1) -
            4 * self.pilot_wave
        )
        self.pilot_wave += dt * laplacian

        # Dissipation - prevents unbounded growth
        self.pilot_wave *= self.pilot_wave_dissipation

        # Couple to energy sources - pilot wave "guides" toward energy
        for ex, ey, strength in self.energy_sources:
            self.pilot_wave[ex, ey] += strength * dt * 0.01

        # Clamp to prevent numerical overflow
        self.pilot_wave = np.clip(self.pilot_wave, -100.0, 100.0)

    def collapse_field(self, x: int, y: int, radius: int = 3) -> None:
        """
        Collapse the field around a point (Penrose-inspired).

        Agent observation triggers localized decoherence: reduces coherence
        and sharpens the pilot wave in the vicinity. This models measurement-like
        interaction where observation affects the system.

        Args:
            x: X coordinate of the observation point
            y: Y coordinate of the observation point
            radius: Radius of influence for collapse (default: 3)
        """
        # Create offset grid
        dx = np.arange(-radius, radius + 1, dtype=np.int32)
        dy = np.arange(-radius, radius + 1, dtype=np.int32)
        ddx, ddy = np.meshgrid(dx, dy, indexing='ij')
        dist = np.sqrt(ddx.astype(np.float32)**2 + ddy.astype(np.float32)**2)
        mask = dist < radius

        # Apply collapse in circular region
        for i, di in enumerate(dx):
            for j, dj in enumerate(dy):
                if mask[i, j]:
                    ni = (x + di) % self.size
                    nj = (y + dj) % self.size
                    self.coherence[ni, nj] *= self.collapse_coherence_decay
                    self.pilot_wave[ni, nj] *= self.collapse_wave_amplify

    def get_guidance_field(self) -> np.ndarray:
        """
        Get the combined classical and quantum guidance field.

        The pilot wave contribution is normalized by its current max amplitude
        and scaled by ``pilot_wave_gain`` so the quantum channel stays
        comparable in magnitude to the classical field regardless of how far
        the wave has dissipated.

        Returns:
            Combined field = classical_potential
                + quantum_coupling * pilot_wave_gain * normalize(pilot_wave)
        """
        pmax = float(self.pilot_wave.max())
        if pmax > 1e-8:
            normalized = self.pilot_wave / pmax
        else:
            normalized = self.pilot_wave
        return self.grid + self.quantum_coupling * self.pilot_wave_gain * normalized

    def get_coherence_at(self, x: int, y: int) -> float:
        """
        Get coherence value at a position.

        Args:
            x: X coordinate
            y: Y coordinate

        Returns:
            Coherence value (0.0 to 1.0+)
        """
        if not (0 <= x < self.size and 0 <= y < self.size):
            return 0.0
        return float(self.coherence[x, y])

    def get_state(self) -> dict:
        """
        Get extended state including quantum fields.

        Returns:
            Dictionary with classical + quantum state information
        """
        state = super().get_state()
        state.update({
            'pilot_wave_range': (self.pilot_wave.min(), self.pilot_wave.max()),
            'pilot_wave_mean': self.pilot_wave.mean(),
            'coherence_range': (self.coherence.min(), self.coherence.max()),
            'coherence_mean': self.coherence.mean(),
            'quantum_coupling': self.quantum_coupling,
        })
        return state
