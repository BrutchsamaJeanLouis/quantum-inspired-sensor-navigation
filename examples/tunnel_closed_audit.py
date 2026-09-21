"""
Module: examples/tunnel_closed_audit.py

Closed-boundary tunnel audit (Priority 7 item): is the seam-wrap result a
torus artifact?

Same tunnel scenario (gapless wall at x=64, source at (96,96)) but with
clamped edges instead of torus wrap: the edge seam no longer exists, so
the ONLY route to the far side is a genuine wall jump (63->65). If
quantum still crosses here and classical does not, the tunneling claim
is not a torus artifact.

Configs: classical (q=0, eps=0), stochastic classical (q=0, eps=0.1),
quantum (q=0.5). 10 seeds each, 500 steps.

Usage:
    python examples/tunnel_closed_audit.py
"""

import csv
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
from src.core.experiments import ExperimentConfig, run_single_experiment

CONFIGS = [
    ('classical', 0.0, 0.0),
    ('eps0.1', 0.0, 0.1),
    ('quantum_q0.5', 0.5, 0.0),
]


def main():
    n = 10
    rows = []
    for name, q, eps in CONFIGS:
        for seed in range(n):
            config = ExperimentConfig(scenario='tunnel', quantum_coupling=q,
                                     collapse_enabled=True, seed=seed,
                                     max_steps=500, classical_epsilon=eps,
                                     barrier_x=64, boundary='closed')
            d = run_single_experiment(config).to_dict()
            rows.append((name, q, eps, seed, d['alive_rate'],
                         d['barrier_crossings'], d['wall_crossings'],
                         d['wall_step_crossings'], d['seam_crossings'],
                         d['first_crossing_latency_median']))
            print(f"{name:<15} seed={seed:<3} alive={d['alive_rate']:.2f} "
                  f"cross={d['barrier_crossings']} wall={d['wall_crossings']} "
                  f"seam={d['seam_crossings']}", flush=True)

    print()
    for name, _q, _e in CONFIGS:
        rs = [r for r in rows if r[0] == name]
        print(f"{name:<15} alive={np.mean([r[4] for r in rs]):.2f} "
              f"cross/run={np.mean([r[5] for r in rs]):.1f} "
              f"wall={sum(r[6] for r in rs)} "
              f"wall_step={sum(r[7] for r in rs)} "
              f"seam={sum(r[8] for r in rs)}")

    out = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                       'tunnel_closed_audit.csv')
    with open(out, 'w', newline='') as f:
        w = csv.writer(f)
        w.writerow(['config', 'quantum_coupling', 'classical_epsilon', 'seed',
                    'alive_rate', 'barrier_crossings', 'wall_crossings',
                    'wall_step_crossings', 'seam_crossings',
                    'first_crossing_latency_median'])
        w.writerows(rows)
    print(f"saved {out}")


if __name__ == '__main__':
    main()
