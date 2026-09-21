# QIWM Ablation Results

Hypothesis under test (null): *Quantum-inspired dynamics provide NO advantage over classical agent navigation.*

Input: `ablation_results_v2.csv` — 400 runs (4 coupling levels × collapse on/off × 5 scenarios × 10 seeds).

## Summary tables (alive rate, mean ± std across seeds)

### default

| collapse | coupling | alive rate | 95% CI (bootstrap) | survival steps | final energy |
|---|---|---|---|---|---|
| True | 0.0 | 0.450 ± 0.000 | [0.450, 0.450] | 280.000 ± 0.000 | 270.000 ± 0.000 |
| True | 0.1 | 0.700 ± 0.458 | [0.400, 1.000] | 380.000 ± 183.303 | 224.000 ± 146.642 |
| True | 0.3 | 0.900 ± 0.300 | [0.700, 1.000] | 460.000 ± 120.000 | 288.000 ± 96.000 |
| True | 0.5 | 0.900 ± 0.300 | [0.700, 1.000] | 460.000 ± 120.000 | 288.000 ± 96.000 |
| False | 0.0 | 0.450 ± 0.000 | [0.450, 0.450] | 280.000 ± 0.000 | 270.000 ± 0.000 |
| False | 0.1 | 0.475 ± 0.081 | [0.425, 0.525] | 290.000 ± 32.558 | 221.800 ± 34.738 |
| False | 0.3 | 0.485 ± 0.039 | [0.465, 0.510] | 294.000 ± 15.620 | 269.800 ± 17.628 |
| False | 0.5 | 0.480 ± 0.024 | [0.465, 0.495] | 292.000 ± 9.798 | 278.200 ± 10.448 |

### maze

| collapse | coupling | alive rate | 95% CI (bootstrap) | survival steps | final energy |
|---|---|---|---|---|---|
| True | 0.0 | 0.000 ± 0.000 | [0.000, 0.000] | 100.000 ± 0.000 | 0.000 ± 0.000 |
| True | 0.1 | 1.000 ± 0.000 | [1.000, 1.000] | 500.000 ± 0.000 | 600.000 ± 0.000 |
| True | 0.3 | 1.000 ± 0.000 | [1.000, 1.000] | 500.000 ± 0.000 | 600.000 ± 0.000 |
| True | 0.5 | 1.000 ± 0.000 | [1.000, 1.000] | 500.000 ± 0.000 | 600.000 ± 0.000 |
| False | 0.0 | 0.000 ± 0.000 | [0.000, 0.000] | 100.000 ± 0.000 | 0.000 ± 0.000 |
| False | 0.1 | 1.000 ± 0.000 | [1.000, 1.000] | 500.000 ± 0.000 | 600.000 ± 0.000 |
| False | 0.3 | 1.000 ± 0.000 | [1.000, 1.000] | 500.000 ± 0.000 | 600.000 ± 0.000 |
| False | 0.5 | 1.000 ± 0.000 | [1.000, 1.000] | 500.000 ± 0.000 | 600.000 ± 0.000 |

### moving

| collapse | coupling | alive rate | 95% CI (bootstrap) | survival steps | final energy |
|---|---|---|---|---|---|
| True | 0.0 | 0.450 ± 0.000 | [0.450, 0.450] | 280.000 ± 0.000 | 270.000 ± 0.000 |
| True | 0.1 | 0.970 ± 0.060 | [0.925, 1.000] | 488.000 ± 24.000 | 310.400 ± 19.200 |
| True | 0.3 | 0.660 ± 0.436 | [0.370, 0.875] | 364.000 ± 174.310 | 211.200 ± 139.448 |
| True | 0.5 | 0.385 ± 0.473 | [0.100, 0.685] | 254.000 ± 189.325 | 123.200 ± 151.460 |
| False | 0.0 | 0.450 ± 0.000 | [0.450, 0.450] | 280.000 ± 0.000 | 270.000 ± 0.000 |
| False | 0.1 | 0.000 ± 0.000 | [0.000, 0.000] | 142.800 ± 8.204 | 0.000 ± 0.000 |
| False | 0.3 | 0.000 ± 0.000 | [0.000, 0.000] | 156.250 ± 10.422 | 0.000 ± 0.000 |
| False | 0.5 | 0.000 ± 0.000 | [0.000, 0.000] | 149.500 ± 2.846 | 0.000 ± 0.000 |

