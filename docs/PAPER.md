# Weakly Quantum-Inspired Navigation: A Pilot-Wave World Model That Finds Routes a Local Greedy Policy Cannot

**Author: Brutchsama Jean-Louis**

*A research prototype report* · QIWM (Quantum-Inspired World Model)

> **Code, data & scripts:** <https://github.com/BrutchsamaJeanLouis/quantum-inspired-sensor-navigation> · **Paper DOI (Zenodo):** <https://doi.org/10.5281/zenodo.22964117> (`10.5281/zenodo.22964117`)

> Scope statement. This is a 10-week research prototype, not a production system and
> not a claim that these dynamics are quantum mechanics. We build a classical
> grid world, add a *quantum-inspired* sensing channel (a Bohmian-style pilot
> wave that globally leaks around obstacles) plus a Penrose-style observation
> collapse, and ask a falsifiable question: *does that channel help a swarm of
> agents navigate, versus a classical local-greedy baseline?* Everything is
> "inspired by," deliberately so. The honest answer, after instrument
> forensics, is **yes in four of five scenarios, with a specific mechanism
> (global route discovery) and a specific cost (coupling must be weak in dynamic
> fields, and directness is traded for reachability).**

---

## Abstract

We test the null hypothesis that quantum-inspired dynamics provide *no* advantage
over classical agent navigation, in a grid world model with energy sources,
obstacles, and a toroidal boundary. The "quantum" agent reads a *guidance field*
= the classical potential **plus** a diffusing, globally-leaked pilot-wave
channel, and makes decisions by Boltzmann sampling over a 5×5 patch; a
Penrose-inspired collapse (local coherence decay + pilot-wave sharpening) fires
on each observation. The classical baseline is deterministic argmax.

After fixing a baseline bug found by reproducibility forensics (the v1 "classical"
arm was actually the quantum sampler in argmax mode — 70–98% survival vs the
true deterministic 0–45%), the calibrated instrument gives: the null is rejected
in **4 of 5 scenarios** (tunnel 0%→100% alive, p≤2.4e-5; maze 0%→100%,
p≤1.6e-5; single-source 20%→100%, p≤1.6e-5; default 45%→90%, p≈7.6e-4), with
the moving scenario showing a **monotone coupling-liability curve** (advantage at
q=0.05–0.15, decaying to baseline by q≥0.2; n=50, p<5e-5 at q=0.05). A crossing
taxonomy shows the mechanism is **global route discovery via the leaked pilot
wave, not wall penetration** — quantum agents wrap the torus seam (~2.5-step
latency), they never jump the wall; deterministic local-greedy classical is
structurally unable to find that route (its gradient always points at the wall).
The tradeoff is *route for the same price*: adding ε-greedy noise to the classical
arm recovers up to 83.5% tunnel survival but at 5–12× first-crossing latency,
while the quantum arm stays at 100% and ~2.4–2.8 latency. The IIT-inspired Φ
metric was re-scoped to an agent-in-the-loop, agent-local coupling measure; it
is **not** 1.5× higher under quantum (ratio 0.874, direction reversed), so that
specific threshold is formally retracted while the re-scoped Φ is retained as a
clean coupling diagnostic. We frame the result as an honest, instrumented null-
rejection with a known mechanism, a known cost, and a documented retraction —
not a silent win.

**Keywords:** world models, pilot-wave dynamics, IIT-inspired coherence, agent
navigation, ablation, reproducibility.

---

## 1. Introduction and motivation

Most agent navigation research assumes the policy can see what it needs: a
gradient, a reward, or a map. We want to know something smaller and more
awkward: **if the only "sensing" an agent gets is a field that leaks around
obstacles the way a wave does, does that help it reach things a local policy
cannot see how to reach?**

This is a toy, deliberately. A 128×128 grid, 20 agents, energy sources (1/r
attraction) and repulsive obstacles, a toroidal boundary, 500 steps. Two arms:

- **Classical.** The agent reads the classical potential field locally (5×5 patch)
  and moves by deterministic argmax toward the steepest descent.
