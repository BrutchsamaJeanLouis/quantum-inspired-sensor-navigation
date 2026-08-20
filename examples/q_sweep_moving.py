"""
Module: examples/q_sweep_moving.py

Finer coupling sweep in the moving scenario (Priority 6 item 1).

Resolves the coupling-liability curve seen in the v2 ablation
(alive rate 97%@q=0.1 -> 39%@q=0.5): does the advantage degrade
monotonically with q, or is there an interior optimum?

Usage:
    python examples/q_sweep_moving.py            # 8 q-levels x 10 seeds
    python examples/q_sweep_moving.py --runs 20  # finer resolution
"""

import argparse
import csv
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.core.experiments import ExperimentConfig, run_single_experiment


def main():
    parser = argparse.ArgumentParser(description="QIWM moving q-sweep")
    parser.add_argument('--runs', type=int, default=10)
    parser.add_argument('--output', default='q_sweep_moving.csv')
    args = parser.parse_args()

    q_levels = [0.0, 0.05, 0.1, 0.15, 0.2, 0.3, 0.4, 0.5]

    fieldnames = [
        'scenario', 'quantum_coupling', 'diffusion_rate', 'collapse_enabled',
        'population', 'max_steps', 'seed', 'alive_count', 'alive_rate',
        'avg_survival_steps', 'max_survival_steps', 'avg_final_energy',
        'avg_steps_taken', 'deadend_escapes', 'barrier_crossings',
        'final_coherence_mean', 'final_pilot_wave_mean',
    ]

    rows = []
    for q in q_levels:
        for seed in range(args.runs):
            config = ExperimentConfig(
                scenario='moving',
                quantum_coupling=q,
                collapse_enabled=True,
                seed=seed,
            )
            result = run_single_experiment(config)
            d = result.to_dict()
            d['quantum_coupling'] = q
            rows.append(d)
            print(f"q={q:<5} seed={seed:<3} alive_rate={d['alive_rate']:.2f}",
                  flush=True)

    with open(args.output, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction='ignore')
        writer.writeheader()
        writer.writerows(rows)
    print(f"\nSweep complete: {len(rows)} runs -> {args.output}")


if __name__ == '__main__':
    main()
