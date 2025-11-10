"""
Module: src\visualization\visualizer.py
Depends on:
  - src.core.toy_world (ToyWorld)

Visualization module for QIWM using Pygame.

Provides real-time rendering of the potential field and world state.
"""

import numpy as np
import pygame
from typing import Optional, Tuple
import matplotlib.pyplot as plt
from matplotlib import cm


class WorldVisualizer:
    """
    Real-time visualization of the ToyWorld using Pygame.

    Displays the potential field as a heatmap and markers for
    energy sources and obstacles.
    """

    def __init__(self, world, window_size: int = 800, fps: int = 30):
        """
        Initialize the visualizer.

        Args:
            world: ToyWorld instance to visualize
            window_size: Size of the display window in pixels
            fps: Target frames per second
        """
        self.world = world
        self.window_size = window_size
        self.fps = fps
        self.scale = window_size / world.size

        # Initialize Pygame
        pygame.init()
        self.screen = pygame.display.set_mode((window_size, window_size))
        pygame.display.set_caption("QIWM - Phase 1: Classical Potential Field")
        self.clock = pygame.time.Clock()

        # Color mapping
        self.colormap = cm.get_cmap('viridis')

        self.running = False

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

    def render_field(self) -> None:
        """Render the potential field as a heatmap."""
        vmin, vmax = self.world.get_guidance_field().min(), self.world.get_guidance_field().max()

        # Render grid cells
        for x in range(self.world.size):
            for y in range(self.world.size):
                value = self.world.get_guidance_field()[x, y]
                color = self.field_to_color(value, vmin, vmax)

                rect = pygame.Rect(
                    int(x * self.scale),
                    int(y * self.scale),
                    int(self.scale) + 1,
                    int(self.scale) + 1
                )
                pygame.draw.rect(self.screen, color, rect)

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

    def render_info(self) -> None:
        """Render information overlay."""
        font = pygame.font.Font(None, 24)
        state = self.world.get_state()

        info_lines = [
            f"Grid Size: {state['size']}x{state['size']}",
            f"Energy Sources: {state['num_energy_sources']}",
            f"Obstacles: {state['num_obstacles']}",
            f"Potential Range: [{state['potential_range'][0]:.2f}, {state['potential_range'][1]:.2f}]",
            f"Pilot Wave Range: [{self.world.pilot_wave.min():.2f}, {self.world.pilot_wave.max():.2f}]",
            f"Coherence Range: [{self.world.coherence.min():.2f}, {self.world.coherence.max():.2f}]",
            f"FPS: {int(self.clock.get_fps())}"
        ]

        y_offset = 10
        for line in info_lines:
            text_surface = font.render(line, True, (255, 255, 255))
            # Background for readability
            bg_rect = text_surface.get_rect()
            bg_rect.topleft = (10, y_offset)
            bg_rect.inflate_ip(10, 4)
            pygame.draw.rect(self.screen, (0, 0, 0, 128), bg_rect)

            self.screen.blit(text_surface, (10, y_offset))
            y_offset += 25

    def render(self) -> None:
        """Render a single frame."""
        self.screen.fill((0, 0, 0))
        self.render_field()
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

            # Update world if callback provided
            if update_callback:
                update_callback(self.world)

            # Render
            self.render()
            self.clock.tick(self.fps)

        pygame.quit()

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