- **Quantum-inspired.** The agent reads a *guidance field* = potential **+** a
  coupling-weighted, normalised pilot wave. The pilot wave is a diffusing field
  (`np.roll`-based Laplacian) that does not respect the obstacle potential the way
  the local gradient does — it *leaks around* walls. The agent decides by
  Boltzmann sampling over the patch (temperature 1.0). Each observation triggers
  a collapse: local coherence decays and the local pilot wave is sharpened
  (Penrose-style).

The question is falsifiable: if the quantum arm does not beat the classical arm on
survival, crossing, or route completion across a set of scenarios, the null
stands. We build the instrument, run a 400-run ablation, and — because the first
instrument was wrong — we document the forensics that caught it. That
forensics is arguably the most reusable part of the project.

**Why "quantum-inspired" and not "quantum".** The pilot wave is a classical
diffusion field we *label* with the pilot-wave name because its useful property
— global leakage around a barrier that a local gradient cannot see — is the
property we care about. We do not implement amplitudes, superposition, or
measurement in the quantum-mechanical sense. We are bridge-building, and we say
so.

---

## 2. World model and agents

### 2.1 The world

`ToyWorld` is a `size×size` (default 128) grid with a scalar potential field.
Energy sources are (x, y, strength) → attractive `1/r` potential; obstacles are
(x, y, radius) → repulsive potential (`−1e6` inside the core in the tunnel
scenario, i.e. an effective wall). The boundary is a **torus** by default
(wrap-around), which is what makes the "seam shortcut" geometry (§4.2) possible.
A `closed` boundary option (clamp instead of wrap) supports maze-style
geometries. The potential is recomputed on demand; the classical field is
*deterministic and, in static scenarios, static* — a fact that matters for the
Φ result in §4.9.

### 2.2 The quantum-inspired channel

`QuantumInspiredWorld` extends the world with three arrays: a **pilot wave**
(diffusing), a **coherence** field, and a **guidance field**. The pilot wave
integrates a diffusion update (rate `diffusion_rate`, gain 3000) and is
*normalised* before it is mixed in. The guidance field the agent actually
perceives is

```
guidance = potential + quantum_coupling * 3000 * normalize(pilot_wave)
```

so at `quantum_coupling = 0` the perceived field *is* the classical potential
(the honest baseline), and the coupling weight is the single knob that turns the
channel on. Two properties matter, and both follow directly from this:

1. **Global leakage.** The pilot wave is a field that diffuses across the whole
   grid; the −1e6 wall cell is a spike in the *potential*, not a hard boundary in
   the *wave*. So the wave on the far side of a wall is non-zero, and the far
   side becomes *attractive* in the guidance field even where the local potential
   says "wall." This is the route-discovery mechanism.
2. **Staleness under change.** The wave diffuses on a timescale set by
   `diffusion_rate`; when a source *moves*, the wave lags the source. A strong
   coupling glues the agent to a stale wave. This is the coupling-liability
   mechanism (§4.4).

### 2.3 The collapse

Each agent observation calls `collapse_field(x, y, radius=3)`: coherence in a
local disk decays (`collapse_coherence_decay=0.5`) and the local pilot wave is
amplified (`collapse_wave_amplify=2.0`) then renormalised. Operationally this
sharpens the field where the agent has "looked." We treat it as the *controller*
in the sensor/controller split of §4.3, and ablate it directly.

### 2.4 Decision rules

Within a `sense_radius=2` (5×5) patch, the agent computes a value per cell
(quantum arm: potential-based value + a local-coherence bonus; classical arm: the
same value without the bonus). **Quantum** arm samples the move with
Boltzmann sampling (`exp(value/1.0)`). **Classical** arm takes argmax. In v1 the
"classical" arm *also* sampled (a bug, §3.4); in v2 it is a genuine
deterministic argmax. A small `sense_bonus` (0.05) rewards moving toward
higher-coherence cells.

### 2.5 The IIT-inspired Φ metric

Two Φ measures exist. The original `compute_phi` takes a fixed region, deep-copies
the world, forward-simulates a few steps *with no agents*, and returns
`max(0, corr(t0, t1) − corr(boundary, t1))` — a self-predictability-vs-external-
drive score. As we found (§4.9), with no agents in the loop and a region the
agents never occupy, this measures **field** self-organization. The re-scoped
`compute_phi_agents` runs the forward sim **with the whole swarm stepping**
(sense/decide/move/collapse) and probes a (2r+1)² window around each agent's
*current* position, on the guidance field the agent perceives, averaged over
agents. That is an agent–world **coupling** measure. Both are "IIT-inspired" in
that high Φ = internally self-organized rather than externally driven; neither
computes integrated information in the formal IIT sense.

