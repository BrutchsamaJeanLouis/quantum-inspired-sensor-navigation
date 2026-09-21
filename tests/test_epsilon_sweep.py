"""
Tunnel ε-sweep harness tests (examples/epsilon_sweep_tunnel.py).

The full 10-seed curve lives in epsilon_sweep_tunnel.csv (see RESULTS.md
§4h). These tests check the harness end-to-end (one row per run, correct
scenario) and the structural arm behaviors that the curve is built on:
deterministic classical never crosses, the quantum arm crosses entirely
via seam wraps, and ε-noise crossings are dominated by wall walk-throughs.
"""

import csv
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from examples.epsilon_sweep_tunnel import ARMS, run_sweep
from src.core.experiments import ExperimentConfig, run_single_experiment


class TestEpsilonSweepTunnel:
    def test_sweep_writes_one_row_per_run(self, tmp_path):
        out = tmp_path / 'sweep.csv'
        per_arm = run_sweep(seeds=1, out_csv=str(out))
        assert set(per_arm) == {a[0] for a in ARMS}
        assert all(len(rows) == 1 for rows in per_arm.values())
        rows = list(csv.DictReader(open(str(out))))
        assert len(rows) == len(ARMS)
        assert all(r['scenario'] == 'tunnel' for r in rows)

    def test_classical_never_crosses_quantum_all_seam(self):
        d_c = run_single_experiment(ExperimentConfig(
            scenario='tunnel', quantum_coupling=0.0,
            seed=42, barrier_x=64)).to_dict()
        assert d_c['barrier_crossings'] == 0

        d_q = run_single_experiment(ExperimentConfig(
            scenario='tunnel', quantum_coupling=0.3,
            seed=42, barrier_x=64)).to_dict()
        assert d_q['barrier_crossings'] == 20
        assert d_q['seam_crossings'] == d_q['barrier_crossings']
        assert d_q['wall_crossings'] + d_q['wall_step_crossings'] == 0

    def test_epsilon_crossings_dominated_by_wall_walkthroughs(self):
        d = run_single_experiment(ExperimentConfig(
            scenario='tunnel', quantum_coupling=0.0,
            classical_epsilon=0.3, seed=42, barrier_x=64)).to_dict()
        assert d['barrier_crossings'] > 0
        assert (d['wall_crossings'] + d['wall_step_crossings']
                > d['seam_crossings'])
