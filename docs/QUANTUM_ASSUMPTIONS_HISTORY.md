# Quantum-Assumptions History

> What this document is: a forensic history of **the quantum calculation** in this
> repository — the pilot-wave / collapse / Φ machinery — from the first commit
> that put a "quantum" line of code in the tree, to the current `QuantumInspiredWorld`.
> For every era it records (a) what the calculation assumed, (b) the concrete code /
> math, (c) what evidence forced each change, and (d) what is still load-bearing
> today. This is the companion to `PAPER.md` §3.4 (instrument forensics) and
> `RESULTS.md` §4b–§4i (mechanism + honest nulls).
>
> Method: reconstructed from `git log`/`git show`/`git diff` across the 15-commit
> history, the committed CSVs, and the results docs. Commit hashes and dates are
> taken from `git log --all`; formulas are quoted from the tagged revision.

---

## 0. TL;DR — the two real turning points

Everything else is refinement. Two commits changed *what the quantum calculation
means*:

1. **v1 → v2 (`5928b5c`, 2026-08-20)** — the *instrument* was wrong, not the
   physics. The v1 "classical baseline" (coupling `q = 0`) was secretly the
   quantum agent in argmax mode (it had already been handed the leaked pilot wave
   and was just taking the max instead of sampling). It survived 70–98 %, so the
   quantum arm looked unremarkable. v2 made `q = 0` a *true* classical baseline
   (perceives only the classical potential, deterministic argmax, prewarmed wave),
   and the honest classical survival dropped to **0–45 %** — which is what makes
   the quantum advantage real and measurable.
2. **Φ re-scope (`b82d2b1`, 2026-09-21, RESULTS §4i)** — the success threshold
   "quantum Φ > 1.5 × classical Φ" was *wired but never met* (ratio ≈ 1.000 on the
   field-only probe; **0.874, direction reversed** on the re-scoped
   agent-in-the-loop probe). The specific 1.5× claim is **formally retracted**;
   Φ is retained as an agent–world-coupling *diagnostic*, not a gap metric.

The pilot-wave-as-sensor + collapse-as-controller model survived both. What got
retired: (a) "the v1 classical arm was a baseline," and (b) "quantum raises local
self-organization Φ to 1.5× classical."

---

## 1. Commit timeline (quantum-relevant)

