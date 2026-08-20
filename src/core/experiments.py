"""
Module: src.core.experiments.py

Experimental framework for QIWM ablation studies and metrics collection.

Provides systematic comparison of quantum-inspired vs classical agent navigation
across multiple scenarios with statistical validation.

Usage:
    from src.core.experiments import run_ablation_study
    results = run_ablation_study(scenario='maze', runs=10)
"""

import csv
import numpy as np
from typing import List, Dict, Tuple, Optional
from .toy_world import ToyWorld
from .quantum_world import QuantumInspiredWorld
from .agents import NanoAgent, AgentSwarm


class ExperimentConfig:
    """Configuration for a single experiment run."""

    def __init__(
        self,
        scenario: str = 'default',
        world_size: int = 128,
        quantum_coupling: float = 0.3,
        diffusion_rate: float = 0.2,
        collapse_enabled: bool = True,
        agent_population: int = 20,
        spawn_mode: str = 'corner',
        max_steps: int = 500,
        seed: Optional[int] = None,
        barrier_x: Optional[int] = None,
        classical_epsilon: float = 0.0,
    ):
        self.scenario = scenario
        self.world_size = world_size
        self.quantum_coupling = quantum_coupling
        self.diffusion_rate = diffusion_rate
        self.collapse_enabled = collapse_enabled
        self.agent_population = agent_population
        self.spawn_mode = spawn_mode
        self.max_steps = max_steps
        self.seed = seed
        self.barrier_x = barrier_x
        self.classical_epsilon = classical_epsilon


class ExperimentMetrics:
    """Metrics collected from a single experiment run."""

    def __init__(self, config: ExperimentConfig):
        self.config = config
        self.agent_survival_times: List[int] = []
        self.agent_steps: List[int] = []
        self.agent_final_energy: List[float] = []
        self.agent_paths_to_energy: List[float] = []
        self.deadend_escapes: int = 0
        self.barrier_crossings: int = 0
        self.first_crossing_latencies: List[float] = []
        self.crossings_toward: int = 0
        self.crossings_total: int = 0
        self.wall_crossings: int = 0
        self.seam_crossings: int = 0
        self.world_coherence_history: List[float] = []
        self.pilot_wave_history: List[float] = []

    def to_dict(self) -> dict:
        alive_count = len([t for t in self.agent_survival_times if t >= self.config.max_steps])
        return {
            'scenario': self.config.scenario,
            'quantum_coupling': self.config.quantum_coupling,
            'diffusion_rate': self.config.diffusion_rate,
            'collapse_enabled': self.config.collapse_enabled,
            'population': self.config.agent_population,
            'max_steps': self.config.max_steps,
            'seed': self.config.seed,
            'alive_count': alive_count,
            'alive_rate': alive_count / len(self.agent_survival_times) if self.agent_survival_times else 0,
            'avg_survival_steps': np.mean(self.agent_survival_times) if self.agent_survival_times else 0,
            'max_survival_steps': max(self.agent_survival_times) if self.agent_survival_times else 0,
            'avg_final_energy': np.mean(self.agent_final_energy) if self.agent_final_energy else 0,
            'avg_steps_taken': np.mean(self.agent_steps) if self.agent_steps else 0,
            'deadend_escapes': self.deadend_escapes,
            'barrier_crossings': self.barrier_crossings,
            'first_crossing_latency_mean': (float(np.mean(self.first_crossing_latencies))
                                             if self.first_crossing_latencies else float('nan')),
            'first_crossing_latency_median': (float(np.median(self.first_crossing_latencies))
                                               if self.first_crossing_latencies else float('nan')),
            'crossing_toward_frac': (self.crossings_toward / self.crossings_total
                                     if self.crossings_total else float('nan')),
            'wall_crossings': self.wall_crossings,
            'seam_crossings': self.seam_crossings,
            'final_coherence_mean': self.world_coherence_history[-1] if self.world_coherence_history else 0,
            'final_pilot_wave_mean': self.pilot_wave_history[-1] if self.pilot_wave_history else 0,
        }


