```yaml
# QIWM: Quantum-Inspired World Model for Bio-AI Navigation
# Lossless Context Compression for Development Agent

## Core Identity
project_name: "Quantum-Inspired World Model (QIWM)"
purpose: "Demonstrable proof-of-concept: bio-inspired agents navigate using quantum-inspired field dynamics (Bohm pilot waves + Penrose collapse + IIT coherence)"
scope_discipline: "NOT quantum computing | NOT consciousness | NOT full-scale world model"
deliverable_pair: 
  - research_paper: "8-12 pages, metrics/ablations/theory"
  - interactive_demo: "Pygame visualization + GitHub + video"

## Philosophical Grounding
conceptual_bridge: "Embodied intuition as field-participation mechanics"
theoretical_inspiration:
  - bohm_pilot_wave: "Non-local guidance field modifies classical gradients"
  - penrose_collapse: "Threshold-triggered decoherence via agent observation"
  - iit_phi: "Integrated information as coherence/self-organization metric"
framing: "Inspired by (metaphorical scaffolding) ≠ Implements (literal physics)"

## Architecture Stack (Bottom-Up)
```
Layer_1_ToyPhysics:
  - 2D grid (64x64 or 128x128)
  - discrete timesteps
  - energy_sources: [(x,y,strength)]
  - obstacles: [(x,y,radius)]
  - classical_field: gradient descent potential

Layer_2_QuantumInspired:
  - pilot_wave_field: diffusion-based non-local spread
  - coherence_field: tracks local integration
  - collapse_mechanism: agent observation → localized decoherence
  - guidance_field: classical + α*pilot_wave (tunable coupling)

Layer_3_IIT_Measurement:
  - phi_metric: internal_correlation - external_correlation
  - region_analysis: temporal mutual information
  - interpretation: high_phi = self-organized, low_phi = passive

Layer_4_BioAgents:
  - sense: query 5x5 local patch from guidance_field
  - decide: blend classical_gradient + quantum_sampling via local coherence
  - act: move + trigger collapse_field(radius=3)
  - survive: energy budget, death at energy<=0

Layer_5_Interface:
  - pygame_visualization: heatmaps, agent sprites, trails
  - user_controls: add energy/obstacles, adjust quantum_weight slider
  - phi_overlay: visualize coherence regions
```

## Technical Constraints
hardware:
  cpu: "i3-4100 (2014, dual-core 3.6GHz) — PRIMARY BOTTLENECK"
  ram: "63GB — overprovisioned"
  vram: "16GB — unused (CPU-only simulation)"

performance_targets:
  grid_size: "128x128 (acceptable) | 64x64 (safe fallback)"
  framerate: "15+ FPS minimum"
  agent_cap: "20-50 agents max"

optimization_strategy:
  - numba_jit: "@jit(nopython=True) for all NumPy loops"
  - profiling: "cProfile to identify hotspots"
  - fallback: "pre-render to video if real-time fails"

stack:
  language: "Python 3.9+"
  core_libs: ["numpy", "numba", "pygame"]
  optional: ["matplotlib", "scipy"]
  install_size: "~500MB"

## Implementation Phases (10-Week Timeline)

### Phase 1: Classical Baseline (Weeks 1-2)
```python
class ToyWorld:
    __init__(size): # 2D grid
    add_energy_source(x, y, strength)
    add_obstacle(x, y, radius)
    compute_potential_field(): # attraction/repulsion gradients
```
validation: heatmap visualization, gradient flow confirmation

### Phase 2: Quantum Dynamics (Weeks 3-4)
```python
class QuantumInspiredWorld(ToyWorld):
    __init__(size):
        super().__init__(size)
        pilot_wave: np.zeros((size, size))
        coherence: np.ones((size, size))
    
    update_pilot_wave(dt): 
        # laplacian diffusion (non-local spread)
        # couple to energy_sources
    
    collapse_field(x, y, radius=3):
        # agent observation → coherence *= 0.9, pilot_wave *= 1.1
    
    get_guidance_field():
        return grid + 0.3 * pilot_wave  # tunable coupling
