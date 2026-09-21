"""
Module: examples/maze_route_audit.py

Maze route audit (Priority 6 item): does the maze advantage reduce to
global route discovery?

For agents that first reach the goal energy source (110,110), classify
the route: torus-edge wrap (global route around contractible walls,
same mechanism as the tunnel seam shortcut) vs hand-crafted gap
(dead-end exit / vertical wall gap).

Configs: deterministic classical (q=0, eps=0), stochastic classical
(q=0, eps=0.1), quantum (q=0.3). 10 seeds each.

Usage:
    python examples/maze_route_audit.py
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
    ('quantum_q0.3', 0.3, 0.0),
]


def main():
    n = 10
    fieldnames = ['config', 'quantum_coupling', 'classical_epsilon', 'seed',
                  'alive_rate', 'maze_goal_reached',
                  'maze_route_gap_frac', 'maze_route_edge_frac']
    rows = []
    for name, q, eps in CONFIGS:
        for seed in range(n):
            config = ExperimentConfig(scenario='maze', quantum_coupling=q,
                                     collapse_enabled=True, seed=seed,
                                     max_steps=500, classical_epsilon=eps,
                                     goal=(110, 110))
            d = run_single_experiment(config).to_dict()
            rows.append((name, q, eps, seed, d['alive_rate'],
                         d['maze_goal_reached'], d['maze_route_gap_frac'],
                         d['maze_route_edge_frac']))
            print(f"{name:<15} seed={seed:<3} alive={d['alive_rate']:.2f} "
                  f"reached={d['maze_goal_reached']} "
                  f"gap={d['maze_route_gap_frac']:.2f} "
                  f"edge={d['maze_route_edge_frac']:.2f}", flush=True)

    print()
    for name, _q, _e in CONFIGS:
        rs = [r for r in rows if r[0] == name]
        reached = [r[5] for r in rs]
        gap = [r[6] for r in rs if not np.isnan(r[6])]
        edge = [r[7] for r in rs if not np.isnan(r[7])]
        gap_m = float(np.mean(gap)) if gap else float('nan')
        edge_m = float(np.mean(edge)) if edge else float('nan')
        print(f"{name:<15} reached/run={np.mean(reached):.1f} "
              f"gap_frac={gap_m:.2f} edge_frac={edge_m:.2f}")

    out = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                       'maze_route_audit.csv')
    with open(out, 'w', newline='') as f:
        w = csv.writer(f)
        w.writerow(fieldnames)
        w.writerows(rows)
    print(f"saved {out}")


if __name__ == '__main__':
    main()
