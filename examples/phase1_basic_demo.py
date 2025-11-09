"""
Phase 1 Basic Demo: Classical Potential Field Visualization

This example demonstrates the baseline classical world model with:
- Energy sources (attractors)
- Obstacles (repulsors)
- Real-time visualization of the potential field

Controls:
    ESC - Exit the visualization
"""

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.core import ToyWorld
from src.visualization import WorldVisualizer


def main():
    """Run the basic Phase 1 demonstration."""
    print("=" * 60)
    print("QIWM Phase 1: Classical Potential Field Demo")
    print("=" * 60)

    # Create world
    world_size = 128
    world = ToyWorld(size=world_size)

    # Add energy sources (attractors)
    world.add_energy_source(30, 30, strength=100.0)
    world.add_energy_source(90, 90, strength=80.0)
    world.add_energy_source(30, 90, strength=60.0)

    # Add obstacles (repulsors)
    world.add_obstacle(60, 60, radius=15.0)
    world.add_obstacle(40, 70, radius=8.0)
    world.add_obstacle(80, 40, radius=10.0)

    # Compute initial potential field
    print("\nComputing potential field...")
    world.compute_potential_field()

    # Print world state
    state = world.get_state()
    print(f"\nWorld State:")
    print(f"  Grid Size: {state['size']}x{state['size']}")
    print(f"  Energy Sources: {state['num_energy_sources']}")
    print(f"  Obstacles: {state['num_obstacles']}")
    print(f"  Potential Range: [{state['potential_range'][0]:.2f}, {state['potential_range'][1]:.2f}]")
    print(f"  Mean Potential: {state['potential_mean']:.2f}")

    print("\nStarting visualization...")
    print("Press ESC to exit")

    # Create and run visualizer
    visualizer = WorldVisualizer(world, window_size=800, fps=30)
    visualizer.run()

    print("\nDemo completed!")


if __name__ == "__main__":
    main()
