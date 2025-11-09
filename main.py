"""
QIWM - Quantum-Inspired World Model
Main entry point for running simulations

Usage:
    python main.py              # Run interactive demo
    python main.py --export     # Export visualizations only
    python main.py --help       # Show help
"""

import sys
import argparse
from src.core import ToyWorld
from src.visualization import WorldVisualizer, export_field_matplotlib


def run_interactive_demo():
    """Run the interactive Pygame visualization."""
    print("=" * 60)
    print("QIWM Phase 1: Interactive Demo")
    print("=" * 60)
    print("\nInitializing world...")

    # Create and setup world
    world = ToyWorld(size=128)

    # Add example configuration
    world.add_energy_source(30, 30, strength=100.0)
    world.add_energy_source(90, 90, strength=80.0)
    world.add_obstacle(60, 60, radius=15.0)

    # Compute potential
    world.compute_potential_field()

    print("World state:", world.get_state())
    print("\nStarting visualization (Press ESC to exit)...")

    # Run visualization
    visualizer = WorldVisualizer(world, window_size=800, fps=30)
    visualizer.run()

    print("\nDemo completed!")


def run_export_mode():
    """Export visualization as static images."""
    print("=" * 60)
    print("QIWM Phase 1: Export Mode")
    print("=" * 60)

    world = ToyWorld(size=128)

    # Example scenario
    print("\nGenerating example potential field...")
    world.add_energy_source(64, 64, strength=100.0)
    world.add_obstacle(32, 32, radius=10.0)
    world.add_obstacle(96, 96, radius=10.0)
    world.compute_potential_field()

    filename = "qiwm_potential_field.png"
    export_field_matplotlib(world, filename)
    print(f"\nVisualization exported to: {filename}")


def main():
    """Main entry point with argument parsing."""
    parser = argparse.ArgumentParser(
        description="Quantum-Inspired World Model (QIWM) - Phase 1",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python main.py                    # Interactive visualization
    python main.py --export           # Export static image
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
            run_interactive_demo()
    except KeyboardInterrupt:
        print("\n\nInterrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\nError: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
