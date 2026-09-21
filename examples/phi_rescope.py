"""
Module: examples/phi_rescope.py

Re-scoped Phi audit (P7): does the agent-in-the-loop, agent-localised Phi
meet the readme threshold ``quantum_phi > 1.5 x classical_phi``?

This is the principled re-scope of the §4e null. The original ``compute_phi``
ran an agent-less forward sim on a fixed central region the agents never
occupy, so it measured FIELD self-organization (ratio 1.000). The re-scoped
metric ``compute_phi_agents`` measures AGENT-WORLD COUPLING: the guidance
field in the neighbourhood where agents actually are, with the swarm stepping
(sense/decide/move/collapse) during the forward sim.

The metric is defined BEFORE looking at the number (local_radius=4, steps=5,
sample every 100 steps, default scenario, collapse ON, n=10 seeds). We report
the ratio and the DIRECTION honestly: MET (re-scoped), or NOT MET / formally
retracted as a clean agent-world-coupling diagnostic.

Usage:
    python examples/phi_rescope.py
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
                                 max_steps=500, phi_agent_in_loop=True)).to_dict()
            rows.append((label, q, seed,
                         d['phi_agent_mean'], d['phi_agent_final'],
                         d['phi_mean'], d['alive_rate']))
            print(f"{label:<15} seed={seed:<3} "
                  f"phi_agent_mean={d['phi_agent_mean']:.4f} "
                  f"phi_agent_final={d['phi_agent_final']:.4f} "
                  f"phi(old)={d['phi_mean']:.4f} alive={d['alive_rate']:.2f}",
                  flush=True)

    print()
    res = {'classical': [], 'quantum_q0.3': []}
    for r in rows:
        res[r[0]].append(r[3])
    for label in ['classical', 'quantum_q0.3']:
        vals = res[label]
        print(f"{label:<15} phi_agent_mean={np.mean(vals):.4f} "
              f"(+/-{np.std(vals):.4f})  min={np.min(vals):.4f} "
              f"max={np.max(vals):.4f}")
    qm = np.mean(res['quantum_q0.3'])
    cm = np.mean(res['classical'])
    ratio = qm / max(cm, 1e-9)
    met = qm > 1.5 * cm
    print(f"\nre-scoped agent-world-coupling Phi  "
          f"quantum/classical ratio = {ratio:.3f}  "
          f"(readme threshold 1.5 -> {'MET (re-scoped)' if met else 'NOT MET'})")
    print(f"direction: quantum is "
          f"{'HIGHER' if qm > cm else 'LOWER'} than classical "
          f"({qm:.4f} vs {cm:.4f})")

    out = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                       'phi_rescope.csv')
    with open(out, 'w', newline='') as f:
        w = csv.writer(f)
        w.writerow(['config', 'quantum_coupling', 'seed', 'phi_agent_mean',
                    'phi_agent_final', 'phi_field_old', 'alive_rate'])
        w.writerows(rows)
    print(f"saved {out}")


if __name__ == '__main__':
    main()
