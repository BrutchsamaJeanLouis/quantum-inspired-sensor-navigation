"""Send a synthesized mouse drag to a window via PostMessage.

pygame/SDL reads WM_LBUTTONDOWN/MOUSEMOVE/LBUTTONUP from its message
queue, so this works even when the SendInput path is blocked.
Coordinates are client-space, logical px (the app is DPI-aware).

Usage: python postmouse.py "<window title>" x0 y0 x1 y1 [steps]
"""
import sys
import time
import ctypes

user32 = ctypes.windll.user32
FindWindowW = user32.FindWindowW
FindWindowW.restype = ctypes.c_void_p
FindWindowW.argtypes = [ctypes.c_wchar_p, ctypes.c_wchar_p]
PostMessageW = user32.PostMessageW
PostMessageW.argtypes = [ctypes.c_void_p, ctypes.c_uint, ctypes.c_void_p, ctypes.c_void_p]

WM_LBUTTONDOWN = 0x0201
WM_MOUSEMOVE = 0x0200
WM_LBUTTONUP = 0x0202


def post(hwnd, msg, x, y):
    lparam = (y << 16) | (x & 0xFFFF)
    PostMessageW(hwnd, msg, ctypes.c_void_p(1), ctypes.c_void_p(lparam))


def main():
    title = sys.argv[1]
    x0, y0, x1, y1 = (int(v) for v in sys.argv[2:6])
    steps = int(sys.argv[6]) if len(sys.argv) > 6 else 30
    hwnd = FindWindowW(None, title)
    if not hwnd:
        print("window not found:", title)
        sys.exit(1)
    post(hwnd, WM_LBUTTONDOWN, x0, y0)
    time.sleep(0.1)
    for i in range(1, steps + 1):
        x = int(x0 + (x1 - x0) * i / steps)
        y = int(y0 + (y1 - y0) * i / steps)
        post(hwnd, WM_MOUSEMOVE, x, y)
        time.sleep(0.02)
    time.sleep(0.1)
    post(hwnd, WM_LBUTTONUP, x1, y1)
    print(f"dragged ({x0},{y0}) -> ({x1},{y1}) in {steps} steps on hwnd={hwnd}")


if __name__ == '__main__':
    main()