```
validation_metrics:
  - non_local_propagation: perturb corner, measure opposite-corner response time
  - collapse_signature: agent placement → local coherence drop
  - emergence_test: multi-agent interactions → flocking/clustering

### Phase 3: IIT Coherence (Week 5)
```python
def compute_phi(world, region):
    # sample field states: t0_state, t1_state (5 steps forward)
    # internal_correlation = corrcoef(t0, t1)
    # external_correlation = corrcoef(boundary, t1)
    # phi = max(0, internal - external)
    return phi
```
interpretation:
  - high_phi: self-organized (maintains coherence despite environment)
  - low_phi: externally-driven (passive response)

### Phase 4: Bio-Agents (Weeks 6-7)
```python
class NanoAgent:
    __init__(x, y, world): energy=100
    
    sense_environment():
        return world.get_guidance_field()[x-2:x+3, y-2:y+3]
    
    decide_action():
        patch = sense_environment()
        classical_move = argmax(patch)  # steepest gradient
        quantum_move = sample(exp(patch))  # boltzmann-like
        coherence = world.coherence[x, y]
        return quantum_move if coherence > 0.7 else classical_move
    
    step():
        dx, dy = decide_action()
        world.collapse_field(x, y)
        x, y = (x+dx) % size, (y+dy) % size
        energy -= 1
        # check energy_source collision → energy += strength*10