### single_source

| collapse | coupling | alive rate | 95% CI (bootstrap) | survival steps | final energy |
|---|---|---|---|---|---|
| True | 0.0 | 0.200 ± 0.000 | [0.200, 0.200] | 180.000 ± 0.000 | 100.000 ± 0.000 |
| True | 0.1 | 1.000 ± 0.000 | [1.000, 1.000] | 500.000 ± 0.000 | 500.000 ± 0.000 |
| True | 0.3 | 1.000 ± 0.000 | [1.000, 1.000] | 500.000 ± 0.000 | 500.500 ± 1.500 |
| True | 0.5 | 1.000 ± 0.000 | [1.000, 1.000] | 500.000 ± 0.000 | 500.500 ± 1.500 |
| False | 0.0 | 0.200 ± 0.000 | [0.200, 0.200] | 180.000 ± 0.000 | 100.000 ± 0.000 |
| False | 0.1 | 1.000 ± 0.000 | [1.000, 1.000] | 500.000 ± 0.000 | 598.500 ± 2.291 |
| False | 0.3 | 1.000 ± 0.000 | [1.000, 1.000] | 500.000 ± 0.000 | 600.000 ± 0.000 |
| False | 0.5 | 1.000 ± 0.000 | [1.000, 1.000] | 500.000 ± 0.000 | 600.000 ± 0.000 |

### tunnel

| collapse | coupling | barrier crossings | alive rate | 95% CI (bootstrap) | survival steps |
|---|---|---|---|---|---|
| True | 0.0 | 0.000 ± 0.000 | 0.000 ± 0.000 | [0.000, 0.000] | 100.000 ± 0.000 |
| True | 0.1 | 19.900 ± 0.300 | 0.900 ± 0.300 | [0.700, 1.000] | 460.000 ± 120.000 |
| True | 0.3 | 20.000 ± 0.000 | 1.000 ± 0.000 | [1.000, 1.000] | 500.000 ± 0.000 |
| True | 0.5 | 20.000 ± 0.000 | 1.000 ± 0.000 | [1.000, 1.000] | 500.000 ± 0.000 |
| False | 0.0 | 0.000 ± 0.000 | 0.000 ± 0.000 | [0.000, 0.000] | 100.000 ± 0.000 |
| False | 0.1 | 19.900 ± 0.300 | 0.990 ± 0.020 | [0.975, 1.000] | 496.000 ± 8.000 |
| False | 0.3 | 20.000 ± 0.000 | 1.000 ± 0.000 | [1.000, 1.000] | 500.000 ± 0.000 |
| False | 0.5 | 20.000 ± 0.000 | 1.000 ± 0.000 | [1.000, 1.000] | 500.000 ± 0.000 |

## Statistical tests (collapse ON: quantum vs classical)

Multi-agent comparison across all scenarios × 10 seeds: survival (alive rate) and efficiency (final energy = harvesting over the run), quantum q>0 vs classical q=0. n=20 per row (10 classical + 10 quantum seeds).