---

## 3. Experimental design

### 3.1 Scenarios

Five built-in scenarios, each a fixed layout (128×128, 20 agents, 500 steps,
corner spawn): **default** (one central source, three obstacle clusters),
**tunnel** (a gapless wall column at x=64 separating the swarm from its only
source), **maze** (hand-crafted wall loops with a goal source at (110,110)),
**single_source** (one source, no obstacles), **moving** (three sources on
circular orbits, sources move every 60 steps). Each scenario is run at coupling
q ∈ {0.0, 0.1, 0.3, 0.5} × collapse {ON, OFF} × 10 seeds = **400 runs**.

### 3.2 Ablations

The two ablation axes are **coupling** (channel strength) and **collapse**
(observation controller ON/OFF). The coupling axis isolates "how much of the
leaked wave the agent trusts"; the collapse axis isolates "does the observation
gate help." The ε-greedy classical control (§4.8) and the n=50 moving sweep
(§4.4) are dedicated follow-up audits, not part of the 400-run grid.

### 3.3 Statistics

Per (scenario, q, collapse): alive rate, survival steps, final energy, barrier
crossings, mean ± std across 10 seeds, with **bootstrap 95% CIs** (40k
resamples). Pairwise quantum-vs-classical comparisons use a **two-sided
Mann-Whitney U** test (α=0.05). The n=50 moving sweep uses the same U test at
each coupling level. We report p-values and CIs, not just means, and we report
*insufficient evidence* as a distinct verdict from *rejected*.

### 3.4 Instrument forensics (v1 → v2) — the reusable part

The first instrument (v1) produced a "classical" baseline with 70–98% survival,
which made the quantum arm look unremarkable. Reproducibility forensics found
the bug: the v1 "classical" arm (q=0.0) was *not* a classical policy — it was the
**quantum sampler in argmax mode**, i.e. it had already been handed the leaked
pilot wave and was just taking the max instead of sampling. It was a quantum
agent wearing a classical costume. The v2 fixes:

1. **True classical baseline:** q=0.0 now perceives *only* the classical
   potential (the guidance field reduces to the potential) and decides by
   deterministic argmax over the 5×5 patch.
2. **Deterministic tie-breaking** (stable argmin with a fixed index order), so a
   "seed" no longer perturbs a policy that should be seed-invariant.
3. **Pilot-wave prewarm** (2000 diffusion steps before agents spawn), so the
   channel is at steady state rather than transient for the first steps.
4. **Collapse ON by default** (the controller is part of the system, not an
   option).
5. **A 2000-step prewarm + fixed RNG order** makes the 400-run dataset
   **byte-identical on re-run** (verified: `data/ablation_results_v2.csv` reproduces
   exactly).

With the calibrated instrument, the true classical survival is **0–45%** (not
70–98%), which is what makes the quantum advantage real and measurable. The
lesson: **an ablation is only as good as its baseline, and a baseline that
shares the treatment's sensing channel is not a baseline.**

### 3.5 Reproducibility

The full 400-run dataset reproduces byte-identically in ~71 s on a 2014
dual-core (i3-4100), CPU-only, no GPU. A GitHub Actions CI runs the unit tests
plus a 15 s headless UI smoke and a 25 s export smoke. All headline numbers are
reproducible from the committed CSVs and the scripts in `examples/`.

---

## 4. Results

### 4.1 Survival: the null is rejected in 4 of 5 scenarios

The null — *quantum-inspired dynamics provide no advantage over classical* — is
rejected (two-sided Mann-Whitney U, α=0.05, n=20 per row) in:

