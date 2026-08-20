"""
Module: examples/run_ablation_study.py

Run ablation studies to compare quantum-inspired vs classical agent navigation.

Usage:
    python examples/run_ablation_study.py                  # Run all scenarios
    python examples/run_ablation_study.py --scenario maze  # Maze only
    python examples/run_ablation_study.py --runs 20        # 20 runs per config
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import argparse
from src.core.experiments import (
    run_ablation_study,
    print_summary,
    export_to_csv,
)


def main():
    parser = argparse.ArgumentParser(
        description="QIWM Ablation Study Runner"
    )
    parser.add_argument(
        '--scenario',
        choices=['default', 'maze', 'moving', 'single_source', 'tunnel', 'all'],
        default='all',
        help='Scenario to run (default: all)'
    )
    parser.add_argument(
        '--runs',
        type=int,
        default=5,
        help='Runs per configuration (default: 5)'
    )
    parser.add_argument(
        '--output',
        type=str,
        default='ablation_results.csv',
        help='Output CSV filename (default: ablation_results.csv)'
    )
    parser.add_argument(
        '--no-collapse',
        action='store_true',
        help='Skip experiments with collapse enabled'
    )
    parser.add_argument(
        '--no-nocollapse',
        action='store_true',
        help='Skip experiments with collapse disabled'
    )

    args = parser.parse_args()

    scenarios = (['default', 'maze', 'moving', 'single_source', 'tunnel']
                if args.scenario == 'all' else [args.scenario])

    all_results = {}

    for scenario in scenarios:
        print(f"\nRunning ablation study for scenario: {scenario}")
        print(f"  Runs per config: {args.runs}")
        print(f"  Couplings: [0.0, 0.1, 0.3, 0.5]")
        print(f"  Collapse: {'ON' if not args.no_collapse else 'OFF'} + {'OFF' if not args.no_nocollapse else 'ON'}")

        results = run_ablation_study(
            scenario=scenario,
            runs_per_config=args.runs,
            with_collapse=not args.no_collapse,
            without_collapse=not args.no_nocollapse,
        )
        all_results.update(results)

    # Print summary
    print_summary(all_results)

    # Export to CSV
    export_to_csv(all_results, args.output)
    print(f"\nResults exported to: {args.output}")


if __name__ == "__main__":
    main()