| commit | date | quantum-calculation significance |
|---|---|---|
| `cc80b63` | 2025-11-09 | **Phase 1.** Classical baseline only. `ToyWorld` (155 ln): `1/r` energy potential, repulsive obstacles, torus, gradient. No quantum yet — but it defines the field the quantum channel will later modulate. |
| `9d5ed27` / `076103c` / `08428ae` | 2025-11-09 | aider setup / project context. No calc. |
| `616d613` | 2025-11-10 | **Phase 2 / v1** (aider). Pilot wave, coherence, `update_pilot_wave` (Laplacian diffusion), `collapse_field` (Penrose-style) added **directly into `ToyWorld`** in `toy_world.py`. This is the first "quantum" code. |
| `da89a89` | 2025-11-10 | v1 follow-up: dependency + 3-line `toy_world.py` touch. |
| — | (Nov 2025 → Aug 2026) | Dormancy. v1 sat un-audited; its "classical" number (70–98 %) was taken at face value. |
| `5928b5c` | 2026-08-20 | **v2.** Quantum dynamics **extracted from `ToyWorld` into a new `QuantumInspiredWorld(ToyWorld)`** (`src/core/quantum_world.py`, 185 ln) + `agents.py` (AgentSwarm), `coherence.py` (Φ), `experiments.py` (ablation harness). Guidance field **recalibrated** (gain + normalization). The v1→v2 forensics. 400-run ablation; null rejected in 4/5. |
| `a4d14b3` | 2026-08-20 | **Retraction (v2-era).** "Moving-scenario fine q-sweep retracts v2 coupling-liability claim": the n=10 slope (97%@0.1→39%@0.5) was partly seed luck. |
| `49d90e6` | 2026-08-20 | **n=50 moving sweep + ε-greedy classical control.** Added `classical_epsilon` to `QuantumInspiredWorld`. Confirms a *monotone* low-q advantage → baseline decay (`q_sweep_moving_n50.csv`). |
| `c0abc3c` | 2026-08-20 | **Crossing taxonomy.** "Quantum tunnel = seam shortcut, not wall jump." Adds crossing classifier (`experiments.py`). |
| `2971739` | 2026-09-21 | Closed boundary (`torus` flag added to `QuantumInspiredWorld`), `y_traj`, path-efficiency, bootstrap CIs, CI, audits. `tunnel_closed_audit`: without the seam, *nobody* tunnels → mechanism = route discovery, not wall penetration. |
| `b82d2b1` | 2026-09-21 | **Φ re-scope (P7 → §4i).** `compute_phi_agents` (agent-in-the-loop, agent-localized Φ) added behind `ExperimentConfig.phi_agent_in_loop` (default OFF so the 400-run v2 CSV is byte-identical). 1.5× threshold formally retracted. |
| `a597baa` | 2026-09-22 | Paper (`docs/PAPER.md`, 513 ln) + demo video. No calc change; freezes the narrative. |
| `77003ed` | 2026-09-25 | **LLM tick controls** (`TimelinePlayer`, `--shot`/`--replay`, slider). No quantum-calc change — but it *depends on* the determinism v2 established (fixed RNG order, prewarm), which is what makes `seek(n) ≡ live tick n` exact. |

---

## 2. Era-by-era detail

### Era 0 — Phase 1: the classical field that everything is measured against
`cc80b63` (2025-11-09), `src/core/toy_world.py` (155 ln).

- `grid` = a 2-D NumPy potential: energy sources are attractive `1/r`, obstacles
  are repulsive, edges wrap (torus). `get_gradient()` gives the local slope.
- **Assumption that still stands:** there is one scalar "value of a cell" that a
  policy can read; a *local greedy* policy that follows `grid` is the honest
  null. This is the field the quantum channel later *adds to*.
- No quantum, no agents. Just the substrate.

### Era 1 — Phase 2 / v1: the naive "quantum-inspired" layer (aider)
`616d613` + `da89a89` (2025-11-10). The quantum machinery was written **into
`ToyWorld` itself** (not a subclass), reflecting the phase-2 intent that "the world
is quantum-inspired by default."

The v1 calculation, quoted from `616d613:src/core/toy_world.py`:

```python
# guidance field — line 145
return self.grid + 0.3 * self.pilot_wave          # "Tunable coupling"

# update_pilot_wave(dt=0.1)
laplacian = (roll(+1,axis0)+roll(-1,axis0)+roll(+1,axis1)+roll(-1,axis1) - 4*pilot_wave)
self.pilot_wave += dt * laplacian
for ex, ey, strength in self.energy_sources:
    self.pilot_wave[ex, ey] += strength * dt     # energy "feeds" the wave
# collapse_field(x,y,radius): coherence *= decay; pilot_wave *= amplify (Penrose-style)
```

**What v1 assumed:**
- The pilot wave is a non-local guidance field built by *Laplacian diffusion* from
  the energy sources; adding it to the classical potential makes the field
  "quantum-inspired."
- Coupling was a **hard-coded 0.3** and the pilot wave was added **raw** — no
  normalization, no gain, no dissipation, no clip, no prewarm. Its magnitude was
  whatever the transient diffusion happened to be.