| scenario | classical (q=0) | quantum (best q) | U-test | verdict |
|---|---|---|---|---|
| tunnel | 0% alive, 0 crossings | 100% alive, 20/20 crossings | p≤2.4e-5 | **decisive** |
| maze | 0% alive | 100% alive at every q>0 | p≤1.6e-5 | **decisive** |
| single_source | 20% alive | 100% alive | p≤1.6e-5 | **decisive** |
| default | 45% alive | 90% at q=0.3/0.5 | p≈7.6e-4 | **significant** |
| moving | 45% alive | 68% at q=0.05 (n=50) | p<5e-5 | **significant** (low q only) |

Bootstrap CIs (40k resamples) confirm: tunnel q=0.3 alive 1.000 [1.000, 1.000]
vs classical 0.000 [0.000, 0.000]; default q=0.3 alive 0.900 [0.700, 1.000] vs
0.450 [0.450, 0.450]. The `default` scenario is *insufficient evidence* at
q=0.1 (CI crosses zero) and becomes significant at q=0.3/0.5 — we report that
gradient rather than picking the best cell.

### 4.2 Mechanism: global route discovery, not wall penetration

The tunnel is the cleanest geometry, and a **crossing taxonomy** (first crossing
per agent, classified as wall-jump / wall walk-through / seam-wrap, 10 seeds
each) tells the mechanism:

| arm | wall jumps (63↔65) | wall walk-throughs (via 64) | seam wraps | 1st-crossing latency |
|---|---|---|---|---|
| classical (ε=0) | 0 | 0 | 0 | — |
| ε-greedy 0.1 | 4 | 124 | 20 | 17.4 |
| ε-greedy 0.3 | 15 | 157 | 24 | 5.2 |
| quantum q=0.1 (ε=0) | 0 | 0 | 169 | 2.8 |
| quantum q=0.5 (ε=0) | 0 | 0 | 200 | 2.4 |

**Quantum agents never jump the wall** (0 wall-jumps and 0 walk-throughs across
all 100 quantum agents — Boltzmann sampling assigns ~zero mass to the −1e6 cell).
They **wrap the torus seam** (~2.5 steps after reaching it). The globally leaked
pilot wave makes the far side attractive, and Boltzmann sampling discovers the
route that a local greedy policy *structurally* cannot find: the classical
gradient always points at the wall, never at the seam (x=0/127). A maze route
audit confirms the same mechanism: agents reach the maze goal by **wrapping the
edge (1.00 fraction)**, not through the hand-crafted gaps (0.00 for quantum,
0.02 for ε-classical). The quantum-specific delta is **completeness** (20/20
reach, 100% survival) vs ε-classical (11.4/20 reach) — the quantum channel makes
the exploration exhaustive.

**Retraction (honest):** the v2-era claim "quantum crosses the wall while
classical cannot" was wrong. The defensible claims are: (1) deterministic
local-greedy classical never reaches the far side (structural); (2) stochastic
classical (ε-greedy) *does* find the route, so the tunnel separates
**determinism vs exploration**, not quantum vs classical per se; (3) the quantum
channel shortens first-crossing latency (2.4–2.8 vs 5.2–17.4) and survives ~100%.

### 4.3 Collapse: the difference between survival and death in dynamic worlds

The collapse ablation splits cleanly by geometry:

- **Static geometries (tunnel, single_source):** the pilot-wave channel *alone*
  suffices — full advantage with collapse **OFF** (tunnel collapse-OFF q=0.3:
  100% alive, 20/20 crossings).
- **Trapped/dynamic geometries (default, moving):** quantum with collapse **OFF**
  does *worse than classical* (default 45–48% ≈ baseline; moving 0% vs 45%). The
  advantage appears **only with collapse ON** (default →90%; moving 39–97% at
  low q).

Reading: **the pilot wave is the sensor; the collapse/coherence gate is the
controller.** The controller switches between Boltzmann exploration and greedy
exploitation where local coherence has been measured. In static fields the sensor
alone wins; against moving fields and trap geometries, sensing *without* the
collapse-driven decision switch is actively fatal.

### 4.4 Dynamic fields: a coupling-liability curve (n=50)

The moving scenario (sources orbit, recompute every 60 steps) at **n=50**
(8 coupling levels × 50 seeds, collapse ON) shows a real, **monotone** effect —
a significant quantum advantage at low q that decays to the classical baseline as
q grows:

