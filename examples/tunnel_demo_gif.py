"""
Tunnel demo GIF/frame exporter.

Removes manual screen capture from the demo-video path: runs the tunnel
scenario headless (SDL dummy driver) and captures WorldVisualizer frames
into an animated GIF (and optionally a PNG frame sequence).

Configs (v2 instrument constants, torus, collapse ON, 20 agents, corner
spawn — same world as the ablation harness):
  quantum   : q=0.3  (pilot-wave channel — the agents cross)
  classical : q=0.0  (deterministic greedy — the agents die on the wall)

Usage:
    python examples/tunnel_demo_gif.py                 # quantum, 150 frames
    python examples/tunnel_demo_gif.py --config classical
    python examples/tunnel_demo_gif.py --frames 60 --frames-dir out/
"""

import argparse
import os
import sys

# Headless BEFORE pygame is imported anywhere in the tree.
os.environ.setdefault('SDL_VIDEODRIVER', 'dummy')
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PIL import Image  # noqa: E402

from src.core.experiments import create_scenario_world  # noqa: E402
from src.core.agents import AgentSwarm  # noqa: E402
from src.visualization import WorldVisualizer  # noqa: E402
import pygame  # noqa: E402

PREWARM_STEPS = 2000  # v2 instrument: wave established before agents
POPULATION = 20
DIFFUSION_RATE = 0.2
COUPLINGS = {'quantum': 0.3, 'classical': 0.0}


def export_gif(
    config: str = 'quantum',
    frames: int = 150,
    steps_per_frame: int = 5,
    window_size: int = 800,
    fps: int = 12,
    gif_path: str = None,
    frames_dir: str = None,
) -> str:
    """Simulate the tunnel scenario and export frames as a GIF.

    Returns the written GIF path.
    """
    assert config in COUPLINGS, f'unknown config {config}'
    if gif_path is None:
        root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        gif_path = os.path.join(root, f'tunnel_demo_{config}.gif')

    world = create_scenario_world(
        'tunnel', 128, COUPLINGS[config], DIFFUSION_RATE)
    for _ in range(PREWARM_STEPS):
        world.update_pilot_wave(dt=DIFFUSION_RATE)
    swarm = AgentSwarm(world, POPULATION, 'corner')

    vis = WorldVisualizer(world, window_size=window_size)
    vis.set_agents(swarm)
    vis.interactive_mode = False

    if frames_dir:
        os.makedirs(frames_dir, exist_ok=True)

    frame_images = []
    for f in range(frames):
        for _ in range(steps_per_frame):
            world.update_pilot_wave(dt=DIFFUSION_RATE)
            swarm.step_all()
        vis.render()
        arr = pygame.surfarray.array3d(vis.screen)
        img = Image.fromarray(arr.transpose(1, 0, 2))
        if frames_dir:
            img.save(os.path.join(frames_dir, f'frame_{f:04d}.png'))
        frame_images.append(img)

    duration = max(1, int(1000 / fps))
    frame_images[0].save(
        gif_path, save_all=True, append_images=frame_images[1:],
        duration=duration, loop=0, optimize=True)
    pygame.quit()
    print(f'{config}: {frames} frames -> {gif_path}')
    return gif_path


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--config', choices=sorted(COUPLINGS), default='quantum')
    p.add_argument('--frames', type=int, default=150)
    p.add_argument('--steps-per-frame', type=int, default=5)
    p.add_argument('--window-size', type=int, default=800)
    p.add_argument('--fps', type=int, default=12)
    p.add_argument('--out', type=str, default=None)
    p.add_argument('--frames-dir', type=str, default=None)
    args = p.parse_args()
    export_gif(
        config=args.config,
        frames=args.frames,
        steps_per_frame=args.steps_per_frame,
        window_size=args.window_size,
        fps=args.fps,
        gif_path=args.out,
        frames_dir=args.frames_dir,
    )