def create_scenario_world(
    scenario: str,
    world_size: int,
    quantum_coupling: float,
    diffusion_rate: float,
    classical_epsilon: float = 0.0,
) -> QuantumInspiredWorld:
    """Create a world configured for a specific scenario."""
    world = QuantumInspiredWorld(
        size=world_size,
        quantum_coupling=quantum_coupling,
        diffusion_rate=diffusion_rate,
        pilot_wave_gain=3000.0,
        classical_epsilon=classical_epsilon,
    )

    if scenario == 'default':
        # Multiple energy sources with obstacles
        world.add_energy_source(30, 30, strength=100.0)
        world.add_energy_source(90, 90, strength=80.0)
        world.add_energy_source(60, 20, strength=60.0)
        world.add_obstacle(60, 60, radius=15.0)
        world.add_obstacle(45, 75, radius=8.0)
        world.add_obstacle(80, 45, radius=8.0)

    elif scenario == 'maze':
        # Maze with real dead ends
        # Goal: energy source in bottom-right corner
        world.add_energy_source(110, 110, strength=100.0)

        # Dead-end corridor (top-left area): gradient descent leads here
        # but there's no exit. Pilot wave should leak through walls.
        # Agents spawn at (0,0) area and gradient pulls them toward this trap
        dead_end_center = (30, 30)
        # Top wall of dead end
        for x in range(10, 50, 2):
            world.add_obstacle(x, 15, radius=2.0)
        # Left wall of dead end
        for y in range(15, 50, 2):
            world.add_obstacle(10, y, radius=2.0)
        # Right wall of dead end (with NO gap - true dead end)
        for y in range(15, 50, 2):
            world.add_obstacle(50, y, radius=2.0)
        # Bottom wall of dead end (with gap at x=30-35 - narrow exit)
        for x in range(10, 50, 2):
            if not (28 <= x <= 35):
                world.add_obstacle(x, 50, radius=2.0)

        # Main path wall: blocks direct route to goal, forces through maze
        for x in range(55, 120, 2):
            world.add_obstacle(x, 60, radius=2.0)

        # Vertical wall with gap leading to goal
        for y in range(65, 120, 2):
            if not (90 <= y <= 100):
                world.add_obstacle(80, y, radius=2.0)

    elif scenario == 'tunnel':
        # Solid wall with NO gap. Energy source on the far side.
        # Classical agents are trapped by wall repulsion; quantum agents
        # should feel the pilot wave leaking through the wall.
        world.add_energy_source(96, 96, strength=100.0)
        for y in range(world_size):
            world.add_obstacle(64, y, radius=2.0)

    elif scenario == 'moving':
        # Moving energy sources (positions updated externally)
        world.add_energy_source(30, 30, strength=100.0)
        world.add_energy_source(90, 30, strength=80.0)
        world.add_energy_source(60, 90, strength=90.0)
        world.add_obstacle(60, 60, radius=12.0)

    elif scenario == 'single_source':
        # Simple: one source, one obstacle — baseline comparison
        world.add_energy_source(100, 100, strength=100.0)
        world.add_obstacle(50, 50, radius=15.0)

    world.compute_potential_field()
    return world


