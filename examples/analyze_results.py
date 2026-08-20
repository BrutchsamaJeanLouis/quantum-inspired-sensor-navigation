"""
Module: examples/analyze_results.py

Statistical analysis of ablation results.

Loads an ablation results CSV, groups by (scenario, quantum_coupling,
collapse_enabled), computes mean ± std, runs Mann-Whitney U tests of
quantum vs classical (q=0) survival and barrier crossings, and writes
a markdown report.

Usage:
    python examples/analyze_results.py --input ablation_results_v2.csv --output docs/RESULTS.md
"""

import argparse
import csv
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def load_rows(filename):
    with open(filename, newline='') as f:
        return list(csv.DictReader(f))


def group(rows):
    groups = {}
    for r in rows:
        key = (r['scenario'], r['quantum_coupling'], r['collapse_enabled'])
        groups.setdefault(key, []).append(r)
    return groups


def fmt_mean_std(values):
    values = np.asarray(values, dtype=float)
    return f"{values.mean():.3f} ± {values.std():.3f}"


def mann_whitney_u(a, b):
    """Two-sided Mann-Whitney U p-value without scipy (rank-based).

    Falls back to a permutation test if scipy is unavailable.
    """
    a = np.asarray(a, dtype=float)
    b = np.asarray(b, dtype=float)
    if a.size == 0 or b.size == 0:
        return 1.0
    if np.all(a == a[0]) and np.all(b == b[0]) and a[0] == b[0]:
        return 1.0
    try:
        from scipy.stats import mannwhitneyu
        return float(mannwhitneyu(a, b, alternative='two-sided').pvalue)
    except ImportError:
        return _permutation_p(a, b)


def _permutation_p(a, b, nsim=20000, seed=0):
    """Two-sided permutation test on the sum statistic (scipy-free)."""
    a, b = np.asarray(a, dtype=float), np.asarray(b, dtype=float)
    combined = np.concatenate([a, b])
    center = combined.mean() * len(a)
    obs = abs(a.sum() - center)
    rng = np.random.default_rng(seed)
    count = 0
    for _ in range(nsim):
        stat = rng.permutation(combined)[:len(a)].sum()
        if abs(stat - center) >= obs:
            count += 1
    return max(count, 1) / nsim


def main():
    parser = argparse.ArgumentParser(description="Analyze QIWM ablation results")
    parser.add_argument('--input', default='ablation_results_v2.csv')
    parser.add_argument('--output', default='docs/RESULTS.md')
    args = parser.parse_args()

    rows = load_rows(args.input)
    groups = group(rows)

    scenarios = sorted({r['scenario'] for r in rows})
    couplings = sorted({r['quantum_coupling'] for r in rows}, key=float)
    collapses = [c for c in ['True', 'False']
                if any(k[2] == c for k in groups)]

    lines = [
        "# QIWM Ablation Results",
        "",
        "Hypothesis under test (null): *Quantum-inspired dynamics provide NO "
        "advantage over classical agent navigation.*",
        "",
        f"Input: `{args.input}` — {len(rows)} runs "
        f"({len(couplings)} coupling levels × collapse on/off × 5 scenarios × 10 seeds).",
        "",
        "## Summary tables (alive rate, mean ± std across seeds)",
        "",
    ]

    for scenario in scenarios:
        lines.append(f"### {scenario}")
        lines.append("")
        header = "| collapse | coupling | alive rate | survival steps | final energy |"
        if scenario == 'tunnel':
            header = "| collapse | coupling | barrier crossings | alive rate | survival steps |"
        lines += [header, "|---|---|---|---|---|"]

        for collapse in collapses:
            for q in couplings:
                key = (scenario, q, collapse)
                if key not in groups:
                    continue
                rs = groups[key]
                alive = [float(r['alive_rate']) for r in rs]
                surv = [float(r['avg_survival_steps']) for r in rs]
                energy = [float(r['avg_final_energy']) for r in rs]
                if scenario == 'tunnel':
                    cross = [float(r['barrier_crossings']) for r in rs]
                    lines.append(
                        f"| {collapse} | {q} | {fmt_mean_std(cross)} "
                        f"| {fmt_mean_std(alive)} | {fmt_mean_std(surv)} |")
                else:
                    lines.append(
                        f"| {collapse} | {q} | {fmt_mean_std(alive)} "
                        f"| {fmt_mean_std(surv)} | {fmt_mean_std(energy)} |")
        lines.append("")

    lines += ["## Statistical tests (collapse ON: quantum vs classical)", ""]
    lines.append("| scenario | comparison | n | U-test p-value | verdict |")
    lines.append("|---|---|---|---|---|")

    for scenario in scenarios:
        for collapse in [c for c in collapses if c == 'True']:
            classical = groups.get((scenario, '0.0', collapse))
            if not classical:
                continue
            for q in [q for q in couplings if q != '0.0']:
                quantum = groups.get((scenario, q, collapse))
                if not quantum:
                    continue
                a = [float(r['alive_rate']) for r in classical]
                b = [float(r['alive_rate']) for r in quantum]
                p = mann_whitney_u(a, b)
                verdict = "reject H₀" if p < 0.05 else "insufficient evidence"
                lines.append(
                    f"| {scenario} | alive rate q={q} vs q=0 | "
                    f"{len(a)+len(b)} | {p:.2e} | {verdict} |")

                if scenario == 'tunnel':
                    a2 = [float(r['barrier_crossings']) for r in classical]
                    b2 = [float(r['barrier_crossings']) for r in quantum]
                    p2 = mann_whitney_u(a2, b2)
                    verdict2 = "reject H₀" if p2 < 0.05 else "insufficient evidence"
                    lines.append(
                        f"| {scenario} | barrier crossings q={q} vs q=0 | "
                        f"{len(a2)+len(b2)} | {p2:.2e} | {verdict2} |")

    interp_existing = None
    if os.path.exists(args.output):
        with open(args.output, 'r', encoding='utf-8') as f:
            existing = f.read()
        interp_pos = existing.find("## Interpretation")
        if interp_pos >= 0:
            interp_text = existing[interp_pos:].strip()
            if interp_text and "_(filled after" not in interp_text:
                interp_existing = interp_text

    lines.append("")
    lines.append("## Interpretation")
    lines.append("")
    if interp_existing:
        lines.append(interp_existing[len("## Interpretation"):].strip())
    else:
        lines.append("_(pending)_")

    os.makedirs(os.path.dirname(args.output) or '.', exist_ok=True)
    with open(args.output, 'w', encoding='utf-8') as f:
        f.write("\n".join(lines) + "\n")
    print(f"Report written to {args.output}")


if __name__ == '__main__':
    main()
