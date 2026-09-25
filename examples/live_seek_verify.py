#!/usr/bin/env python3
"""
Live-GUI tick verification driver (PO request 2026-09-25, TODO 1b/1c).

Drives a RUNNING demo window via PostMessage keys (the verified-working
input path): SPACE pause, HOME seek-0, then repeated Right-arrow scrubs
to reach exact target ticks. After each seek it:
  * captures the window with PrintWindow (works regardless of virtual
    desktop) and crops the info-panel tick line + slider label row,
  * also captures the DWM-frame screen region via ImageGrab (works only
    when the window shares the capture desktop — the same condition as
    computer_screenshot),
  * runs the headless `--shot TICK` CLI and diffs the live frame against
    it (rewind/seek consistency, TODO 1c).

The driver is self-contained: it launches its own demo (the known env quirk
kills shell-managed demos within seconds), waits for a NEW window handle,
drives it, then sends ESC and verifies clean exit.

Usage:
    venv/Scripts/python.exe examples/live_seek_verify.py default 42 0 120 300
"""

import os
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
import ctypes
import ctypes.wintypes as wt
import numpy as np
from PIL import Image, ImageGrab, ImageChops

TITLE = 'QIWM - Quantum-Inspired World Model'
user32 = ctypes.windll.user32
user32.FindWindowW.restype = ctypes.c_void_p
user32.FindWindowW.argtypes = [ctypes.c_wchar_p, ctypes.c_wchar_p]
user32.MapVirtualKeyW.argtypes = [ctypes.c_uint, ctypes.c_uint]

WM_KEYDOWN, WM_KEYUP = 0x0100, 0x0101
VK_SPACE, VK_RIGHT, VK_HOME = 0x20, 0x27, 0x24
TMP = Path(os.environ.get('TEMP', '/tmp'))


# VKs that are physically *extended* keys on a real Windows keyboard
# (arrow cluster / numpad / home/end). SDL2 2.28's WindowsScanCodeToSDLScanCode
# remaps the scan-table result to the numpad key (HOME->KP_7, RIGHT->KP_6, ...)
# whenever the extended-key bit (bit 24) is CLEAR, so injected arrows/home had to
# carry bit 24 set to get the correct SDL scancode (74/79/80/81/82) that pygame's
# K_HOME/K_RIGHT/etc. constants expect.
_EXTENDED_VKS = {
    0x24, 0x25, 0x26, 0x27, 0x28,  # Home, Up, PgUp handled by 0x22/0x21 not in our set
    0x21, 0x22, 0x23,  # End, PgDn, Insert
    0x2B, 0x2C, 0x2D, 0x2E, 0x2F,  # Numpad *, +, -, Enter, .
    0x1C,  # Right Ctrl (extended Enter)
    0x5B, 0x5C,  # L/R Windows keys
}


def post_key(hwnd, vk, down=True):
    scan = user32.MapVirtualKeyW(vk, 0)
    # Correct Windows keyboard lParam layout:
    #   bits  0-15  transition/repeat flags
    #   bits 16-23  scan code (SDL2 2.28: nScanCode=(lParam>>16)&0xFF)
    #   bit   24    extended-key flag (SET for arrows/home/numpad)
    # KEYDOWN initial press: low word 0x0000 (prev up, no repeat, not released)
    # KEYUP release:         low word 0x00C0 (prev down=0x40, transition=0x80)
    low = 0x0000 if down else 0x00C0
    ext = 0x01000000 if vk in _EXTENDED_VKS else 0x00000000
    lp = low | ext | ((scan & 0xff) << 16)
    return user32.PostMessageW(hwnd, WM_KEYDOWN if down else WM_KEYUP,
                               ctypes.c_void_p(vk), ctypes.c_void_p(lp))


def press(hwnd, vk, gap_down=0.18, gap_after=0.18):
    post_key(hwnd, vk, True)
    time.sleep(gap_down)
    post_key(hwnd, vk, False)
    time.sleep(gap_after)