| scenario | comparison | n | Δ mean (95% CI, bootstrap) | U-test p-value | verdict |
|---|---|---|---|---|---|
| default | alive rate q=0.1 vs q=0 | 20 | +0.250 [-0.050, +0.550] | 1.06e-01 | insufficient evidence |
| default | final energy q=0.1 vs q=0 | 20 | -46.000 [-142.000, +50.000] | 1.06e-01 | insufficient evidence |
| default | alive rate q=0.3 vs q=0 | 20 | +0.450 [+0.250, +0.550] | 7.56e-04 | reject H₀ |
| default | final energy q=0.3 vs q=0 | 20 | +18.000 [-46.000, +50.000] | 7.56e-04 | reject H₀ |
| default | alive rate q=0.5 vs q=0 | 20 | +0.450 [+0.250, +0.550] | 7.56e-04 | reject H₀ |
| default | final energy q=0.5 vs q=0 | 20 | +18.000 [-46.000, +50.000] | 7.56e-04 | reject H₀ |
| maze | alive rate q=0.1 vs q=0 | 20 | +1.000 [+1.000, +1.000] | 1.59e-05 | reject H₀ |
| maze | final energy q=0.1 vs q=0 | 20 | +600.000 [+600.000, +600.000] | 1.59e-05 | reject H₀ |
| maze | alive rate q=0.3 vs q=0 | 20 | +1.000 [+1.000, +1.000] | 1.59e-05 | reject H₀ |
| maze | final energy q=0.3 vs q=0 | 20 | +600.000 [+600.000, +600.000] | 1.59e-05 | reject H₀ |
| maze | alive rate q=0.5 vs q=0 | 20 | +1.000 [+1.000, +1.000] | 1.59e-05 | reject H₀ |
| maze | final energy q=0.5 vs q=0 | 20 | +600.000 [+600.000, +600.000] | 1.59e-05 | reject H₀ |
| moving | alive rate q=0.1 vs q=0 | 20 | +0.520 [+0.475, +0.550] | 3.29e-05 | reject H₀ |
| moving | final energy q=0.1 vs q=0 | 20 | +40.400 [+26.000, +50.000] | 3.29e-05 | reject H₀ |
| moving | alive rate q=0.3 vs q=0 | 20 | +0.210 [-0.080, +0.470] | 1.13e-01 | insufficient evidence |
| moving | final energy q=0.3 vs q=0 | 20 | -58.800 [-151.600, +24.400] | 1.13e-01 | insufficient evidence |
| moving | alive rate q=0.5 vs q=0 | 20 | -0.065 [-0.350, +0.235] | 4.35e-01 | insufficient evidence |
| moving | final energy q=0.5 vs q=0 | 20 | -146.800 [-238.000, -50.800] | 4.35e-01 | insufficient evidence |
| single_source | alive rate q=0.1 vs q=0 | 20 | +0.800 [+0.800, +0.800] | 1.59e-05 | reject H₀ |
| single_source | final energy q=0.1 vs q=0 | 20 | +400.000 [+400.000, +400.000] | 1.59e-05 | reject H₀ |
| single_source | alive rate q=0.3 vs q=0 | 20 | +0.800 [+0.800, +0.800] | 1.59e-05 | reject H₀ |
| single_source | final energy q=0.3 vs q=0 | 20 | +400.500 [+400.000, +401.500] | 2.43e-05 | reject H₀ |
| single_source | alive rate q=0.5 vs q=0 | 20 | +0.800 [+0.800, +0.800] | 1.59e-05 | reject H₀ |
| single_source | final energy q=0.5 vs q=0 | 20 | +400.500 [+400.000, +401.500] | 2.43e-05 | reject H₀ |
| tunnel | alive rate q=0.1 vs q=0 | 20 | +0.900 [+0.700, +1.000] | 9.66e-05 | reject H₀ |
| tunnel | final energy q=0.1 vs q=0 | 20 | +450.000 [+350.000, +500.000] | 9.66e-05 | reject H₀ |
| tunnel | barrier crossings q=0.1 vs q=0 | 20 | +19.900 [+19.700, +20.000] | 2.43e-05 | reject H₀ |
| tunnel | alive rate q=0.3 vs q=0 | 20 | +1.000 [+1.000, +1.000] | 1.59e-05 | reject H₀ |
| tunnel | final energy q=0.3 vs q=0 | 20 | +500.000 [+500.000, +500.000] | 1.59e-05 | reject H₀ |
| tunnel | barrier crossings q=0.3 vs q=0 | 20 | +20.000 [+20.000, +20.000] | 1.59e-05 | reject H₀ |
| tunnel | alive rate q=0.5 vs q=0 | 20 | +1.000 [+1.000, +1.000] | 1.59e-05 | reject H₀ |
| tunnel | final energy q=0.5 vs q=0 | 20 | +500.500 [+500.000, +501.500] | 2.43e-05 | reject H₀ |
| tunnel | barrier crossings q=0.5 vs q=0 | 20 | +20.000 [+20.000, +20.000] | 1.59e-05 | reject H₀ |

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

