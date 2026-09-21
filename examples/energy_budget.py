"""
Energy budget analysis (paper methods input).

Part 1: analytic cost structure.
    Movement cost: 1.0 energy/step (agents.py, movement_cost default).
    Harvest: +strength when within radius 3 of a source, 50-step cooldown.
    => per 50-step window at strength S: net = h*S - 50, h = harvests/window.
    Break-even residency for S=100: one harvest per 50-step window.

Part 2: empirical energy balance from the v2 ablation CSV, grouped by
scenario x coupling (collapse ON): final energy vs initial 100,
survival steps, alive rate.

Usage:
    python examples/energy_budget.py [--input ablation_results_v2.csv]
"""
import argparse
import csv
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

MOVEMENT_COST = 1.0
INITIAL_ENERGY = 100.0
HARVEST_RADIUS = 3.0
HARVEST_COOLDOWN = 50


def analytic_table(strengths=(50.0, 100.0, 200.0)):
    """Net energy per 50-step window for harvest rates 0..2."""
    rows = []
    for s in strengths:
        for h in (0, 1, 2):
            net = h * s - HARVEST_COOLDOWN * MOVEMENT_COST
            rows.append({
                'source_strength': s,
                'harvests_per_50_steps': h,
                'net_energy_per_50_steps': net,
                'net_per_step': net / HARVEST_COOLDOWN,
                'break_even': abs(net) < 1e-9,
            })
    return rows


def empirical_balance(csv_path):
    """Per scenario x coupling (collapse ON) energy balance from v2 CSV."""
    out = []
    with open(csv_path) as f:
        rows = list(csv.DictReader(f))
    for scen in ('default', 'maze', 'moving', 'single_source', 'tunnel'):
        for q in ('0.0', '0.1', '0.3', '0.5'):
            sub = [r for r in rows if r['scenario'] == scen
                   and r['quantum_coupling'] == q
                   and r['collapse_enabled'] == 'True']
            if not sub:
                continue
            fin = [float(r['avg_final_energy']) for r in sub]
            surv = [float(r['avg_survival_steps']) for r in sub]
            alive = [float(r['alive_rate']) for r in sub]
            n = len(fin)
            out.append({
                'scenario': scen,
                'quantum_coupling': q,
                'runs': n,
                'alive_rate_mean': sum(alive) / n,
                'avg_survival_steps': sum(surv) / n,
                'avg_final_energy': sum(fin) / n,
                'energy_balance_vs_initial': sum(fin) / n - INITIAL_ENERGY,
            })
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--input', default='ablation_results_v2.csv')
    ap.add_argument('--output', default='energy_budget.csv')
    args = ap.parse_args()

    print('Part 1: analytic cost structure (movement_cost=%.1f/step, '
          'harvest r<%.0f, cooldown=%d)' % (MOVEMENT_COST, HARVEST_RADIUS,
                                           HARVEST_COOLDOWN))
    ana = analytic_table()
    hdr = ['source_strength', 'harvests_per_50_steps',
           'net_energy_per_50_steps', 'net_per_step', 'break_even']
    print('  ' + '  '.join(f'{h:>24}' for h in hdr))
    for r in ana:
        print('  ' + '  '.join(f'{str(r[h]):>24}' for h in hdr))

    print('\nPart 2: empirical energy balance (v2 CSV, collapse ON)')
    emp = empirical_balance(args.input)
    for r in emp:
        print(f"  {r['scenario']:<14} q={r['quantum_coupling']:<4} "
              f"alive={r['alive_rate_mean']:.3f} "
              f"surv_steps={r['avg_survival_steps']:.1f} "
              f"final_E={r['avg_final_energy']:.1f} "
              f"balance={r['energy_balance_vs_initial']:+.1f}")

    with open(args.output, 'w', newline='') as f:
        w = csv.writer(f)
        w.writerow(['section', 'source_strength', 'harvests_per_50_steps',
                    'net_energy_per_50_steps', 'net_per_step', 'break_even'])
        for r in ana:
            w.writerow(['analytic', r['source_strength'],
                        r['harvests_per_50_steps'],
                        r['net_energy_per_50_steps'],
                        r['net_per_step'], r['break_even']])
        w.writerow([])
        w.writerow(['scenario', 'quantum_coupling', 'runs', 'alive_rate_mean',
                    'avg_survival_steps', 'avg_final_energy',
                    'energy_balance_vs_initial'])
        for r in emp:
            w.writerow([r['scenario'], r['quantum_coupling'], r['runs'],
                        f"{r['alive_rate_mean']:.3f}",
                        f"{r['avg_survival_steps']:.3f}",
                        f"{r['avg_final_energy']:.3f}",
                        f"{r['energy_balance_vs_initial']:.3f}"])
    print(f'\nWrote {args.output}')


if __name__ == '__main__':
    main()
