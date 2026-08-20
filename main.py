"""
Module: main.py
Depends on:
  - src.core (ToyWorld, QuantumInspiredWorld, AgentSwarm)
  - src.visualization (WorldVisualizer, export_field_matplotlib)

QIWM - Quantum-Inspired World Model
Main entry point for running simulations

Usage:
    python main.py              # Run interactive demo with agents
    python main.py --export     # Export visualizations only
    python main.py --maze       # Maze scenario (dead ends test)
    python main.py --help       # Show help
"""

import sys
import argparse
import numpy as np
from src.core import ToyWorld, QuantumInspiredWorld, AgentSwarm
from src.visualization import WorldVisualizer, export_field_matplotlib


def setup_world(size: int = 128) -> QuantumInspiredWorld:
    """Setup default world with energy sources and obstacles."""
    world = QuantumInspiredWorld(
        size=size,
        quantum_coupling=0.3,
        diffusion_rate=0.1,
    )
    world.add_energy_source(30, 30, strength=100.0)
    world.add_energy_source(90, 90, strength=80.0)
    world.add_energy_source(60, 20, strength=60.0)
    world.add_obstacle(60, 60, radius=15.0)
    world.add_obstacle(45, 75, radius=8.0)
    world.add_obstacle(80, 45, radius=8.0)
    world.compute_potential_field()
    return world


def setup_maze_world(size: int = 128) -> QuantumInspiredWorld:
    """Setup maze world with dead ends."""
    world = QuantumInspiredWorld(
        size=size,
        quantum_coupling=0.5,
        diffusion_rate=0.15,
    )
    world.add_energy_source(110, 110, strength=150.0)
    # Horizontal wall with gap
    for x in range(20, 110, 3):
        if not (60 <= x <= 75):
            world.add_obstacle(x, 40, radius=2.5)
    # Vertical wall with gap
    for y in range(20, 110, 3):
        if not (50 <= y <= 65):
            world.add_obstacle(80, y, radius=2.5)
    world.compute_potential_field()
    return world


def run_interactive_demo(maze: bool = False):
    """Run the interactive Pygame visualization with agents."""
    print("=" * 60)
    print(f"QIWM: Quantum-Inspired World Model - Interactive Demo")
    print(f"Scenario: {'Maze' if maze else 'Default'}")
    print("=" * 60)

    # Setup world
    if maze:
        world = setup_maze_world()
    else:
        world = setup_world()

    print(f"\nWorld state: {world.get_state()}")

    # Create agent swarm
    swarm = AgentSwarm(world, population=20, spawn_mode='corner')
    print(f"Spawned {len(swarm.agents)} agents")

    # Setup visualization
    visualizer = WorldVisualizer(world, window_size=800, fps=30)
    visualizer.set_agents(swarm)

    print("\nStarting visualization...")
    print("Controls:")
    print("  ESC - Exit")
    print("  P   - Toggle Phi/Coherence overlay")
    print("  T   - Toggle agent trails")
    print()

    visualizer.run(update_callback=lambda w: w.update_pilot_wave(dt=0.1))

    # Print final stats
    stats = swarm.get_stats()
    print("\n" + "=" * 60)
    print("Simulation Complete")
    print(f"Agents alive: {stats['alive']}/{stats['total']}")
    print(f"Average steps: {stats.get('avg_steps', 0):.1f}")
    print(f"Max steps: {stats.get('max_steps', 0)}")
    print("=" * 60)


def run_export_mode():
    """Export visualization as static images."""
    print("=" * 60)
    print("QIWM: Export Mode")
    print("=" * 60)

    world = QuantumInspiredWorld(size=128)
    world.add_energy_source(64, 64, strength=100.0)
    world.add_obstacle(32, 32, radius=10.0)
    world.add_obstacle(96, 96, radius=10.0)
    world.compute_potential_field()

    for _ in range(100):
        world.update_pilot_wave(dt=0.1)

    filename = "qiwm_potential_field.png"
    export_field_matplotlib(world, filename)
    print(f"\nVisualization exported to: {filename}")


def main():
    """Main entry point with argument parsing."""
    parser = argparse.ArgumentParser(
        description="Quantum-Inspired World Model (QIWM)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python main.py                    # Interactive visualization with agents
    python main.py --export           # Export static image
    python main.py --maze             # Maze scenario (dead ends test)
    python main.py --size 256         # Use larger grid

For more examples, see the examples/ directory.
        """
    )

    parser.add_argument(
        '--export',
        action='store_true',
        help='Export visualization as image instead of interactive mode'
    )
    parser.add_argument(
        '--maze',
        action='store_true',
        help='Run maze scenario (agents must navigate through gaps)'
    )
    parser.add_argument(
        '--size',
        type=int,
        default=128,
        help='Grid size (default: 128)'
    )

    args = parser.parse_args()

    try:
        if args.export:
            run_export_mode()
        else:
            run_interactive_demo(maze=args.maze)
    except KeyboardInterrupt:
        print("\n\nInterrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\nError: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
