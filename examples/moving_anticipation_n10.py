"""
Module: examples/moving_anticipation_n10.py

Anticipatory positioning metric at n=10 (moving scenario, Priority 2).

Measures whether agents sit closer to the energy sources' FUTURE position
(t + LEAD_HORIZON_STEPS) than to their CURRENT position.

Usage:
    python examples/moving_anticipation_n10.py
"""

import csv
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
from src.core.experiments import ExperimentConfig, run_single_experiment


def main():
    q_levels = [0.0, 0.1, 0.3]
    n = 10
    rows = []
    for q in q_levels:
        for seed in range(n):
            d = run_single_experiment(
                ExperimentConfig(scenario='moving', quantum_coupling=q,
                                 seed=seed, max_steps=500)).to_dict()
            rows.append((q, seed, d['anticipatory_index_mean'],
                         d['anticipatory_frac_mean'], d['alive_rate']))
            print(f"q={q:<5} seed={seed:<3} idx={d['anticipatory_index_mean']:+.2f} "
                  f"frac={d['anticipatory_frac_mean']:.3f} alive={d['alive_rate']:.2f}",
                  flush=True)

    for q in q_levels:
        idx = [r[2] for r in rows if r[0] == q]
        fr = [r[3] for r in rows if r[0] == q]
        print(f"q={q}: idx={np.mean(idx):+.2f} (+/-{np.std(idx):.2f})  "
              f"frac={np.mean(fr):.3f} (+/-{np.std(fr):.3f})")

    out = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                       'moving_anticipation_n10.csv')
    with open(out, 'w', newline='') as f:
        w = csv.writer(f)
        w.writerow(['q', 'seed', 'anticipatory_index_mean',
                    'anticipatory_frac_mean', 'alive_rate'])
        w.writerows(rows)
    print(f"saved {out}")


if __name__ == '__main__':
    main()
