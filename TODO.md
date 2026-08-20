# QIWM TODO

## Completed

### Phase 1: Classical Baseline ✅
- [x] ToyWorld class with vectorized potential field computation
- [x] Energy sources (attractors) and obstacles (repulsors)
- [x] Gradient calculation
- [x] Pygame visualization (field heatmap)
- [x] Matplotlib export
- [x] Unit tests (11 tests pass)

### Phase 2: Quantum-Inspired Dynamics ✅
- [x] QuantumInspiredWorld(ToyWorld) class
- [x] Pilot wave diffusion (Laplacian-based)
- [x] Collapse mechanics (agent observation → decoherence)
- [x] Guidance field (classical + quantum_coupling × pilot_wave)
- [x] Unit tests (12 tests pass)

### Phase 3: IIT Coherence ✅
- [x] compute_phi(world, region) function
- [x] compute_phi_map() for world-wide coherence visualization
- [x] Unit tests (8 tests pass)

### Phase 4: Bio-Inspired Agents ✅
- [x] NanoAgent class (sense/decide/act/survive)
- [x] Classical gradient descent + quantum Boltzmann sampling
- [x] Coherence-based decision switching
- [x] Energy system + death mechanics
- [x] AgentSwarm class for multi-agent management
- [x] Unit tests (19 tests pass)

### Infrastructure ✅
- [x] main.py fixed (uses QuantumInspiredWorld)
- [x] Export mode working
- [x] 52 total tests passing

## Priority 1: Make It Work Together ✅

- [x] Add agent rendering to WorldVisualizer
- [x] Add coherence/phi visualization overlay to WorldVisualizer (P key)
- [x] Create integrated demo with agents navigating quantum field (main.py + phase4_full_demo.py)
- [x] Fix render_field() performance (vectorized via pygame.surfarray)

## Priority 2: Experimental Scenarios (Prove the Hypothesis)

- [x] Maze scenario: pilot wave leaks through walls vs classical stuck
- [x] Tunnel scenario: gapless solid wall, classical trapped 0/20, quantum 20/20 (v2 instrument)
- [ ] Moving energy sources: anticipatory positioning test (scenario exists, needs dedicated metric)
- [ ] Multi-agent comparison: quantum vs classical survival/efficiency (in v2 run: all scenarios × 10 seeds)
- [x] Dead-end escape rate measurement (metric live; v2 run populates it)

## Priority 3: Ablation Studies & Metrics

- [x] Systematic comparison: quantum_coupling 0.0 vs 0.3 vs 0.5 (v2 run: +0.1)
- [x] Ablation: collapse off vs on
- [x] Metrics logging (CSV export): survival time, path efficiency, steps, barrier crossings
- [x] Statistical validation: analyzer with Mann-Whitney U (examples/analyze_results.py)
- [x] v2 run: full suite → ablation_results_v2.csv (400 runs) → docs/RESULTS.md

## Priority 2b: Instrument Forensics (done 2026-08-19)

- [x] Diagnose why v1 ablations were flat (dead quantum channel, no-op coupling)
- [x] Normalize pilot wave in guidance field + gain (quantum_world.py)
- [x] Dissipation 0.98 → 0.9999, dt 0.1 → 0.2, prewarm 2000 steps
- [x] q=0 → classical argmax decision guard (agents.py)
- [x] Tunnel scenario: gapless wall + barrier_crossings metric
- [x] examples/analyze_results.py: mean±std + Mann-Whitney U + docs/RESULTS.md
- [x] Null hypothesis REJECTED: tunnel 0%→100% alive (p≤2.4e-5); maze 0%→100%; single_source 20%→100%; default 45%→90%; moving q-dependent (97%@0.1 → 39%@0.5)

## Priority 6: Follow-ups (new, from v2 results)

- [x] Finer q-sweep in moving scenario (examples/q_sweep_moving.py, 8×10 runs): NO systematic liability — v2's 97→39% slope was seed luck; effect is a modest low-q bump (0.67±0.44 @q≤0.1 vs 0.45), n.s. at n=10 (p≥0.11). Retracted in docs/RESULTS.md §4.
- [x] Moving scenario at n=50 (q_sweep_moving_n50.csv, 400 runs): REAL monotone curve — 0.679@q=0.05 (p<5e-5), 0.653@0.1, 0.621@0.15, decays to baseline by q≥0.2; interior optimum at weak coupling
- [x] ε-greedy stochastic classical baseline (classical_epsilon: world/agent/config + 3 tests): tunnel leaks at ANY noise (ε=0.05 → 43% alive, ε=0.1 → 68%, ε=0.3 → 92%) — claim re-scoped to "crossing without decision noise"; see RESULTS.md §4b
- [x] Crossing-latency/directionality metric (x_traj + wall/seam taxonomy): quantum tunnel crossings are 100% seam wraps (torus shortcut), 0 wall jumps; ε-noise is the wall-jump signature; first-crossing latency quantum 2.4-2.8 vs eps 5.2-17.4. Tunnel claim RETRACTED to "route discovery via globally leaked sensor" — see RESULTS.md §4b
- [ ] Maze/dead-end route audit: extend crossing taxonomy to maze (does that advantage also reduce to global route discovery?)
- [ ] Phi metric wired into ablation harness (thresholds: phi row in readme)
- [ ] Path-efficiency ratio metric (threshold: 15%)
- [ ] Paper (8-12 pages): forensics → tunnel → collapse ablation → moving-scenario null (honest edge case)
- [ ] Demo video: tunnel scenario with phi overlay as centerpiece
- [ ] Interactive controls: click to add energy/obstacles, coupling slider (real dial now)

## Priority 4: Entertainification (Phase 5)

- [ ] Interactive controls: click to add energy/obstacles
- [ ] Quantum coupling slider
- [x] Phi overlay toggle (P key)
- [x] Agent trail visualization (T key toggle)

## Priority 5: Deliverables

- [ ] Research paper (8-12 pages)
- [ ] Demo video (screen recording + voiceover)
- [x] README cleanup (removed garbage header)
- [ ] GitHub repo polish

## Notes

- v2 instrument constants (gain 3000, dt 0.2, diss 0.9999, prewarm 2000) are identical for all coupling levels — instrument calibration, not per-condition fudging. Absolute advantage magnitude is instrument-dependent; the 0%→100% contrast is not (classical impossibility is structural: −1e6 wall spike).
- Hardware constraint: i3-4100 CPU is bottleneck. Profile before optimizing.
- Null hypothesis to falsify: "Quantum-inspired dynamics provide NO advantage over classical"
- Target: 15-30 FPS @ 128×128 with 20-50 agents
