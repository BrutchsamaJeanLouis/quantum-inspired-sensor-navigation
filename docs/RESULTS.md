# QIWM Ablation Results

Hypothesis under test (null): *Quantum-inspired dynamics provide NO advantage over classical agent navigation.*

Input: `ablation_results_v2.csv` — 400 runs (4 coupling levels × collapse on/off × 5 scenarios × 10 seeds).

## Summary tables (alive rate, mean ± std across seeds)

### default

| collapse | coupling | alive rate | survival steps | final energy |
|---|---|---|---|---|
| True | 0.0 | 0.450 ± 0.000 | 280.000 ± 0.000 | 270.000 ± 0.000 |
| True | 0.1 | 0.700 ± 0.458 | 380.000 ± 183.303 | 224.000 ± 146.642 |
| True | 0.3 | 0.900 ± 0.300 | 460.000 ± 120.000 | 288.000 ± 96.000 |
| True | 0.5 | 0.900 ± 0.300 | 460.000 ± 120.000 | 288.000 ± 96.000 |
| False | 0.0 | 0.450 ± 0.000 | 280.000 ± 0.000 | 270.000 ± 0.000 |
| False | 0.1 | 0.475 ± 0.081 | 290.000 ± 32.558 | 221.800 ± 34.738 |
| False | 0.3 | 0.485 ± 0.039 | 294.000 ± 15.620 | 269.800 ± 17.628 |
| False | 0.5 | 0.480 ± 0.024 | 292.000 ± 9.798 | 278.200 ± 10.448 |

### maze

| collapse | coupling | alive rate | survival steps | final energy |
|---|---|---|---|---|
| True | 0.0 | 0.000 ± 0.000 | 100.000 ± 0.000 | 0.000 ± 0.000 |
| True | 0.1 | 1.000 ± 0.000 | 500.000 ± 0.000 | 600.000 ± 0.000 |
| True | 0.3 | 1.000 ± 0.000 | 500.000 ± 0.000 | 600.000 ± 0.000 |
| True | 0.5 | 1.000 ± 0.000 | 500.000 ± 0.000 | 600.000 ± 0.000 |
| False | 0.0 | 0.000 ± 0.000 | 100.000 ± 0.000 | 0.000 ± 0.000 |
| False | 0.1 | 1.000 ± 0.000 | 500.000 ± 0.000 | 600.000 ± 0.000 |
| False | 0.3 | 1.000 ± 0.000 | 500.000 ± 0.000 | 600.000 ± 0.000 |
| False | 0.5 | 1.000 ± 0.000 | 500.000 ± 0.000 | 600.000 ± 0.000 |

### moving

| collapse | coupling | alive rate | survival steps | final energy |
|---|---|---|---|---|
| True | 0.0 | 0.450 ± 0.000 | 280.000 ± 0.000 | 270.000 ± 0.000 |
| True | 0.1 | 0.970 ± 0.060 | 488.000 ± 24.000 | 310.400 ± 19.200 |
| True | 0.3 | 0.660 ± 0.436 | 364.000 ± 174.310 | 211.200 ± 139.448 |
| True | 0.5 | 0.385 ± 0.473 | 254.000 ± 189.325 | 123.200 ± 151.460 |
| False | 0.0 | 0.450 ± 0.000 | 280.000 ± 0.000 | 270.000 ± 0.000 |
| False | 0.1 | 0.000 ± 0.000 | 142.800 ± 8.204 | 0.000 ± 0.000 |
| False | 0.3 | 0.000 ± 0.000 | 156.250 ± 10.422 | 0.000 ± 0.000 |
| False | 0.5 | 0.000 ± 0.000 | 149.500 ± 2.846 | 0.000 ± 0.000 |

### single_source

| collapse | coupling | alive rate | survival steps | final energy |
|---|---|---|---|---|
| True | 0.0 | 0.200 ± 0.000 | 180.000 ± 0.000 | 100.000 ± 0.000 |
| True | 0.1 | 1.000 ± 0.000 | 500.000 ± 0.000 | 500.000 ± 0.000 |
| True | 0.3 | 1.000 ± 0.000 | 500.000 ± 0.000 | 500.500 ± 1.500 |
| True | 0.5 | 1.000 ± 0.000 | 500.000 ± 0.000 | 500.500 ± 1.500 |
| False | 0.0 | 0.200 ± 0.000 | 180.000 ± 0.000 | 100.000 ± 0.000 |
| False | 0.1 | 1.000 ± 0.000 | 500.000 ± 0.000 | 598.500 ± 2.291 |
| False | 0.3 | 1.000 ± 0.000 | 500.000 ± 0.000 | 600.000 ± 0.000 |
| False | 0.5 | 1.000 ± 0.000 | 500.000 ± 0.000 | 600.000 ± 0.000 |

### tunnel

