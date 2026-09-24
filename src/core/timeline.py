"""
Timeline Player - deterministic tick engine for the QIWM demo.

Gives the visualizer (and any LLM driving the demo) a scrubbable timeline:
    - step(n): advance n ticks (pilot wave + swarm), no rendering
    - seek(n): jump to tick n
        * n >= tick  -> fast-forward: just step forward
        * n <  tick -> rewind: re-seed, rebuild world+swarm, re-run n ticks
          (deterministic replay: same seed => identical state at any tick)
    - pause()/resume(): control whether the live loop steps

Determinism contract
--------------------
The simulation is deterministic given (world factory, seed): agents sample
actions with the global numpy RNG, and pilot-wave update is pure. So
``seek(n)`` reproduces exactly the state the live run would have shown at
tick n. This is what makes scrubbing / rewinding meaningful.

Example
-------
    from src.core.timeline import TimelinePlayer
    from src.core.world_factory import make_maze
    from main import build_world_and_swarm   # (world, swarm) at t=0

    player = TimelinePlayer(seed=42, factory=make_maze)
    player.rebuild()
    player.seek(150)   # render world/swarm now, tick label = 150
"""

from typing import Callable, Optional, Tuple

import numpy as np

from src.core.agents import AgentSwarm
from src.core.toy_world import ToyWorld
from src.core.quantum_world import QuantumInspiredWorld


class TimelinePlayer:
    """Deterministic, scrubbable tick engine around (world, swarm) pairs."""

    def __init__(
        self,
        factory: Callable[[], Tuple[ToyWorld, AgentSwarm]],
        seed: int = 42,
        dt: float = 0.1,
    ):
        """
        Args:
            factory: Zero-arg callable returning a fresh (world, swarm) at t=0.
                     Called once in __init__ and again on every rewind.
            seed: numpy global RNG seed used before every build (t=0 and
                  rewind). Forward steps consume the RNG from the live state,
                  so a rewind to tick n re-seeds and re-steps n times.
            dt: Pilot-wave time step (matches the live 30 FPS loop's 0.1).
        """
        self.factory = factory
        self.seed = seed
        self.dt = dt
        self.world: Optional[ToyWorld] = None
        self.swarm: Optional[AgentSwarm] = None
        self.tick: int = 0
        self._build()

    def _build(self) -> None:
        """(Re)seed and build a fresh t=0 world+swarm."""
        np.random.seed(self.seed)
        self.world, self.swarm = self.factory()
        self.tick = 0

    def rebuild(self) -> None:
        """Back to tick 0 (fresh seed)."""
        self._build()

    def step(self, n: int = 1) -> int:
        """Advance n ticks (n may be 0). Returns the new tick number."""
        if n < 0:
            raise ValueError(f"step(n) requires n >= 0, got {n}")
        for _ in range(n):
            self.world.update_pilot_wave(dt=self.dt)
            self.swarm.step_all()
        self.tick += n
        return self.tick

    def seek(self, tick: int) -> int:
        """Jump to `tick`: fast-forward if ahead, deterministic replay if behind.

        Returns the resulting tick number (clamped to >= 0).
        """
        if tick < 0:
            tick = 0
        if tick == self.tick:
            return self.tick
        if tick > self.tick:
            self.step(tick - self.tick)
        else:
            self._build()
            self.step(tick)
        return self.tick

    @property
    def size(self) -> int:
        return int(self.world.size)

    def guidance_field(self) -> np.ndarray:
        """Current guidance field (for rendering / headless snapshots)."""
        return self.world.get_guidance_field()

    def stats(self) -> dict:
        """Compact state summary for LLM consumers / logs."""
        s = self.swarm.get_stats()
        return {
            "tick": self.tick,
            "seed": self.seed,
            "alive": s.get("alive", 0),
            "population": s.get("total", 0),
            "avg_steps": s.get("avg_steps", 0.0),
        }
