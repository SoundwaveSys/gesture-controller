import time
import pyautogui
import subprocess
import platform


class MediaController:

    def __init__(self):

        # ========================================================
        # ACTION CONTROL
        # ========================================================

        self.last_action = 0
        self.cooldown = 0.5
        self.os_type = platform.system()

    # ============================================================
    # COOLDOWN
    # ============================================================

    def ready(self):

        now = time.monotonic()

        if now - self.last_action < self.cooldown:
            return False

        self.last_action = now

        return True

    # ============================================================
    # PLAY / PAUSE (More Reliable)
    # ============================================================

    def play_pause(self):

        if not self.ready():
            return

        pyautogui.press("space")

        print("\n▶️ PLAY / PAUSE")

    # ============================================================
    # NEXT TRACK (Reliable Method)
    # ============================================================

    def next_track(self):

        if not self.ready():
            return

        pyautogui.hotkey("shift", "right")

        print("\n⏭️ NEXT TRACK")

    # ============================================================
    # PREVIOUS TRACK (Reliable Method)
    # ============================================================

    def previous_track(self):

        if not self.ready():
            return

        pyautogui.hotkey("shift", "left")

        print("\n⏮️ PREVIOUS TRACK")

    # ============================================================
    # STOP
    # ============================================================

    def stop(self):

        if not self.ready():
            return

        pyautogui.press("escape")

        print("\n⏹️ STOP")

    # ============================================================
    # SEEK FORWARD (10 seconds)
    # ============================================================

    def seek_forward(self):

        if not self.ready():
            return

        pyautogui.press("right")

        print("\n⏩ SEEK FORWARD")

    # ============================================================
    # SEEK BACKWARD (10 seconds)
    # ============================================================

    def seek_backward(self):

        if not self.ready():
            return

        pyautogui.press("left")

        print("\n⏪ SEEK BACKWARD")
