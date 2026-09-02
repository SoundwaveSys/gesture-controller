import time
import pyautogui


class SystemController:

    def __init__(self):
        self.last_action = 0
        self.cooldown = 0.7

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
    # VOLUME
    # ============================================================

    def volume_up(self):

        if not self.ready():
            return

        pyautogui.press("volumeup")
        print("\n🔊 VOLUME UP")

    def volume_down(self):

        if not self.ready():
            return

        pyautogui.press("volumedown")
        print("\n🔉 VOLUME DOWN")

    def mute(self):

        if not self.ready():
            return

        pyautogui.press("volumemute")
        print("\n🔇 MUTE")

    # ============================================================
    # MEDIA
    # ============================================================

    def play_pause(self):

        if not self.ready():
            return

        pyautogui.press("playpause")
        print("\n▶️ PLAY / PAUSE")

    def next_track(self):

        if not self.ready():
            return

        pyautogui.press("nexttrack")
        print("\n⏭️ NEXT TRACK")

    def previous_track(self):

        if not self.ready():
            return

        pyautogui.press("prevtrack")
        print("\n⏮️ PREVIOUS TRACK")

    # ============================================================
    # WINDOWS
    # ============================================================

    def alt_tab(self):

        if not self.ready():
            return

        pyautogui.hotkey("alt", "tab")
        print("\n🪟 ALT + TAB")

    def show_desktop(self):

        if not self.ready():
            return

        pyautogui.hotkey("win", "d")
        print("\n🖥️ SHOW DESKTOP")

    def lock_windows(self):

        if not self.ready():
            return

        pyautogui.hotkey("win", "l")
        print("\n🔒 WINDOWS LOCKED")

    # ============================================================
    # SWIPES
    # ============================================================

    def swipe_right(self):

        self.next_track()

    def swipe_left(self):

        self.previous_track()

    def swipe_up(self):

        self.alt_tab()

    def swipe_down(self):

        self.show_desktop()