def run_single_experiment(config: ExperimentConfig) -> ExperimentMetrics:
    """Run a single experiment and collect metrics."""
    # Set random seed if provided
    if config.seed is not None:
        np.random.seed(config.seed)

    # Create world and agents
    world = create_scenario_world(
        config.scenario,
        config.world_size,
        config.quantum_coupling,
        config.diffusion_rate,
        config.classical_epsilon,
    )

    # Prewarm the pilot wave so the diffusive field is established before
    # agents arrive (the world exists before observation begins)
    for _ in range(2000):
        world.update_pilot_wave(dt=config.diffusion_rate)

    swarm = AgentSwarm(world, config.agent_population, config.spawn_mode)
    metrics = ExperimentMetrics(config)

    # Simulation loop
    for step in range(config.max_steps):
        # Update pilot wave
        world.update_pilot_wave(dt=config.diffusion_rate)

        # Moving scenario: update energy sources periodically
        if config.scenario == 'moving' and step % 60 == 0 and step > 0:
            world.energy_sources.clear()
            angle = step * 0.02
            for base_x, base_y, strength in [(30, 30, 100), (90, 30, 80), (60, 90, 90)]:
                new_x = int(base_x + 20 * np.cos(angle))
                new_y = int(base_y + 20 * np.sin(angle))
                new_x = max(5, min(world.size - 5, new_x))
                new_y = max(5, min(world.size - 5, new_y))
                world.add_energy_source(new_x, new_y, strength)
            world.compute_potential_field()

        # Step agents
        for agent in swarm.agents:
            if not agent.alive:
                continue

            # Store position before step for dead-end detection
            old_x, old_y = agent.x, agent.y

            # Apply collapse only if enabled
            if config.collapse_enabled and hasattr(world, 'collapse_field'):
                agent.step()
            else:
                # Step without collapse
                dx, dy = agent.decide_action()
                new_x = (agent.x + dx) % world.size
                new_y = (agent.y + dy) % world.size
                agent.x = new_x
                agent.y = new_y
                agent.x_traj.append(agent.x)
                agent.steps_taken += 1
                agent.trail.append((agent.x, agent.y))
                if len(agent.trail) > agent.max_trail_length:
                    agent.trail = agent.trail[-agent.max_trail_length:]
                agent.energy -= agent.movement_cost
                agent._check_energy_sources()
                if agent.energy <= 0:
                    agent.alive = False

            # Dead-end detection: use agent's built-in detection
            if step > 30:
                agent.check_dead_end_status(window=20, stuck_threshold=5)

        # Record world state periodically
        if step % 50 == 0:
            metrics.world_coherence_history.append(float(world.coherence.mean()))
            metrics.pilot_wave_history.append(float(world.pilot_wave.mean()))

        # Check if all agents dead
        if not swarm.get_alive_agents():
            break

    # Collect final metrics
    for agent in swarm.agents:
        metrics.agent_survival_times.append(agent.steps_taken)
        metrics.agent_steps.append(agent.steps_taken)
        metrics.agent_final_energy.append(agent.energy)

        # Path to nearest energy source
        if agent.alive and world.energy_sources:
            min_dist = min(
                np.sqrt((agent.x - ex)**2 + (agent.y - ey)**2)
                for ex, ey, _ in world.energy_sources
            )
            metrics.agent_paths_to_energy.append(min_dist)

    # Collect dead-end escape stats
    for agent in swarm.agents:
        metrics.deadend_escapes += agent.dead_end_escapes

    # Barrier crossings (tunnel scenario): agents that got past the wall
    if config.barrier_x is not None:
        metrics.barrier_crossings = sum(
            1 for agent in swarm.agents if agent.x > config.barrier_x
        )

        # First-crossing taxonomy per agent. The x=64 wall on a 128-torus
        # does NOT separate the surface: the x=0/127 seam is a passage
        # around it. Distinguish (a) genuine wall jumps (63<->65, i.e.
        # pilot-wave/noise tunneling through the spike) from (b) seam
        # wraps (x<=1 <-> x>=size-2, going around the loop). Latency is
        # measured from first arrival at the wall-adjacent cell (wall
        # crossings) or first arrival at the seam (seam wraps).
        bx = config.barrier_x
        size = world.size
        src_xs = [ex for ex, _ey, _s in world.energy_sources]
        src_side = 1.0 if (src_xs and np.mean(src_xs) > bx) else -1.0
        adj = bx - 1 if src_side > 0 else bx + 1
        for agent in swarm.agents:
            traj = agent.x_traj
            if len(traj) < 2:
                continue
            cross_i, kind = None, None
            for i in range(1, len(traj)):
                p, c = traj[i - 1], traj[i]
                if {p, c} == {bx - 1, bx + 1}:
                    cross_i, kind = i, 'wall'
                    break
                if (p <= 1 and c >= size - 2) or (p >= size - 2 and c <= 1):
                    cross_i, kind = i, 'seam'
                    break
            if cross_i is None:
                continue
            metrics.crossings_total += 1
            if kind == 'wall':
                metrics.wall_crossings += 1
            else:
                metrics.seam_crossings += 1
            cdir = 1.0 if traj[cross_i] > traj[cross_i - 1] else -1.0
            if kind == 'seam':
                cdir = 1.0 if traj[cross_i] >= size - 2 else -1.0
            if cdir == src_side:
                metrics.crossings_toward += 1
            if kind == 'wall':
                arrive_i = next((i for i, v in enumerate(traj) if v == adj), None)
            else:
                arrive_i = next(
                    (i for i, v in enumerate(traj)
                     if v <= 1 or v >= size - 2), None)
            if arrive_i is not None and arrive_i < cross_i:
                metrics.first_crossing_latencies.append(cross_i - arrive_i)

    return metrics


