"""
Demo video for the QIWM tunnel result (the project's centerpiece).

Renders the tunnel scenario headless and composes a single labelled video:

  SEGMENT A  — side-by-side A/B:  classical (q=0.0, trapped on the wall)  |
              quantum (q=0.3, crosses the seam).  This is the headline.
  SEGMENT B  — the P-key phi / COHERENCE overlay on the quantum run
              (vis.show_phi=True — the same toggle the interactive UI binds to P).
  SEGMENT C  — a summary card with the headline numbers + pointers.

No manual screen capture: the world is simulated in-process and frames are
captured from WorldVisualizer. Output: MP4 (H.264, yuv420p) via ffmpeg, plus a
smaller MP4-safe GIF fallback.

Usage:
    python examples/make_demo_video.py
    python examples/make_demo_video.py --frames 120 --phi-frames 40 --out demo.mp4
"""

import argparse
import os
import shutil
import subprocess
import sys
import tempfile

# Headless BEFORE pygame is imported anywhere in the tree.
os.environ.setdefault('SDL_VIDEODRIVER', 'dummy')
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PIL import Image, ImageDraw, ImageFont  # noqa: E402

from src.core.experiments import create_scenario_world  # noqa: E402
from src.core.agents import AgentSwarm  # noqa: E402
from src.visualization import WorldVisualizer  # noqa: E402
import pygame  # noqa: E402

# v2 instrument constants — same world as the ablation harness (torus,
# collapse ON, 20 agents, corner spawn) so the video matches the CSVs.
PREWARM_STEPS = 2000
POPULATION = 20
DIFFUSION_RATE = 0.2
COUPLINGS = {'quantum': 0.3, 'classical': 0.0}

# Layout (source panels are 800x800).
PANEL = 800
HEADER_H = 60
GAP = 8
AB_W = 2 * PANEL + GAP                 # 1608
CANVAS_W = AB_W + 8                    # 1616 (2px border each side)
CANVAS_H = HEADER_H + PANEL + 8        # 868
BG = (10, 12, 18)
FONT_PATH = (r"C:/Users/brutc/qwm-core/venv/Lib/site-packages/matplotlib/"
             r"mpl-data/fonts/ttf/DejaVuSans-Bold.ttf")


def _font(size: int):
    try:
        return ImageFont.truetype(FONT_PATH, size)
    except Exception:
        return ImageFont.load_default()


def _cap(vis: WorldVisualizer) -> Image.Image:
    arr = pygame.surfarray.array3d(vis.screen)
    return Image.fromarray(arr.transpose(1, 0, 2))


def _new_canvas() -> Image.Image:
    return Image.new('RGB', (CANVAS_W, CANVAS_H), BG)


def _header(d: ImageDraw.ImageDraw, title: str, sub: str = '') -> None:
    d.text((12, 8), title, font=_font(28), fill=(240, 240, 245))
    if sub:
        d.text((12, 40), sub, font=_font(16), fill=(150, 160, 180))


def _label(d: ImageDraw.ImageDraw, x: int, y: int, text: str,
           color=(240, 240, 245)) -> None:
    d.text((x, y), text, font=_font(22), fill=color)


def simulate(config: str, frames: int, steps_per_frame: int,
             with_phi: bool = False):
    """Run the tunnel sim once; return (guidance_frames, phi_frames)."""
    world = create_scenario_world('tunnel', 128, COUPLINGS[config],
                                 DIFFUSION_RATE)
    for _ in range(PREWARM_STEPS):
        world.update_pilot_wave(dt=DIFFUSION_RATE)
    swarm = AgentSwarm(world, POPULATION, 'corner')

    vis = WorldVisualizer(world, window_size=PANEL)
    vis.set_agents(swarm)
    vis.interactive_mode = False

    guidance, phi = [], []
    for _ in range(frames):
        for _ in range(steps_per_frame):
            world.update_pilot_wave(dt=DIFFUSION_RATE)
            swarm.step_all()
        vis.show_phi = False
        vis.render()
        guidance.append(_cap(vis))
        if with_phi:
            vis.show_phi = True          # the P-key overlay
            vis.render()
            phi.append(_cap(vis))
    pygame.quit()
    return guidance, phi