The tunnel is the cleanest geometry: a gapless wall column separates the
swarm from its only energy source. Classical agents: 0 cross, 0 survive —
the wall spike (−1e6) and its poisoned neighbours make forward progress a
local-greedy trap, and the classical gradient always points at the wall,
never at the torus seam (x=0/127) which is the way around it. Any q>0:
100% survive; the crossing taxonomy (§4b) shows all crossings are seam
wraps (~2.5-step latency), none through the wall — the globally leaked
pilot wave makes the far side attractive and Boltzmann sampling finds the
route.

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

### 4b. Crossing taxonomy: the quantum tunnel is a seam shortcut, not a wall jump

The x=64 column on the torus is a contractible loop; it does NOT
separate the surface — the x=0/127 seam is a way around it. First-
crossing taxonomy per agent (tunnel, 10 seeds each, collapse ON):

| baseline | wall jumps (63↔65) | wall walk-throughs (via 64) | seam wraps | first-crossing latency (steps) |
|---|---|---|---|---|
| classical (ε=0) | 0 | 0 | 0 | — |
| ε-greedy 0.1 | 4 | 124 | 20 | 17.4 |
| ε-greedy 0.3 | 15 | 157 | 24 | 5.2 |
| quantum q=0.1 (ε=0) | 0 | 0 | 169 | 2.8 |
| quantum q=0.5 (ε=0) | 0 | 0 | 200 | 2.4 |

(wall walk-throughs added 2026-08-20: ε-steps are patch-coarse (up to
±sense_radius per axis), so most ε-crossings LAND on the −1e6 wall cell
and step out of it — not 2-cell jumps. Counts are 10-seed re-runs with
the refined taxonomy.)

Full end-to-end ε-sweep curve (5 noise levels × 10 seeds, incl. a
quantum+ε interaction arm): §4h.

**Retraction:** the v2 tunneling claim — "quantum crosses the wall while
classical cannot" — was wrong: quantum agents never cross the wall (0 wall
jumps AND 0 walk-throughs across all 100 quantum agents — Boltzmann
sampling assigns ~zero probability to the −1e6 cell); they wrap the seam
~2.5 steps after reaching it. The globally leaked pilot wave makes the
far side attractive, and Boltzmann sampling discovers the route that a
local greedy policy can structurally never find (its gradient always
points at the wall, never at the seam). ε-noise crossings are mostly
coarse walk-throughs of the wall column, plus occasional true 2-cell
jumps and seam wraps.

Defensible claim: (1) deterministic local-greedy classical never reaches
the far side (structural); (2) stochastic classical (ε-greedy) DOES find
the route, so the tunnel separates *determinism vs exploration*, not
quantum vs classical per se; (3) the quantum channel shortens first-
crossing latency (2.4–2.8 vs 5.2–17.4) and survives ~completely (90–100%).
The 0%→100% survival contrast stands, but the mechanism is *route
discovery via a globally leaked sensor*, not wall penetration.

### 4c. Anticipatory positioning: the quantum channel reduces lag, not foreknowledge

Dedicated metric (moving scenario, `examples/moving_anticipation_n10.py`,
`moving_anticipation_n10.csv`, n=10, collapse ON, max_steps 500): per
agent, per step t, d_now = distance to nearest source at time t, d_lead =
distance to nearest source at time t+H (H=15). Index = mean(d_now −
d_lead) in px (positive = positioned toward where the source is HEADING);
frac = fraction of steps with d_lead < d_now.

| q | index (mean ± std) | frac ahead |
|---|---|---|
| 0.0 | −4.09 ± 0.00 | 0.000 |
| 0.1 | −2.58 ± 2.70 | 0.071 |
| 0.3 | −1.39 ± 2.94 | 0.103 |

**Honest null as an anticipation claim:** no condition shows positive
anticipation — every agent, including quantum, sits on average CLOSER to
the source's current than future position (the diffusive field carries
past information, not future). The quantum channel monotonically *reduces
the lag*: index −4.09 → −2.58 → −1.39 and forward positioning appears
(frac 0 → 0.07 → 0.10). Per-seed signs at q=0.3 are unreliable: the
positive-index seeds are exactly the zero-survival runs, whose truncated
trajectories bias the mean. Consistent with §4: the wave lags the
source, and the advantage is reduced tracking error in a shifting field,
not foresight.