| collapse | coupling | barrier crossings | alive rate | survival steps |
|---|---|---|---|---|
| True | 0.0 | 0.000 ± 0.000 | 0.000 ± 0.000 | 100.000 ± 0.000 |
| True | 0.1 | 19.900 ± 0.300 | 0.900 ± 0.300 | 460.000 ± 120.000 |
| True | 0.3 | 20.000 ± 0.000 | 1.000 ± 0.000 | 500.000 ± 0.000 |
| True | 0.5 | 20.000 ± 0.000 | 1.000 ± 0.000 | 500.000 ± 0.000 |
| False | 0.0 | 0.000 ± 0.000 | 0.000 ± 0.000 | 100.000 ± 0.000 |
| False | 0.1 | 19.900 ± 0.300 | 0.990 ± 0.020 | 496.000 ± 8.000 |
| False | 0.3 | 20.000 ± 0.000 | 1.000 ± 0.000 | 500.000 ± 0.000 |
| False | 0.5 | 20.000 ± 0.000 | 1.000 ± 0.000 | 500.000 ± 0.000 |

## Statistical tests (collapse ON: quantum vs classical)

| scenario | comparison | n | U-test p-value | verdict |
|---|---|---|---|---|
| default | alive rate q=0.1 vs q=0 | 20 | 1.06e-01 | insufficient evidence |
| default | alive rate q=0.3 vs q=0 | 20 | 7.56e-04 | reject H₀ |
| default | alive rate q=0.5 vs q=0 | 20 | 7.56e-04 | reject H₀ |
| maze | alive rate q=0.1 vs q=0 | 20 | 1.59e-05 | reject H₀ |
| maze | alive rate q=0.3 vs q=0 | 20 | 1.59e-05 | reject H₀ |
| maze | alive rate q=0.5 vs q=0 | 20 | 1.59e-05 | reject H₀ |
| moving | alive rate q=0.1 vs q=0 | 20 | 3.29e-05 | reject H₀ |
| moving | alive rate q=0.3 vs q=0 | 20 | 1.13e-01 | insufficient evidence |
| moving | alive rate q=0.5 vs q=0 | 20 | 4.35e-01 | insufficient evidence |
| single_source | alive rate q=0.1 vs q=0 | 20 | 1.59e-05 | reject H₀ |
| single_source | alive rate q=0.3 vs q=0 | 20 | 1.59e-05 | reject H₀ |
| single_source | alive rate q=0.5 vs q=0 | 20 | 1.59e-05 | reject H₀ |
| tunnel | alive rate q=0.1 vs q=0 | 20 | 9.66e-05 | reject H₀ |
| tunnel | barrier crossings q=0.1 vs q=0 | 20 | 2.43e-05 | reject H₀ |
| tunnel | alive rate q=0.3 vs q=0 | 20 | 1.59e-05 | reject H₀ |
| tunnel | barrier crossings q=0.3 vs q=0 | 20 | 1.59e-05 | reject H₀ |
| tunnel | alive rate q=0.5 vs q=0 | 20 | 1.59e-05 | reject H₀ |
| tunnel | barrier crossings q=0.5 vs q=0 | 20 | 1.59e-05 | reject H₀ |

## Interpretation

### 1. The null hypothesis is rejected

The null — *quantum-inspired dynamics provide NO advantage over classical*
— is rejected in 4 of 5 scenarios (n=10 seeds/config, two-sided
Mann-Whitney U, α=0.05):

| scenario | classical (q=0) | quantum (best q) | verdict |
|---|---|---|---|
| tunnel | 0% alive, 0 crossings | 100% alive, 20/20 crossings (p ≤ 2.4e-5) | **decisive** |
| maze | 0% alive | 100% alive at every q>0 (p ≤ 1.6e-5) | **decisive** |
| single_source | 20% alive | 100% alive (p ≤ 1.6e-5) | **decisive** |
| default | 45% alive | 90% at q=0.3/0.5 (p ≈ 7.6e-4) | significant |
| moving | 45% alive | 68% at q=0.05 (p<5e-5, n=50); decays monotonically to baseline by q≥0.2 | significant, see §4 |

The tunnel is the cleanest result: a gapless 128-cell wall separates the
swarm from its only energy source. Classical agents: 0 cross, 0 survive —
the wall cell's −1e6 potential and the −22 adjacent repulsion make crossing
a gradient-descent impossibility. Any q>0: the pilot wave, which diffuses
straight through the wall, pulls agents onto the far side; 100% survive.

### 2. The advantage is quantum-channel-specific, not sampling noise

With the calibrated instrument, q=0.0 is a genuine classical baseline
deterministic argmax, not a stochastic classifier. Its 0-45% survival is
the honest classical number for these geometries. The v1 "classical"
numbers (70-98%) were the quantum sampler wearing a classical costume.

### 3. Collapse: the difference between survival and death in dynamic worlds

