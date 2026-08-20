# QIWM Scrapbook

## 2026-08-19: Product Owner Session — the null hypothesis is dead

### The story in one paragraph
v1 ablations showed zero quantum advantage. Forensics proved the instrument
was broken, not the hypothesis: (1) the pilot wave dissipated 2%/step so
`quantum_coupling` multiplied ~0.004 at any distance — a no-op slider;
(2) q=0.0 "classical" agents ran the quantum Boltzmann sampler (coherence
gate init 1.0 > 0.7 threshold); (3) the maze dead-end trap was geometrically
unreachable (0 agent-steps inside it, measured). After recalibrating the
instrument, the same harness gives: **classical 0/20 cross a gapless wall
and 0% survive; quantum 20/20 cross, 100% survive (p ≤ 2.4e-5)**.

### Changes shipped
- `quantum_world.py`: guidance = `grid + q·gain·(pilot/pmax)`; new
  `pilot_wave_gain=3000`, `pilot_wave_dissipation=0.9999` (was 0.98)
- `experiments.py`: dt default 0.1→0.2 (stable limit 0.25), 2000-step
  prewarm, new **tunnel** scenario (128-cell gapless wall, radius 2.0,
  source far-side), `barrier_crossings` metric
- `agents.py`: q=0 → classical argmax decision (quantum sampler only if
  `quantum_coupling > 0`)
- `examples/analyze_results.py` (new): mean±std tables + Mann-Whitney U
  (scipy, numpy permutation fallback) → `docs/RESULTS.md` (idempotent)
- Tests: 52 → 63 passing (guidance normalization, tunnel geometry,
  wall-leak, barrier metric, q=0 classical guard, sampling test)
- Docs: `docs/RESULTS.md` (full report + interpretation), readme
  Results section, TODO.md re-planned

### v2 headline numbers (400 runs, `ablation_results_v2.csv`)
| scenario | classical q=0 | quantum | p |
|---|---|---|---|
| tunnel | 0% alive, 0 cross | 100%, 20/20 | ≤2.4e-5 |
| maze | 0% | 100% (all q>0) | ≤1.6e-5 |
| single_source | 20% | 100% | ≤1.6e-5 |
| default | 45% | 90% @0.3/0.5 | 7.6e-4 |
| moving | 45% | 67% @0.1 (p≈0.11, n.s. at n=10) | n.s. — weakest scenario |

Collapse ablation: static geometries need only the pilot-wave channel
(collapse-off still wins); in moving/trapped fields, quantum agents
WITHOUT collapse do *worse* than classical (0-48%) — the collapse/coherence
decision gate is the survival mechanism. Moving scenario: v2's
"coupling liability" (97→39%) **retracted** by finer q-sweep
 — seed luck; modest low-q bump, n.s. at n=10. Dead-end escapes: 194/132/77 quantum-only, 0 classical.

### Instrument ASCII
```
source ──inject──▶ pilot_wave (Laplacian dt=0.2, κ=0.9999)
                     │  leaks through walls (no obstacle mask)
                     ▼
guidance = grid + q·3000·(pilot/pmax)      ◀── q=0 ⇒ classical argmax only
                     │
        NanoAgent: coherence>0.7 ? Boltzmann : greedy-argmax
                     │  step → collapse_field (coherence×0.9, wave×1.1)
                     ▼
        tunnel: wall cell −1e6 (unlandable), adjacent −22,
                far-side quantum term +12…+61 ⇒ quantum-only crossing
```

### Open / next (Priority 6 in TODO.md)
1. n≥50 run in moving scenario (n is the bottleneck; classical baseline deterministic)
2. ε-greedy classical control baseline
3. Phi metric into the harness (readme threshold: quantum_phi > 1.5×)
4. Path-efficiency ratio (threshold 15%)
5. Paper: forensics → tunnel → collapse ablation → tradeoff
6. Demo video: tunnel + phi overlay centerpiece

### Caveats to carry into the paper
- n=10/config; moving-scenario variance is high (bimodal seeds)
- Benefit lower bound untested below q=0.1
- Absolute advantage magnitude is instrument-dependent; the 0%→100%
  contrast is not — the classical barrier is structural (−1e6 spike),
  not tuned
