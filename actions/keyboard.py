import time
import pyautogui


class KeyboardController:

    def __init__(self):

        # ========================================================
        # ACTION CONTROL
        # ========================================================

        self.last_action = 0

        # Prevent repeated keyboard actions
        self.cooldown = 0.3

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
    # ENTER
    # ============================================================

    def press_enter(self):

        if not self.ready():
            return

        pyautogui.press("return")

        print("\n⏎ ENTER")

    # ============================================================
    # ESCAPE
    # ============================================================

    def press_escape(self):

        if not self.ready():
            return

        pyautogui.press("escape")

        print("\n❌ ESCAPE")

    # ============================================================
    # SPACE
    # ============================================================

    def press_space(self):

        if not self.ready():
            return

        pyautogui.press("space")

        print("\n⎵ SPACE")

    # ============================================================
    # BACKSPACE
    # ============================================================

    def press_backspace(self):

        if not self.ready():
            return

        pyautogui.press("backspace")

        print("\n⌫ BACKSPACE")

    # ============================================================
    # DELETE
    # ============================================================

    def press_delete(self):

        if not self.ready():
            return

        pyautogui.press("delete")

        print("\n🗑️ DELETE")

    # ============================================================
    # COPY
    # ============================================================

    def copy(self):

        if not self.ready():
            return

        pyautogui.hotkey("ctrl", "c")

        print("\n📋 COPY")

    # ============================================================
    # PASTE
    # ============================================================

    def paste(self):

        if not self.ready():
            return

        pyautogui.hotkey("ctrl", "v")

        print("\n📌 PASTE")

    # ============================================================
    # CUT
    # ============================================================

    def cut(self):

        if not self.ready():
            return

        pyautogui.hotkey("ctrl", "x")

        print("\n✂️ CUT")

    # ============================================================
    # UNDO
    # ============================================================

    def undo(self):

        if not self.ready():
            return

        pyautogui.hotkey("ctrl", "z")

        print("\n↩️ UNDO")

    # ============================================================
    # REDO
    # ============================================================

    def redo(self):

        if not self.ready():
            return

        pyautogui.hotkey("ctrl", "y")

        print("\n↪️ REDO")

    # ============================================================
    # ARROW UP
    # ============================================================

    def arrow_up(self):

        if not self.ready():
            return

        pyautogui.press("up")

        print("\n⬆️ ARROW UP")

    # ============================================================
    # ARROW DOWN
    # ============================================================

    def arrow_down(self):

        if not self.ready():
            return

        pyautogui.press("down")

        print("\n⬇️ ARROW DOWN")

    # ============================================================
    # ARROW LEFT
    # ============================================================

    def arrow_left(self):

        if not self.ready():
            return

        pyautogui.press("left")

        print("\n⬅️ ARROW LEFT")

    # ============================================================
    # ARROW RIGHT
    # ============================================================

    def arrow_right(self):

        if not self.ready():
            return

        pyautogui.press("right")

        print("\n➡️ ARROW RIGHT")

    # ============================================================
    # SELECT ALL
    # ============================================================

    def select_all(self):

        if not self.ready():
            return

        pyautogui.hotkey("ctrl", "a")

        print("\n✓ SELECT ALL")

    # ============================================================
    # TAB
    # ============================================================

    def press_tab(self):

        if not self.ready():
            return

        pyautogui.press("tab")

        print("\n⇥ TAB")

    # ============================================================
    # PAGE UP
    # ============================================================

    def page_up(self):

        if not self.ready():
            return

        pyautogui.press("pageup")

        print("\n📄 PAGE UP")

    # ============================================================
    # PAGE DOWN
    # ============================================================

    def page_down(self):

        if not self.ready():
            return

        pyautogui.press("pagedown")

        print("\n📄 PAGE DOWN")
