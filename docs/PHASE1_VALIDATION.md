# Phase 1 Validation Criteria

## Overview

Phase 1 establishes the **classical baseline** that quantum-inspired enhancements (Phase 2+) will be compared against. This document defines success criteria and validation procedures.

## Timeline: Weeks 1-2

### Week 1: Implementation ✅
- [x] Project structure setup
- [x] ToyWorld physics class
- [x] Visualization system
- [x] Example scenarios
- [x] Unit tests

### Week 2: Validation & Optimization ⏳
- [ ] Performance profiling
- [ ] Parameter optimization
- [ ] Validation metrics
- [ ] Documentation of baseline behavior

## Success Criteria

### 1. Functional Requirements ✅

#### Core Physics
- [x] **Potential field computation**: Combines 1/r attraction and repulsion
- [x] **Energy sources**: Create attractive potential wells
- [x] **Obstacles**: Create repulsive potential barriers
- [x] **Gradient calculation**: Directional derivatives for navigation

#### Visualization
- [x] **Real-time rendering**: Pygame heatmap visualization
- [x] **Static export**: Matplotlib high-quality output
- [x] **Interactive controls**: ESC to exit, smooth FPS
- [x] **Info overlay**: Display world state and performance

#### Code Quality
- [x] **Modular structure**: Separated core, visualization, utilities
- [x] **Type hints**: All public APIs annotated
- [x] **Documentation**: Docstrings for classes and methods
- [x] **Unit tests**: Core functionality covered

### 2. Performance Requirements

Target hardware: **i3-4100 CPU (2014, dual-core 3.6GHz), 63GB RAM**

| Metric | Target | Measurement Method |
|--------|--------|-------------------|
| **FPS (64×64 grid)** | 30+ FPS | Pygame clock.get_fps() |
| **FPS (128×128 grid)** | 15+ FPS | Pygame clock.get_fps() |
| **Memory usage** | < 4GB | Task Manager / htop |
| **Startup time** | < 5 seconds | Manual timing |
| **Field computation** | < 100ms | Python time.time() |

#### Performance Testing Procedure

```python
import time
from src.core import ToyWorld

# Test 1: Field computation time
world = ToyWorld(size=128)
world.add_energy_source(64, 64, strength=100)
world.add_obstacle(32, 32, radius=10)

start = time.time()
world.compute_potential_field()
elapsed = time.time() - start

print(f"Field computation: {elapsed*1000:.2f}ms")
assert elapsed < 0.1, "Too slow!"

# Test 2: Visualization FPS
from src.visualization import WorldVisualizer
viz = WorldVisualizer(world)
# Run for 10 seconds, measure average FPS
```

### 3. Validation Metrics

These metrics establish the **classical baseline** for Phase 2 comparison.

#### A. Potential Field Properties

**Test**: Energy source creates monotonic gradient

```python
world = ToyWorld(size=64)
world.add_energy_source(32, 32, strength=100)
world.compute_potential_field()

# Verify potential decreases with distance
center = world.get_potential(32, 32)
near = world.get_potential(34, 32)
far = world.get_potential(40, 32)

assert center > near > far, "Gradient not monotonic!"
```

**Expected**: ✅ Potential follows 1/r law

#### B. Gradient Flow

**Test**: Gradient points toward energy source

```python
# Place source at (50, 32)
world.clear()
world.add_energy_source(50, 32, strength=100)
world.compute_potential_field()

# Test point to the left
dx, dy = world.get_gradient(40, 32)
assert dx > 0, "Gradient should point right (toward source)"
```

**Expected**: ✅ Gradient vector points toward nearest attractor

#### C. Obstacle Repulsion

**Test**: Obstacles create negative potential wells

```python
world.clear()
world.add_obstacle(32, 32, radius=10)
world.compute_potential_field()

obstacle_center = world.get_potential(32, 32)
edge = world.get_potential(42, 32)

assert obstacle_center < edge, "Obstacle should create low potential"
```

**Expected**: ✅ Potential is negative/reduced near obstacles

### 4. Visual Validation