- **The fatal implicit assumption (the v1 bug):** a "classical baseline" is the
  same code path with the coupling turned off. But because the field, the patch
  reader, and the *decision machinery* were all already quantum-shaped, the
  `q = 0` arm was still a **quantum agent in argmax mode** — it had been handed
  the leaked pilot wave and was just taking the max instead of sampling. It was a
  quantum agent wearing a classical costume. Consequence: the v1 "classical"
  baseline survived **70–98 %**, so the quantum arm (also high) looked
  unremarkable. *A baseline that shares the treatment's sensing channel is not a
  baseline.*

### Era 2 — v2: the instrument is the finding (`5928b5c`, 2026-08-20)
The quantum dynamics were **extracted from `ToyWorld` into `QuantumInspiredWorld`**
(`src/core/quantum_world.py`), and a true classical baseline was made
structurally possible. The guidance field was **recalibrated** so the quantum
channel is comparable in magnitude to the classical field *and* zero-able:

```python
# get_guidance_field() — current form, unchanged since v2
pmax = float(self.pilot_wave.max())
normalized = self.pilot_wave / pmax if pmax > 1e-8 else self.pilot_wave
return self.grid + self.quantum_coupling * self.pilot_wave_gain * normalized
#                                        coupling(0.3)  gain(3000)   max-normalized
```

and `update_pilot_wave` gained the terms v1 lacked:

```python
self.pilot_wave += dt * laplacian
self.pilot_wave *= self.pilot_wave_dissipation        # 0.9999 (v2) — stable, non-exploding
for ex, ey, strength in self.energy_sources:
    self.pilot_wave[ex, ey] += strength * dt * 0.01   # v2 — 100× weaker feed
self.pilot_wave = np.clip(self.pilot_wave, -100.0, 100.0)   # v2 — numeric guard
```

The five v2 fixes (PAPER §3.4, `RESULTS.md` §1–2):

1. **True classical baseline** — `q = 0.0` now perceives *only* the classical
   potential (the guidance field reduces to `grid`) and decides by deterministic
   argmax over the 5×5 patch.
2. **Deterministic tie-breaking** — stable argmin with a fixed index order, so a
   "seed" no longer perturbs a policy that should be seed-invariant.
3. **Pilot-wave prewarm** — 2000 diffusion steps before agents spawn, so the
   channel is at steady state, not transient.
4. **Collapse ON by default** — the controller is part of the system, not an
   option.
5. **Fixed RNG order + prewarm** → the 400-run `ablation_results_v2.csv` is
   **byte-identical on re-run** (~71 s, 2014 dual-core).

**Evidence that forced this:** reproducibility forensics on the ablation. The
honest classical survival is **0–45 %**, not 70–98 %. With the calibrated
instrument the null ("quantum gives no advantage over classical") is **rejected in
4 of 5 scenarios** (Mann-Whitney U, α=0.05): tunnel 0%→100 %, maze 0%→100 %,
single_source 20%→100 %, default 45%→90 % (q=0.3/0.5); the *moving* scenario is
coupling-dependent (§4).

**What changed as an assumption:** `q = 0` went from "a quantum sampler with the
knob off" to "a genuinely local-greedy classical policy." This is the load-bearing
correction of the whole project.

### Era 3 — Robustness & mechanism (2026-08-20 → 2026-09-21)
After v2, the calc was *not* re-derived; it was stress-tested and the mechanism was
pinned down. Each sub-era added a control, not a formula change:

- **`a4d14b3` — coupling-liability retraction.** The n=10 moving sweep showed a
  slope (97%@0.1 → 39%@0.5) that was partly seed luck; the fine n=10 sweep was
  underpowered. *Retraction recorded, not deleted.*
- **`49d90e6` — n=50 moving sweep + ε-greedy control.** `classical_epsilon` added
  to `QuantumInspiredWorld` (a *stochastic classical* baseline). `q_sweep_moving_n50.csv`
  (8 levels × 50 seeds) **confirms a real monotone effect**: significant quantum
  advantage at low q (0.05–0.15) decaying to baseline by q≥0.2. Reading: the
  classical field updates instantly when a source moves; the pilot wave lags. A
  *weak* channel = non-local sensing (advantage); a *strong* channel = glued to a
  stale wave (liability).