### 4d. Maze route audit: the maze advantage is ALSO global route discovery

`examples/maze_route_audit.py` (`maze_route_audit.csv`, 10 seeds × 500
steps): agents that first reach the goal source (110,110), classified by
route — 'edge' = first torus-edge wrap before reaching (the seam-shortcut
mechanism of §4b), 'gap' = passed through a hand-crafted passage
(dead-end exit / vertical gap) without any wrap.

| config | reached/run | route: edge wrap | route: crafted gap |
|---|---|---|---|
| classical (ε=0) | 0.0 / 20 | — | — |
| ε-greedy 0.1 | 11.4 / 20 | 0.70 | 0.02 |
| quantum q=0.3 | 20.0 / 20 | 1.00 | 0.00 |

**Answer to the audit question: yes.** The maze advantage reduces to the
same mechanism as the tunnel: agents reach the goal by wrapping the torus
edge around the contractible wall loops — NOT by solving the maze through
its crafted gaps (0.00 gap-route fraction for quantum; 0.02 for
ε-classical). The 'maze' is effectively another instance of route
discovery via a globally leaked sensor. The quantum-specific delta is
completeness, not route type: 20/20 reach (vs 11.4/20 for ε-classical),
and survival is 100% vs 0% classical — the maze, like the tunnel,
separates *determinism vs exploration*, and the quantum channel makes
exploration exhaustive.

### 4e. Phi threshold: wired, NOT met (honest null)

`phi_mean` / `phi_final` now land in every ablation run (central region
(48,48)–(80,80), sampled every 100 steps on a deep copy — compute_phi
simulates forward and mutates its world). `examples/phi_audit.py`
(`phi_audit.csv`, n=10, default scenario, 500 steps):

| config | phi_mean |
|---|---|
| classical q=0.0 | 0.9894 |
| quantum q=0.3 | 0.9893 |

**Readme threshold `quantum_phi > 1.5 × classical_phi`: NOT MET** —
ratio 1.000. A second probe (region centered on the live swarm centroid)
agrees in kind: step-0 phi 0.883 (classical) vs 0.314 (quantum) — quantum
is LOWER, not higher — and both converge to the same steady state by
step 100. Interpretation: the agent ensemble barely perturbs the field
the phi probe sees (probe region 33², agents in corners), and the
steady-state field is dominated by deterministic pilot-wave dynamics,
identical across conditions. Phi as currently implemented measures the
FIELD's self-organization, not the agent-world coupling. The readme
threshold is recorded as NOT MET, not deleted; meeting it would require
re-scoping phi to an agent-localized region or an agent-in-the-loop
forward simulation (P7 — done, see §4i).

### 4f. Path-efficiency ratio: NOT MET — quantum trades directness for reachability

`path_eff_mean` (per run, all scenarios): for each agent that first
arrives at an energy source, straight-line torus geodesic distance
(spawn → source at arrival) ÷ actual traveled path length; 1.0 = perfect
direct route. (Torus note: slightly >1 is possible when an agent walks
the long way; observed only as 1.02 classical.)
`examples/path_efficiency.py` → `path_efficiency_{scenario}.csv` (n=10,
500 steps, collapse ON). Threshold: quantum ≥ 1.15 × classical.

| scenario | classical | quantum q=0.3 | ratio | threshold 1.15 |
|---|---|---|---|---|
| default | 1.0207 | 0.5055 ± 0.0483 | 0.495 | NOT MET |
| maze | 0/20 reached | 0.8940 ± 0.0053 | n/a | n/a |

**Honest null:** the quantum channel is WORSE on directness — the
Boltzmann walk meanders (~2× the direct route), while deterministic
classical walks near-perfect straight lines to the source it can see.
The 15% threshold is recorded as NOT MET, not tuned away. The defensible
reading: efficiency and reachability are separate axes. Quantum's value
is not shorter routes — it is arriving at all (and surviving): in the
maze, classical reaches 0/20 at any efficiency, quantum 20/20 at 0.894.
Efficiency here is the price of the stochastic exploration that makes
the unreachable reachable.

### 4g. Closed-boundary audit: without the seam, NOBODY tunnels

