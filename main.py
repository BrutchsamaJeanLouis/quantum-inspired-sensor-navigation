#!/usr/bin/env python3
"""
QIWM: Quantum-Inspired World Model
Phase 1-4 Complete Demo

Interactive:
    python main.py
    python main.py --scenario maze
    python main.py --seed 7

Timeline controls (in the window):
    Space      pause / resume
    Left/Right scrub +/-1 tick (Shift = +/-10)
    Home       seek to tick 0
    bottom slider  drag to scrub 0..500 ticks

Replay mode (screenshot each tick hop, then pause for ESC):
    python main.py --scenario tunnel --replay 0 30 60 90

Headless single-tick render (the LLM primitive):
    python main.py --scenario maze --seed 42 --shot 150 --out tick150.png
    # rewind/replay determinism: --seed fixed => tick N is reproducible
"""

import argparse
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import numpy as np
import pygame

from src.core.toy_world import ToyWorld
from src.core.quantum_world import QuantumInspiredWorld
from src.core.agents import AgentSwarm
from src.core.timeline import TimelinePlayer
from src.visualization import WorldVisualizer


def setup_world() -> QuantumInspiredWorld:
    """Setup default world (3 sources, 5 obstacles)."""
    print("Setting up Quantum-Inspired World (Phase 2)...")
    world = QuantumInspiredWorld(
        size=128,
        quantum_coupling=0.5,
        diffusion_rate=0.15
    )
    # Classic setup: 3 energy sources
    world.add_energy_source(30, 30, strength=100.0)
    world.add_energy_source(90, 30, strength=80.0)
    world.add_energy_source(60, 90, strength=120.0)
    # Obstacles
    world.add_obstacle(40, 40, radius=3.0)
    world.add_obstacle(80, 80, radius=4.0)
    world.add_obstacle(60, 60, radius=2.5)
    world.add_obstacle(20, 90, radius=3.5)
    world.add_obstacle(100, 60, radius=3.0)
    world.compute_potential_field()
    print(f"World created: {world.size}x{world.size}")
    return world


def setup_maze_world() -> QuantumInspiredWorld:
    """Setup maze world with walls and a single source."""
    print("Setting up Quantum-Inspired World (maze scenario)...")
    world = QuantumInspiredWorld(
        size=128,
        quantum_coupling=0.5,
        diffusion_rate=0.15
    )
    # Single source far away
    world.add_energy_source(110, 110, strength=150.0)
    # Maze walls (vertical bars with gaps)
    for x in range(20, 110, 3):
        if not (60 <= x <= 75):  # gap for tunnel
            world.add_obstacle(x, 40, radius=2.5)
            world.add_obstacle(x, 70, radius=2.5)
    return world


def build_world_and_swarm(scenario: str, population: int = 20):
    """Fresh t=0 (world, swarm) pair for the given scenario (TimelinePlayer factory)."""
    if scenario == 'maze':
        world = setup_maze_world()
    else:
        world = setup_world()
    swarm = AgentSwarm(world, population=population, spawn_mode='corner')
    print(f"Spawned {swarm.get_stats()['total']} agents")
    return world, swarm


def parse_args():
    parser = argparse.ArgumentParser(description='QIWM Interactive Demo')
    parser.add_argument('--scenario', choices=['default', 'maze'], default='default',
                        help='Demo scenario (default: default)')
    parser.add_argument('--seed', type=int, default=42,
                        help='RNG seed for deterministic replay (default: 42)')
    parser.add_argument('--replay', type=int, nargs='+', metavar='TICK',
                        help='Open window, hop to each listed tick (screenshot each), pause')
    parser.add_argument('--shot', type=int, metavar='TICK',
                        help='Headless: render the given tick to --out and exit')
    parser.add_argument('--out', type=str, default='qiwm_tick.png',
                        help='Output PNG for --shot (default: qiwm_tick.png)')
    return parser.parse_args()


def run_shot_mode(player: TimelinePlayer, out_path: str) -> None:
    """Headless single-tick render: seek, draw one frame, save PNG."""
    os.environ['SDL_VIDEODRIVER'] = 'dummy'
    vis = WorldVisualizer(player.world, window_size=800, fps=30, player=player)
    vis.render()
    vis.save_snapshot(out_path)
    print(f"Tick {player.tick} saved to {out_path}")
    pygame.quit()


def run_replay_mode(player: TimelinePlayer, ticks: list, window_size: int = 800) -> None:
    """Open the window, hop between the listed ticks (one frame each), then pause.

    This is the LLM-driven path: an operator (or a screenshot loop) can watch
    the state at any chosen ticks, then the window sits paused for ESC.
    """
    vis = WorldVisualizer(player.world, window_size=window_size, fps=30, player=player)
    for tick in ticks:
        player.seek(tick)
        vis._sync_player()
        vis.render()
        time.sleep(0.3)
    vis.playing = False
    print("Replay done - window paused. Press Space to play, arrows to scrub, ESC to exit.")
    vis.run()


def main() -> None:
    """Main entry point: interactive demo with a scrubbable timeline."""
    args = parse_args()
    print("=" * 60)
    print("QIWM: Quantum-Inspired World Model - Interactive Demo")
    print(f"Scenario: {args.scenario}")
    print(f"Seed: {args.seed}")
    print("=" * 60)

    player = TimelinePlayer(
        factory=lambda: build_world_and_swarm(args.scenario),
        seed=args.seed,
    )
    print(f"World state: {player.world.get_state()}")

    if args.shot is not None:
        player.seek(args.shot)
        run_shot_mode(player, args.out)
        return

    if args.replay:
        run_replay_mode(player, args.replay)
        return

    # Interactive: window with Space/arrows/slider timeline controls
    print("Controls:")
    print("  ESC - Exit")
    print("  P   - Toggle Phi/Coherence overlay")
    print("  T   - Toggle agent trails")
    print("  R   - Reset to tick 0 (pauses)")
    print("  L/U - Adjust coupling")
    print("  Space - Pause / resume")
    print("  Left/Right - Scrub ticks (Shift = x10)")
    print("  Home - Seek to tick 0")
    print("  Bottom slider - Drag to scrub tick")
    print()

    vis = WorldVisualizer(player.world, window_size=800, fps=30, player=player)
    print("Starting visualization...")
    vis.run()

    print()
    print("=" * 60)
    print("Simulation Complete")
    stats = player.stats()
    print(f"Final tick: {stats['tick']}")
    print(f"Agents alive: {stats['alive']}/{stats['population']}")
    print(f"Average steps: {stats['avg_steps']:.1f}")
    print("=" * 60)


if __name__ == '__main__':
    main()