def _ab_frame(c_img: Image.Image, q_img: Image.Image) -> Image.Image:
    cv = _new_canvas()
    d = ImageDraw.Draw(cv)
    _header(d, 'TUNNEL  —  A/B',
            'classical (q=0.0): trapped on the wall   |   '
            'quantum (q=0.3): finds the seam route')
    cv.paste(c_img, (4, HEADER_H))
    cv.paste(q_img, (4 + PANEL + GAP, HEADER_H))
    _label(d, 8, HEADER_H + 6, 'CLASSICAL', (255, 200, 120))
    _label(d, 4 + PANEL + GAP + 8, HEADER_H + 6, 'QUANTUM', (120, 220, 255))
    return cv


def _phi_frame(p_img: Image.Image) -> Image.Image:
    cv = _new_canvas()
    d = ImageDraw.Draw(cv)
    _header(d, 'COHERENCE / \u03a6 OVERLAY  (P key)',
            'the collapse field the agent observes; press P in the '
            'interactive UI to toggle')
    x = (CANVAS_W - PANEL) // 2
    cv.paste(p_img, (x, HEADER_H))
    _label(d, x + 8, HEADER_H + 6, 'QUANTUM q=0.3  ·  \u03a4/Phi view',
           (255, 170, 240))
    return cv


def _summary_card() -> Image.Image:
    cv = _new_canvas()
    d = ImageDraw.Draw(cv)
    _header(d, 'HEADLINE')
    lines = [
        'Deterministic local-greedy classical (q=0.0): 0% alive, 0/20 crossings.',
        'Quantum-inspired (q=0.3): 100% alive, 20/20 seam crossings.',
        'Mechanism: the pilot wave leaks around the wall, so Boltzmann sampling',
        'discovers the seam route the local gradient can never point at.',
        'Classical never jumps the wall; it wraps the torus seam (latency ~2.0).',
        '',
        'Null hypothesis (quantum adds no advantage): rejected in 4 of 5 scenarios.',
        'See docs/RESULTS.md (S4, S4b, S4h) and docs/PAPER.md. Data:',
        'ablation_results_v2.csv, epsilon_sweep_tunnel.csv.',
    ]
    y = HEADER_H + 40
    for ln in lines:
        d.text((24, y), ln, font=_font(24), fill=(220, 225, 235))
        y += 44
    return cv


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--frames', type=int, default=150,
                   help='A/B segment frames (tunnel run)')
    p.add_argument('--phi-frames', type=int, default=40,
                   help='phi-overlay segment frames')
    p.add_argument('--steps-per-frame', type=int, default=5)
    p.add_argument('--fps', type=int, default=12)
    p.add_argument('--out', type=str, default=None,
                   help='output .mp4 path (default: demo_video.mp4)')
    args = p.parse_args()

    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    out_mp4 = args.out or os.path.join(root, 'demo_video.mp4')

    print('Simulating classical (q=0.0)...')
    classic, _ = simulate('classical', args.frames, args.steps_per_frame)
    print('Simulating quantum (q=0.3) with phi overlay...')
    q_guid, q_phi = simulate('quantum', args.frames, args.steps_per_frame,
                             with_phi=True)

    # Compose all frames (identical canvas size).
    frames = []
    n_ab = min(len(classic), len(q_guid))
    for i in range(n_ab):
        frames.append(_ab_frame(classic[i], q_guid[i]))
    for i in range(min(args.phi_frames, len(q_phi))):
        frames.append(_phi_frame(q_phi[i]))
    card = _summary_card()
    for _ in range(60):          # hold the card ~5s at 12fps
        frames.append(card)

    # Write PNG sequence to a temp dir, feed ffmpeg.
    tmp = tempfile.mkdtemp(prefix='qiwm_video_')
    try:
        for i, fr in enumerate(frames):
            fr.save(os.path.join(tmp, f'f_{i:05d}.png'))
        dur = max(1, int(1000 / args.fps))
        gif = os.path.join(root, 'demo_video.gif')
        frames[0].save(
            gif, save_all=True, append_images=frames[1:], duration=dur,
            loop=0, optimize=True)
        print(f'GIF fallback: {gif}')
        if not shutil.which('ffmpeg'):
            print('ffmpeg not found; wrote GIF only.')
            return
        cmd = ['ffmpeg', '-y', '-framerate', str(args.fps),
               '-i', os.path.join(tmp, 'f_%05d.png'),
               '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-r', str(args.fps),
               '-movflags', '+faststart', out_mp4]
        subprocess.run(cmd, check=True,
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(f'MP4: {out_mp4}  ({len(frames)} frames)')
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == '__main__':
    main()