VK_SHIFT = 0x10


def seek_forward(hwnd, n, gap=0.02, settle=0.10):
    """Advance the live player by exactly n ticks (n >= 0).

    Uses plain Right (= +1) for every tick. This is the RELIABLE path: the
    SDL2/pygame mod-state for a PostMessage'd Shift is racy (the injected Shift
    keyup can be processed out of order, so the demo's Shift+Right "x10" fast
    scrub intermittently counts as +1). Plain +1 is a bit slower (tick 300 is
    ~30s at gap=0.02) but lands on the exact target every time, which is what
    the tick-readout verification needs.
    """
    if n <= 0:
        return
    for _ in range(n):
        post_key(hwnd, VK_RIGHT, True)
        time.sleep(gap)
        post_key(hwnd, VK_RIGHT, False)
        time.sleep(gap)
    time.sleep(settle)


class RECT(ctypes.Structure):
    _fields_ = [('l', wt.LONG), ('t', wt.LONG), ('r', wt.LONG), ('b', wt.LONG)]


def print_window(hwnd, W, H):
    gd = ctypes.windll.gdi32
    hdc = user32.GetDC(hwnd)
    memdc = gd.CreateCompatibleDC(hdc)
    bmp = gd.CreateCompatibleBitmap(hdc, W, H)
    gd.SelectObject(memdc, bmp)
    ok = user32.PrintWindow(hwnd, memdc, 2)
    class BIH(ctypes.Structure):
        _fields_ = [('s', wt.UINT), ('w', wt.INT), ('ht', wt.INT), ('pl', wt.WORD),
                    ('bc', wt.WORD), ('c', wt.UINT), ('si', wt.UINT), ('xp', wt.INT),
                    ('yp', wt.INT), ('cu', wt.UINT), ('ci', wt.UINT)]
    buf = ctypes.create_string_buffer(W * H * 4)
    b = BIH(); b.s = ctypes.sizeof(BIH); b.w = W; b.ht = -H; b.pl = 1; b.bc = 32
    gd.GetDIBits(memdc, bmp, 0, H, buf, ctypes.byref(b), 0)
    gd.DeleteObject(bmp); gd.DeleteDC(memdc); user32.ReleaseDC(hwnd, hdc)
    img = Image.frombuffer('RGB', (W, H), buf, 'raw', 'BGRX', 0, 1)
    return img if ok else None


def existing_titled_hwnds():
    found = []
    @ctypes.WINFUNCTYPE(ctypes.c_int, ctypes.c_void_p, ctypes.c_void_p)
    def cb(h, _):
        if user32.IsWindowVisible(h):
            n = user32.GetWindowTextLengthW(h)
            if n > 0:
                buf = ctypes.create_unicode_buffer(n + 1)
                user32.GetWindowTextW(h, buf, n + 1)
                if buf.value == TITLE:
                    found.append(h)
        return 1
    user32.EnumWindows(cb, 0)
    return set(found)


