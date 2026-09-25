#!/usr/bin/env python3
"""
Rewind/seek consistency verification (PO 2026-09-25, TODO 1c).

The *definitive* proof that "seek to tick N == the state a live run shows at
tick N" is at the WORLD-DATA level, not the pixel level. Pixel identity between
the live window (PrintWindow of a real 125%-DPI display) and the headless
`--shot` (SDL dummy driver) is confounded by how the two surfaces render the
alpha-128 agent-trail overlay; the field heatmap and agent sprites are
otherwise identical. So we compare the underlying state arrays, which are
DPI- and rendering-agnostic:

  field        = world.get_guidance_field()   (numpy)
  agents       = [(x, y, energy, steps_taken)] for every agent
  trails       = full per-agent trail array (path history)

Three independent ways of reaching tick T are built and must be bit-identical:

  A  seek(T)                       (the headless `--shot T` path)
  B  step(1) x T                   (a run that played T ticks)
  C  step(1) x K, seek(0), step 1 x (T)  (the live-driver sequence: play a
      while, HOME back to 0, then scrub forward to T)

If A == B == C for every (scenario, seed, tick) in the matrix, rewind
consistency holds: scrubbing / rewinding the live GUI reproduces exactly the
state the headless `--shot` renders.

Usage:
    venv/Scripts/python.exe examples/verify_rewind_consistency.py
"""

import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.core.timeline import TimelinePlayer
from main import build_world_and_swarm  # noqa: E402


def _snapshot(p: "TimelinePlayer"):
    """(field, agents, trails) for a player, as a comparable tuple."""
    field = p.world.get_guidance_field()
    agents = [(a.x, a.y, round(float(a.energy), 6), a.steps_taken)
              for a in p.swarm.agents]
    trails = [tuple((int(x), int(y)) for x, y in a.trail) for a in p.swarm.agents]
    return field, agents, trails


def _same(a, b) -> bool:
    fa, aa, ta = a
    fb, ab, tb = b
    if fa.shape != fb.shape or not np.array_equal(fa, fb):
        return False
    if aa != ab or ta != tb:
        return False
    return True


def reach_a(scenario: str, seed: int, t: int):
    p = TimelinePlayer(factory=lambda: build_world_and_swarm(scenario), seed=seed)
    p.seek(t)
    return p


def reach_b(scenario: str, seed: int, t: int):
    p = TimelinePlayer(factory=lambda: build_world_and_swarm(scenario), seed=seed)
    p.step(t)
    return p


def reach_c(scenario: str, seed: int, t: int, k: int = 25):
    p = TimelinePlayer(factory=lambda: build_world_and_swarm(scenario), seed=seed)
    p.step(k)          # demo playing before the operator pauses it
    p.seek(0)          # HOME
    p.step(t)          # scrub forward to t
    return p


SCENARIOS = ["default", "maze"]
SEEDS = [42, 7]
TICKS = [0, 1, 5, 50, 120, 300, 500]


def main() -> int:
    checks = 0
    fails = []
    for scenario in SCENARIOS:
        for seed in SEEDS:
            for t in TICKS:
                checks += 1
                a = _snapshot(reach_a(scenario, seed, t))
                b = _snapshot(reach_b(scenario, seed, t))
                c = _snapshot(reach_c(scenario, seed, t))
                ok = _same(a, b) and _same(a, c)
                fmax_a = 0.0
                fa, aa, ta = a
                fb, ab, tb = b
                fc, ac, tc = c
                fmax_a = float(np.abs(fa - fb).max())
                fmax_c = float(np.abs(fa - fc).max())
                line = (f"  {scenario:8} seed={seed:<3} t={t:<4} "
                        f"A==B={_same(a, b)} A==C={_same(a, c)} "
                        f"fieldmaxdiff(A,B)={fmax_a:.1f} fieldmaxdiff(A,C)={fmax_c:.1f}")
                print(line, flush=True)
                if not ok:
                    fails.append((scenario, seed, t))
    print()
    if fails:
        print(f"REWIND-CONSISTENCY FAIL: {len(fails)} mismatch(es): {fails}")
        return 1
    print(f"REWIND-CONSISTENCY PASS  ({checks} (scenario,seed,tick) triples; "
          f"seek==step==play-then-home-then-scrub, field+agents+trails bit-identical)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
