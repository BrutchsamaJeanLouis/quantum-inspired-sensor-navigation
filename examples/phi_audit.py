"""
Module: examples/phi_audit.py

Phi harness audit (Priority 6 item): is the readme threshold met?

    threshold: quantum_phi > 1.5 x classical_phi

Measures the central-region IIT phi (PHI_REGION in experiments.py)
sampled every 100 steps over 500-step runs, default scenario,
collapse ON, n=10 seeds.

Usage:
    python examples/phi_audit.py
"""

import csv
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
from src.core.experiments import ExperimentConfig, run_single_experiment


def main():
    n = 10
    rows = []
    for q, label in [(0.0, 'classical'), (0.3, 'quantum_q0.3')]:
        for seed in range(n):
            d = run_single_experiment(
                ExperimentConfig(scenario='default', quantum_coupling=q,
                                 collapse_enabled=True, seed=seed,
                                 max_steps=500)).to_dict()
            rows.append((label, q, seed, d['phi_mean'], d['phi_final'],
                         d['alive_rate']))
            print(f"{label:<15} seed={seed:<3} phi_mean={d['phi_mean']:.4f} "
                  f"phi_final={d['phi_final']:.4f} alive={d['alive_rate']:.2f}",
                  flush=True)

    print()
    res = {}
    for label, _q in [('classical', 0.0), ('quantum_q0.3', 0.3)]:
        phis = [r[3] for r in rows if r[0] == label]
        res[label] = phis
        print(f"{label:<15} phi_mean={np.mean(phis):.4f} "
              f"(+/-{np.std(phis):.4f})")
    ratio = np.mean(res['quantum_q0.3']) / max(np.mean(res['classical']), 1e-9)
    met = np.mean(res['quantum_q0.3']) > 1.5 * np.mean(res['classical'])
    print(f"\nquantum/classical ratio = {ratio:.3f}  "
          f"(threshold 1.5 -> {'MET' if met else 'NOT MET'})")

    out = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                       'phi_audit.csv')
    with open(out, 'w', newline='') as f:
        w = csv.writer(f)
        w.writerow(['config', 'quantum_coupling', 'seed', 'phi_mean',
                    'phi_final', 'alive_rate'])
        w.writerows(rows)
    print(f"saved {out}")


if __name__ == '__main__':
    main()