| q | 0.0 | 0.05 | 0.1 | 0.15 | 0.2 | 0.3 | 0.4 | 0.5 |
|---|---|---|---|---|---|---|---|---|
| alive (n=50) | 0.450 | 0.679 | 0.653 | 0.621 | 0.569 | 0.528 | 0.451 | 0.435 |
| p vs q=0 | — | <5e-5 | 8e-4 | 9e-3 | 0.14 | 0.46 | 0.46 | 0.26 |

Mechanistic read: the classical field updates *instantly* when a source moves;
the pilot wave **lags**. A *weak* channel adds non-local sensing (advantage); a
*strong* channel glues the agent to a stale wave (liability). There is an
**interior optimum at low coupling** for dynamic fields, while the static
scenarios saturate by q=0.1. Operating point: **weak coupling for dynamic fields,
anything above for statics.** (Earlier n=10 runs were underpowered/noise; the
n=50 sweep is the one we cite.)

### 4.5 Anticipation: lag reduction, not foreknowledge

A dedicated lead-horizon metric (H=15 steps; index = mean(d_now − d_lead),
positive = positioned toward where the source is *heading*; `n=10`):

| q | index (mean ± std) | frac steps ahead |
|---|---|---|
| 0.0 | −4.09 ± 0.00 | 0.000 |
| 0.1 | −2.58 ± 2.70 | 0.071 |
| 0.3 | −1.39 ± 2.94 | 0.103 |

**Honest null as an anticipation claim:** no condition shows *positive*
anticipation — every agent, including quantum, sits on average *closer* to the
source's current than future position (the diffusive field carries *past*
information, not future). The quantum channel monotonically **reduces the lag**
(−4.09 → −2.58 → −1.39) and forward positioning appears (frac 0 → 0.07 → 0.10).
The advantage is *reduced tracking error in a shifting field*, not foresight.

### 4.6 Efficiency: directness is traded for reachability

