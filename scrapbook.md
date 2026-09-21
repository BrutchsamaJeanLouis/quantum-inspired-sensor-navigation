# QIWM Scrapbook

## 2026-09-21 (2): PO session — Phi re-scope (P7) → §4i, formally retracted

- `compute_phi_agents` (src/core/coherence.py): re-scoped agent-in-the-loop,
  agent-localised Φ. Per agent, a (2·r+1)² window (r=4) around its *current*
  position; forward-sim `steps`=5 WITH the whole swarm stepping
  (sense/decide/move/collapse); max(0, corr(t0_R,t1_R) − corr(boundary_t0_R,t1_R))
  on the guidance field the agent perceives, averaged over agents. Deep-copies
  (world, agents). Wired behind `ExperimentConfig.phi_agent_in_loop` (default OFF
  → 400-run v2 dataset byte-identical). 5 new unit tests; suite 102→107 green.
- `examples/phi_rescope.py` → `phi_rescope.csv` (default, n=10, 500 steps,
  collapse ON). **RESULT: classical pinned 1.0000 (±0.0000); quantum 0.8740
  ±0.0125 (0.8546–0.8883). Ratio 0.874 — NOT MET vs 1.5×, DIRECTION REVERSED
  (quantum lower).** Moving scenario: classical 1.0000, quantum 0.4630±0.1965
  — same direction. Direction consistent across 3 probe designs (field-only
  1.000 §4e; swarm-centroid quantum-lower §4e; agent-local quantum-lower §4i).
- Instrument property (documented, not a finding): classical=1.0000 in every
  scenario because its perceived field is the deterministic potential, locally
  STATIC over the 5-step horizon → t0_R≡t1_R → self-predictability 1.0 (ceiling).
  Quantum <1.0 because the perceived guidance field adds the diffusive pilot-wave
  channel (gain 3000·normalize(pilot)), evolving → less self-predictable over 5
  steps. Magnitude partly a ceiling effect; DIRECTION is the robust signal.
- PO decision: **formally retract the "quantum Φ is 1.5× classical" threshold as
  stated; retain re-scoped Φ as a clean agent–world-coupling diagnostic**
  (instrumentation improvement — the original measured field self-organization,
  1.000, not coupling). Documented HONESTLY in RESULTS.md §4i + readme
  (threshold status + repro row). Paper carries it as an honest negative with a
  fixed instrument + consistent direction, not a silent null.

## 2026-09-21: PO session — ε-sweep curve (§4h) + tunnel demo GIFs

- `examples/epsilon_sweep_tunnel.py` → `epsilon_sweep_tunnel.csv`
  (7 arms × 10 seeds, tunnel/torus/v2 instrument): alive 0 → 48.0±7.8 →
  66.5±11.6 → 79.0±12.6 → 83.5±12.3 (ε→0.3). Parity with quantum
  (100±0, 20/20) NOT reached; latency quantum med 2.2 vs 11–28 ε-arms
  (5–12×); ε-taxonomy stable (77–84% wall walk-throughs, seam flat
  ~2/run, 2-cell jumps 0.3→1.6/run); interaction arm q=0.3/ε=0.1 benign
  (100%, 20/20 seam, med 2.7, overlapping seed ranges). Paper framing:
  the tradeoff is *route for the same price*, not parity. RESULTS.md
  §4h + §4b pointer.
- `examples/tunnel_demo_gif.py`: headless (SDL dummy) WorldVisualizer
  frame capture → animated GIF + optional PNG frames; configs quantum
  (q=0.3) / classical (q=0.0), v2 constants, 20 agents corner spawn,
  prewarm 2000. Final-frame check: quantum 20/20 alive @750 steps vs
  classical 0/20 — the A/B centerpiece. Artifacts:
  tunnel_demo_{quantum,classical}.gif (150f @12fps). pillow →
  requirements.
- **Bootstrap 95% CIs (P7 closed):** analyze_results.py gains
  bootstrap_ci/delta_ci (2000 resamples, fixed seed); the 95% CI column
  is on every summary alive-rate row and the Δ-mean 95% CI on all
  U-test comparisons (alive/energy/crossings). docs/RESULTS.md
  regenerated (interpretation §4a–§4h preserved).
- **Repro quickstart (P7 closed):** readme “Reproducing the headline
  numbers” table — every headline claim → exact command → CSV/section.
  All commands executed: 6 audit CSVs md5-stable on re-run; v2 + n50
  reproduce every headline rate (dead-end 0/194/132/77; §4a curve to
  3rd decimal). ε-sweep CLI → argparse; phase4_full_demo sys.path fix.
- **CI + energy budget + interactive UI (P7/P4 closed):**
  .github/workflows/ci.yml (pytest, SDL-dummy 15s smoke rc=124,
  --export; steps verified locally); energy_budget.py →
  energy_budget.csv (break-even net = h·S−50 per 50-step window);
  visualizer: L/R click-to-add, draggable coupling slider (live),
  K_r double-bind fix.
- Tests 81→102; UI smoke (interactive rc=124 + --export rc=0) clean.
  Remaining: phi re-scope; paper + demo video (dedicated sessions).

## 2026-08-20 (compressed): closed boundary + late metrics

- **Closed boundaries (§4g):** no channel penetrates an impenetrable
  barrier — without the torus seam quantum crosses 0/20 (0% alive);
  ε0.1 walk-throughs at 25% alive. Quantum value = exhaustive non-local
  exploration of locally invisible routes.
- **Path efficiency (§4f, 15% NOT MET):** quantum 0.5055 vs classical
  1.0207 (default); maze: classical 0/20 reached, quantum 20/20 @0.894.
- **Phi (§4e, 1.5× NOT MET):** ratio 1.000; phi measures field
  self-organization, not agent-world coupling.
- **Maze route audit (§4d):** quantum 20/20 reach via 100% edge wraps —
  same global-route mechanism.
- **Anticipation (§4c, honest null):** nobody anticipates; quantum
  monotonically reduces lag (index −4.09→−1.39, frac ahead 0→0.10).

## 2026-08-19 (compressed): the null hypothesis is dead

- v1 flat ablations = broken instrument (2%/step dissipation; q=0 agents
  ran the quantum sampler; unreachable dead-end trap). v2 instrument
  (gain 3000, dt 0.2, diss 0.9999, prewarm 2000, q=0 argmax guard):
  tunnel 0%→100% alive (p≤2.4e-5); maze/single_source 0%→100%; default
  45%→90%.
- Re-scoped (§4b): quantum tunnel crossings are 100% seam wraps —
  separates *determinism vs exploration*; ε-greedy leaks too. Moving:
  real monotone coupling-liability curve at n=50 (0.679@q=0.05 →
  baseline by q≥0.2) — interior optimum at weak coupling.
- Caveat: advantage magnitude instrument-dependent; 0%→100% contrast is
  not (structural −1e6 wall).
