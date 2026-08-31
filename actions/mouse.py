import time
import pyautogui


class MouseController:

    def __init__(self):

        self.screen_width, self.screen_height = pyautogui.size()

        # Cursor
        self.margin_x = 0.10
        self.margin_y = 0.10
        self.smoothing = 0.30

        self.prev_x = None
        self.prev_y = None

        # Left pinch
        self.pinch_active = False

        # Double click
        self.last_pinch_time = 0
        self.double_click_window = 0.45

        # Click cooldown
        self.last_click_time = 0
        self.click_cooldown = 0.20

        # Drag
        self.dragging = False
        self.drag_start_time = None
        self.drag_delay = 0.35

        # Right click
        self.right_click_active = False

        pyautogui.PAUSE = 0.01

    # ============================================================
    # CAMERA → SCREEN
    # ============================================================

    def _map_coordinate(self, value, margin):

        value = (
            value - margin
        ) / (
            1.0 - 2.0 * margin
        )

        return max(
            0.0,
            min(1.0, value)
        )

    # ============================================================
    # MOVE CURSOR
    # ============================================================

    def move_to_landmark(self, landmark):

        normalized_x = self._map_coordinate(
            landmark.x,
            self.margin_x
        )

        normalized_y = self._map_coordinate(
            landmark.y,
            self.margin_y
        )

        target_x = int(
            normalized_x
            * (self.screen_width - 1)
        )

        target_y = int(
            normalized_y
            * (self.screen_height - 1)
        )

        if self.prev_x is None:

            self.prev_x = target_x
            self.prev_y = target_y

        smooth_x = (
            self.prev_x
            + (target_x - self.prev_x)
            * self.smoothing
        )

        smooth_y = (
            self.prev_y
            + (target_y - self.prev_y)
            * self.smoothing
        )

        self.prev_x = smooth_x
        self.prev_y = smooth_y

        pyautogui.moveTo(
            int(smooth_x),
            int(smooth_y),
            duration=0
        )

    # ============================================================
    # LEFT CLICK / DOUBLE CLICK / DRAG
    # ============================================================

    def handle_left_click(self, pinch_detected):

        now = time.monotonic()

        if pinch_detected:

            # Already holding pinch
            if self.pinch_active:

                # Start drag after holding
                if (
                    not self.dragging
                    and self.drag_start_time is not None
                    and now - self.drag_start_time
                    >= self.drag_delay
                ):

                    pyautogui.mouseDown()

                    self.dragging = True

                    print("\nDRAG START")

                return

            # New pinch
            self.pinch_active = True
            self.drag_start_time = now

            # Cooldown
            if (
                now - self.last_click_time
                < self.click_cooldown
            ):
                return

            # Double click
            if (
                now - self.last_pinch_time
                <= self.double_click_window
            ):

                pyautogui.doubleClick(
                    interval=0.08
                )

                print("\nDOUBLE CLICK")

                self.last_pinch_time = 0

            else:

                pyautogui.click()

                print("\nLEFT CLICK")

                self.last_pinch_time = now

            self.last_click_time = now

        else:

            if self.pinch_active:

                if self.dragging:

                    pyautogui.mouseUp()

                    print("\nDRAG END")

                    self.dragging = False

            self.pinch_active = False
            self.drag_start_time = None

    # ============================================================
    # RIGHT CLICK
    # ============================================================

    def handle_right_click(self, detected):

        if detected:

            if not self.right_click_active:

                pyautogui.rightClick()

                print("\nRIGHT CLICK")

                self.right_click_active = True

        else:

            self.right_click_active = False

    # ============================================================
    # SCROLL
    # ============================================================

    def scroll(self, amount):

        if abs(amount) < 1:
            return

        pyautogui.scroll(
            int(amount)
        )

    # ============================================================
    # RESET
    # ============================================================

    def reset(self):

        if self.dragging:

            pyautogui.mouseUp()

            self.dragging = False

        self.prev_x = None
        self.prev_y = None

        self.pinch_active = False
        self.drag_start_time = None

        self.right_click_active = False