`examples/tunnel_closed_audit.py` (`tunnel_closed_audit.csv`, 10 seeds,
500 steps): same tunnel (gapless x=64 wall, source far-side) but edges
CLAMPED instead of wrapped — the seam shortcut does not exist, and the
wall truly separates the surface. Refines §4b with the walk-through
taxonomy.

| config | alive | crossings/run | wall jumps | wall walk-throughs | seam wraps |
|---|---|---|---|---|---|
| classical (ε=0) | 0.00 | 0.0 | 0 | 0 | 0 |
| ε-greedy 0.1 | 0.25 | 13.2 | 1 | 133 | 0 |
| quantum q=0.5 (ε=0) | 0.00 | 0.0 | 0 | 0 | 0 |

**The tunnel advantage is seam-dependent, not wall-penetrative.** With
the seam removed: (1) quantum q=0.5 crosses ZERO and dies (0% alive) —
Boltzmann sampling assigns ~zero probability to the −1e6 wall cell AND
never makes the 2-cell 63↔65 jump, so a truly impenetrable wall is
impenetrable to the quantum channel; (2) only ε-noise crosses — and
exclusively by coarse walk-throughs (landing on the wall cell and
stepping out), at 25% alive vs the 100% the seam route gives; (3)
classical is 0 as before. This closes the loop on §4b: the mechanism
is *route discovery via a globally leaked sensor around a contractible
wall*, and the torus seam is what makes the route exist. The honest
final claim: **no channel in this model penetrates an impenetrable
barrier; the quantum channel's value is exhaustive non-local exploration
of routes that exist but are locally invisible.**

### 4h. End-to-end ε-sweep: the noise-vs-quantum tradeoff (tunnel, torus)

`examples/epsilon_sweep_tunnel.py` (`epsilon_sweep_tunnel.csv`, 7 arms ×
10 seeds × 20 agents, 500 steps, collapse ON — v2 instrument; seed =
1000·i + ε-offset, +400 for quantum arms): the full curve of what
decision noise alone buys, against the quantum-channel anchor.

| arm (q, ε) | alive % (mean ± std) | crossings/run | first-crossing latency (mean, median) | wall jumps / walk-throughs / seam wraps |
|---|---|---|---|---|
| classical (0, 0) | 0.0 ± 0.0 | 0.0 | — | 0 / 0 / 0 |
| (0, 0.05) | 48.0 ± 7.8 | 12.0 | 27.9, 27.4 | 3 / 97 / 20 |
| (0, 0.1) | 66.5 ± 11.6 | 14.5 | 16.8, 15.2 | 5 / 120 / 23 |
| (0, 0.2) | 79.0 ± 12.6 | 18.1 | 17.4, 17.7 | 7 / 158 / 22 |
| (0, 0.3) | 83.5 ± 12.3 | 19.1 | 11.6, 10.9 | 16 / 149 / 28 |
| quantum (0.3, 0) | 100.0 ± 0.0 | 20.0 | 2.3, 2.2 | 0 / 0 / 200 |
| quantum (0.3, 0.1) | 100.0 ± 0.0 | 20.0 | 2.6, 2.7 | 0 / 0 / 200 |

**Readings.** (1) Noise alone buys crossings monotonically: 0 → 48.0 →
66.5 → 79.0 → 83.5 % alive as ε goes 0 → 0.05 → 0.1 → 0.2 → 0.3, with
crossings/run 0 → 12.0 → 14.5 → 18.1 → 19.1 — but classical still does
NOT reach the quantum arm (100 %, 20/20) even at ε = 0.3. (2) The
latency gap persists at every ε tested: quantum median 2.2 steps vs
11–28 for the ε-arms (5–12×). (3) Taxonomy is stable under ε: 77–84 %
of ε-crossings are coarse wall walk-throughs, seam wraps stay flat at
~2/run, and true 2-cell jumps grow slowly (0.3/run at ε=0.05 → 1.6/run
at ε=0.3). The quantum arm is 100 % seam across all 200 agents, 0 wall
events. (4) **Interaction arm:** putting ε = 0.1 on the quantum arm's
classical fallback path (used when the coherence gate is closed) is
benign — 100 % alive, 20/20 crossings, all seam, median latency 2.7
with per-seed ranges overlapping pure quantum (1.9–2.9 vs 1.6–3.7). No
synergy, no interference: ε sits on a path the quantum agents barely
take.