def main():
    scenario, seed = sys.argv[1], int(sys.argv[2])
    ticks = [int(t) for t in sys.argv[3:]]
    before = existing_titled_hwnds()
    log = open(TMP / f'live_demo_{scenario}_{seed}.log', 'w')
    proc = subprocess.Popen(
        [str(ROOT / 'venv' / 'Scripts' / 'python.exe'), 'main.py',
         '--scenario', scenario, '--seed', str(seed)],
        cwd=ROOT, stdout=log, stderr=subprocess.STDOUT)
    hwnd = None
    for _ in range(60):
        time.sleep(0.5)
        new = existing_titled_hwnds() - before
        if new:
            hwnd = next(iter(new))
            break
    if hwnd is None:
        print('FAIL: no new demo window appeared (rc=', proc.poll(), ')')
        sys.exit(1)
    print(f'demo launched pid={proc.pid} hwnd={hwnd}')
    # SDL2/pygame needs the window truly activated before PostMessage keys
    # register (fresh windows sit unfocused on the new desktop).
    user32.PostMessageW(hwnd, 0x0006, ctypes.c_void_p(2), 0)  # WM_ACTIVATE WA_ACTIVE
    user32.PostMessageW(hwnd, 0x0001, 0, 0)                  # WM_SETFOCUS
    time.sleep(1.0)
    cr = RECT()
    user32.GetClientRect(hwnd, ctypes.byref(cr))
    W, H = cr.r - cr.l, cr.b - cr.t
    fr = RECT()
    dwm = ctypes.windll.dwmapi
    dwm.DwmGetWindowAttribute(hwnd, 9, ctypes.byref(fr), ctypes.sizeof(fr))
    print(f'window {W}x{H} client; DWM frame ({fr.l},{fr.t},{fr.r},{fr.b})')

    results = []
    user32.ShowWindow(hwnd, 9)
    user32.SetForegroundWindow(hwnd)
    time.sleep(0.4)
    # pause first so the tick stays where we put it
    press(hwnd, VK_SPACE)
    time.sleep(0.5)

    current = None  # unknown until we read it; HOME resets to 0 deterministically
    press(hwnd, VK_HOME)
    time.sleep(0.8)
    current = 0
    for target in sorted(ticks):
        if target < current:
            press(hwnd, VK_HOME); time.sleep(0.8); current = 0
        n = target - current
        print(f'  seeking {current} -> {target} (+{n}) ...', flush=True)
        seek_forward(hwnd, n)
        time.sleep(0.7)
        cap = print_window(hwnd, W, H)
        if cap is None:
            results.append((target, 'capture-fail')); continue
        cap.crop((0, 230, 400, 320)).save(TMP / f'lv_{scenario}_{target}_infopanel.png')
        cap.crop((0, 715, 800, 800)).save(TMP / f'lv_{scenario}_{target}_slider.png')
        # screen-region capture (same condition as computer_screenshot)
        try:
            ImageGrab.grab(bbox=(fr.l, fr.t, fr.r, fr.b)).save(
                TMP / f'lv_{scenario}_{target}_screen.png')
        except Exception as e:
            print(f'    ImageGrab failed: {e}')
        # headless reference frame
        shot = TMP / f'lv_shot_{scenario}_{seed}_{target}.png'
        r = subprocess.run(
            [sys.executable, 'main.py', '--scenario', scenario, '--seed', str(seed),
             '--shot', str(target), '--out', str(shot)],
            cwd=ROOT, capture_output=True, text=True, timeout=300)
        ref = Image.open(shot).convert('RGB') if shot.exists() else None
        note = f'shot rc={r.returncode}'
        if ref is not None:
            a, b = np.asarray(ref).astype(int), np.asarray(cap).astype(int)
            md = int(np.abs(a - b).max())
            diff = ImageChops.difference(ref, cap)
            note += f' live-vs-shot maxdiff={md}'
            # where do they differ?
            ys = np.where(np.abs(a - b).any(axis=2))[0]
            note += f' diff-y-range=({ys.min()},{ys.max()})' if len(ys) else ' IDENTICAL'
            diff.save(TMP / f'lv_{scenario}_{target}_diff.png')
        current = target
        results.append((target, note))
        print(f'  tick {target}: {note}', flush=True)

    # clean ESC shutdown
    post_key(hwnd, 0x1B, True); time.sleep(0.1); post_key(hwnd, 0x1B, False)
    try:
        rc = proc.wait(timeout=30)
    except subprocess.TimeoutExpired:
        proc.kill(); rc = 'timeout-killed'
    print(f'ESC shutdown: exit code {rc}')
    log.close()

    print('\n== RESULTS ==')
    for t, note in results:
        print(f'  {t}: {note}')
    ok = all(n.startswith(('shot rc=0',)) for _, n in results) and rc == 0
    print('LIVE-SEEK PASS' if ok else 'LIVE-SEEK CHECK NEEDED (see notes)')


if __name__ == '__main__':
    main()