def run_ablation_study(
    scenario: str = 'maze',
    couplings: List[float] = None,
    runs_per_config: int = 10,
    with_collapse: bool = True,
    without_collapse: bool = True,
) -> Dict[str, List[ExperimentMetrics]]:
    """
    Run ablation study comparing quantum couplings and collapse mechanics.

    Args:
        scenario: Scenario name ('default', 'maze', 'moving', 'single_source')
        couplings: List of quantum coupling values to test
        runs_per_config: Number of runs per configuration (for statistics)
        with_collapse: Run experiments with collapse enabled
        without_collapse: Run experiments with collapse disabled

    Returns:
        Dictionary mapping config descriptions to lists of metrics
    """
    if couplings is None:
        couplings = [0.0, 0.1, 0.3, 0.5]

    results = {}

    for coupling in couplings:
        for collapse_enabled, collapse_label in [
            (True, 'collapse'),
            (False, 'nocollapse'),
        ]:
            if collapse_enabled and not with_collapse:
                continue
            if not collapse_enabled and not without_collapse:
                continue

            config_key = f"{scenario}_q{coupling:.1f}_{collapse_label}"
            results[config_key] = []

            for run_idx in range(runs_per_config):
                config = ExperimentConfig(
                    scenario=scenario,
                    quantum_coupling=coupling,
                    collapse_enabled=collapse_enabled,
                    seed=run_idx * 1000 + int(coupling * 100),
                    barrier_x=64 if scenario == 'tunnel' else None,
                )
                metrics = run_single_experiment(config)
                results[config_key].append(metrics)

    return results


def aggregate_results(
    results: Dict[str, List[ExperimentMetrics]]
) -> Dict[str, Dict[str, float]]:
    """
    Aggregate metrics across runs for each configuration.

    Returns:
        Dictionary mapping config descriptions to aggregated stats (mean ± std)
    """
    aggregated = {}

    for config_key, metrics_list in results.items():
        if not metrics_list:
            continue

        stats = {}
        for metric_name in [
            'alive_rate', 'avg_survival_steps', 'max_survival_steps',
            'avg_final_energy', 'avg_steps_taken',
        ]:
            values = [m.to_dict()[metric_name] for m in metrics_list]
            stats[f'{metric_name}_mean'] = float(np.mean(values))
            stats[f'{metric_name}_std'] = float(np.std(values))

        aggregated[config_key] = stats

    return aggregated


def export_to_csv(
    results: Dict[str, List[ExperimentMetrics]],
    filename: str = 'experiment_results.csv',
) -> None:
    """Export experiment results to CSV file."""
    rows = []
    for config_key, metrics_list in results.items():
        for metrics in metrics_list:
            rows.append(metrics.to_dict())

    if not rows:
        return

    fieldnames = list(rows[0].keys())
    with open(filename, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def print_summary(
    results: Dict[str, List[ExperimentMetrics]]
) -> None:
    """Print a summary table of aggregated results."""
    aggregated = aggregate_results(results)

    print("\n" + "=" * 80)
    print("ABSTRACTION STUDY RESULTS")
    print("=" * 80)

    # Column headers
    header = f"{'Config':<25} {'Alive%':>7} {'AvgSteps':>9} {'MaxSteps':>9} {'AvgEnergy':>9}"
    print(header)
    print("-" * 80)

    for config_key in sorted(aggregated.keys()):
        stats = aggregated[config_key]
        alive_pct = stats['alive_rate_mean'] * 100
        avg_steps = stats['avg_survival_steps_mean']
        max_steps = stats['max_survival_steps_mean']
        avg_energy = stats['avg_final_energy_mean']

        print(f"{config_key:<25} {alive_pct:>6.1f}% {avg_steps:>9.1f} {max_steps:>9.1f} {avg_energy:>9.1f}")

    print("=" * 80)

    # Highlight best vs worst (classical baseline)
    classical_key = None
    for key in aggregated:
        if '_q0.0_' in key:
            classical_key = key
            break

    if classical_key:
        classical = aggregated[classical_key]
        best_key = None
        best_alive = 0
        for key, stats in aggregated.items():
            if stats['alive_rate_mean'] > best_alive:
                best_alive = stats['alive_rate_mean']
                best_key = key

        if best_key and best_key != classical_key:
            improvement = (best_alive - classical['alive_rate_mean']) / classical['alive_rate_mean'] * 100 if classical['alive_rate_mean'] > 0 else 0
            print(f"\nBest: {best_key} ({best_alive*100:.1f}% alive)")
            print(f"Classical baseline: {classical_key} ({classical['alive_rate_mean']*100:.1f}% alive)")
            print(f"Improvement: {improvement:+.1f}%")
