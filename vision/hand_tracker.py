import cv2
import mediapipe as mp
from pathlib import Path

from mediapipe.tasks import python
from mediapipe.tasks.python import vision


class HandTracker:

    def __init__(
        self,
        model_path=None,
        num_hands=2,
        detection_confidence=0.7,
        presence_confidence=0.7,
        tracking_confidence=0.7,
    ):

        # ========================================================
        # MEDIAPIPE MODEL
        # ========================================================

        if model_path is None:
            model_path = (
                Path(__file__).resolve().parent.parent
                / "models"
                / "hand_landmarker.task"
            )

        model_path = Path(model_path)

        if not model_path.is_file():
            raise FileNotFoundError(
                f"MediaPipe model not found: {model_path}"
            )

        base_options = python.BaseOptions(
            model_asset_path=str(model_path)
        )

        options = vision.HandLandmarkerOptions(
            base_options=base_options,
            running_mode=vision.RunningMode.VIDEO,
            num_hands=num_hands,
            min_hand_detection_confidence=detection_confidence,
            min_hand_presence_confidence=presence_confidence,
            min_tracking_confidence=tracking_confidence,
        )

        self.landmarker = (
            vision.HandLandmarker.create_from_options(
                options
            )
        )

        self.timestamp_ms = 0

    # ============================================================
    # PROCESS FRAME
    # ============================================================

    def process(self, frame):

        # OpenCV = BGR
        # MediaPipe = RGB

        rgb_frame = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2RGB
        )

        mp_image = mp.Image(
            image_format=mp.ImageFormat.SRGB,
            data=rgb_frame
        )

        self.timestamp_ms += 33

        result = self.landmarker.detect_for_video(
            mp_image,
            self.timestamp_ms
        )

        return result

    # ============================================================
    # GET HANDS
    # ============================================================

    def get_hands(self, result):

        hands = []

        if not result.hand_landmarks:
            return hands

        for index, landmarks in enumerate(
            result.hand_landmarks
        ):

            # Default label
            label = "Unknown"

            # MediaPipe handedness
            if (
                result.handedness
                and index < len(result.handedness)
            ):

                handedness = result.handedness[index]

                if handedness:

                    label = handedness[0].category_name

                    if label == "Left":
                        label = "Right"
                    elif label == "Right":
                        label = "Left"

            hands.append(
                {
                    "label": label,
                    "landmarks": landmarks,
                }
            )

        return hands

    # ============================================================
    # GET LEFT HAND
    # ============================================================

    def get_left_hand(self, result):

        hands = self.get_hands(result)

        for hand in hands:

            if hand["label"] == "Left":

                return hand["landmarks"]

        return None

    # ============================================================
    # GET RIGHT HAND
    # ============================================================

    def get_right_hand(self, result):

        hands = self.get_hands(result)

        for hand in hands:

            if hand["label"] == "Right":

                return hand["landmarks"]

        return None

    # ============================================================
    # DRAW LANDMARKS
    # ============================================================

    def draw_landmarks(
        self,
        frame,
        result
    ):

        if not result.hand_landmarks:
            return frame

        connections = (
            vision.HandLandmarksConnections.HAND_CONNECTIONS
        )

        height, width, _ = frame.shape

        for index, hand_landmarks in enumerate(
            result.hand_landmarks
        ):

            # ----------------------------------------------------
            # Determine hand label
            # ----------------------------------------------------

            label = "Unknown"

            if (
                result.handedness
                and index < len(result.handedness)
                and result.handedness[index]
            ):

                label = (
                    result.handedness[index][0]
                    .category_name
                )

                if label == "Left":
                    label = "Right"
                elif label == "Right":
                    label = "Left"

            # ----------------------------------------------------
            # Draw connections
            # ----------------------------------------------------

            for connection in connections:

                start = hand_landmarks[
                    connection.start
                ]

                end = hand_landmarks[
                    connection.end
                ]

                start_point = (
                    int(start.x * width),
                    int(start.y * height)
                )

                end_point = (
                    int(end.x * width),
                    int(end.y * height)
                )

                cv2.line(
                    frame,
                    start_point,
                    end_point,
                    (0, 255, 0),
                    2
                )

            # ----------------------------------------------------
            # Draw 21 landmarks
            # ----------------------------------------------------

            for landmark in hand_landmarks:

                x = int(
                    landmark.x * width
                )

                y = int(
                    landmark.y * height
                )

                cv2.circle(
                    frame,
                    (x, y),
                    5,
                    (0, 0, 255),
                    -1
                )

            # ----------------------------------------------------
            # Hand label
            # ----------------------------------------------------

            wrist = hand_landmarks[0]

            label_x = int(
                wrist.x * width
            )

            label_y = int(
                wrist.y * height
            ) - 15

            cv2.putText(
                frame,
                label,
                (
                    label_x,
                    label_y
                ),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.65,
                (255, 255, 0),
                2
            )

        return frame

    # ============================================================
    # CLOSE
    # ============================================================

    def close(self):

        self.landmarker.close()