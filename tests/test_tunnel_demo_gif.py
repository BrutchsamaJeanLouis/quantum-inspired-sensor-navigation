"""
Tunnel demo GIF exporter tests (examples/tunnel_demo_gif.py).

Headless (SDL dummy) frame capture: the exporter must produce a real
animated GIF with the requested frame count for both configs, and
optionally a PNG frame sequence.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PIL import Image  # noqa: E402

from examples.tunnel_demo_gif import export_gif  # noqa: E402


class TestTunnelDemoGif:
    def _tiny(self, config, tmp_path):
        gif = tmp_path / f'{config}.gif'
        frames_dir = tmp_path / f'{config}_frames'
        export_gif(config=config, frames=4, steps_per_frame=3,
                   window_size=320, gif_path=str(gif),
                   frames_dir=str(frames_dir))
        return gif, frames_dir

    def test_quantum_gif(self, tmp_path):
        gif, frames_dir = self._tiny('quantum', tmp_path)
        assert gif.exists()
        with Image.open(str(gif)) as im:
            assert im.format == 'GIF'
            assert im.n_frames == 4
        pngs = sorted(os.listdir(str(frames_dir)))
        assert len(pngs) == 4
        with Image.open(os.path.join(str(frames_dir), pngs[0])) as im:
            assert im.size == (320, 320)

    def test_classical_gif(self, tmp_path):
        gif, _ = self._tiny('classical', tmp_path)
        assert gif.exists()
        with Image.open(str(gif)) as im:
            assert im.format == 'GIF'
            assert im.n_frames == 4
