# QIWM Project Structure

## Directory Layout

```
qwm-core/
├── src/                          # Source code
│   ├── core/                     # Core physics simulation
│   │   ├── __init__.py
│   │   ├── toy_world.py         # Phase 1: Classical world model
│   │   ├── quantum_world.py     # Phase 2: pilot wave + collapse + guidance field
│   │   ├── coherence.py         # Phase 3: IIT-inspired Φ (compute_phi, compute_phi_agents §4i)
│   │   ├── agents.py            # Phase 4: AgentSwarm (sense/decide/move/collapse, y_traj)
│   │   └── experiments.py       # v2 ablation harness + scenario factory + metrics
│   ├── visualization/            # Rendering and display
│   │   ├── __init__.py
│   │   └── visualizer.py        # Pygame-based visualization
│   ├── utils/                    # Utility functions
│   │   └── __init__.py
│   └── __init__.py
│
├── examples/                     # Example scripts
│   ├── phase1_basic_demo.py     # Interactive demo
│   └── phase1_export_demo.py    # Static export demo
│
├── tests/                        # Unit tests (107)
│   └── test_*.py                # per-module + validation suites
│
├── docs/                         # Documentation
│   ├── RESULTS.md               # ablations, instrument forensics, §4i
│   └── PAPER.md                 # 8-12 page research paper
│
├── main.py                       # Main entry point
├── requirements.txt              # Python dependencies
├── setup.py                      # Package installation
├── readme.md                     # Project plan and overview
├── PROJECT_STRUCTURE.md          # This file
└── .gitignore                    # Git ignore rules
```

## Module Overview

### `src.core.toy_world`
Classical 2D physics simulation with:
- Potential field computation
- Energy sources (attractors)
- Obstacles (repulsors)
- Gradient calculation

**Key Classes:**
- `ToyWorld`: Main world simulation class

### `src.visualization.visualizer`
Real-time and static visualization:
- Pygame-based interactive display
- Matplotlib export functionality
- Heatmap rendering of potential fields

**Key Classes:**
- `WorldVisualizer`: Interactive visualization
- `export_field_matplotlib()`: Static export function

## Running the Code

### Quick Start
```bash
# Install dependencies
pip install -r requirements.txt

# Run interactive demo
python main.py

# Export static visualization
python main.py --export
```

### Examples
```bash
# Run basic interactive demo
python examples/phase1_basic_demo.py

# Generate multiple scenario exports
python examples/phase1_export_demo.py
```

## Phase Status

✅ **Phases 1–4 complete:**
- Phase 1: ToyWorld classical physics, Pygame visualization, Matplotlib export
- Phase 2: `quantum_world.py` — pilot wave + Penrose collapse + guidance field
- Phase 3: `coherence.py` — IIT-inspired Φ (`compute_phi`, `compute_phi_agents` §4i)
- Phase 4: `agents.py` — AgentSwarm navigation (Boltzmann/argmax, `y_traj`)
- 107 unit tests; 400-run ablation dataset (byte-reproducible); `docs/PAPER.md`

⏳ **Next:** push to GitHub, confirm CI green. (Numba JIT = optional optimization.)

## Development Guidelines

### Code Style
- Follow PEP 8
- Use type hints
- Document all public APIs
- Keep functions focused and small

### Performance Considerations
- Grid size: 64x64 (fast) to 128x128 (balanced)
- Target: 15-30 FPS on i3-4100 CPU
- Use Numba JIT for hot loops (Phase 2+)

### Testing
```bash
# Run tests (once implemented)
pytest tests/

# With coverage
pytest --cov=src tests/
```

## Phase Deliverables (status)

### Phase 2: Quantum-Inspired Dynamics ✅
- `quantum_world.py`: pilot wave field, collapse mechanics, guidance field

### Phase 3: IIT Coherence ✅
- `coherence.py`: Φ (phi) calculation + agent-coupling re-scope (§4i)

### Phase 4: Bio-Inspired Agents ✅
- `agents.py`: AgentSwarm (NanoAgent) navigation + experiments

### Phase 5: Entertainification (partial)
- Interactive demo + P-key Φ overlay + `demo_video.mp4` done
- Interactive level editor, export/share: future work

## Notes

- Keep scope disciplined - follow the plan in readme.md
- Validate each phase before moving forward
- Document all experiments and results
- Optimize only when necessary (profile first!)
