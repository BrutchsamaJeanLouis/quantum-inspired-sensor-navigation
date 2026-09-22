# QIWM Quick Start Guide

## Installation

### 1. Clone/Navigate to Project
```bash
cd qwm-core
```

### 2. Create Virtual Environment (Recommended)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

## Running Phase 1 Demo

### Interactive Visualization
```bash
python main.py
```

This will open a Pygame window showing:
- Potential field as colorful heatmap (blue=low, yellow=high)
- White/yellow stars = energy sources (attractors)
- Red/dark circles = obstacles (repulsors)
- Real-time FPS and stats overlay

**Controls:**
- `ESC` - Exit

### Export Static Image
```bash
python main.py --export
```

Generates `qiwm_potential_field.png` with matplotlib visualization.

## Example Scripts

### Basic Demo
```bash
python examples/phase1_basic_demo.py
```

Interactive demo with pre-configured world.

### Export Multiple Scenarios
```bash
python examples/phase1_export_demo.py
```

Generates three scenario images:
- Simple gradient
- Multiple energy sources
- Maze with obstacles

## Testing

Run unit tests:
```bash
pytest tests/ -v
```

With coverage report:
```bash
pytest --cov=src tests/
```

## Understanding the Output

### Potential Field Colors
- **Yellow/White**: High potential (attractive regions)
- **Green**: Medium potential
- **Blue/Dark**: Low potential (repulsive or far from sources)

### Energy Sources (Attractors)
- Bright white/yellow stars
- Agents will naturally move toward these

### Obstacles (Repulsors)
- Dark red circles
- Create low/negative potential zones
- Agents should avoid these

## Performance Notes

Current configuration targets:
- **Grid Size**: 128x128 (adjustable)
- **Target FPS**: 30 (should achieve on i3-4100)
- **Memory Usage**: ~2GB

If visualization is slow:
- Reduce grid size: `python main.py --size 64`
- Close other applications
- Phase 2 will add Numba JIT optimization

## Next Steps

After validating Phase 1:

1. **Experiment with Parameters**
   - Try different grid sizes
   - Add more energy sources/obstacles
   - Observe potential field patterns

2. **Validation Metrics** (Week 2 of Phase 1)
   - Measure gradient flow
   - Validate field properties
   - Profile performance

3. **Move to Phase 2** (Weeks 3-4)
   - Add quantum-inspired pilot wave
   - Implement collapse dynamics
   - Compare with classical baseline

## Troubleshooting

### Pygame Won't Start
```bash
# Reinstall pygame
pip uninstall pygame
pip install pygame --upgrade
```

### Import Errors
Make sure you're in the project root and virtual environment is activated:
```bash
# Check Python can find src/
python -c "import sys; print(sys.path)"
```

### Performance Issues
Reduce grid size:
```bash
# Edit main.py, change:
world = ToyWorld(size=64)  # Instead of 128
```

## File Structure Quick Reference

```
qwm-core/
├── main.py                    # Main entry point (start here!)
├── examples/                  # Example scripts
├── src/
│   ├── core/toy_world.py     # Physics simulation
│   └── visualization/        # Rendering code
└── tests/                     # Unit tests
```

## Getting Help

- Check [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) for detailed architecture
- See [readme.md](readme.md) for full project plan
- Review code comments in `src/core/toy_world.py`

## What's Working (Phases 1–4 ✅)

- ✅ Classical potential field simulation (Phase 1)
- ✅ Energy sources (attractors), obstacles (repulsors), torus boundary
- ✅ Quantum-inspired pilot wave + Penrose collapse (Phase 2)
- ✅ IIT-inspired Φ metric + agent-coupling re-scope (§4i) (Phase 3)
- ✅ AgentSwarm navigation: Boltzmann/argmax, closed boundary, `y_traj` (Phase 4)
- ✅ Real-time Pygame visualization (P-key Φ overlay) + `demo_video.mp4`
- ✅ 400-run ablation dataset (byte-reproducible) + 107 unit tests
- ✅ Research paper (`docs/PAPER.md`) + results (`docs/RESULTS.md`)

## What's Next (⏳)

- ⏳ Push to GitHub (`git remote -v`); confirm CI green
- ⏳ Optional: Numba JIT for hot loops (optimization, not required)
- ⏳ Future work: larger/multi-scale worlds (documented, not in scope)

---

**Ready to begin!** Run `python main.py` and watch the potential field in action.
