import time
import pyautogui
import subprocess
import platform


class VolumeController:

    def __init__(self):

        # ========================================================
        # ACTION CONTROL
        # ========================================================

        self.last_action = 0
        self.cooldown = 0.3
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
    # VOLUME UP (Cross-platform)
    # ============================================================

    def volume_up(self):

        if not self.ready():
            return

        if self.os_type == "Windows":
            try:
                # Use Windows API for volume control
                pyautogui.press("volumeup")
            except:
                # Fallback: use keyboard shortcut
                pyautogui.hotkey("alt", "pageup")
        else:
            pyautogui.press("volumeup")

        print("\n🔊 VOLUME UP")

    # ============================================================
    # VOLUME DOWN (Cross-platform)
    # ============================================================

    def volume_down(self):

        if not self.ready():
            return

        if self.os_type == "Windows":
            try:
                pyautogui.press("volumedown")
            except:
                # Fallback: use keyboard shortcut
                pyautogui.hotkey("alt", "pagedown")
        else:
            pyautogui.press("volumedown")

        print("\n🔉 VOLUME DOWN")

    # ============================================================
    # MUTE (Cross-platform)
    # ============================================================

    def mute(self):

        if not self.ready():
            return

        if self.os_type == "Windows":
            try:
                pyautogui.press("volumemute")
            except:
                # Fallback: use app-specific mute (if available)
                pyautogui.hotkey("ctrl", "m")
        else:
            pyautogui.press("volumemute")

        print("\n🔇 MUTE")

    # ============================================================
    # UNMUTE
    # ============================================================

    def unmute(self):

        if not self.ready():
            return

        # Usually mute toggles, but this ensures unmute
        if self.os_type == "Windows":
            pyautogui.press("volumemute")
        else:
            pyautogui.press("volumemute")

        print("\n🔔 UNMUTE")

    # ============================================================
    # SET VOLUME TO MAX
    # ============================================================

    def volume_max(self):

        if not self.ready():
            return

        # Press volume up 10 times to maximize volume
        for _ in range(10):
            pyautogui.press("volumeup")
            time.sleep(0.05)

        print("\n🔊🔊 MAX VOLUME")

    # ============================================================
    # SET VOLUME TO MIN
    # ============================================================

    def volume_min(self):

        if not self.ready():
            return

        # Press volume down 10 times to minimize volume
        for _ in range(10):
            pyautogui.press("volumedown")
            time.sleep(0.05)

        print("\n🔇 MIN VOLUME")
