import math


# ============================================================
# MEDIAPIPE LANDMARK INDEXES
# ============================================================

WRIST = 0

THUMB_CMC = 1
THUMB_MCP = 2
THUMB_IP = 3
THUMB_TIP = 4

INDEX_MCP = 5
INDEX_PIP = 6
INDEX_DIP = 7
INDEX_TIP = 8

MIDDLE_MCP = 9
MIDDLE_PIP = 10
MIDDLE_DIP = 11
MIDDLE_TIP = 12

RING_MCP = 13
RING_PIP = 14
RING_DIP = 15
RING_TIP = 16

PINKY_MCP = 17
PINKY_PIP = 18
PINKY_DIP = 19
PINKY_TIP = 20


# ============================================================
# DISTANCE
# ============================================================

def distance(a, b):

    return math.sqrt(
        (a.x - b.x) ** 2
        + (a.y - b.y) ** 2
        + (a.z - b.z) ** 2
    )


# ============================================================
# ANGLE
# ============================================================

def angle(a, b, c):

    ba = (
        a.x - b.x,
        a.y - b.y,
        a.z - b.z
    )

    bc = (
        c.x - b.x,
        c.y - b.y,
        c.z - b.z
    )

    dot = (
        ba[0] * bc[0]
        + ba[1] * bc[1]
        + ba[2] * bc[2]
    )

    mag_ba = math.sqrt(
        ba[0] ** 2
        + ba[1] ** 2
        + ba[2] ** 2
    )

    mag_bc = math.sqrt(
        bc[0] ** 2
        + bc[1] ** 2
        + bc[2] ** 2
    )

    if mag_ba == 0 or mag_bc == 0:
        return 0

    cosine = dot / (mag_ba * mag_bc)

    cosine = max(-1, min(1, cosine))

    return math.degrees(
        math.acos(cosine)
    )


# ============================================================
# FINGER EXTENSION
# ============================================================

def finger_extended(
    landmarks,
    tip,
    pip,
    mcp
):

    tip_distance = distance(
        landmarks[tip],
        landmarks[WRIST]
    )

    pip_distance = distance(
        landmarks[pip],
        landmarks[WRIST]
    )

    finger_angle = angle(
        landmarks[mcp],
        landmarks[pip],
        landmarks[tip]
    )

    return (
        finger_angle > 150
        and tip_distance > pip_distance * 1.04
    )


# ============================================================
# THUMB EXTENSION
# ============================================================

def thumb_extended(
    landmarks,
    hand_label="Right"
):

    thumb_tip = landmarks[THUMB_TIP]
    thumb_ip = landmarks[THUMB_IP]
    thumb_mcp = landmarks[THUMB_MCP]

    index_mcp = landmarks[INDEX_MCP]
    pinky_mcp = landmarks[PINKY_MCP]

    # --------------------------------------------------------
    # Thumb angle
    # --------------------------------------------------------

    thumb_angle = angle(
        thumb_tip,
        thumb_ip,
        thumb_mcp
    )

    # --------------------------------------------------------
    # Palm width
    # --------------------------------------------------------

    palm_width = distance(
        index_mcp,
        pinky_mcp
    )

    thumb_length = distance(
        thumb_tip,
        thumb_mcp
    )

    angle_check = (
        thumb_angle > 140
    )

    distance_check = (
        thumb_length >
        palm_width * 0.60
    )

    return (
        angle_check
        and distance_check
    )


# ============================================================
# PINCH
# ============================================================

def is_pinched(
    landmarks,
    tip1,
    tip2
):

    palm_width = distance(
        landmarks[INDEX_MCP],
        landmarks[PINKY_MCP]
    )

    return (
        distance(
            landmarks[tip1],
            landmarks[tip2]
        )
        < palm_width * 0.35
    )


# ============================================================
# FINGER STATES
# ============================================================

def get_finger_states(
    landmarks,
    hand_label="Right"
):

    return {

        "thumb": thumb_extended(
            landmarks,
            hand_label
        ),

        "index": finger_extended(
            landmarks,
            INDEX_TIP,
            INDEX_PIP,
            INDEX_MCP
        ),

        "middle": finger_extended(
            landmarks,
            MIDDLE_TIP,
            MIDDLE_PIP,
            MIDDLE_MCP
        ),

        "ring": finger_extended(
            landmarks,
            RING_TIP,
            RING_PIP,
            RING_MCP
        ),

        "pinky": finger_extended(
            landmarks,
            PINKY_TIP,
            PINKY_PIP,
            PINKY_MCP
        )
    }


# ============================================================
# COUNT FINGERS
# ============================================================

def count_extended_fingers(states):

    return sum(
        states.values()
    )


# ============================================================
# CLASSIFY GESTURE
# ============================================================

def classify_gesture(
    landmarks,
    hand_label="Right"
):

    states = get_finger_states(
        landmarks,
        hand_label
    )

    thumb = states["thumb"]
    index = states["index"]
    middle = states["middle"]
    ring = states["ring"]
    pinky = states["pinky"]

    # ========================================================
    # INDEX + THUMB PINCH
    # ========================================================

    if is_pinched(
        landmarks,
        INDEX_TIP,
        THUMB_TIP
    ):

        return (
            "PINCH_INDEX",
            states
        )

    # ========================================================
    # MIDDLE + THUMB PINCH
    # ========================================================

    if (
        is_pinched(
            landmarks,
            MIDDLE_TIP,
            THUMB_TIP
        )
        and not index
    ):

        return (
            "PINCH_MIDDLE",
            states
        )

    # ========================================================
    # OPEN PALM
    # ========================================================

    if (
        thumb
        and index
        and middle
        and ring
        and pinky
    ):

        return (
            "OPEN_PALM",
            states
        )

    # ========================================================
    # THUMB UP
    # ========================================================

    if (
        thumb
        and not index
        and not middle
        and not ring
        and not pinky
    ):

        return (
            "THUMB_UP",
            states
        )

    # ========================================================
    # PEACE / SCROLL
    # ========================================================

    if (
        index
        and middle
        and not ring
        and not pinky
    ):

        return (
            "PEACE",
            states
        )

    # ========================================================
    # INDEX / CURSOR
    # ========================================================

    if (
        index
        and not middle
        and not ring
        and not pinky
    ):

        return (
            "INDEX",
            states
        )

    # ========================================================
    # FIST
    # ========================================================

    if (
        not thumb
        and not index
        and not middle
        and not ring
        and not pinky
    ):

        return (
            "FIST",
            states
        )

    # ========================================================
    # UNKNOWN
    # ========================================================

    return (
        "UNKNOWN",
        states
    )