"""
Module: examples/path_efficiency.py

Path-efficiency ratio audit (Priority 6 item, threshold: 15%).

Per agent that first arrives at an energy source:
    efficiency = geodesic(torus) distance(spawn -> source at arrival)
                 / steps taken to arrive
1.0 = perfect direct route; lower = detour.

Threshold: quantum mean efficiency >= 1.15 x classical mean efficiency
(same scenario, seeds, max_steps).

Usage:
    python examples/path_efficiency.py [--scenario default]
"""

import argparse
import csv
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
from src.core.experiments import ExperimentConfig, run_single_experiment


def main():
    parser = argparse.ArgumentParser(description="Path-efficiency audit")
    parser.add_argument('--scenario', default='default')
    parser.add_argument('--runs', type=int, default=10)
    args = parser.parse_args()

    n = args.runs
    rows = []
    for q, label in [(0.0, 'classical'), (0.3, 'quantum_q0.3')]:
        for seed in range(n):
            d = run_single_experiment(
                ExperimentConfig(scenario=args.scenario, quantum_coupling=q,
                                 collapse_enabled=True, seed=seed,
                                 max_steps=500)).to_dict()
            rows.append((label, q, seed, d['path_eff_reached'],
                         d['path_eff_mean'], d['alive_rate']))
            eff = d['path_eff_mean']
            print(f"{label:<15} seed={seed:<3} reached={d['path_eff_reached']} "
                  f"eff={eff:.3f} alive={d['alive_rate']:.2f}"
                  if np.isfinite(eff) else
                  f"{label:<15} seed={seed:<3} reached=0 eff=nan",
                  flush=True)

    print()
    res = {}
    for label in ('classical', 'quantum_q0.3'):
        effs = [r[4] for r in rows if r[0] == label and np.isfinite(r[4])]
        res[label] = effs
        m = float(np.mean(effs)) if effs else float('nan')
        print(f"{label:<15} mean efficiency = {m:.4f} "
              f"(+/-{np.std(effs):.4f}, n_reached_runs={len(effs)})")
    c, qm = res['classical'], res['quantum_q0.3']
    if c and qm:
        ratio = np.mean(qm) / max(np.mean(c), 1e-9)
        met = np.mean(qm) >= 1.15 * np.mean(c)
        print(f"\nquantum/classical ratio = {ratio:.3f}  "
              f"(threshold 1.15 -> {'MET' if met else 'NOT MET'})")
    else:
        print("\nnot enough reached agents to compare")

    out = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                       f'path_efficiency_{args.scenario}.csv')
    with open(out, 'w', newline='') as f:
        w = csv.writer(f)
        w.writerow(['config', 'quantum_coupling', 'seed', 'path_eff_reached',
                    'path_eff_mean', 'alive_rate'])
        w.writerows(rows)
    print(f"saved {out}")


if __name__ == '__main__':
    main()
