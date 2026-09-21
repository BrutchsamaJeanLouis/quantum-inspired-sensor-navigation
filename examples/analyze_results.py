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


def bootstrap_ci(values, n_boot: int = 2000, ci: float = 0.95, seed: int = 0):
    """Nonparametric bootstrap confidence interval for the mean."""
    v = np.asarray(values, dtype=float)
    if v.size == 0:
        return (float('nan'), float('nan'))
    rng = np.random.default_rng(seed)
    idx = rng.integers(0, v.size, size=(n_boot, v.size))
    means = v[idx].mean(axis=1)
    alpha = (1.0 - ci) / 2.0
    return (float(np.quantile(means, alpha)), float(np.quantile(means, 1 - alpha)))


def delta_ci(a, b, n_boot: int = 2000, ci: float = 0.95, seed: int = 0):
    """Bootstrap CI for the difference of means (b - a)."""
    a = np.asarray(a, dtype=float)
    b = np.asarray(b, dtype=float)
    if a.size == 0 or b.size == 0:
        return (float('nan'), float('nan'))
    rng = np.random.default_rng(seed)
    ia = rng.integers(0, a.size, size=(n_boot, a.size))
    ib = rng.integers(0, b.size, size=(n_boot, b.size))
    diffs = b[ib].mean(axis=1) - a[ia].mean(axis=1)
    alpha = (1.0 - ci) / 2.0
    return (float(np.quantile(diffs, alpha)), float(np.quantile(diffs, 1 - alpha)))


def fmt_ci(vals, n_boot: int = 2000, seed: int = 0) -> str:
    lo, hi = bootstrap_ci(vals, n_boot=n_boot, seed=seed)
    if np.isnan(lo) or np.isnan(hi):
        return "–"
    return f"[{lo:.3f}, {hi:.3f}]"


def fmt_delta_ci(a, b, n_boot: int = 2000, seed: int = 0) -> str:
    """Format mean diff with its bootstrap 95% CI: '+0.550 [+0.300, +0.750]'."""
    a = np.asarray(a, dtype=float)
    b = np.asarray(b, dtype=float)
    if a.size == 0 or b.size == 0:
        return "–"
    lo, hi = delta_ci(a, b, n_boot=n_boot, seed=seed)
    return f"{b.mean() - a.mean():+.3f} [{lo:+.3f}, {hi:+.3f}]"


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
        header = ("| collapse | coupling | alive rate | 95% CI (bootstrap) "
                  "| survival steps | final energy |")
        if scenario == 'tunnel':
            header = ("| collapse | coupling | barrier crossings | alive rate "
                      "| 95% CI (bootstrap) | survival steps |")
        lines += [header, "|---|---|---|---|---|---|"]

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
                        f"| {fmt_mean_std(alive)} | {fmt_ci(alive)} "
                        f"| {fmt_mean_std(surv)} |")
                else:
                    lines.append(
                        f"| {collapse} | {q} | {fmt_mean_std(alive)} "
                        f"| {fmt_ci(alive)} | {fmt_mean_std(surv)} "
                        f"| {fmt_mean_std(energy)} |")
        lines.append("")

    lines += [
        "## Statistical tests (collapse ON: quantum vs classical)",
        "",
        "Multi-agent comparison across all scenarios × 10 seeds: survival "
        "(alive rate) and efficiency (final energy = harvesting over the run), "
        "quantum q>0 vs classical q=0. n=20 per row (10 classical + 10 "
        "quantum seeds).",
        "",
        "| scenario | comparison | n | Δ mean (95% CI, bootstrap) | U-test p-value | verdict |",
        "|---|---|---|---|---|---|",
    ]

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
                    f"{len(a)+len(b)} | {fmt_delta_ci(a, b)} | {p:.2e} | {verdict} |")

                # Efficiency: final energy (harvesting efficiency over the
                # run), quantum vs classical.
                e0 = [float(r['avg_final_energy']) for r in classical]
                e1 = [float(r['avg_final_energy']) for r in quantum]
                pe = mann_whitney_u(e0, e1)
                verdict_e = "reject H₀" if pe < 0.05 else "insufficient evidence"
                lines.append(
                    f"| {scenario} | final energy q={q} vs q=0 | "
                    f"{len(e0)+len(e1)} | {fmt_delta_ci(e0, e1)} | {pe:.2e} | {verdict_e} |")

                if scenario == 'tunnel':
                    a2 = [float(r['barrier_crossings']) for r in classical]
                    b2 = [float(r['barrier_crossings']) for r in quantum]
                    p2 = mann_whitney_u(a2, b2)
                    verdict2 = "reject H₀" if p2 < 0.05 else "insufficient evidence"
                    lines.append(
                        f"| {scenario} | barrier crossings q={q} vs q=0 | "
                        f"{len(a2)+len(b2)} | {fmt_delta_ci(a2, b2)} | {p2:.2e} | {verdict2} |")

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
