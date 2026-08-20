"""
Module: src\visualization\visualizer.py
Depends on:
  - src.core.toy_world (ToyWorld)

Visualization module for QIWM using Pygame.

Provides real-time rendering of the potential field and world state.
"""

import numpy as np
import pygame
from typing import Optional, Tuple, List, Union
import matplotlib.pyplot as plt
from matplotlib import cm

from src.core import NanoAgent, AgentSwarm


class WorldVisualizer:
    """
    Real-time visualization of QIWM using Pygame.

    Displays the potential/guidance field as a heatmap, markers for
    energy sources and obstacles, and agent sprites with trails.
    """

    def __init__(
        self,
        world,
        window_size: int = 800,
        fps: int = 30,
        show_phi: bool = False,
        show_trails: bool = True,
    ):
        """
        Initialize the visualizer.

        Args:
            world: ToyWorld or QuantumInspiredWorld instance
            window_size: Size of the display window in pixels
            fps: Target frames per second
            show_phi: Show coherence/phi overlay
            show_trails: Show agent movement trails
        """
        self.world = world
        self.window_size = window_size
        self.fps = fps
        self.scale = window_size / world.size
        self.show_phi = show_phi
        self.show_trails = show_trails

        # Initialize Pygame
        pygame.init()
        self.screen = pygame.display.set_mode((window_size, window_size))
        pygame.display.set_caption("QIWM - Quantum-Inspired World Model")
        self.clock = pygame.time.Clock()

        # Color mapping
        self.colormap = cm.get_cmap('viridis')
        self.phi_colormap = cm.get_cmap('plasma')

        # Pre-render surface for field (avoids per-pixel Python loops)
        self.field_surface = pygame.Surface((window_size, window_size))

        self.agents: List[NanoAgent] = []
        self.swarm: Optional[AgentSwarm] = None
        self.running = False

        # Interactive mode state
        self.interactive_mode = True  # Enable click interactions
        self.obstacle_radius = 8.0
        self.energy_strength = 100.0

        # Save initial world state for reset
        self._initial_world_state = {
            'sources': list(world.energy_sources),
            'obstacles': list(world.obstacles),
        }

    def field_to_color(self, value: float, vmin: float, vmax: float) -> Tuple[int, int, int]:
        """
        Convert a field value to RGB color using colormap.

        Args:
            value: Field value
            vmin: Minimum field value for normalization
            vmax: Maximum field value for normalization

        Returns:
            RGB tuple (0-255)
        """
        if vmax > vmin:
            normalized = (value - vmin) / (vmax - vmin)
        else:
            normalized = 0.5

        normalized = np.clip(normalized, 0.0, 1.0)
        rgba = self.colormap(normalized)
        return (int(rgba[0] * 255), int(rgba[1] * 255), int(rgba[2] * 255))

    def set_agents(self, agents_or_swarm: Union[List[NanoAgent], AgentSwarm]) -> None:
        """
        Set agents to visualize.

        Args:
            agents_or_swarm: List of NanoAgent or AgentSwarm instance
        """
        if isinstance(agents_or_swarm, AgentSwarm):
            self.swarm = agents_or_swarm
            self.agents = agents_or_swarm.agents
        else:
            self.agents = agents_or_swarm
            self.swarm = None

    def render_field(self) -> None:
        """Render the potential field as a heatmap (vectorized)."""
        # Get field data
        if hasattr(self.world, 'get_guidance_field'):
            field = self.world.get_guidance_field()
        else:
            field = self.world.grid

        if self.show_phi and hasattr(self.world, 'coherence'):
            field = self.world.coherence

        vmin, vmax = field.min(), field.max()

        # Normalize to [0, 1]
        if vmax > vmin:
            normalized = (field - vmin) / (vmax - vmin)
        else:
            normalized = np.ones_like(field) * 0.5

        # Map to RGB using colormap
        cmap = self.phi_colormap if self.show_phi else self.colormap
        rgba = cmap(normalized)
        rgb = (rgba[:, :, :3] * 255).astype(np.uint8)

        # pygame.surfarray expects (width, height, 3) = (x, y, rgb)
        # numpy array is (x, y, rgb) already from meshgrid indexing='ij'
        # but imshow-style needs transpose. Here field is (x, y), so rgb is (x, y, 3)
        # pygame wants (width, height, 3) = (x, y, 3) — same!
        # But we need to flip Y because pygame origin is top-left
        rgb_flipped = np.flipud(rgb)

        # Create surface from array (vectorized, no Python loops)
        self.field_surface = pygame.surfarray.make_surface(rgb_flipped)
        self.field_surface = pygame.transform.scale(self.field_surface, (self.window_size, self.window_size))
        self.screen.blit(self.field_surface, (0, 0))

    def render_energy_sources(self) -> None:
        """Render energy sources as bright circles."""
        for ex, ey, strength in self.world.energy_sources:
            center = (
                int((ex + 0.5) * self.scale),
                int((ey + 0.5) * self.scale)
            )
            radius = max(3, int(strength * 5))

            # Outer glow
            pygame.draw.circle(self.screen, (255, 255, 100), center, radius + 2)
            # Inner core
            pygame.draw.circle(self.screen, (255, 255, 255), center, radius)

    def render_obstacles(self) -> None:
        """Render obstacles as dark circles."""
        for ox, oy, obstacle_radius in self.world.obstacles:
            center = (
                int((ox + 0.5) * self.scale),
                int((oy + 0.5) * self.scale)
            )
            radius = int(obstacle_radius * self.scale)

            # Outer edge
            pygame.draw.circle(self.screen, (100, 0, 0), center, radius + 2)
            # Inner dark core
            pygame.draw.circle(self.screen, (20, 20, 20), center, radius)

    def render_agents(self) -> None:
        """Render all agents as circles with optional trails."""
        if not self.agents:
            return

        for agent in self.agents:
            if not agent.alive:
                continue

            center = (
                int((agent.x + 0.5) * self.scale),
                int((agent.y + 0.5) * self.scale)
            )
            radius = max(2, int(self.scale * 0.8))

            # Draw trail
            if self.show_trails and len(agent.trail) > 1:
                trail_points = [
                    (int((tx + 0.5) * self.scale), int((ty + 0.5) * self.scale))
                    for tx, ty in agent.trail[-50:]
                ]
                if len(trail_points) > 1:
                    pygame.draw.lines(
                        self.screen,
                        (100, 200, 255, 128),
                        False,
                        trail_points,
                        max(1, int(self.scale * 0.3))
                    )

            # Color based on energy
            energy_ratio = min(1.0, agent.energy / 100.0)
            color = (
                int(255 * energy_ratio),
                int(255 * (1.0 - energy_ratio)),
                200
            )

            # Draw agent
            pygame.draw.circle(self.screen, color, center, radius)
            pygame.draw.circle(self.screen, (255, 255, 255), center, radius, 1)

    def render_info(self) -> None:
        """Render information overlay."""
        font = pygame.font.Font(None, 24)
        state = self.world.get_state()

        info_lines = [
            f"Grid: {state['size']}x{state['size']}",
            f"Energy Sources: {state['num_energy_sources']}",
            f"Obstacles: {state['num_obstacles']}",
            f"View: {'Phi/Coherence' if self.show_phi else 'Guidance Field'}",
        ]

        # Add quantum-specific info
        if hasattr(self.world, 'pilot_wave'):
            info_lines.append(
                f"Pilot Wave: [{self.world.pilot_wave.min():.2f}, {self.world.pilot_wave.max():.2f}]"
            )
            info_lines.append(
                f"Coherence: [{self.world.coherence.min():.2f}, {self.world.coherence.max():.2f}]"
            )
            info_lines.append(f"Quantum Coupling: {self.world.quantum_coupling:.2f}")

        # Add agent info
        if self.swarm:
            stats = self.swarm.get_stats()
            info_lines.append(f"Agents: {stats['alive']}/{stats['total']} alive")
            info_lines.append(f"Avg Energy: {stats.get('avg_energy', 0):.1f}")
            info_lines.append(f"Avg Steps: {stats.get('avg_steps', 0):.1f}")

        info_lines.append(f"FPS: {int(self.clock.get_fps())}")
        info_lines.append("[ESC] Exit | [P] Phi | [T] Trails | [R] Reset | [L/R] Coupling")
        info_lines.append("[L-Click] Add Energy | [R-Click] Add Obstacle")

        y_offset = 10
        for line in info_lines:
            text_surface = font.render(line, True, (255, 255, 255))
            # Background for readability
            bg_rect = text_surface.get_rect()
            bg_rect.topleft = (10, y_offset)
            bg_rect.inflate_ip(10, 4)
            pygame.draw.rect(self.screen, (0, 0, 0), bg_rect)

            self.screen.blit(text_surface, (10, y_offset))
            y_offset += 25

    def render(self) -> None:
        """Render a single frame."""
        self.render_field()
        self.render_agents()
        self.render_obstacles()
        self.render_energy_sources()
        self.render_info()
        pygame.display.flip()

    def run(self, update_callback: Optional[callable] = None) -> None:
        """
        Run the visualization loop.

        Args:
            update_callback: Optional function to call each frame for world updates
        """
        self.running = True

        while self.running:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                    elif event.key == pygame.K_p:
                        self.show_phi = not self.show_phi
                    elif event.key == pygame.K_t:
                        self.show_trails = not self.show_trails
                    elif event.key == pygame.K_r:
                        self._reset_world()
                    elif event.key == pygame.K_l:
                        self._adjust_coupling(-0.05)
                    elif event.key == pygame.K_r:
                        self._adjust_coupling(0.05)
                elif event.type == pygame.MOUSEBUTTONDOWN and self.interactive_mode:
                    if event.button == 1:  # Left click - add energy source
                        self._add_energy_at_click(event.pos)
                    elif event.button == 3:  # Right click - add obstacle
                        self._add_obstacle_at_click(event.pos)

            # Update world if callback provided
            if update_callback:
                update_callback(self.world)

            # Step agents if swarm exists
            if self.swarm:
                self.swarm.step_all()

            # Render
            self.render()
            self.clock.tick(self.fps)

        pygame.quit()

    def _screen_to_world(self, pos: Tuple[int, int]) -> Tuple[int, int]:
        """Convert screen coordinates to world coordinates."""
        x = int(pos[0] / self.scale)
        y = int(pos[1] / self.scale)
        return (max(0, min(self.world.size - 1, x)),
                max(0, min(self.world.size - 1, y)))

    def _add_energy_at_click(self, pos: Tuple[int, int]) -> None:
        """Add an energy source at click position."""
        x, y = self._screen_to_world(pos)
        self.world.add_energy_source(x, y, self.energy_strength)
        self.world.compute_potential_field()

    def _add_obstacle_at_click(self, pos: Tuple[int, int]) -> None:
        """Add an obstacle at click position."""
        x, y = self._screen_to_world(pos)
        self.world.add_obstacle(x, y, self.obstacle_radius)
        self.world.compute_potential_field()

    def _adjust_coupling(self, delta: float) -> None:
        """Adjust quantum coupling strength."""
        if hasattr(self.world, 'quantum_coupling'):
            self.world.quantum_coupling = max(0.0, min(1.0, self.world.quantum_coupling + delta))

    def _reset_world(self) -> None:
        """Reset world to initial state."""
        # Clear current state
        self.world.clear()
        # Restore initial configuration
        for x, y, s in self._initial_world_state['sources']:
            self.world.add_energy_source(x, y, s)
        for x, y, r in self._initial_world_state['obstacles']:
            self.world.add_obstacle(x, y, r)
        self.world.compute_potential_field()

        # Reset agents if swarm exists
        if self.swarm:
            self.swarm._spawn_agents(self.swarm.get_stats()['total'], 'corner')

    def save_snapshot(self, filename: str) -> None:
        """
        Save current visualization as an image.

        Args:
            filename: Output filename (PNG format)
        """
        pygame.image.save(self.screen, filename)
        print(f"Snapshot saved to {filename}")