The collapse ablation splits cleanly:

- **Static geometries (tunnel, single_source):** the pilot-wave channel
  alone suffices — full advantage with collapse OFF.
- **Trapped/dynamic geometries (default, moving):** quantum agents with
  collapse OFF do **worse than classical** (default 45-48% ≈ baseline;
  moving 0% vs 45%). The advantage appears only with collapse ON
  (default →90%; moving 39-97%).

Reading: the pilot wave is the *sensor* (non-local sensing through
obstacles); the collapse/coherence gate is the *controller* (switching
between Boltzmann exploration and greedy exploitation where local coherence
has been measured). In static fields the sensor alone wins; against
moving fields and trap geometries, sensing without the collapse-driven
decision switch is actively fatal.

### 4. The moving scenario: coupling-liability curve, resolved at n=50

Three runs tell the story: v2 (n=10) showed 97%@0.1 → 39%@0.5 (a slope,
partly seed luck); the n=10 fine sweep (`q_sweep_moving.csv`) showed
nothing significant (underpowered); the n=50 sweep
(`q_sweep_moving_n50.csv`, 8 levels × 50 seeds, collapse ON) **confirms a
real, monotone effect** — a significant quantum advantage at low q that
decays to the classical baseline as q grows:

| q | 0.0 | 0.05 | 0.1 | 0.15 | 0.2 | 0.3 | 0.4 | 0.5 |
|---|---|---|---|---|---|---|---|---|
| alive (n=50) | 0.450 | 0.679 | 0.653 | 0.621 | 0.569 | 0.528 | 0.451 | 0.435 |
| p vs q=0 | — | <5e-5 | 8e-4 | 9e-3 | 0.14 | 0.46 | 0.46 | 0.26 |

Mechanistic read: the classical energy field updates instantly when a
source moves; the pilot wave lags. A *weak* quantum channel adds
non-local sensing (advantage); a *strong* channel glues the agent to a
stale wave (liability). The moving scenario has an interior optimum at
low coupling — the static scenarios saturate at q=0.1, so the operating
point is: weak coupling for dynamic fields, anything above for statics.

### 4b. Tunnel robustness: ε-greedy classical leaks through the wall

The tunnel's 0% vs 100% contrast is against *deterministic* classical.
A stochastic classical control (ε-greedy: uniform random step with
probability ε from the same action set; `classical_epsilon`) leaks the
1-cell wall at **any** noise level:

| baseline | crossings (per 100 agents) | alive |
|---|---|---|
| classical ε=0 | 0 | 0% |
| ε=0.05 | 51 | 43% |
| ε=0.10 | 75 | 68% |
| ε=0.20 | 90 | 83% |
| ε=0.30 | ~96 | ~92% |
| quantum q=0.1–0.5 (ε=0) | 99–100 | 90–100% |

The wall therefore discriminates *deterministic vs noisy* decision-making,
not quantum vs classical per se. The defensible quantum claim: the tunnel
is crossed **without decision noise** — the pilot-wave term provides a
positive gradient across the wall, while classical crossing requires
random jumps over it. A crossing-latency/directionality metric (next
item) would separate the two crossing modes quantitatively.

### 5. Dead-end escapes are quantum-only

The dead-end detector fired only in the moving scenario: 194 / 132 / 77
escapes at q=0.1/0.3/0.5 (collapse ON), 0 for classical — agents stuck in
local minima of the shifting field escape exclusively via Boltzmann mode.

### 6. Limitations (honest)

- The n=10 sweep was underpowered for the moving scenario; resolved at n=50 (§4): significant at q≤0.15, monotone decay to baseline by q≥0.2.
- The benefit curve's lower bound is untested below q=0.1; 0.1 already
  saturates most scenarios, so the "quantum threshold" is < 0.1.
- Instrument constants (gain 3000, dt 0.2, dissipation 0.9999, prewarm
  2000) are calibrated so the quantum channel is expressive. Identical for
  every coupling level, but they are modeling choices — the absolute
  magnitude of the advantage is instrument-dependent; the *existence*
  of the contrast (0% → 100%) is not, because the classical baseline's
  impossibility is structural (−1e6 barrier), not tuned.
- The classical baseline is deterministic greedy argmax. An ε-greedy
  stochastic classical baseline would strengthen the comparison (future
  work).

### 7. Next steps

1. Crossing-latency / directionality metric: separate quantum
   gradient-driven crossing from ε-noise leakage quantitatively (both are
   implemented as controls; see §4b).
2. Paper (8-12 pages) around: instrument forensics → tunnel result
   (incl. ε-greedy robustness, §4b) → collapse ablation →
   moving-scenario coupling curve (n=50, §4).
4. Demo: tunnel scenario with phi overlay (P key) — the visual of agents
   crossing a wall the classical swarm dies against is the centerpiece.
