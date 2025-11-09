"""
Phase 1 Export Demo: Generate static visualization

This example demonstrates exporting the potential field as a
high-quality matplotlib figure for analysis and documentation.
"""

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.core import ToyWorld
from src.visualization import export_field_matplotlib


def main():
    """Generate and export potential field visualization."""
    print("=" * 60)
    print("QIWM Phase 1: Potential Field Export Demo")
    print("=" * 60)

    # Create world
    world = ToyWorld(size=128)

    # Scenario 1: Simple gradient
    print("\nScenario 1: Simple Energy Gradient")
    world.clear()
    world.add_energy_source(64, 64, strength=100.0)
    world.compute_potential_field()
    export_field_matplotlib(world, "output_simple_gradient.png")

    # Scenario 2: Multiple sources
    print("\nScenario 2: Multiple Energy Sources")
    world.clear()
    world.add_energy_source(32, 32, strength=80.0)
    world.add_energy_source(96, 96, strength=80.0)
    world.add_energy_source(32, 96, strength=80.0)
    world.add_energy_source(96, 32, strength=80.0)
    world.compute_potential_field()
    export_field_matplotlib(world, "output_multiple_sources.png")

    # Scenario 3: Maze-like with obstacles
    print("\nScenario 3: Maze with Obstacles")
    world.clear()
    world.add_energy_source(110, 110, strength=120.0)

    # Create obstacle maze
    for y in range(20, 100, 20):
        world.add_obstacle(40, y, radius=8.0)
        world.add_obstacle(80, y + 10, radius=8.0)

    world.compute_potential_field()
    export_field_matplotlib(world, "output_maze_scenario.png")

    print("\n" + "=" * 60)
    print("Export completed! Check the generated PNG files.")
    print("=" * 60)


if __name__ == "__main__":
    main()
