"""Send virtual key events to a window via WM_KEYDOWN/WM_KEYDOWN messages.

Bypasses the blocked SendInput path: SDL's Windows message pump reads
PostMessage'd WM_KEYDOWN/WM_KEYUP events from its own queue.
Usage: python postkey.py "<window title>" space|left|right|home [count]
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

WM_KEYDOWN = 0x0100
WM_KEYUP = 0x0101
MAPVK_VK_TO_VSC = 0
ToVirtKey = user32.MapVirtualKeyW
ToVirtKey.argtypes = [ctypes.c_uint, ctypes.c_uint]

KEYS = {
    'space': 0x20, 'left': 0x25, 'right': 0x27, 'home': 0x24,
    'p': 0x50, 't': 0x54, 'r': 0x52, 'l': 0x4C, 'u': 0x55, 'escape': 0x1B,
}


def post_key(hwnd, vk, down=True):
    scan = ToVirtKey(vk, MAPVK_VK_TO_VSC)
    flags = 0x0001  # previous key state: was down
    if not down:
        flags |= 0x8000  # transition: up
    lparam = (scan << 16) | (flags << 30)
    msg = WM_KEYDOWN if down else WM_KEYUP
    return PostMessageW(hwnd, msg, ctypes.c_void_p(vk), ctypes.c_void_p(lparam))


def main():
    title, key_name = sys.argv[1], sys.argv[2].lower()
    count = int(sys.argv[3]) if len(sys.argv) > 3 else 1
    vk = KEYS[key_name]
    hwnd = FindWindowW(None, title)
    if not hwnd:
        print("window not found:", title)
        sys.exit(1)
    for _ in range(count):
        post_key(hwnd, vk, down=True)
        time.sleep(0.02)
        post_key(hwnd, vk, down=False)
        time.sleep(0.05)
    print(f"sent {count}x {key_name} to hwnd={hwnd}")


if __name__ == '__main__':
    main()
