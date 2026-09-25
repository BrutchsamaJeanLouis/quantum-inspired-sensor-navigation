#!/usr/bin/env python3
"""
Exhaustive tick-setting verification matrix (PO request, 2026-09-25).

Checks, across scenarios x seeds x tick regions:
  1. Every (scenario, seed, tick) renders a valid, non-degenerate 800x800 frame.
  2. Determinism: the CLI `--shot` path is pixel-identical across processes
     (the LLM primitive an operator would actually call).
  3. Cross-tick divergence: frames at different ticks differ (the seek
     actually changed state), and stats() reflects the tick.
  4. Edge ticks: 0 (pre-step) and 1 (post-step) both render; the 0-frame
     has zero pilot-wave diffusion (t=0 invariant).

Usage:
    venv/Scripts/python.exe examples/verify_tick_matrix.py
    venv/Scripts/python.exe examples/verify_tick_matrix.py --quick
"""

import argparse
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import numpy as np
from PIL import Image

SCENARIOS = ['default', 'maze']
SEEDS = [42, 7]
TICKS = [0, 1, 5, 50, 120, 300, 500]
FRAME = 800
TMP = Path(os.environ.get('TEMP', '/tmp'))


def frame_stats(img):
    """Compact non-degeneracy stats for a rendered frame."""
    a = np.asarray(img.convert('RGB')).astype(np.int32)
    return {
        'size': img.size,
        'var': float(a.var()),
        'colors': int(len(np.unique(a.reshape(-1, 3), axis=0))),
        'mean': tuple(int(c) for c in a.reshape(-1, 3).mean(axis=0)),
    }


def in_process_frames(scenario, seed, ticks):
    """Render the requested ticks in-process via the same classes main.py uses."""
    import pygame
    os.environ['SDL_VIDEODRIVER'] = 'dummy'
    pygame.init()
    from main import build_world_and_swarm
    from src.core.timeline import TimelinePlayer
    from src.visualization import WorldVisualizer

    player = TimelinePlayer(
        factory=lambda: build_world_and_swarm(scenario), seed=seed)
    vis = WorldVisualizer(player.world, window_size=FRAME, fps=30, player=player)
    out = {}
    try:
        for t in sorted(set(ticks)):
            player.seek(t)
            vis._sync_player()
            vis.render()
            assert vis.screen.get_size() == (FRAME, FRAME), 'surface not 800x800'
            tmp_png = TMP / f'ip_{scenario}_{seed}_{t}.png'
            pygame.image.save(vis.screen, str(tmp_png))
            img = Image.open(tmp_png)
            out[t] = img
            stats = player.stats()
            assert stats['tick'] == t, (
                f'stats tick {stats["tick"]} != {t} after seek({t})')
    finally:
        pygame.quit()
    return out


def cli_shot(scenario, seed, tick, out_path):
    """Run the exact CLI an operator (LLM) would call; return (ok, printed_tick)."""
    r = subprocess.run(
        [sys.executable, 'main.py', '--scenario', scenario, '--seed', str(seed),
         '--shot', str(tick), '--out', str(out_path)],
        cwd=ROOT, capture_output=True, text=True, timeout=300)
    ok = r.returncode == 0 and Path(out_path).exists()
    printed = None
    for line in r.stdout.splitlines():
        if line.strip().startswith('Tick ') and 'saved' in line:
            printed = int(line.split()[1])
    return ok, printed, r


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--quick', action='store_true',
                    help='fewer CLI determinism pairs (for fast re-runs)')
    args = ap.parse_args()

    fails = []
    # ---- 1 + 3 + 4: in-process matrix across all configs/ticks -------------
    all_frames = {}   # (scenario, seed) -> {tick: PIL.Image}
    for scenario in SCENARIOS:
        for seed in SEEDS:
            print(f'== in-process matrix: {scenario} seed={seed} ==', flush=True)
            frames = in_process_frames(scenario, seed, TICKS)
            all_frames[(scenario, seed)] = frames
            for t in TICKS:
                fs = frame_stats(frames[t])
                degenerate = (fs['var'] < 200 or fs['colors'] < 10)
                tag = f'  tick={t:>4}: var={fs["var"]:9.1f} colors={fs["colors"]:5d} mean={fs["mean"]}'
                print(tag, 'DEGENERATE' if degenerate else '', flush=True)
                if degenerate:
                    fails.append(f'{scenario}/{seed}/t{t}: degenerate frame {fs}')
            # cross-tick divergence: each tick should differ from tick 0
            base = np.asarray(frames[0])
            for t in TICKS[1:]:
                d = int(np.abs(np.asarray(frames[t]).astype(int) - base.astype(int)).max())
                print(f'  diverge t{t} vs t0: maxdiff={d}', flush=True)
                if d == 0:
                    fails.append(f'{scenario}/{seed}: tick {t} frame == tick 0 frame')
    # t=0 invariant: pilot wave undiffused (identical across seeds for same scenario)
    for scenario in SCENARIOS:
        a = np.asarray(all_frames[(scenario, 42)][0])
        b = np.asarray(all_frames[(scenario, 7)][0])
        md = int(np.abs(a.astype(int) - b.astype(int)).max())
        print(f'== t0 cross-seed maxdiff ({scenario}): {md}', flush=True)
        if md != 0:
            fails.append(f'{scenario}: tick-0 frame differs across seeds (maxdiff {md})')

    # ---- 2: CLI determinism pairs (the real operator path) -----------------
    cli_configs = [(s, se, t) for s in SCENARIOS for se in SEEDS for t in [0, 120, 500]]
    if args.quick:
        cli_configs = [(s, se, 120) for s in SCENARIOS for se in SEEDS]
    for scenario, seed, tick in cli_configs:
        p1, p2 = TMP / f'mx_{scenario}_{seed}_{tick}_a.png', TMP / f'mx_{scenario}_{seed}_{tick}_b.png'
        ok1, pr1, r1 = cli_shot(scenario, seed, tick, p1)
        ok2, pr2, r2 = cli_shot(scenario, seed, tick, p2)
        same = False
        if ok1 and ok2:
            i1, i2 = Image.open(p1).convert('RGB'), Image.open(p2).convert('RGB')
            same = np.abs(np.asarray(i1).astype(int) - np.asarray(i2).astype(int)).max() == 0
        status = 'OK' if (ok1 and ok2 and same and pr1 == tick and pr2 == tick) else 'FAIL'
        print(f'== CLI determinism {scenario}/{seed}/t{tick}: '
              f'rc1={r1.returncode} rc2={r2.returncode} printed={pr1},{pr2} pixel-same={same} [{status}]',
              flush=True)
        if status == 'FAIL':
            fails.append(f'CLI {scenario}/{seed}/t{tick}: '
                         f'ok1={ok1} ok2={ok2} same={same} printed={pr1},{pr2}')
            print((r1.stderr or r2.stderr)[-500:], flush=True)

    print('\n' + '=' * 60)
    if fails:
        print(f'MATRIX FAIL ({len(fails)}):')
        for f in fails:
            print('  -', f)
        sys.exit(1)
    n = len(SCENARIOS) * len(SEEDS) * len(TICKS)
    print(f'MATRIX PASS: {n} in-process frames + '
          f'{len(SCENARIOS) * len(SEEDS) * (2 if not args.quick else 1)} CLI determinism pairs')


if __name__ == '__main__':
    main()
