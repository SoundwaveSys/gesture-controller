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