def export_field_matplotlib(world, filename: str = "potential_field.png") -> None:
    """
    Export the potential field as a high-quality matplotlib figure.

    Args:
        world: ToyWorld instance
        filename: Output filename
    """
    fig, ax = plt.subplots(figsize=(10, 8))

    # Plot potential field as heatmap
    im = ax.imshow(world.grid.T, origin='lower', cmap='viridis', interpolation='bilinear')
    plt.colorbar(im, ax=ax, label='Potential')

    # Mark energy sources
    if world.energy_sources:
        ex_coords = [ex for ex, ey, s in world.energy_sources]
        ey_coords = [ey for ex, ey, s in world.energy_sources]
        ax.scatter(ex_coords, ey_coords, c='yellow', s=100, marker='*',
                   edgecolors='white', linewidths=2, label='Energy Sources')

    # Mark obstacles
    if world.obstacles:
        for ox, oy, radius in world.obstacles:
            circle = plt.Circle((ox, oy), radius, color='red', fill=True,
                                alpha=0.5, label='Obstacle' if ox == world.obstacles[0][0] else '')
            ax.add_patch(circle)

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_title('Classical Potential Field Visualization')
    ax.legend()
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(filename, dpi=150)
    plt.close()
    print(f"High-quality export saved to {filename}")