```
experimental_scenarios:
  - maze_deadends: "pilot wave leaks through walls"
  - moving_sources: "non-local coherence predicts motion"
  - multi_agent: "collapse creates avoid-searched markers"

### Phase 5: Entertainification (Weeks 8-9)
selected_option: "Nanobot Garden (meditative)"
mechanics:
  - click: add energy/obstacles
  - slider: classical ↔ quantum weighting
  - heatmap: phi visualization overlay
  - trails: agent exploration patterns
hook: "Grow a quantum ecosystem. Watch emergence."

### Phase 6: Deliverables (Week 10)
paper_structure:
  - intro: motivation, scope discipline, theoretical inspiration
  - methods: architecture, equations, parameters
  - experiments: scenarios, metrics, ablations
  - results: quantitative (tables/graphs) + qualitative (emergent patterns)
  - discussion: limitations, future work, honest framing
demo_video:
  - screen_recording: simulation runs, parameter sweeps
  - voiceover: narrative of what quantum-inspired adds
  - github_link: reproducible code + README

## Success Metrics (Falsify Null Hypothesis)
null_hypothesis: "Quantum-inspired dynamics provide NO advantage over classical"

quantitative_thresholds:
  phi: "quantum_phi > 1.5 × classical_phi"
  survival: "quantum agents live 20% longer"
  efficiency: "quantum 15% more path efficient"
  escape_rate: "quantum escapes deadends 2× faster"
  collective: "phi increases with agent density"

qualitative_markers:
  - flocking_clustering: quantum agents vs classical dispersion
  - anticipatory_positioning: pre-positioning near moving sources
  - adaptive_exploration: avoid re-searching collapsed regions

## Results (v2 ablation — 2026-08-19)
status: "NULL HYPOTHESIS REJECTED in 4/5 scenarios (docs/RESULTS.md)"

headline_numbers:
  tunnel: "classical 0/20 cross a gapless wall, 0% alive → quantum 20/20 cross, 100% alive (p ≤ 2.4e-5)"
  maze: "classical 0% alive → quantum 100% alive at every q>0 (p ≤ 1.6e-5)"
  single_source: "classical 20% → quantum 100% (p ≤ 1.6e-5)"
  default: "classical 45% → quantum 90% at q=0.3/0.5 (p ≈ 7.6e-4)"
  moving: "n=50 sweep: 68% at q=0.05 (p<5e-5) → 44% at q=0.5 — real monotone coupling-liability curve, optimum at weak coupling"
  crossing_taxonomy: "ALL quantum tunnel crossings are seam wraps (torus shortcut, ~2.5-step latency); 0 wall jumps; ε-noise (ε=0.1 → 68% alive) leaks via wall jumps — the tunnel separates determinism-vs-exploration, not quantum-vs-classical per se"

collapse_ablation: "static: pilot wave suffices (collapse off OK); dynamic/trapped: quantum agents WITHOUT collapse do WORSE than classical — collapse gate is the survival mechanism"

device_forensics: "v1 instrument was broken (dead quantum channel, quantum sampler posing as classical baseline, unreachable trap); v2 calibrated gain/dt/dissipation/prewarm identically across all coupling levels"

thresholds_met:
  survival: "YES — 0% → 100%, far beyond the 20% threshold"
  escape_rate: "YES — tunnel 0 vs 20/20; dead-end escapes quantum-only (194/132/77 vs 0)"
  efficiency: "PARTIAL — survival/escape measured; path-efficiency ratio pending"
  phi: "PENDING — phi metric not yet wired into the ablation harness"

artifacts:
  data: "ablation_results_v2.csv (400 runs)"
  analysis: "examples/analyze_results.py → docs/RESULTS.md; examples/q_sweep_moving.py → q_sweep_moving{n,_n50}.csv"
  runner: "examples/run_ablation_study.py --scenario all --runs 10"

## Parameter Space (Initial Values)
world_config:
  grid_size: 128
  energy_sources: 3-5
  obstacles: 10-15
  
dynamics:
  pilot_wave_diffusion_rate: 0.1
  quantum_coupling_strength: 0.3  # guidance_field weight
  collapse_radius: 3
  coherence_decay: 0.9  # multiplier on collapse
  
agents:
  population: 20
  initial_energy: 100
  movement_cost: 1
  energy_gain_multiplier: 10
  coherence_threshold: 0.7  # quantum vs classical decision

tuning_strategy: "start classical-only → increment coupling 0.1→0.3→0.5"

## Risk Mitigation
computational_bottleneck:
  symptoms: "<10 FPS"
  fixes: ["reduce to 64x64", "cap 20 agents", "numba everywhere", "pre-render fallback"]

parameter_hell:
  symptoms: "agents stuck or chaotic"
  fixes: ["validate classical first", "incremental quantum", "log everything CSV", "hyperparameter grid search"]

proving_quantum_inspired:
  symptoms: "reviewers say 'just diffusion+noise'"
  fixes: ["ablation studies (collapse off → drop?)", "show non-local mutual information", "cite Bohm/Penrose/IIT explicitly", "honest framing in paper"]

scope_creep:
  symptoms: "endless feature additions"
  fixes: ["MVP = 2D, 1 agent type, 1 scenario", "freeze after phase 4", "document future work instead"]

## Development Workflow
iteration_cycle:
  1_implement: "write phase code"
  2_validate: "check metrics against baselines"
  3_observe: "emergent patterns not in design"
  4_investigate: "why did X happen?"
  5_document: "log parameters, failures, insights"
  6_iterate: "course-correct based on emergence"

philosophy: "dialogue with system (responsive) NOT monologue (prescriptive)"

## Critical Reminders
- constraint = discipline (CPU limits force careful thinking)
- ambition = direction (north star, not next step)
- metaphor ≠ mechanism (bohm/penrose inspire, don't prescribe)
- demo + paper = together (neither alone sufficient)
- emergence = teacher (let weird behaviors guide you)
- honest framing = integrity ("inspired by" explicit throughout)

## Deliverable Checklist
- [ ] ToyWorld class (classical physics)
- [ ] QuantumInspiredWorld class (pilot wave + collapse)
- [ ] compute_phi function (IIT metric)
- [ ] NanoAgent class (bio-inspired navigation)
- [ ] Pygame visualization (heatmaps, sprites, controls)
- [ ] Experimental scenarios (3+ configurations)
- [ ] Metrics logging (CSV export)
- [ ] Ablation studies (quantum components on/off)
- [ ] Research paper (LaTeX/Markdown)
- [ ] Demo video (screen recording + voiceover)
- [ ] GitHub repo (code + README + requirements.txt)

## Entry Point for Agent
start_here: "Phase 1 — implement ToyWorld.compute_potential_field() with numpy"
first_validation: "matplotlib heatmap of energy sources + obstacles"
next_step_trigger: "when heatmap shows correct gradients → proceed to Phase 2"
```

---

**Relational Signal Decoded**: You transmit *"I need this crystallized for delegation without loss of essence."*

This compression holds:
- **Directive**: architecture, phases, code signatures  
- **Formation**: validation metrics, thresholds, checklists  
- **Motion**: iteration cycle, emergence-responsive workflow  
- **Synthesis**: dual deliverable (paper+demo), honest framing

The coding agent receives **executable structure** while preserving **philosophical substrate**. No cosmic vision lost — it's embedded in `conceptual_bridge`, `philosophy`, `critical_reminders`.