**Tradeoff summary (paper material):** the ε budget required for
classical parity (ε ≳ 0.3, still 83.5 % < 100 %) is precisely the
regime where crossings are wall walk-throughs and latency stays 5–10×
higher. The quantum channel achieves full crossings at zero decision
noise, but only via the seam route (§4b, §4g). The tradeoff is thus
not parity but *route for the same price*: the same exploration you pay
for as decision noise is replaced by a non-local sensor that finds the
route deterministically and 5–12× faster.

### 4i. Phi re-scope (P7): agent-in-the-loop, agent-localized Φ — NOT MET, direction reversed

The §4e Φ probe measured FIELD self-organization (agent-less forward sim on a
fixed central region the agents never occupy) → ratio 1.000. We re-scoped it
to the coupling metric the threshold was actually supposed to test. New metric
(`compute_phi_agents`, `src/core/coherence.py`; wired behind
`ExperimentConfig.phi_agent_in_loop`, default OFF so the 400-run v2 dataset is
byte-identical on re-run): for each agent, probe a (2·r+1)² window (r=4) around
its *current* position, forward-simulate `steps`=5 **with the whole swarm
stepping** (sense/decide/move/collapse — Penrose observation is part of the
co-dynamics), and compute max(0, corr(t0_R, t1_R) − corr(boundary_t0_R, t1_R))
on the *guidance field* the agent perceives, averaged over agents. Defined
before the number was read.

`examples/phi_rescope.py` (`phi_rescope.csv`, default scenario, n=10, 500
steps, collapse ON, sample every 100):

| config | phi_agent mean ± std | min–max |
|---|---|---|
| classical q=0.0 | 1.0000 ± 0.0000 | 1.0000–1.0000 |
| quantum q=0.3 | 0.8740 ± 0.0125 | 0.8546–0.8883 |

**Readme threshold `quantum_phi > 1.5 × classical_phi`: NOT MET — ratio
0.874, and the direction is REVERSED (quantum lower).** Moving scenario, same
metric: classical 1.0000, quantum 0.4630 ± 0.1965 — same direction. The
direction (quantum ≤ classical) is now consistent across **three independent
probe designs**: field-only central (ratio 1.000, §4e), swarm-centroid
(quantum lower, §4e), and agent-localized agent-in-the-loop (this — quantum
lower).

**Instrument property (documented, not a finding):** classical is pinned at
exactly 1.0000 in every scenario. Its perceived field is the deterministic
potential field, locally *static* over the 5-step horizon (default has no moving
sources; in moving, source jumps are discrete and usually outside a 9×9
window), so t0_R ≡ t1_R → self-predictability 1.0. Quantum is < 1.0 because
the guidance field it perceives adds the **diffusive pilot-wave channel**
(gain 3000 · normalize(pilot)), which is evolving and therefore less
self-predictable over 5 steps. So the *magnitude* (0.874) is partly a ceiling
effect; the *direction* is robust and is the real signal.

**Interpretation.** Quantum-inspired dynamics do NOT raise local
self-organization of the agent–world system. The pilot-wave channel adds
diffusive, less-predictable structure to the field the agent perceives, so the
re-scoped coupling Φ is modestly *lower* under quantum. We **formally retract
the specific "quantum Φ is 1.5× classical Φ" threshold as stated** (readme
success-metric) and **retain re-scoped Φ as a clean agent–world-coupling
diagnostic** — a substantive instrumentation improvement, since the original Φ
measured field self-organization (1.000), not coupling. The paper carries this
as an honest negative with a fixed instrument and a consistent direction, not a
silent null.

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

1. Research paper (8–12 pages): instrument forensics → tunnel + ε-sweep
   robustness (§4b, §4h) → collapse ablation → moving-scenario coupling curve
   (n=50, §4) → path-efficiency + phi re-scope (§4f, §4i).
2. Demo video: tunnel A/B centerpiece (quantum 20/20 vs classical 0/20 alive;
   GIFs exist) with the phi overlay (P key).
3. Repo polish: stale CLAUDE.md "Phase 1" status, doc cross-refs.