- **`c0abc3c` — crossing taxonomy.** The x=64 wall column on the torus is a
  *contractible loop*; the x=0/127 seam is the way around it. Per-agent
  first-crossing taxonomy (tunnel): **all** quantum crossings are ~2.5-step-latency
  **seam wraps, none through the wall.** The leaked pilot wave makes the far side
  attractive; Boltzmann sampling finds the route.
- **`2971739` — closed boundary + audits.** `torus` flag added
  (`False` = clamped edges, no seam). `tunnel_closed_audit.csv`: with the seam
  removed, **nobody tunnels** — quantum q=0.5 crosses 0 and dies (0 % alive);
  only coarse ε-noise walk-throughs cross (25 %). The final honest claim: *no
  channel penetrates an impenetrable barrier; the quantum channel's value is
  exhaustive non-local exploration of routes that exist but are locally
  invisible.*
- **`2971739` — ε-sweep (`epsilon_sweep_tunnel.csv`).** The full curve of what
  decision *noise alone* buys: classical alive 0→48→66.5→79→83.5 % as
  ε 0→0.05→0.1→0.2→0.3, but never reaches the quantum arm (100 %, 20/20, median
  latency 2.2 steps vs 11–28). *The same exploration you pay for as decision noise
  is replaced by a non-local sensor that finds the route deterministically, 5–12×
  faster.*

**Honest nulls recorded here (not tuned away):**
- **§4f path efficiency — NOT MET** (quantum ratio 0.495 < 1.15 threshold in
  default; 0/20 vs 20/20 in maze). The quantum channel is *worse* on directness
  (Boltzmann meanders ~2×) and its value is **reachability, not directness**.
- **§5 dead-end escapes are quantum-only** (moving: 194/132/77 escapes at
  q=0.1/0.3/0.5; 0 classical).

