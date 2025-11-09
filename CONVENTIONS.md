# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Quantum-Inspired World Model (QIWM)** - A 5-phase research project building bio-inspired AI agents that navigate using quantum-inspired world models (Bohmian pilot waves, Penrose collapse, IIT coherence).

**Current Status**: Phase 1 complete (classical baseline). Ready for Phase 2 (quantum-inspired dynamics).

**Key Constraint**: Runs on modest hardware (i3-4100 CPU, 63GB RAM, 16GB VRAM). Target 15-30 FPS with 128×128 grids.

## Essential Commands

### Development
```bash
# Install dependencies
pip install -r requirements.txt

# Run interactive demo (Pygame window)
python main.py

# Export static visualization
python main.py --export

# Run specific examples
python examples/phase1_basic_demo.py
python examples/phase1_export_demo.py
```

### Testing
```bash
# Run all unit tests
pytest tests/test_toy_world.py -v

# Run with coverage
pytest --cov=src tests/

# Validate Phase 1 completion (5 automated suites)
python tests/validate_phase1.py
```

### Performance Profiling
```bash
# Profile hot loops (for optimization work)
python -m cProfile -s cumtime main.py --export > profile.txt
```

## Architecture

### Core Conceptual Stack (5 Phases)
```
Phase 5: Entertainification (UI/UX sandbox)
Phase 4: Bio-Inspired Agents (NanoAgent navigation)
Phase 3: IIT Coherence (Φ calculation)
Phase 2: Quantum-Inspired Dynamics (pilot waves, collapse)
Phase 1: Classical Baseline (ToyWorld) ← CURRENT
```

### Code Structure
```
src/
  core/         - Physics simulation (ToyWorld, future: QuantumInspiredWorld)
  visualization/- Pygame + Matplotlib rendering
  utils/        - Shared utilities (currently minimal)

examples/       - Runnable demos
tests/          - Unit tests + validation suites
docs/           - Phase validation criteria
```

### Key Classes

**`ToyWorld` (src/core/toy_world.py)** - Phase 1 classical physics
- Grid-based 2D potential field (NumPy array)
- Energy sources: (x, y, strength) → attractive 1/r potential
- Obstacles: (x, y, radius) → repulsive potential
- Methods: `add_energy_source()`, `add_obstacle()`, `compute_potential_field()`, `get_gradient()`

**`WorldVisualizer` (src/visualization/visualizer.py)** - Real-time rendering
- Pygame-based heatmap display
- Runs at configurable FPS (default: 30)
- Interactive controls: ESC to exit

**Phase 2 Extension (not yet implemented)**:
```python
class QuantumInspiredWorld(ToyWorld):
    # Adds: pilot_wave field, coherence tracking, collapse mechanics
```

## Development Workflow

### When Adding New Features

1. **Scope discipline**: Check readme.md phase plan - does this belong in current phase?
2. **Test-driven**: Add unit test to `tests/test_toy_world.py` first
3. **Type hints**: All public methods must have type annotations
4. **Documentation**: Docstrings required (Google style)
5. **Performance**: Profile before optimizing (target 15+ FPS @ 128×128)

### Phase Transition Checklist

Before moving to next phase:
1. Run `python tests/validate_phase1.py` (or current phase validator)
2. Verify performance targets met
3. Update `PROJECT_STRUCTURE.md` with new modules
4. Document baseline metrics for comparison

### Parameter Tuning

When quantum-inspired features are added (Phase 2+):
- Start with classical-only baseline (validate it works)
- Add pilot wave with low coupling (0.1 → 0.3 → 0.5)
- Log everything to CSV for analysis
- Use ablation studies (turn off features to prove necessity)

## Critical Design Constraints

### Performance Targets
- **Grid size**: 64×64 (fast) to 128×128 (balanced) - do NOT exceed without profiling
- **Agent cap**: 20-50 agents max (CPU bottleneck beyond this)
- **Frame rate**: 15-30 FPS minimum for interactive demos
- **Field computation**: < 200ms per update

