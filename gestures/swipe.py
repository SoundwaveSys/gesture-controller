import time
import math


class SwipeDetector:

    def __init__(self):
        self.points = []

        self.max_points = 8

        self.min_distance = 0.18

        self.max_time = 0.6

        self.cooldown = 0.8

        self.last_swipe = 0

    def update(self, landmark):

        now = time.monotonic()

        self.points.append(
            (
                landmark.x,
                landmark.y,
                now
            )
        )

        if len(self.points) > self.max_points:
            self.points.pop(0)

        # Not enough points
        if len(self.points) < 4:
            return None

        start_x, start_y, start_time = self.points[0]
        end_x, end_y, end_time = self.points[-1]

        elapsed = end_time - start_time

        if elapsed > self.max_time:
            self.points.pop(0)
            return None

        dx = end_x - start_x
        dy = end_y - start_y

        distance = math.sqrt(
            dx * dx + dy * dy
        )

        # Minimum movement
        if distance < self.min_distance:
            return None

        # Cooldown
        if now - self.last_swipe < self.cooldown:
            return None

        # Horizontal swipe
        if abs(dx) > abs(dy):

            if dx > 0:

                self.last_swipe = now
                self.points.clear()

                return "RIGHT"

            else:

                self.last_swipe = now
                self.points.clear()

                return "LEFT"

        # Vertical swipe
        else:

            if dy < 0:

                self.last_swipe = now
                self.points.clear()

                return "UP"

            else:

                self.last_swipe = now
                self.points.clear()

                return "DOWN"

    def reset(self):

        self.points.clear()