### Era 4 — Φ re-scope (`b82d2b1`, 2026-09-21, RESULTS §4i)
The IIT-inspired Φ is the metric most tied to a *quantum assumption* ("quantum
dynamics raise self-organization"), so it took the biggest re-scope.

- **§4e — the original probe was a field self-organizer, not a coupling.**
  `compute_phi` ran an *agent-less* forward sim on a fixed central region the
  agents never occupy. `phi_audit.csv`: classical 0.9894 vs quantum 0.9893 —
  ratio **1.000**. The readme threshold `quantum_phi > 1.5 × classical_phi` was
  **wired, NOT met.**
- **§4i — re-scoped to the metric the threshold actually meant.** New
  `compute_phi_agents` (in `src/core/coherence.py`, behind
  `ExperimentConfig.phi_agent_in_loop`, **default OFF** so the 400-run v2 CSV is
  byte-identical): for each agent, probe a (2·r+1)² window (r=4) around its
  *current* position, forward-simulate 5 steps **with the whole swarm stepping**
  (Penrose observation is part of the co-dynamics), and compute
  `max(0, corr(t0_R,t1_R) − corr(boundary_t0_R,t1_R))` on the *guidance field the
  agent perceives*, averaged over agents. Defined before the number was read.
  `phi_rescope.csv`: classical **1.0000**, quantum **0.8740** (moving: 0.4630).
- **The 1.5× claim is formally retracted; direction is reversed** (quantum ≤
  classical), consistent across **three** independent probe designs (field-only
  central = 1.000, swarm-centroid = quantum lower, agent-localized in-the-loop =
  quantum lower).
- **Instrument property (documented, not a finding):** classical is pinned at
  exactly 1.0000 because its perceived field is the deterministic potential,
  locally *static* over the 5-step horizon → `t0_R ≡ t1_R` → self-predictability
  1.0. Quantum is < 1.0 because the guidance field it perceives adds the
  **diffusive pilot-wave channel** (gain 3000 · normalize(pilot)), which is
  evolving and therefore less self-predictable. The *magnitude* (0.874) is partly
  a ceiling effect; the *direction* is the robust signal.
- **Assumption retired:** "quantum raises local self-organization Φ to 1.5×
  classical." **Retained:** Φ as a clean agent–world-coupling *diagnostic*.

### Era 5 — Paper + demo (`a597baa`, 2026-09-22)
`docs/PAPER.md` (513 ln) + `examples/make_demo_video.py`. No calc change; freezes
the narrative (title: *"Weakly Quantum-Inspired Navigation: A Pilot-Wave World
Model That Finds Routes a Local Greedy Policy Cannot"*).

### Era 6 — LLM tick controls (`77003ed`, 2026-09-25)
`src/core/timeline.py` (`TimelinePlayer`), `--shot`/`--replay`, the visualizer
tick slider. **No quantum-calc change**, but it *consumes* the determinism v2
established: because the RNG order, prewarm, and seed are fixed, `seek(n) ≡
live tick n` is *exact* (rewind = re-seed + re-step, bit-identical — see
`examples/verify_rewind_consistency.py`, REWIND-CONSISTENCY PASS across 28
scenario/seed/tick triples). This is a downstream *consequence* of the v2
calibration, not a new assumption.

---

## 3. Assumption ledger

| # | Assumption | introduced | evidence that killed / kept it | status |
|---|---|---|---|---|
| A1 | A scalar per-cell value + local-greedy argmax is the honest null | Phase 1 (`cc80b63`) | — (still the baseline) | **standing** |
| A2 | Pilot wave = Laplacian diffusion from energy sources, added raw to the field | v1 (`616d613`) | Kept the *diffusion-as-sensor* idea; killed the *raw addition* (uncalibrated magnitude) | partly retired |
| A3 | "Classical baseline" = same code path with coupling off | v1 (`616d613`) | **Killed** by forensics: the `q=0` arm was the quantum sampler in argmax mode (70–98 %). v2 `5928b5c`. | **retired** (replaced by true classical argmax) |
| A4 | The quantum channel is comparable in magnitude to the classical field *and* zero-able | v2 (`5928b5c`) | `gain·normalize(pilot)` makes `q=0` reduce exactly to the classical potential; 0%→100% contrast appears | **standing** |
| A5 | Collapse (Penrose-style) is the decision *controller* (Boltzmann↔greedy switch), not an option | v2 (`5928b5c`), collapse-ON default | Collapse ablation: OFF→worse-than-classical in trapped/dynamic worlds (moving 0%); ON→advantage | **standing** |
| A6 | Quantum advantage is *sampling* (Boltzmann noise) — "coupling-liability" | v2 n=10 (`5928b5c`) | **Retracted** at n=50 (`49d90e6`): the n=10 slope was seed luck; the real effect is a monotone low-q advantage, mechanism = route discovery, not noise | **retired** (refined to "route discovery") |
| A7 | "Quantum crosses the wall" | v2-era framing | **Retracted** (`c0abc3c` + `2971739`): crossings are seam wraps; with the seam removed nobody tunnels (`tunnel_closed_audit`) | **retired** (→ "route discovery around a contractible barrier") |
| A8 | Decision noise (ε) alone can match the quantum arm | ε-sweep (`2971739`) | **Not met**: ε=0.3 → 83.5 % < 100 %, latency 5–12× worse, crossings are walk-throughs not routes (`epsilon_sweep_tunnel.csv`) | **rejected** (honest null) |
| A9 | Path efficiency: quantum finds *shorter* routes | efficiency audit (`2971739`) | **Not met** (ratio 0.495 < 1.15): quantum is *worse* on directness; value = reachability (`path_efficiency_*.csv`) | **rejected** (honest null) |
| A10 | "Quantum Φ > 1.5 × classical Φ" (readme success metric) | Φ phase 3 → re-scoped (`b82d2b1`) | **Retracted**: field-only ratio 1.000 (§4e); agent-in-the-loop ratio 0.874, direction reversed (§4i), consistent across 3 probe designs | **retired** (Φ kept as coupling diagnostic) |
| A11 | Rewind/seek to tick N reproduces live tick N exactly | LLM controls (`77003ed`) | **Holds**: fixed RNG order + prewarm ⇒ `seek(N)≡step(1)×N≡play-then-home-then-scrub`, bit-identical field+agents+trails (REWIND-CONSISTENCY PASS, 28 triples) | **standing** (consequence of A4) |

---

## 4. The central instrument bug (the reusable lesson)

The single most important assumption error, and the reason the v2 commit exists:

> **The v1 "classical" arm (q=0) was not a classical policy. It was the quantum
> sampler in argmax mode — it had already been handed the leaked pilot wave and
> was just taking the max instead of sampling.** It survived 70–98 %, so the
> quantum arm looked unremarkable.

The fix was *not* to tune the quantum channel harder; it was to make the baseline
**structurally** classical (perceives only the classical potential, deterministic
argmax, prewarmed wave, collapse ON, fixed RNG order). After the fix the honest
classical number is 0–45 % and the null is rejected in 4/5. The general lesson,
verbatim from PAPER §3.4:

> *An ablation is only as good as its baseline, and a baseline that shares the
> treatment's sensing channel is not a baseline.*

---

## 5. The quantum calculation as of HEAD (`77003ed`)

`src/core/quantum_world.py`, `QuantumInspiredWorld(ToyWorld)`. The exact, stable
formulas:

```python
# pilot-wave update (diffusion-as-sensor) — v2 form, unchanged since 5928b5c
laplacian = (roll(+1,0)+roll(-1,0)+roll(+1,1)+roll(-1,1) - 4*pilot_wave)
pilot_wave += dt * laplacian
pilot_wave *= pilot_wave_dissipation            # 0.9999
for ex, ey, s in energy_sources:
    pilot_wave[ex, ey] += s * dt * 0.01
pilot_wave = clip(pilot_wave, -100, 100)

# collapse (Penrose-style observation) — the controller
#   coherence[x,y] *= collapse_coherence_decay   (0.9)
#   pilot_wave[x,y] *= collapse_wave_amplify     (1.1)   over a radius-3 disc

# combined guidance field (sensor on top of the classical field)
guidance = grid + quantum_coupling * 3000.0 * normalize(pilot_wave)
#   q=0  ⇒ guidance == grid  (true classical baseline)
```

Constants (instrument, identical at every coupling level — modeling choices, not
findings): `pilot_wave_gain=3000.0`, `diffusion_rate=0.1` (dt 0.2 in the ablation),
`pilot_wave_dissipation=0.9999`, prewarm **2000** steps, `quantum_coupling` swept
over 0.0–0.5. The *existence* of the 0%→100% contrast is **not** instrument
dependent (the classical impossibility is structural, the −1e6 wall); its
*absolute magnitude* is.

---

## 6. What is stable vs what is instrument-dependent (honest)

- **Stable / load-bearing:** A1 (local-greedy null), A4 (calibrated, zero-able
  quantum channel), A5 (collapse as controller), A7-refined (route discovery around
  a contractible barrier, not wall penetration), A11 (determinism).
- **Instrument-dependent (report the existence, not the size):** the 0%→100 %
  gap's magnitude, the low-q moving optimum's exact location, all Φ magnitudes.
- **Formally retired (kept as honest nulls, not deleted):** A3 (v1 classical
  costume), A6 (coupling-liability), A8 (ε parity), A9 (path efficiency), A10
  (1.5× Φ).

This document is the "assumptions" half of the history; the *numbers* half lives
in `RESULTS.md` (tables trace to the committed CSVs) and `PAPER.md`.
