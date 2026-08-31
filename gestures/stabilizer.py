import time
from collections import deque


class GestureStabilizer:

    def __init__(
        self,
        required_frames=6,
        cooldown=0.7
    ):
        self.required_frames = required_frames
        self.cooldown = cooldown

        self.history = deque(
            maxlen=required_frames
        )

        self.current_gesture = "NO HAND"
        self.last_triggered = None
        self.last_action_time = 0

    def update(self, gesture):

        self.history.append(gesture)

        # Not enough frames yet
        if len(self.history) < self.required_frames:
            return self.current_gesture, False

        # All recent frames must agree
        if len(set(self.history)) != 1:
            return self.current_gesture, False

        stable_gesture = self.history[-1]

        changed = (
            stable_gesture != self.current_gesture
        )

        self.current_gesture = stable_gesture

        now = time.monotonic()

        can_trigger = (
            changed
            and
            now - self.last_action_time >= self.cooldown
        )

        if can_trigger:
            self.last_triggered = stable_gesture
            self.last_action_time = now

        return stable_gesture, can_trigger

    def reset(self):

        self.history.clear()

        self.current_gesture = "NO HAND"

        self.last_triggered = None