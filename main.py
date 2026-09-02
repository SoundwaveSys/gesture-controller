import cv2
import time

from vision.hand_tracker import HandTracker
from gestures.classifier import classify_gesture
from gestures.swipe import SwipeDetector

from actions.keyboard import KeyboardController
from actions.media import MediaController
from actions.volume import VolumeController
from actions.mouse import MouseController
from actions.system import SystemController


def main():

    # ============================================================
    # CAMERA
    # ============================================================

    camera = cv2.VideoCapture(0)

    if not camera.isOpened():

        print("ERROR: Could not open webcam.")

        return

    camera.set(
        cv2.CAP_PROP_FRAME_WIDTH,
        640
    )

    camera.set(
        cv2.CAP_PROP_FRAME_HEIGHT,
        480
    )

    # ============================================================
    # CONTROLLERS
    # ============================================================

    try:
        tracker = HandTracker(
            num_hands=2
        )
    except Exception as error:
        camera.release()
        print(f"ERROR: Could not load hand tracker: {error}")
        return

    keyboard = KeyboardController()
    media = MediaController()
    volume = VolumeController()
    mouse = MouseController()
    system = SystemController()
    swipe = SwipeDetector()

    # ============================================================
    # TWO-HAND WINDOWS LOCK
    # ============================================================

    lock_start_time = None
    lock_triggered = False

    # User must hold both fists for this long
    LOCK_HOLD_TIME = 1.5

    # ============================================================
    # STARTUP
    # ============================================================

    print()
    print("==============================================")
    print("       GESTURE CONTROLLER v1.2")
    print("          TWO HAND MODE")
    print("==============================================")
    print()

    print("RIGHT HAND")
    print("----------------------------------------------")
    print("INDEX          -> MOVE CURSOR")
    print("INDEX PINCH    -> LEFT CLICK")
    print("MIDDLE PINCH   -> RIGHT CLICK")
    print("PEACE          -> SCROLL")
    print()

    print("LEFT HAND")
    print("----------------------------------------------")
    print("THUMB UP       -> VOLUME UP")
    print("OPEN PALM      -> PLAY / PAUSE")
    print()

    print("SWIPE")
    print("----------------------------------------------")
    print("RIGHT          -> NEXT TRACK")
    print("LEFT           -> PREVIOUS TRACK")
    print("UP             -> ALT + TAB")
    print("DOWN           -> SHOW DESKTOP")
    print()

    print("SECURITY")
    print("----------------------------------------------")
    print("LEFT FIST + RIGHT FIST")
    print("HOLD 1.5 SEC    -> LOCK WINDOWS")
    print()

    print("ONE HAND")
    print("----------------------------------------------")
    print("INDEX          -> MOVE")
    print("PINCH          -> CLICK")
    print("PEACE          -> SCROLL")
    print()

    print("Press Q to quit.")
    print()
    print("==============================================")

    # ============================================================
    # MAIN LOOP
    # ============================================================

    try:

        while True:

            # ====================================================
            # READ CAMERA
            # ====================================================

            success, frame = camera.read()

            if not success:

                print(
                    "\nERROR: Could not read webcam frame."
                )

                break

            # Mirror camera
            frame = cv2.flip(
                frame,
                1
            )

            # ====================================================
            # HAND TRACKING
            # ====================================================

            result = tracker.process(
                frame
            )

            frame = tracker.draw_landmarks(
                frame,
                result
            )

            # ====================================================
            # GET HANDS
            # ====================================================

            hands = tracker.get_hands(
                result
            )

            gesture_text = "NO HAND"

            # ====================================================
            # TWO HAND MODE
            # ====================================================

            if len(hands) >= 2:

                left_hand = None
                right_hand = None

                # ------------------------------------------------
                # Find left and right hands
                # ------------------------------------------------

                for hand in hands:

                    if hand["label"] == "Left":

                        left_hand = hand["landmarks"]

                    elif hand["label"] == "Right":

                        right_hand = hand["landmarks"]

                # ------------------------------------------------
                # Classify both hands
                # ------------------------------------------------

                left_gesture = None
                right_gesture = None

                left_states = None
                right_states = None

                if left_hand is not None:

                    left_gesture, left_states = (
                        classify_gesture(
                            left_hand,
                            "Left"
                        )
                    )

                if right_hand is not None:

                    right_gesture, right_states = (
                        classify_gesture(
                            right_hand,
                            "Right"
                        )
                    )

                # =================================================
                # TWO FIST SECURITY LOCK
                # =================================================

                both_fists = (
                    left_gesture == "FIST"
                    and
                    right_gesture == "FIST"
                )

                if both_fists:

                    # Start timer
                    if lock_start_time is None:

                        lock_start_time = time.monotonic()

                        lock_triggered = False

                        print(
                            "\n🔐 TWO FIST LOCK SEQUENCE STARTED"
                        )

                    # Calculate hold time
                    elapsed = (
                        time.monotonic()
                        - lock_start_time
                    )

                    remaining = max(
                        0,
                        LOCK_HOLD_TIME - elapsed
                    )

                    # ------------------------------------------------
                    # Lock after required hold duration
                    # ------------------------------------------------

                    if (
                        elapsed >= LOCK_HOLD_TIME
                        and not lock_triggered
                    ):

                        system.lock_windows()

                        lock_triggered = True

                        gesture_text = (
                            "🔒 WINDOWS LOCKED"
                        )

                    else:

                        gesture_text = (
                            f"🔐 LOCKING... "
                            f"{remaining:.1f}s"
                        )

                    # ------------------------------------------------
                    # Stop mouse while security gesture is active
                    # ------------------------------------------------

                    mouse.handle_left_click(False)
                    mouse.handle_right_click(False)
                    mouse.reset()

                else:

                    # Reset lock sequence when fists are released
                    lock_start_time = None
                    lock_triggered = False

                    # =================================================
                    # RIGHT HAND CONTROLS
                    # =================================================

                    if right_hand is not None:

                        # ---------------------------------------------
                        # INDEX -> MOVE
                        # ---------------------------------------------

                        if right_gesture == "INDEX":

                            mouse.handle_left_click(False)
                            mouse.handle_right_click(False)

                            mouse.move_to_landmark(
                                right_hand[8]
                            )

                            gesture_text = (
                                "RIGHT INDEX - MOVE"
                            )

                        # ---------------------------------------------
                        # INDEX PINCH -> LEFT CLICK
                        # ---------------------------------------------

                        elif right_gesture == "PINCH_INDEX":

                            mouse.handle_right_click(False)

                            mouse.move_to_landmark(
                                right_hand[8]
                            )

                            mouse.handle_left_click(True)

                            gesture_text = (
                                "RIGHT PINCH - LEFT CLICK"
                            )

                        # ---------------------------------------------
                        # MIDDLE PINCH -> RIGHT CLICK
                        # ---------------------------------------------

                        elif right_gesture == "PINCH_MIDDLE":

                            mouse.handle_left_click(False)

                            mouse.handle_right_click(True)

                            gesture_text = (
                                "RIGHT PINCH - RIGHT CLICK"
                            )

                        # ---------------------------------------------
                        # PEACE -> SCROLL
                        # ---------------------------------------------

                        elif right_gesture == "PEACE":

                            mouse.handle_left_click(False)
                            mouse.handle_right_click(False)

                            middle_tip = right_hand[12]

                            difference = (
                                0.50
                                - middle_tip.y
                            )

                            if abs(difference) > 0.04:

                                scroll_amount = (
                                    difference * 35
                                )

                                mouse.scroll(
                                    scroll_amount
                                )

                            gesture_text = (
                                "RIGHT PEACE - SCROLL"
                            )

                        else:

                            mouse.handle_left_click(False)
                            mouse.handle_right_click(False)

                    # =================================================
                    # LEFT HAND CONTROLS
                    # =================================================

                    if left_hand is not None:

                        # ---------------------------------------------
                        # THUMB UP -> VOLUME
                        # ---------------------------------------------

                        if left_gesture == "THUMB_UP":

                            system.volume_up()

                            gesture_text = (
                                "LEFT THUMB - VOLUME UP"
                            )

                        # ---------------------------------------------
                        # OPEN PALM -> PLAY / PAUSE
                        # ---------------------------------------------

                        elif left_gesture == "OPEN_PALM":

                            system.play_pause()

                            gesture_text = (
                                "LEFT PALM - PLAY / PAUSE"
                            )

                        # ---------------------------------------------
                        # FIST
                        # ---------------------------------------------

                        elif left_gesture == "FIST":

                            gesture_text = (
                                "LEFT FIST"
                            )

                        # ---------------------------------------------
                        # UNKNOWN
                        # ---------------------------------------------

                        else:

                            pass

                # =================================================
                # TWO HAND STATUS
                # =================================================

                if not both_fists:

                    if (
                        left_gesture is not None
                        and right_gesture is not None
                    ):

                        gesture_text = (
                            f"L:{left_gesture} | "
                            f"R:{right_gesture}"
                        )

            # ====================================================
            # ONE HAND MODE
            # ====================================================

            elif len(hands) == 1:

                # Reset security timer
                lock_start_time = None
                lock_triggered = False

                hand = hands[0]

                landmarks = hand["landmarks"]
                label = hand["label"]

                # ------------------------------------------------
                # Classify gesture
                # ------------------------------------------------

                gesture, states = classify_gesture(
                    landmarks,
                    label
                )

                gesture_text = (
                    f"{label}: {gesture}"
                )

                # =================================================
                # SWIPE
                # =================================================

                swipe_direction = None

                if gesture == "INDEX":

                    swipe_direction = swipe.update(
                        landmarks[8]
                    )

                else:

                    swipe.reset()

                # =================================================
                # SWIPE ACTIONS
                # =================================================

                if swipe_direction == "RIGHT":

                    mouse.reset()

                    system.swipe_right()

                    gesture_text = (
                        "SWIPE RIGHT - NEXT"
                    )

                elif swipe_direction == "LEFT":

                    mouse.reset()

                    system.swipe_left()

                    gesture_text = (
                        "SWIPE LEFT - PREVIOUS"
                    )

                elif swipe_direction == "UP":

                    mouse.reset()

                    system.swipe_up()

                    gesture_text = (
                        "SWIPE UP - ALT TAB"
                    )

                elif swipe_direction == "DOWN":

                    mouse.reset()

                    system.swipe_down()

                    gesture_text = (
                        "SWIPE DOWN - DESKTOP"
                    )

                # =================================================
                # NORMAL MOUSE
                # =================================================

                elif gesture == "INDEX":

                    mouse.handle_left_click(False)
                    mouse.handle_right_click(False)

                    mouse.move_to_landmark(
                        landmarks[8]
                    )

                # =================================================
                # LEFT CLICK
                # =================================================

                elif gesture == "PINCH_INDEX":

                    mouse.handle_right_click(False)

                    mouse.move_to_landmark(
                        landmarks[8]
                    )

                    mouse.handle_left_click(True)

                # =================================================
                # RIGHT CLICK
                # =================================================

                elif gesture == "PINCH_MIDDLE":

                    mouse.handle_left_click(False)

                    mouse.handle_right_click(True)

                # =================================================
                # PEACE / SCROLL
                # =================================================

                elif gesture == "PEACE":

                    mouse.handle_left_click(False)
                    mouse.handle_right_click(False)

                    middle_tip = landmarks[12]

                    difference = (
                        0.50
                        - middle_tip.y
                    )

                    if abs(difference) > 0.04:

                        scroll_amount = (
                            difference * 35
                        )

                        mouse.scroll(
                            scroll_amount
                        )

                # =================================================
                # THUMB UP
                # =================================================

                elif gesture == "THUMB_UP":

                    mouse.reset()

                    system.volume_up()

                # =================================================
                # OPEN PALM
                # =================================================

                elif gesture == "OPEN_PALM":

                    mouse.reset()

                    system.play_pause()

                # =================================================
                # FIST
                # =================================================

                elif gesture == "FIST":

                    mouse.reset()

                # =================================================
                # UNKNOWN
                # =================================================

                else:

                    mouse.handle_left_click(False)
                    mouse.handle_right_click(False)

            # ====================================================
            # NO HAND
            # ====================================================

            else:

                mouse.handle_left_click(False)
                mouse.handle_right_click(False)

                mouse.reset()

                swipe.reset()

                # Reset security gesture
                lock_start_time = None
                lock_triggered = False

            # ====================================================
            # TERMINAL STATUS
            # ====================================================

            print(
                f"\r"
                f"Hands: {len(hands):<2} | "
                f"{gesture_text:<45}",
                end="",
                flush=True
            )

            # ====================================================
            # CAMERA UI
            # ====================================================

            cv2.rectangle(
                frame,
                (10, 10),
                (630, 105),
                (0, 0, 0),
                -1
            )

            # Main gesture
            cv2.putText(
                frame,
                f"{gesture_text}",
                (20, 55),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.72,
                (0, 255, 0),
                2
            )

            # Hands detected
            cv2.putText(
                frame,
                f"HANDS DETECTED: {len(hands)}",
                (20, 88),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.55,
                (255, 255, 255),
                2
            )

            # ====================================================
            # LOCK PROGRESS BAR
            # ====================================================

            if (
                lock_start_time is not None
                and not lock_triggered
            ):

                elapsed = (
                    time.monotonic()
                    - lock_start_time
                )

                progress = min(
                    elapsed / LOCK_HOLD_TIME,
                    1.0
                )

                # Background
                cv2.rectangle(
                    frame,
                    (10, 115),
                    (630, 135),
                    (50, 50, 50),
                    -1
                )

                # Progress
                cv2.rectangle(
                    frame,
                    (10, 115),
                    (
                        10 + int(
                            620 * progress
                        ),
                        135
                    ),
                    (0, 0, 255),
                    -1
                )

                cv2.putText(
                    frame,
                    "HOLD BOTH FISTS TO LOCK",
                    (20, 155),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.55,
                    (0, 0, 255),
                    2
                )

            # ====================================================
            # BOTTOM HELP
            # ====================================================

            cv2.putText(
                frame,
                "INDEX=MOVE | PINCH=CLICK | PEACE=SCROLL | Q=QUIT",
                (15, 465),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.48,
                (255, 255, 255),
                2
            )

            # ====================================================
            # DISPLAY
            # ====================================================

            cv2.imshow(
                "Gesture Controller",
                frame
            )

            # ====================================================
            # QUIT
            # ====================================================

            if cv2.waitKey(1) & 0xFF == ord("q"):

                break

    # ============================================================
    # CLEANUP
    # ============================================================

    finally:

        print()
        print()
        print(
            "Shutting down Gesture Controller..."
        )

        mouse.reset()

        swipe.reset()

        tracker.close()

        camera.release()

        cv2.destroyAllWindows()

        print(
            "Gesture Controller stopped."
        )


# ================================================================
# ENTRY POINT
# ================================================================

if __name__ == "__main__":

    main()