#### Heatmap Correctness
- **Energy sources** appear as bright (yellow/white) spots
- **Obstacles** appear as dark (blue/black) regions
- **Gradient flow** is smooth and continuous (no artifacts)

#### Test Scenarios

Generate these standard scenarios for visual inspection:

1. **Single Source**: One energy source, no obstacles
   - Should show circular gradient radiating outward

2. **Multiple Sources**: 4 sources in corners
   - Should show interaction/superposition in center

3. **Maze**: Energy at corner, obstacles form barriers
   - Should show gradient "flowing around" obstacles

```bash
python examples/phase1_export_demo.py
# Manually inspect: output_*.png files
```

### 5. Comparison to Expectations

| Property | Expected (from Plan) | Actual | Status |
|----------|---------------------|---------|--------|
| Grid sizes | 64×64 to 128×128 | 128×128 default | ✅ |
| Visualization | Pygame heatmap | Implemented | ✅ |
| Potential law | 1/r attraction | Implemented | ✅ |
| Obstacles | Negative potential | Implemented | ✅ |
| Export | Matplotlib PNG | Implemented | ✅ |

## Known Limitations (By Design)

These are **intentional** for Phase 1 baseline:

1. **No time evolution**: Field is static (recomputed on changes only)
2. **No agents**: Navigation tested in Phase 4
3. **Simple 1/r potential**: Not physically accurate, but sufficient for demo
4. **No quantum effects**: This is the classical baseline

## Phase 1 → Phase 2 Transition Checklist

Before moving to Phase 2 (Quantum-Inspired Dynamics):

- [ ] All validation tests pass
- [ ] Performance meets targets (15+ FPS @ 128×128)
- [ ] Baseline metrics documented (for comparison)
- [ ] Visual inspection confirms correct behavior
- [ ] Code reviewed and cleaned
- [ ] Unit test coverage > 80%

## Validation Script

Create `tests/validate_phase1.py`:

```python
"""
Automated validation script for Phase 1.
Run this before moving to Phase 2!
"""

import time
from src.core import ToyWorld

def validate_performance():
    print("Testing performance...")
    world = ToyWorld(size=128)
    world.add_energy_source(64, 64, 100)

    start = time.time()
    world.compute_potential_field()
    elapsed = time.time() - start

    print(f"  Field computation: {elapsed*1000:.2f}ms")
    assert elapsed < 0.2, "Performance too slow!"
    print("  ✅ Performance OK")

def validate_gradient():
    print("Testing gradient flow...")
    world = ToyWorld(size=64)
    world.add_energy_source(40, 32, 100)
    world.compute_potential_field()

    dx, dy = world.get_gradient(30, 32)
    assert dx > 0, "Gradient should point toward source"
    print("  ✅ Gradient correct")

def validate_obstacles():
    print("Testing obstacles...")
    world = ToyWorld(size=64)
    world.add_obstacle(32, 32, 10)
    world.compute_potential_field()

    center = world.get_potential(32, 32)
    edge = world.get_potential(50, 50)
    assert center < edge, "Obstacle should reduce potential"
    print("  ✅ Obstacles correct")

if __name__ == "__main__":
    print("=" * 50)
    print("PHASE 1 VALIDATION")
    print("=" * 50)

    validate_performance()
    validate_gradient()
    validate_obstacles()

    print("\n" + "=" * 50)
    print("✅ ALL PHASE 1 VALIDATIONS PASSED")
    print("Ready for Phase 2!")
    print("=" * 50)
```

Run with:
```bash
python tests/validate_phase1.py
```

## Documentation Requirements

Before Phase 1 completion:

1. **Baseline Metrics Report**: Document performance numbers
2. **Visual Gallery**: Save example scenarios as references
3. **Known Issues Log**: Document any quirks or limitations
4. **Phase 2 Planning**: Outline quantum-inspired additions

## Sign-Off

Phase 1 is complete when:

✅ All validation tests pass
✅ Performance targets met
✅ Visual inspection confirms correctness
✅ Documentation complete
✅ Code clean and commented

**Date Completed**: _____________
**Ready for Phase 2**: [ ] Yes [ ] No
**Notes**: _________________________________
