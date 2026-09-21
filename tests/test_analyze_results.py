"""
Bootstrap CI + analyzer end-to-end tests (examples/analyze_results.py).

Covers the CI math (bracketing, degeneracy, determinism, direction of the
difference) and that the regenerated report contains CI columns on both
the summary tables and every U-test comparison row.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np  # noqa: E402

from examples.analyze_results import (  # noqa: E402
    bootstrap_ci, delta_ci, fmt_ci, fmt_delta_ci, main as analyze_main)

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class TestBootstrapCI:
    def test_ci_brackets_mean_and_range(self):
        v = np.array([0.1, 0.2, 0.3, 0.9])
        lo, hi = bootstrap_ci(v)
        assert lo <= float(np.mean(v)) <= hi
        assert float(np.min(v)) <= lo and hi <= float(np.max(v))
        assert hi > lo

    def test_degenerate_values_give_point_ci(self):
        lo, hi = bootstrap_ci([0.5, 0.5, 0.5])
        assert lo == hi == 0.5

    def test_delta_ci_sign_and_determinism(self):
        a = [0.1, 0.2, 0.3]
        b = [0.8, 0.9, 1.0]
        lo1, hi1 = delta_ci(a, b)
        lo2, hi2 = delta_ci(a, b)
        assert (lo1, hi1) == (lo2, hi2)
        assert lo1 > 0  # b clearly above a: whole interval positive
        assert delta_ci(b, a)[0] < 0  # sign flips with order

    def test_fmt_helpers(self):
        assert '[' in fmt_ci([0.2, 0.4, 0.6])
        assert fmt_ci([]) == '–'
        s = fmt_delta_ci([0.0, 0.0], [0.4, 0.6])
        assert s.startswith('+0.') and '[' in s


class TestAnalyzeReportEndToEnd:
    def test_report_has_ci_columns(self, tmp_path, monkeypatch):
        monkeypatch.chdir(REPO_ROOT)
        out = tmp_path / 'RESULTS_ci.md'
        sys.argv = ['analyze_results.py',
                    '--input', 'ablation_results_v2.csv',
                    '--output', str(out)]
        analyze_main()
        text = open(str(out), encoding='utf-8').read()
        assert '95% CI (bootstrap)' in text
        assert 'Δ mean (95% CI, bootstrap)' in text
        # Every summary alive-rate row carries a CI interval; count of CI
        # column headers equals number of scenario sections.
        assert text.count('| collapse | coupling') == \
            text.count('### ') - text.count('#### ')
        # At least one interval of the form [0.100, 0.900] is present.
        assert '[0.' in text or '[-' in text