Path efficiency = (spawn→final distance) / (steps taken), on trajectories that
reach a source. **Classical is more direct; quantum reaches more.** Default:
classical 1.0207 (9/10 reach) vs quantum 0.5055 (20/20 reach). Maze: classical
**0.0000** (0/20 reach) vs quantum 0.8940 (20/20). The readme's `path_efficiency
≥ 1.15×` threshold is *not* met — and that is the right result, because the
quantum arm's win is **reachability** (it gets there at all), while the
classical arm's "efficiency" is partly the efficiency of *giving up* (it never
reaches, so its short paths are cheap). We report the tradeoff, not the artifact.

### 4.7 Energy cost

Per-run mean net energy (final − initial): classical always dies at 0 net
(initial 300, harvest 0 → but net is measured over the run). Quantum is
*slightly cheaper per surviving run* in the tunnel (−0.266 vs −0.446) and
*more expensive* in the maze (+0.08 vs +1.54 classical — classical dies at 0
energy; the +1.54 is the mean over the few that harvest). The energy budget
(`examples/energy_budget.py`) exists to keep "quantum is more expensive" an
*measured* claim, not an assumption. The honest summary: the channel is cheap
enough that it does not eat the survival advantage, and the per-run cost is
dominated by *whether the agent survives to harvest*, not by the sensing itself.

### 4.8 Noise robustness: route for the same price (ε-sweep)

A 5-level ε-greedy classical control (7 arms × 10 seeds, tunnel) shows the
tradeoff precisely:

| arm | alive | 1st-crossing latency (median) | wall walk-throughs/agent | seam wraps/agent |
|---|---|---|---|---|
| classical ε=0 | 0.00 | — | 0.0 | 0.0 |
| ε=0.05 | 0.480 | 21.5 | 9.7 | 2.0 |
| ε=0.1 | 0.665 | 13.8 | 12.0 | 2.3 |
| ε=0.2 | 0.790 | 11.2 | 15.8 | 2.2 |
| ε=0.3 | 0.835 | 7.0 | 14.9 | 2.8 |
| **quantum q=0.3 (ε=0)** | **1.000** | **2.0** | **0.0** | **20.0** |
| quantum q=0.3 + ε=0.1 | 1.000 | 2.0 | 0.0 | 20.0 |

Noise *helps* the classical arm cross (monotone 0→48→66.5→79→83.5% alive as ε
rises 0.05→0.3) but at a steep latency cost (quantum median 2.0 vs 7.0–21.5 for
the ε-arms, **3–10×**), and the ε-taxonomy shifts (wall walk-throughs 0→~16/agent;
seam stays flat ~2/agent; true 2-cell jumps 0.3→1.6/agent). **Parity (100% alive)
is never reached** at any ε≤0.3. Adding ε *on top of* the quantum arm is
**benign** (100% alive, 20/20 seam wraps, median latency 2.0) — the quantum
channel is not destroyed by exploration noise. Framing: the quantum channel is
**a route for the same price**, not parity with a noisier classical policy.

### 4.9 Φ re-scope: an agent–world coupling diagnostic

The original `compute_phi` (agent-less forward sim on a fixed central region the
agents never occupy) measured **field** self-organization → ratio **1.000**
across conditions (an instrument artifact, not a finding). We re-scoped it to
`compute_phi_agents`: the forward sim runs **with the swarm stepping**
(sense/decide/move/collapse) and probes a 9×9 window around each agent's current
position, on the guidance field the agent perceives, averaged over agents — a
**coupling** measure. Defined before the number was read (`n=10`, default
scenario, collapse ON):

| config | phi_agent (mean ± std) | min–max |
|---|---|---|
| classical q=0 | 1.0000 ± 0.0000 | 1.0000–1.0000 |
| quantum q=0.3 | 0.8740 ± 0.0125 | 0.8546–0.8883 |

The readme threshold `quantum_Φ > 1.5 × classical_Φ` is **NOT MET** (ratio
0.874) and the **direction is reversed** (quantum lower). Moving scenario:
classical 1.0000, quantum 0.4630 ± 0.1965 — same direction. The direction is
consistent across **three** probe designs (field-only 1.000, swarm-centroid
quantum-lower, agent-local quantum-lower).

**Instrument property (documented, not a finding):** classical is pinned at
1.0000 in every scenario because its perceived field is the deterministic
potential, locally *static* over the 5-step horizon → t0≡t1 → self-predictability
1.0 (a ceiling). Quantum is <1.0 because its perceived field adds the diffusive
pilot-wave channel, which is *evolving* and therefore less self-predictable over
5 steps. So the *magnitude* (0.874) is partly a ceiling effect; the *direction*
is the robust signal.

**Decision:** we **formally retract** the specific "quantum Φ is 1.5× classical
Φ" threshold as stated, and **retain** the re-scoped Φ as a clean agent–world-
coupling diagnostic. The paper carries this as an honest negative with a fixed
instrument and a consistent direction — not a silent null.

---

## 5. Applications

The practical value of the result is not the word "quantum" in the title — it is
that the finding **replaces a fantasy with a mechanism**, and hands you the
operating map. A "clean win" ("quantum is 1.5× better, ship it") would have been
*less* useful: it would not tell you when the channel breaks (it does, in the
dynamic/moving case at high coupling). "Route discovery, not wall penetration"
is *buildable* — a specific architecture you bolt onto an existing local policy
that measurably reaches more — and the ablation tells you exactly how to deploy
it (weak coupling, on the gate). Ranked most → least impactful, here is what this
everything enables, and the deliverable each one becomes.

### 5.1 A drop-in exploration channel for local-greedy navigation agents

*Most impactful — directly productizable.* Every agent that gets stuck in local
minima today — warehouse AMRs, game NPCs, multi-agent swarms, network routing,
protein/sequence search, any gradient-descent-style policy — can add this stack
*on top of the existing greedy policy*, not instead of it: a cheap
**globally-leaked sensing channel** (here, pilot-wave diffusion) + **Boltzmann
sampling** + a **decision gate**, with the greedy policy as the fallback. The
finding tells you the correct operating point — *weak coupling, always on the
gate* — so it is shipped without the v1 "full-strength" bug.
**Deliverable:** a library / agent mode ("greedy policy + leaky-sensor
exploration") whose spec *is* the ablation CSV; a before/after on any local-greedy
nav stack shows the reachability gain (maze: 0/20 → 20/20 arrivals).

### 5.2 A reusable "is your baseline really a baseline?" eval method

*The paper's most reusable piece.* The instrument forensics caught a
control that shared the treatment's sensing channel (the v1 "classical" arm was
the quantum sampler in argmax mode). The general rule — *an ablation is only as
good as its baseline; a baseline that shares the treatment's channel is not a
baseline* — applies to any A/B or feature-ablation claim in ML. **Deliverable:**
a test/audit harness + checklist (deterministic baseline, deterministic
tie-breaking, prewarm, fixed RNG order) that catches "the control is wearing the
treatment's costume," with the v1→v2 forensics as the worked example.

### 5.3 A sensor-vs-controller decomposition rule

The cleanest causal statement in the project: **the leaky channel is the sensor;
the collapse is the controller; they are not interchangeable** — sensing without
the collapse-driven decision switch is *worse than classical* in dynamic/trapped
worlds (moving: 0% vs 45%). This is a design rule for any sensing/planning split
(robot perception+control, ranking+recsys, monitor+reactor): *when you add a
new sensing channel, co-design its decision gate, or it backfires.*
**Deliverable:** a one-page design pattern with the moving-scenario numbers as
the proof.

### 5.4 "Completeness, not directness" as a product axis

The path-efficiency result (quantum ratio 0.495 < 1.15, i.e. *worse* on
directness) reframes the "quantum is less efficient" objection as *"less
direct, but actually arrives"* (maze: classical 0/20 at any efficiency, quantum
20/20). For search/retrieval/recommender products, "recall over precision,
exhaustive over fast" is a real, defensible positioning axis.
**Deliverable:** copy + a metric ("reachability @ equal cost") for any product
where missing the reachable target matters more than route length.

### 5.5 A coupling auto-tuning rule

The n=50 moving sweep is a monotone *"weak coupling wins, strong coupling is a
liability"* curve (a moving target → the sensor lags). **Deliverable:** a
controller that **down-regulates coupling in dynamic fields** — a concrete,
measurable policy rather than a guess at a fixed hyperparameter.

### 5.6 Honest-nulls as a "when NOT to use" boundary

The ε-sweep (noise alone reaches 83.5%, never 100%) and the closed-boundary
audit (remove the seam, *nobody* tunnels) give clear negative boundaries: no
impenetrable-barrier penetration; plain stochastic noise is a cheap *partial*
substitute. **Deliverable:** a one-page applicability boundary — *use when*
occluded/contractible routes exist; *do not expect* wall-penetration or shorter
paths. This stops a team from over-buying the "quantum" framing.

### 5.7 A teaching / demo artifact

The interactive demo (scrubbable timeline, `--shot` headless primitives, A/B
field + Φ overlay) is a *visual proof of the mechanism* — you can watch the
leaked field light up the far side of a wall ~2 steps before the agent goes.
**Deliverable:** a talk/teaching demo for "non-local route discovery without a
global map."

### 5.8 A reproducible, CPU-only benchmark

The whole thing is a tiny, **byte-reproducible** benchmark (128×128, 20 agents,
one i3, ~71 s for 400 runs) for the question *"does global sensing beat local
greedy here?"* **Deliverable:** a benchmark harness others can plug new
scenarios or policies into.

---

## 6. Discussion

Three claims survive the instrument forensics and the ablations:

1. **A globally-leaked sensing channel lets a swarm reach things a local greedy
   policy cannot structurally reach.** The mechanism is route discovery (wrap the
   seam / wrap the edge), not wall penetration, and it is robust across the
   tunnel and the maze. The quantum-specific delta is *completeness* (exhaustive
   exploration), because Boltzmann sampling over the leaked field assigns non-zero
   mass to routes the local gradient never points at.

2. **The channel is a sensor; the collapse is the controller.** The collapse
   ablation is the cleanest causal statement in the project: in dynamic/trapped
   geometries, sensing without the collapse-driven decision switch is *worse than
   classical*. The two are not interchangeable.

3. **The advantage has a known, cheap cost: coupling must be weak in dynamic
   fields, and directness is traded for reachability.** The n=50 moving sweep is
   the most honest number in the report (a monotone liability curve, not a
   "quantum wins everywhere" claim), and the path-efficiency result reframes the
   "quantum is less efficient" finding as "quantum is less direct but actually
   arrives."

What we *retract* and what we *keep* is explicit: the wall-jumping mechanism
(retracted → seam/edge route discovery), the "quantum Φ is 1.5×" threshold
(retracted → re-scoped coupling diagnostic), and the v1 baseline (replaced by the
calibrated deterministic classical). What we keep: the 4/5 null rejection, the
sensor/controller split, and the coupling-liability curve.

**Framing for honesty.** This is a *negative-tilted positive*: a real,
mechanism-explained advantage in 4/5 scenarios, a monotone cost curve in the
fifth, and two honest retractions. We would rather report "advantage in 4/5 with
a known cost and a documented retraction" than "advantage everywhere." The
instrument forensics (§3.4) is the piece we expect to be most reusable: a
baseline that shares the treatment's sensing channel is not a baseline.

---

## 7. Limitations

- **One world model, one grid, 20 agents, 500 steps.** Results are for *this*
  geometry family and scale. Generalization to larger/multi-scale worlds is
  future work, not a claim.
- **The "quantum" is inspired, not quantum.** No amplitudes, superposition, or
  formal measurement; the pilot wave is a classical diffusion field we label with
  the name because of its leakage property.
- **Φ is IIT-*inspired*, not integrated information.** Two proxy measures
  (self-predictability vs external drive); the re-scoped one is a coupling
  diagnostic, not a Φ computation in the IIT sense.
- **n=10 for most of the 400-run grid** (n=50 only for the moving sweep). Some
  `default`-scenario contrasts are *insufficient evidence* at q=0.1; we report
  the gradient, not a point win.
- **Static-field Φ ceiling.** Classical Φ is pinned at 1.0 by the static
  potential; the magnitude of the quantum Φ dip is partly a ceiling effect (the
  direction is the robust part).
- **Single seed-order / RNG** for reproducibility; we did not re-derive the
  dataset under a different RNG (we re-ran it under the same one, byte-identical).

---

## 8. Conclusion

A weakly quantum-inspired sensing channel — a pilot wave that leaks around
obstacles, read through Boltzmann sampling, gated by a Penrose-style collapse —
gives a swarm of grid agents a real, mechanism-explained navigation advantage
over a deterministic local-greedy classical baseline in four of five scenarios
(tunnel, maze, single-source, default) and a coupling-dependent advantage in the
fifth (moving). The mechanism is **global route discovery via the leaked sensor**,
not wall penetration; the controller (collapse) is what makes sensing useful in
dynamic fields; and the cost is a **weak-coupling operating point in dynamic
fields** plus **directness traded for reachability**. After instrument forensics
caught a costume-wearing classical baseline, the honest report is a 4/5
null-rejection with a known mechanism, a known cost, a monotone liability curve,
and two explicit retractions (wall-jumping; the 1.5× Φ threshold). That is, in
our view, a more useful result than a clean win would have been.

---

## Data and code availability

- **Repository:** <https://github.com/BrutchsamaJeanLouis/quantum-inspired-sensor-navigation> (world model, agents, Φ, ablation harness, all scripts, tests, and this report).
- **Paper DOI (Zenodo):** <https://doi.org/10.5281/zenodo.22964117> (`10.5281/zenodo.22964117`)
- **Dataset** (all under `data/`): `ablation_results_v2.csv` (400 runs,
  byte-reproducible), `q_sweep_moving_n50.csv`, `epsilon_sweep_tunnel.csv`,
  `phi_rescope.csv`, `maze_route_audit.csv`, `path_efficiency_*.csv`,
  `energy_budget.csv`, `moving_anticipation_n10.csv`, `phi_audit.csv`,
  `tunnel_closed_audit.csv`.
- Scripts: `examples/` (one script per table above); `src/core/` (world, agents,
  coherence, experiments).
- Reproduce: `pip install -r requirements.txt && python examples/ablation_v2.py`,
  then `python examples/analyze_results.py`. Unit tests: `pytest tests -q`
  (120 passed). CI: `.github/workflows/ci.yml`.
- All headline numbers trace to a committed CSV and a named script; the
  re-scoped Φ audit is `python examples/phi_rescope.py`.
