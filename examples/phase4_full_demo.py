"""
Module: examples/phase4_full_demo.py

QIWM Full Demo — Quantum-Inspired Agents Navigating a Dynamic World

This demo shows the complete system:
- QuantumInspiredWorld with pilot waves and collapse
- NanoAgents using quantum/classical hybrid navigation
- Real-time visualization with agent trails and phi overlay

Usage:
    python examples/phase4_full_demo.py          # Default scenario
    python examples/phase4_full_demo.py --maze   # Maze with dead ends
    python examples/phase4_full_demo.py --moving # Moving energy sources
"""

import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
from src.core import QuantumInspiredWorld, AgentSwarm
from src.visualization import WorldVisualizer


def setup_default_scenario(world_size: int = 128) -> QuantumInspiredWorld:
    """Default scenario: multiple energy sources with obstacles."""
    world = QuantumInspiredWorld(
        size=world_size,
        quantum_coupling=0.3,
        diffusion_rate=0.1,
    )

    # Energy sources
    world.add_energy_source(30, 30, strength=100.0)
    world.add_energy_source(90, 90, strength=80.0)
    world.add_energy_source(60, 20, strength=60.0)

    # Obstacles creating interesting paths
    world.add_obstacle(60, 60, radius=15.0)
    world.add_obstacle(45, 75, radius=8.0)
    world.add_obstacle(80, 45, radius=8.0)

    world.compute_potential_field()
    return world


def setup_maze_scenario(world_size: int = 128) -> QuantumInspiredWorld:
    """Maze scenario: dead ends where pilot waves leak through walls."""
    world = QuantumInspiredWorld(
        size=world_size,
        quantum_coupling=0.5,  # Higher coupling for maze
        diffusion_rate=0.15,
    )

    # Energy source in corner (goal)
    world.add_energy_source(110, 110, strength=150.0)

    # Create maze-like walls
    # Horizontal wall with gap
    for x in range(20, 110, 3):
        if not (60 <= x <= 75):  # Gap
            world.add_obstacle(x, 40, radius=2.5)

    # Vertical wall with gap
    for y in range(20, 110, 3):
        if not (50 <= y <= 65):  # Gap
            world.add_obstacle(80, y, radius=2.5)

    # Dead-end corridors
    for x in range(20, 60, 3):
        world.add_obstacle(x, 80, radius=2.5)
    for y in range(80, 110, 3):
        world.add_obstacle(20, y, radius=2.5)

    world.compute_potential_field()
    return world


def setup_moving_scenario(world_size: int = 128) -> QuantumInspiredWorld:
    """Moving energy sources scenario."""
    world = QuantumInspiredWorld(
        size=world_size,
        quantum_coupling=0.4,
        diffusion_rate=0.12,
    )

    # Multiple energy sources
    world.add_energy_source(30, 30, strength=100.0)
    world.add_energy_source(90, 30, strength=80.0)
    world.add_energy_source(60, 90, strength=90.0)

    # Some obstacles
    world.add_obstacle(60, 60, radius=12.0)

    world.compute_potential_field()
    return world


def run_demo(scenario: str = "default", world_size: int = 128):
    """Run the full demo."""
    print("=" * 60)
    print(f"QIWM Full Demo — {scenario.title()} Scenario")
    print("=" * 60)

    # Setup world
    if scenario == "maze":
        world = setup_maze_scenario(world_size)
    elif scenario == "moving":
        world = setup_moving_scenario(world_size)
    else:
        world = setup_default_scenario(world_size)

    print(f"\nWorld state: {world.get_state()}")

    # Create agent swarm
    swarm = AgentSwarm(
        world=world,
        population=20,
        spawn_mode='corner',  # Spawn in corner, must navigate to energy
    )
    print(f"Spawned {len(swarm.agents)} agents")

    # Setup visualization
    visualizer = WorldVisualizer(
        world=world,
        window_size=800,
        fps=30,
        show_phi=False,
        show_trails=True,
    )
    visualizer.set_agents(swarm)

    # Moving source state
    moving_step = 0
    original_sources = [s for s in world.energy_sources]

    def update_step(w):
        nonlocal moving_step, original_sources

        # Update pilot wave
        w.update_pilot_wave(dt=0.1)

        # Move energy sources in moving scenario
        if scenario == "moving":
            moving_step += 1
            if moving_step % 60 == 0:  # Every 60 steps (~2 seconds)
                w.energy_sources.clear()
                for x, y, strength in original_sources:
                    # Circular motion
                    angle = moving_step * 0.02
                    new_x = int(x + 20 * np.cos(angle))
                    new_y = int(y + 20 * np.sin(angle))
                    new_x = max(5, min(w.size - 5, new_x))
                    new_y = max(5, min(w.size - 5, new_y))
                    w.add_energy_source(new_x, new_y, strength)
                w.compute_potential_field()

    print("\nStarting visualization...")
    print("Controls:")
    print("  ESC - Exit")
    print("  P   - Toggle Phi/Coherence overlay")
    print("  T   - Toggle agent trails")
    print()

    visualizer.run(update_callback=update_step)

    # Print final stats
    stats = swarm.get_stats()
    print("\n" + "=" * 60)
    print("Simulation Complete")
    print("=" * 60)
    print(f"Agents alive: {stats['alive']}/{stats['total']}")
    print(f"Average steps: {stats.get('avg_steps', 0):.1f}")
    print(f"Max steps: {stats.get('max_steps', 0)}")
    print(f"Average energy: {stats.get('avg_energy', 0):.1f}")


def main():
    parser = argparse.ArgumentParser(
        description="QIWM Full Demo — Quantum-Inspired Agent Navigation"
    )
    parser.add_argument(
        '--maze',
        action='store_true',
        help='Run maze scenario (dead ends test)'
    )
    parser.add_argument(
        '--moving',
        action='store_true',
        help='Run moving energy sources scenario'
    )
    parser.add_argument(
        '--size',
        type=int,
        default=128,
        help='Grid size (default: 128)'
    )

    args = parser.parse_args()

    if args.maze:
        scenario = "maze"
    elif args.moving:
        scenario = "moving"
    else:
        scenario = "default"

    run_demo(scenario=scenario, world_size=args.size)


if __name__ == "__main__":
    main()