### Optimization Strategy
1. **NumPy vectorization**: Use array operations, not Python loops
2. **Numba JIT** (Phase 2+): Add `@jit(nopython=True)` to hot loops
3. **Grid size scaling**: Reduce to 64×64 if performance drops
4. **Profiling**: Use `cProfile` to find bottlenecks before optimizing

### Hardware Reality
- CPU: i3-4100 (2014, dual-core) - the bottleneck
- RAM: 63GB - sufficient (uses ~2GB)
- VRAM: 16GB - unused (CPU-based simulation)

## Quantum-Inspired Concepts (Phase 2+)

### Bohmian Pilot Wave
- **Not quantum computing** - inspired by, not implementing
- Mechanism: Laplacian diffusion creates non-local correlations
- Implementation: `np.roll()` for efficient neighbor operations
- Coupling: Blends classical gradient + pilot wave (tunable weight)

### Penrose Collapse
- Trigger: Agent observation or coherence threshold
- Effect: Reduces local coherence, sharpens pilot wave
- Interpretation: Measurement-like interaction (IIT-inspired)

### IIT Φ (Coherence)
- Simplified metric: Internal correlation - external influence
- High Φ regions: Self-organized, maintain structure despite environment
- Low Φ regions: Driven by external forces, passive

## Common Pitfalls

### What NOT to Do
- ❌ Don't add features from future phases (scope creep)
- ❌ Don't optimize prematurely (profile first)
- ❌ Don't increase grid beyond 256×256 (CPU can't handle)
- ❌ Don't claim this is "quantum computing" (it's quantum-*inspired*)
- ❌ Don't skip validation between phases

### What TO Do
- ✅ Start with classical baseline, validate it works
- ✅ Add quantum features incrementally with low coupling
- ✅ Log all parameters and metrics for analysis
- ✅ Use ablation studies to prove each feature's value
- ✅ Document "future work" instead of implementing everything

## Validation Approach

### Quantitative Metrics (Phase 2+ comparison)
- Φ (coherence): Quantum vs. classical regions
- Agent survival time: Longevity in maze scenarios
- Path efficiency: Distance/energy ratio
- Dead-end escape rate: Local minima avoidance

### Qualitative Observations
- Emergent patterns: Flocking, clustering
- Anticipatory behavior: Pre-positioning near moving targets
- Adaptive exploration: Avoiding re-searched areas

### Null Hypothesis
"Quantum-inspired dynamics provide no advantage over classical gradient descent."
Goal: Falsify this with 10-20% improvements.

## File Naming Conventions

- **Phases**: `phase1_*.py`, `phase2_*.py` (examples, tests)
- **Modules**: Snake_case (`toy_world.py`, `quantum_world.py`)
- **Classes**: PascalCase (`ToyWorld`, `NanoAgent`)
- **Validation**: `validate_phase{N}.py` in tests/

## Project Philosophy

**Scope Discipline**: This is a 10-week research prototype, not production software. Build the minimal viable demonstration of quantum-inspired principles, then stop.

**Validation-First**: Each phase must prove value over previous baseline. No speculative features.

**Honest Framing**: "Inspired by Bohm/Penrose/IIT" ≠ "implements quantum mechanics". This is conceptual bridge-building, not physics simulation.

**Entertainification**: The demo must be visceral and engaging. Research lives through experiences people can't stop thinking about.

## References

- **Full Project Plan**: See readme.md for detailed phase breakdowns
- **Architecture Guide**: PROJECT_STRUCTURE.md for module organization
- **Quick Start**: QUICKSTART.md for setup and first run
- **Phase 1 Status**: PHASE1_COMPLETE.md for what's implemented

## When in Doubt

1. Check readme.md phase plan for scope boundaries
2. Run validation script for current phase
3. Profile before optimizing
4. Prefer simplicity over cleverness
5. Document why, not just what
