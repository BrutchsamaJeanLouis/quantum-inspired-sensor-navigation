"""Tests for the energy budget analysis (examples/energy_budget.py)."""
import csv
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from examples.energy_budget import analytic_table, empirical_balance  # noqa: E402

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def test_analytic_break_even():
    rows = analytic_table()
    be = [r for r in rows if r['break_even']]
    # S=50, 1 harvest/50 steps: 50 - 50 = 0
    assert len(be) == 1
    assert be[0]['source_strength'] == 50.0 and be[0]['harvests_per_50_steps'] == 1
    # S=100: 0 harvests -> -50, 1 -> +50, 2 -> +150
    r = {(r['source_strength'], r['harvests_per_50_steps']):
         r['net_energy_per_50_steps'] for r in rows}
    assert r[(100.0, 0)] == -50.0
    assert r[(100.0, 1)] == 50.0
    assert r[(100.0, 2)] == 150.0


def test_empirical_balance_shape_and_known_values():
    rows = empirical_balance(os.path.join(REPO, 'ablation_results_v2.csv'))
    assert len(rows) == 20  # 5 scenarios x 4 couplings
    d0 = [r for r in rows if r['scenario'] == 'default'
          and r['quantum_coupling'] == '0.0'][0]
    assert abs(d0['alive_rate_mean'] - 0.45) < 1e-6
    assert abs(d0['avg_final_energy'] - 270.0) < 1e-6
    assert abs(d0['energy_balance_vs_initial'] - 170.0) < 1e-6
    t0 = [r for r in rows if r['scenario'] == 'tunnel'
          and r['quantum_coupling'] == '0.0'][0]
    assert t0['alive_rate_mean'] == 0.0
    assert t0['avg_final_energy'] == 0.0


def test_energy_budget_csv_written():
    out = os.path.join(REPO, 'energy_budget.csv')
    assert os.path.exists(out)
    with open(out) as f:
        lines = [l for l in f if l.strip()]
    assert len(lines) >= 9 + 20  # analytic + blank + empirical header+rows
