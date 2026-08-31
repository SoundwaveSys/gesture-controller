import time
import pyautogui


class SystemController:

    def __init__(self):

        # ========================================================
        # ACTION CONTROL
        # ========================================================

        self.last_action = 0

        # Prevent repeated system actions
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
    # VOLUME UP
    # ============================================================

    def volume_up(self):

        if not self.ready():
            return

        pyautogui.press("volumeup")

        print("\n🔊 VOLUME UP")

    # ============================================================
    # VOLUME DOWN
    # ============================================================

    def volume_down(self):

        if not self.ready():
            return

        pyautogui.press("volumedown")

        print("\n🔉 VOLUME DOWN")

    # ============================================================
    # MUTE
    # ============================================================

    def mute(self):

        if not self.ready():
            return

        pyautogui.press("volumemute")

        print("\n🔇 MUTE")

    # ============================================================
    # PLAY / PAUSE
    # ============================================================

    def play_pause(self):

        if not self.ready():
            return

        pyautogui.press("playpause")

        print("\n▶️ PLAY / PAUSE")

    # ============================================================
    # NEXT TRACK
    # ============================================================

    def next_track(self):

        if not self.ready():
            return

        pyautogui.press("nexttrack")

        print("\n⏭️ NEXT TRACK")

    # ============================================================
    # PREVIOUS TRACK
    # ============================================================

    def previous_track(self):

        if not self.ready():
            return

        pyautogui.press("prevtrack")

        print("\n⏮️ PREVIOUS TRACK")

    # ============================================================
    # ALT + TAB
    # ============================================================

    def alt_tab(self):

        if not self.ready():
            return

        pyautogui.hotkey(
            "alt",
            "tab"
        )

        print("\n🪟 ALT + TAB")

    # ============================================================
    # SHOW DESKTOP
    # ============================================================

    def show_desktop(self):

        if not self.ready():
            return

        pyautogui.hotkey(
            "win",
            "d"
        )

        print("\n🖥️ SHOW DESKTOP")

    # ============================================================
    # LOCK WINDOWS
    # ============================================================

    def lock_windows(self):

        if not self.ready():
            return

        pyautogui.hotkey(
            "win",
            "l"
        )

        print("\n🔒 WINDOWS LOCKED")

    # ============================================================
    # SWIPE RIGHT
    # ============================================================

    def swipe_right(self):

        if not self.ready():
            return

        pyautogui.press(
            "nexttrack"
        )

        print("\n👉 NEXT TRACK")

    # ============================================================
    # SWIPE LEFT
    # ============================================================

    def swipe_left(self):

        if not self.ready():
            return

        pyautogui.press(
            "prevtrack"
        )

        print("\n👈 PREVIOUS TRACK")

    # ============================================================
    # SWIPE UP
    # ============================================================

    def swipe_up(self):

        if not self.ready():
            return

        pyautogui.hotkey(
            "alt",
            "tab"
        )

        print("\n⬆️ ALT + TAB")

    # ============================================================
    # SWIPE DOWN
    # ============================================================

    def swipe_down(self):

        if not self.ready():
            return

        pyautogui.hotkey(
            "win",
            "d"
        )

        print("\n⬇️ SHOW DESKTOP")