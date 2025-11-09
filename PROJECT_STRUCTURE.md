# QIWM Project Structure

## Directory Layout

```
qwm-core/
├── src/                          # Source code
│   ├── core/                     # Core physics simulation
│   │   ├── __init__.py
│   │   └── toy_world.py         # Phase 1: Classical world model
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
├── tests/                        # Unit tests (TODO)
│   └── test_toy_world.py
│
├── docs/                         # Documentation (TODO)
│   └── phase1_validation.md
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

## Phase 1 Objectives

✅ **Completed:**
- Project structure setup
- ToyWorld classical physics simulation
- Pygame visualization
- Matplotlib export functionality
- Example demos

⏳ **Next Steps (Week 2):**
- Parameter optimization (grid size, performance)
- Validation metrics implementation
- Unit test suite
- Performance profiling with Numba

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

## Future Phases

### Phase 2: Quantum-Inspired Dynamics
- Add `quantum_world.py` extending ToyWorld
- Implement pilot wave field
- Add collapse mechanics

### Phase 3: IIT Coherence
- Add `coherence.py` module
- Implement Φ (phi) calculation
- Validation metrics

### Phase 4: Bio-Inspired Agents
- Add `agents/` directory
- Implement NanoAgent class
- Navigation experiments

### Phase 5: Entertainification
- Enhanced UI/UX
- Interactive level editor
- Export/share functionality

## Notes

- Keep scope disciplined - follow the plan in readme.md
- Validate each phase before moving forward
- Document all experiments and results
- Optimize only when necessary (profile first!)
