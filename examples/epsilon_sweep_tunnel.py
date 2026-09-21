"""
Tunnel ε-sweep curve — end-to-end noise-vs-quantum tradeoff.

Question (§4b had only 2 noise points): at what decision-noise level does
the stochastic classical channel (ε-greedy) match the quantum channel
(pilot wave + Boltzmann) on the gapless-wall tunnel scenario?

Arms (tunnel, torus, collapse ON, 20 agents, 500 steps — v2 instrument):
  classical  : q=0.0, ε=0.00  (deterministic gradient descent — anchor)
  eps0.05/0.1/0.2/0.3 : q=0.0, ε sweep
  quantum     : q=0.3, ε=0.00  (pilot-wave channel, no decision noise)
  quantum_eps : q=0.3, ε=0.10  (interaction: ε on the classical fallback
                                  path used whenever the coherence gate is
                                  closed — does noise help the quantum arm?)

Seeds: 10 per arm, seed = 1000*i + arm_offset (offset 400 for quantum
arms so ε arms and quantum arms do not share draws).

Output: epsilon_sweep_tunnel.csv (one row per run, full metric set) +
a per-arm summary table printed to stdout.
"""

import argparse
import csv
import os
import sys
import time

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.core.experiments import ExperimentConfig, run_single_experiment

ARMS = [
    # (name, quantum_coupling, classical_epsilon)
    ('classical',        0.0, 0.00),
    ('eps0.05',          0.0, 0.05),
    ('eps0.1',           0.0, 0.10),
    ('eps0.2',           0.0, 0.20),
    ('eps0.3',           0.0, 0.30),
    ('quantum',          0.3, 0.00),
    ('quantum_eps0.1',   0.3, 0.10),
]

SEEDS = 10
OUT_CSV = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    'epsilon_sweep_tunnel.csv')


def seed_for(i: int, q: float, eps: float) -> int:
    offset = 400 if q > 0 else 0
    return 1000 * i + offset + int(round(eps * 1000))


def run_sweep(seeds: int = SEEDS, arms: list = None, out_csv: str = OUT_CSV):
    if arms is None:
        arms = ARMS
    all_rows = []
    per_arm = {}
    t0 = time.time()
    for name, q, eps in arms:
        rows = []
        for i in range(seeds):
            cfg = ExperimentConfig(
                scenario='tunnel',
                quantum_coupling=q,
                classical_epsilon=eps,
                seed=seed_for(i, q, eps),
                barrier_x=64,
                max_steps=500,
            )
            m = run_single_experiment(cfg)
            d = m.to_dict()
            d['config'] = name
            rows.append(d)
            print(f'  {name} seed {i}: alive={d["alive_rate"]:.0%} '
                  f'cross={d["barrier_crossings"]} '
                  f'lat={d["first_crossing_latency_mean"]:.1f}', flush=True)
        per_arm[name] = rows
        all_rows.extend(rows)
    elapsed = time.time() - t0

    if out_csv:
        fieldnames = list(all_rows[0].keys())
        with open(out_csv, 'w', newline='') as f:
            w = csv.DictWriter(f, fieldnames=fieldnames)
            w.writeheader()
            w.writerows(all_rows)
        print(f'\nwrote {len(all_rows)} rows -> {out_csv} '
              f'({elapsed:.1f}s total)')

    # Per-arm summary
    print(f'\n{"arm":<16} {"alive%":>7} {"cross/run":>9} {"lat med":>8} '
          f'{"wall":>5} {"wallstep":>8} {"seam":>5}')
    for name, rows in per_arm.items():
        n = len(rows)
        alive = 100.0 * np.mean([r['alive_rate'] for r in rows])
        cross = np.mean([r['barrier_crossings'] for r in rows])
        lats = [r['first_crossing_latency_mean'] for r in rows
                if not np.isnan(r['first_crossing_latency_mean'])]
        lat_med = float(np.median(lats)) if lats else float('nan')
        wall = sum(r['wall_crossings'] for r in rows) / n
        wstep = sum(r['wall_step_crossings'] for r in rows) / n
        seam = sum(r['seam_crossings'] for r in rows) / n
        print(f'{name:<16} {alive:>6.0f}% {cross:>9.1f} {lat_med:>8.1f} '
              f'{wall:>5.1f} {wstep:>8.1f} {seam:>5.1f}')
    return per_arm


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description='Tunnel ε-sweep curve')
    ap.add_argument('seeds', type=int, nargs='?', default=SEEDS)
    ap.add_argument('--out', type=str, default=OUT_CSV)
    args = ap.parse_args()
    run_sweep(seeds=args.seeds, out_csv=args.out)
