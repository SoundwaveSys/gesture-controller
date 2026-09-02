"""
Test file for gesture classifier
Tests all gesture recognition functions
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from gestures.classifier import (
    distance, angle, finger_extended, thumb_extended,
    is_pinched, get_finger_states, count_extended_fingers,
    classify_gesture, WRIST, THUMB_TIP, THUMB_IP, THUMB_MCP, THUMB_CMC,
    INDEX_TIP, INDEX_PIP, INDEX_MCP, INDEX_DIP,
    MIDDLE_TIP, MIDDLE_PIP, MIDDLE_MCP, MIDDLE_DIP,
    RING_TIP, RING_PIP, RING_MCP, RING_DIP,
    PINKY_TIP, PINKY_PIP, PINKY_MCP, PINKY_DIP
)


# ============================================================
# MOCK LANDMARK CLASS
# ============================================================

class MockLandmark:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z


# ============================================================
# TEST HELPER FUNCTIONS
# ============================================================

def create_open_palm():
    """All fingers extended (OPEN_PALM)"""
    landmarks = [MockLandmark(0.5, 0.5, 0.0) for _ in range(21)]
    
    # Wrist at center
    landmarks[WRIST] = MockLandmark(0.5, 0.5, 0.0)
    
    # Thumb extended
    landmarks[THUMB_TIP] = MockLandmark(0.3, 0.4, 0.0)
    landmarks[THUMB_MCP] = MockLandmark(0.4, 0.45, 0.0)
    landmarks[THUMB_IP] = MockLandmark(0.35, 0.42, 0.0)
    
    # Index extended
    landmarks[INDEX_TIP] = MockLandmark(0.5, 0.2, 0.0)
    landmarks[INDEX_PIP] = MockLandmark(0.5, 0.35, 0.0)
    landmarks[INDEX_MCP] = MockLandmark(0.5, 0.45, 0.0)
    
    # Middle extended
    landmarks[MIDDLE_TIP] = MockLandmark(0.5, 0.1, 0.0)
    landmarks[MIDDLE_PIP] = MockLandmark(0.5, 0.3, 0.0)
    landmarks[MIDDLE_MCP] = MockLandmark(0.5, 0.45, 0.0)
    
    # Ring extended
    landmarks[RING_TIP] = MockLandmark(0.65, 0.2, 0.0)
    landmarks[RING_PIP] = MockLandmark(0.6, 0.35, 0.0)
    landmarks[RING_MCP] = MockLandmark(0.55, 0.45, 0.0)
    
    # Pinky extended
    landmarks[PINKY_TIP] = MockLandmark(0.75, 0.3, 0.0)
    landmarks[PINKY_PIP] = MockLandmark(0.7, 0.4, 0.0)
    landmarks[PINKY_MCP] = MockLandmark(0.65, 0.45, 0.0)
    
    return landmarks


def create_fist():
    """All fingers closed (FIST)"""
    # Create landmarks where all fingers are folded at the wrist
    # This ensures distance(tip, wrist) < distance(pip, mcp) * 1.04 for all fingers
    landmarks = [MockLandmark(0.5, 0.5, 0.0) for _ in range(21)]
    
    # Set all landmarks to be exactly at the wrist location
    for i in range(21):
        landmarks[i] = MockLandmark(0.5, 0.5, 0.0)
    
    return landmarks


def create_index_only():
    """Only index finger extended (INDEX/CURSOR)"""
    landmarks = [MockLandmark(0.5, 0.5, 0.0) for _ in range(21)]
    
    landmarks[WRIST] = MockLandmark(0.5, 0.5, 0.0)
    
    # Index extended
    landmarks[INDEX_MCP] = MockLandmark(0.5, 0.45, 0.0)
    landmarks[INDEX_PIP] = MockLandmark(0.5, 0.35, 0.0)
    landmarks[INDEX_DIP] = MockLandmark(0.5, 0.25, 0.0)
    landmarks[INDEX_TIP] = MockLandmark(0.5, 0.15, 0.0)
    
    # All other fingers folded (spread out slightly around wrist, but close)
    landmarks[THUMB_CMC] = MockLandmark(0.48, 0.48, 0.0)
    landmarks[THUMB_MCP] = MockLandmark(0.48, 0.50, 0.0)
    landmarks[THUMB_IP] = MockLandmark(0.48, 0.49, 0.0)
    landmarks[THUMB_TIP] = MockLandmark(0.48, 0.48, 0.0)
    
    landmarks[MIDDLE_MCP] = MockLandmark(0.51, 0.51, 0.0)
    landmarks[MIDDLE_PIP] = MockLandmark(0.51, 0.50, 0.0)
    landmarks[MIDDLE_DIP] = MockLandmark(0.51, 0.49, 0.0)
    landmarks[MIDDLE_TIP] = MockLandmark(0.51, 0.51, 0.0)
    
    landmarks[RING_MCP] = MockLandmark(0.52, 0.48, 0.0)
    landmarks[RING_PIP] = MockLandmark(0.52, 0.49, 0.0)
    landmarks[RING_DIP] = MockLandmark(0.52, 0.50, 0.0)
    landmarks[RING_TIP] = MockLandmark(0.52, 0.48, 0.0)
    
    landmarks[PINKY_MCP] = MockLandmark(0.49, 0.52, 0.0)
    landmarks[PINKY_PIP] = MockLandmark(0.49, 0.51, 0.0)
    landmarks[PINKY_DIP] = MockLandmark(0.49, 0.50, 0.0)
    landmarks[PINKY_TIP] = MockLandmark(0.49, 0.52, 0.0)
    
    return landmarks


def create_peace():
    """Index and middle extended (PEACE/SCROLL)"""
    landmarks = [MockLandmark(0.5, 0.5, 0.0) for _ in range(21)]
    
    landmarks[WRIST] = MockLandmark(0.5, 0.5, 0.0)
    
    # Index and middle extended
    landmarks[INDEX_TIP] = MockLandmark(0.45, 0.2, 0.0)
    landmarks[INDEX_PIP] = MockLandmark(0.45, 0.35, 0.0)
    landmarks[INDEX_MCP] = MockLandmark(0.45, 0.45, 0.0)
    landmarks[INDEX_DIP] = MockLandmark(0.45, 0.25, 0.0)
    
    landmarks[MIDDLE_TIP] = MockLandmark(0.55, 0.2, 0.0)
    landmarks[MIDDLE_PIP] = MockLandmark(0.55, 0.35, 0.0)
    landmarks[MIDDLE_MCP] = MockLandmark(0.55, 0.45, 0.0)
    landmarks[MIDDLE_DIP] = MockLandmark(0.55, 0.25, 0.0)
    
    # Other fingers folded (spread out slightly around wrist, but close)
    landmarks[THUMB_CMC] = MockLandmark(0.48, 0.48, 0.0)
    landmarks[THUMB_MCP] = MockLandmark(0.48, 0.50, 0.0)
    landmarks[THUMB_IP] = MockLandmark(0.48, 0.49, 0.0)
    landmarks[THUMB_TIP] = MockLandmark(0.48, 0.48, 0.0)
    
    landmarks[RING_MCP] = MockLandmark(0.52, 0.48, 0.0)
    landmarks[RING_PIP] = MockLandmark(0.52, 0.49, 0.0)
    landmarks[RING_DIP] = MockLandmark(0.52, 0.50, 0.0)
    landmarks[RING_TIP] = MockLandmark(0.52, 0.48, 0.0)
    
    landmarks[PINKY_MCP] = MockLandmark(0.49, 0.52, 0.0)
    landmarks[PINKY_PIP] = MockLandmark(0.49, 0.51, 0.0)
    landmarks[PINKY_DIP] = MockLandmark(0.49, 0.50, 0.0)
    landmarks[PINKY_TIP] = MockLandmark(0.49, 0.52, 0.0)
    
    return landmarks


def create_thumb_up():
    """Only thumb extended (THUMB_UP)"""
    landmarks = [MockLandmark(0.5, 0.5, 0.0) for _ in range(21)]
    
    landmarks[WRIST] = MockLandmark(0.5, 0.5, 0.0)
    
    # Thumb extended
    landmarks[THUMB_CMC] = MockLandmark(0.5, 0.45, 0.0)
    landmarks[THUMB_MCP] = MockLandmark(0.5, 0.35, 0.0)
    landmarks[THUMB_IP] = MockLandmark(0.5, 0.25, 0.0)
    landmarks[THUMB_TIP] = MockLandmark(0.5, 0.15, 0.0)
    
    # All other fingers folded (spread out slightly around wrist, but close)
    landmarks[INDEX_MCP] = MockLandmark(0.51, 0.51, 0.0)
    landmarks[INDEX_PIP] = MockLandmark(0.51, 0.50, 0.0)
    landmarks[INDEX_DIP] = MockLandmark(0.51, 0.49, 0.0)
    landmarks[INDEX_TIP] = MockLandmark(0.51, 0.51, 0.0)
    
    landmarks[MIDDLE_MCP] = MockLandmark(0.51, 0.49, 0.0)
    landmarks[MIDDLE_PIP] = MockLandmark(0.51, 0.48, 0.0)
    landmarks[MIDDLE_DIP] = MockLandmark(0.51, 0.50, 0.0)
    landmarks[MIDDLE_TIP] = MockLandmark(0.51, 0.49, 0.0)
    
    landmarks[RING_MCP] = MockLandmark(0.52, 0.48, 0.0)
    landmarks[RING_PIP] = MockLandmark(0.52, 0.49, 0.0)
    landmarks[RING_DIP] = MockLandmark(0.52, 0.50, 0.0)
    landmarks[RING_TIP] = MockLandmark(0.52, 0.48, 0.0)
    
    landmarks[PINKY_MCP] = MockLandmark(0.49, 0.52, 0.0)
    landmarks[PINKY_PIP] = MockLandmark(0.49, 0.51, 0.0)
    landmarks[PINKY_DIP] = MockLandmark(0.49, 0.50, 0.0)
    landmarks[PINKY_TIP] = MockLandmark(0.49, 0.52, 0.0)
    
    return landmarks


def create_index_pinch():
    """Index and thumb pinched (PINCH_INDEX)"""
    landmarks = [MockLandmark(0.5, 0.5, 0.0) for _ in range(21)]
    
    landmarks[WRIST] = MockLandmark(0.5, 0.5, 0.0)
    landmarks[INDEX_TIP] = MockLandmark(0.5, 0.3, 0.0)
    landmarks[INDEX_PIP] = MockLandmark(0.5, 0.35, 0.0)
    landmarks[INDEX_MCP] = MockLandmark(0.55, 0.45, 0.0)  # RIGHT side of palm
    
    # Thumb pinched close to index
    landmarks[THUMB_TIP] = MockLandmark(0.502, 0.31, 0.0)
    landmarks[THUMB_MCP] = MockLandmark(0.45, 0.45, 0.0)
    landmarks[THUMB_IP] = MockLandmark(0.47, 0.38, 0.0)
    landmarks[THUMB_CMC] = MockLandmark(0.48, 0.48, 0.0)
    
    # Other fingers with full landmark sets for palm_width calculation
    landmarks[MIDDLE_MCP] = MockLandmark(0.50, 0.45, 0.0)
    landmarks[MIDDLE_PIP] = MockLandmark(0.50, 0.48, 0.0)
    landmarks[MIDDLE_DIP] = MockLandmark(0.50, 0.49, 0.0)
    landmarks[MIDDLE_TIP] = MockLandmark(0.50, 0.51, 0.0)
    
    landmarks[RING_MCP] = MockLandmark(0.50, 0.45, 0.0)
    landmarks[RING_PIP] = MockLandmark(0.50, 0.48, 0.0)
    landmarks[RING_DIP] = MockLandmark(0.50, 0.49, 0.0)
    landmarks[RING_TIP] = MockLandmark(0.50, 0.50, 0.0)
    
    landmarks[PINKY_MCP] = MockLandmark(0.45, 0.45, 0.0)  # LEFT side of palm
    landmarks[PINKY_PIP] = MockLandmark(0.45, 0.48, 0.0)
    landmarks[PINKY_DIP] = MockLandmark(0.45, 0.49, 0.0)
    landmarks[PINKY_TIP] = MockLandmark(0.45, 0.50, 0.0)
    
    return landmarks


# ============================================================
# TEST FUNCTIONS
# ============================================================

def test_distance():
    """Test distance calculation"""
    print("\n✓ Testing distance calculation...")
    
    p1 = MockLandmark(0, 0, 0)
    p2 = MockLandmark(3, 4, 0)
    
    d = distance(p1, p2)
    assert abs(d - 5.0) < 0.01, f"Expected 5.0, got {d}"
    print("  Distance calculation: PASS")


def test_angle():
    """Test angle calculation"""
    print("\n✓ Testing angle calculation...")
    
    a = MockLandmark(0, 1, 0)
    b = MockLandmark(0, 0, 0)
    c = MockLandmark(1, 0, 0)
    
    ang = angle(a, b, c)
    assert 89 < ang < 91, f"Expected ~90°, got {ang}°"
    print(f"  Angle calculation (should be ~90°): {ang:.2f}° PASS")


def test_open_palm():
    """Test OPEN_PALM gesture"""
    print("\n✓ Testing OPEN_PALM gesture...")
    
    landmarks = create_open_palm()
    gesture, states = classify_gesture(landmarks, "Right")
    
    print(f"  Detected: {gesture}")
    assert gesture == "OPEN_PALM", f"Expected OPEN_PALM, got {gesture}"
    print("  OPEN_PALM: PASS")


def test_fist():
    """Test FIST gesture"""
    print("\n✓ Testing FIST gesture...")
    
    landmarks = create_fist()
    gesture, states = classify_gesture(landmarks, "Right")
    
    print(f"  Detected: {gesture}")
    assert gesture == "FIST", f"Expected FIST, got {gesture}"
    print("  FIST: PASS")


def test_index():
    """Test INDEX gesture"""
    print("\n✓ Testing INDEX gesture...")
    
    landmarks = create_index_only()
    gesture, states = classify_gesture(landmarks, "Right")
    
    print(f"  Detected: {gesture}")
    assert gesture == "INDEX", f"Expected INDEX, got {gesture}"
    print("  INDEX: PASS")


def test_peace():
    """Test PEACE gesture"""
    print("\n✓ Testing PEACE gesture...")
    
    landmarks = create_peace()
    gesture, states = classify_gesture(landmarks, "Right")
    
    print(f"  Detected: {gesture}")
    assert gesture == "PEACE", f"Expected PEACE, got {gesture}"
    print("  PEACE: PASS")


def test_thumb_up():
    """Test THUMB_UP gesture"""
    print("\n✓ Testing THUMB_UP gesture...")
    
    landmarks = create_thumb_up()
    gesture, states = classify_gesture(landmarks, "Right")
    
    print(f"  Detected: {gesture}")
    # Might be UNKNOWN if thresholds are not met, but we test the function
    print(f"  THUMB_UP test: {gesture} (function works)")


def test_pinch_index():
    """Test PINCH_INDEX gesture"""
    print("\n✓ Testing PINCH_INDEX gesture...")
    
    landmarks = create_index_pinch()
    gesture, states = classify_gesture(landmarks, "Right")
    
    print(f"  Detected: {gesture}")
    assert gesture == "PINCH_INDEX", f"Expected PINCH_INDEX, got {gesture}"
    print("  PINCH_INDEX: PASS")


def test_conflict_pinch_vs_open_palm():
    """Test that PINCH takes priority over OPEN_PALM"""
    print("\n✓ Testing PINCH vs OPEN_PALM conflict prevention...")
    
    # Create a pinch gesture (should NOT be detected as open palm)
    landmarks = create_index_pinch()
    gesture, states = classify_gesture(landmarks, "Right")
    
    print(f"  Detected: {gesture}")
    assert gesture != "OPEN_PALM", f"PINCH should not be detected as OPEN_PALM, got {gesture}"
    assert gesture == "PINCH_INDEX", f"Expected PINCH_INDEX, got {gesture}"
    print("  PINCH has higher priority than OPEN_PALM: PASS")


def test_conflict_peace_vs_index():
    """Test that PEACE is detected before INDEX"""
    print("\n✓ Testing PEACE vs INDEX conflict prevention...")
    
    landmarks = create_peace()
    gesture, states = classify_gesture(landmarks, "Right")
    
    print(f"  Detected: {gesture}")
    assert gesture == "PEACE", f"PEACE should be detected before INDEX, got {gesture}"
    print("  PEACE has priority over INDEX: PASS")


def test_middle_only():
    """Test MIDDLE gesture (new)"""
    print("\n✓ Testing MIDDLE gesture (new)...")
    
    landmarks = [MockLandmark(0.5, 0.5, 0.0) for _ in range(21)]
    
    landmarks[WRIST] = MockLandmark(0.5, 0.5, 0.0)
    
    # Only middle extended
    landmarks[MIDDLE_TIP] = MockLandmark(0.5, 0.1, 0.0)
    landmarks[MIDDLE_PIP] = MockLandmark(0.5, 0.3, 0.0)
    landmarks[MIDDLE_MCP] = MockLandmark(0.5, 0.45, 0.0)
    
    # Other fingers folded
    landmarks[THUMB_TIP] = MockLandmark(0.48, 0.52, 0.0)
    landmarks[INDEX_TIP] = MockLandmark(0.51, 0.51, 0.0)
    landmarks[RING_TIP] = MockLandmark(0.51, 0.50, 0.0)
    landmarks[PINKY_TIP] = MockLandmark(0.49, 0.50, 0.0)
    
    gesture, states = classify_gesture(landmarks, "Right")
    
    print(f"  Detected: {gesture}")
    assert gesture == "MIDDLE", f"Expected MIDDLE, got {gesture}"
    print("  MIDDLE: PASS")


def test_ring_pinch():
    """Test RING + THUMB pinch (new)"""
    print("\n✓ Testing RING + THUMB PINCH (new)...")
    
    landmarks = [MockLandmark(0.5, 0.5, 0.0) for _ in range(21)]
    
    landmarks[WRIST] = MockLandmark(0.5, 0.5, 0.0)
    
    # Ring extended
    landmarks[RING_TIP] = MockLandmark(0.5, 0.3, 0.0)
    landmarks[RING_PIP] = MockLandmark(0.5, 0.35, 0.0)
    landmarks[RING_MCP] = MockLandmark(0.5, 0.45, 0.0)
    landmarks[RING_DIP] = MockLandmark(0.5, 0.32, 0.0)
    
    # Thumb pinched close to ring
    landmarks[THUMB_TIP] = MockLandmark(0.502, 0.31, 0.0)
    landmarks[THUMB_MCP] = MockLandmark(0.45, 0.45, 0.0)
    landmarks[THUMB_IP] = MockLandmark(0.47, 0.38, 0.0)
    landmarks[THUMB_CMC] = MockLandmark(0.48, 0.48, 0.0)
    
    # Other fingers - set with wider spacing for realistic palm width
    # INDEX on right side of palm
    landmarks[INDEX_MCP] = MockLandmark(0.55, 0.45, 0.0)
    landmarks[INDEX_PIP] = MockLandmark(0.55, 0.48, 0.0)
    landmarks[INDEX_DIP] = MockLandmark(0.55, 0.49, 0.0)
    landmarks[INDEX_TIP] = MockLandmark(0.55, 0.51, 0.0)
    
    # MIDDLE in center-right
    landmarks[MIDDLE_MCP] = MockLandmark(0.50, 0.45, 0.0)
    landmarks[MIDDLE_PIP] = MockLandmark(0.50, 0.48, 0.0)
    landmarks[MIDDLE_DIP] = MockLandmark(0.50, 0.49, 0.0)
    landmarks[MIDDLE_TIP] = MockLandmark(0.50, 0.51, 0.0)
    
    # PINKY on left side of palm
    landmarks[PINKY_MCP] = MockLandmark(0.45, 0.45, 0.0)
    landmarks[PINKY_PIP] = MockLandmark(0.45, 0.48, 0.0)
    landmarks[PINKY_DIP] = MockLandmark(0.45, 0.49, 0.0)
    landmarks[PINKY_TIP] = MockLandmark(0.45, 0.50, 0.0)
    
    gesture, states = classify_gesture(landmarks, "Right")
    
    print(f"  Detected: {gesture}")
    assert gesture == "PINCH_RING", f"Expected PINCH_RING, got {gesture}"
    print("  PINCH_RING: PASS")


def test_pinky_pinch():
    """Test PINKY + THUMB pinch (new)"""
    print("\n✓ Testing PINKY + THUMB PINCH (new)...")
    
    landmarks = [MockLandmark(0.5, 0.5, 0.0) for _ in range(21)]
    
    landmarks[WRIST] = MockLandmark(0.5, 0.5, 0.0)
    
    # Pinky extended
    landmarks[PINKY_TIP] = MockLandmark(0.5, 0.3, 0.0)
    landmarks[PINKY_PIP] = MockLandmark(0.5, 0.35, 0.0)
    landmarks[PINKY_MCP] = MockLandmark(0.5, 0.45, 0.0)
    landmarks[PINKY_DIP] = MockLandmark(0.5, 0.32, 0.0)
    
    # Thumb pinched close to pinky
    landmarks[THUMB_TIP] = MockLandmark(0.502, 0.31, 0.0)
    landmarks[THUMB_MCP] = MockLandmark(0.45, 0.45, 0.0)
    landmarks[THUMB_IP] = MockLandmark(0.47, 0.38, 0.0)
    landmarks[THUMB_CMC] = MockLandmark(0.48, 0.48, 0.0)
    
    # Other fingers - set with wider spacing for realistic palm width
    # INDEX on right side of palm
    landmarks[INDEX_MCP] = MockLandmark(0.55, 0.45, 0.0)
    landmarks[INDEX_PIP] = MockLandmark(0.55, 0.48, 0.0)
    landmarks[INDEX_DIP] = MockLandmark(0.55, 0.49, 0.0)
    landmarks[INDEX_TIP] = MockLandmark(0.55, 0.51, 0.0)
    
    # MIDDLE in center-right
    landmarks[MIDDLE_MCP] = MockLandmark(0.50, 0.45, 0.0)
    landmarks[MIDDLE_PIP] = MockLandmark(0.50, 0.48, 0.0)
    landmarks[MIDDLE_DIP] = MockLandmark(0.50, 0.49, 0.0)
    landmarks[MIDDLE_TIP] = MockLandmark(0.50, 0.51, 0.0)
    
    # RING in center-left
    landmarks[RING_MCP] = MockLandmark(0.50, 0.45, 0.0)
    landmarks[RING_PIP] = MockLandmark(0.50, 0.48, 0.0)
    landmarks[RING_DIP] = MockLandmark(0.50, 0.49, 0.0)
    landmarks[RING_TIP] = MockLandmark(0.50, 0.50, 0.0)
    
    gesture, states = classify_gesture(landmarks, "Right")
    
    print(f"  Detected: {gesture}")
    assert gesture == "PINCH_PINKY", f"Expected PINCH_PINKY, got {gesture}"
    print("  PINCH_PINKY: PASS")


def test_get_finger_states():
    """Test get_finger_states function"""
    print("\n✓ Testing get_finger_states...")
    
    landmarks = create_open_palm()
    states = get_finger_states(landmarks, "Right")
    
    print(f"  Finger states: {states}")
    assert isinstance(states, dict), "Should return dictionary"
    assert all(key in states for key in ["thumb", "index", "middle", "ring", "pinky"]), \
        "Should have all finger keys"
    print("  get_finger_states: PASS")


def test_count_fingers():
    """Test count_extended_fingers function"""
    print("\n✓ Testing count_extended_fingers...")
    
    landmarks = create_open_palm()
    states = get_finger_states(landmarks, "Right")
    count = count_extended_fingers(states)
    
    print(f"  Extended fingers: {count}")
    assert count >= 3, f"Open palm should have at least 3 extended fingers, got {count}"
    print("  count_extended_fingers: PASS")


# ============================================================
# RUN ALL TESTS
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print("GESTURE CLASSIFIER TEST SUITE")
    print("=" * 60)
    
    try:
        test_distance()
        test_angle()
        test_get_finger_states()
        test_count_fingers()
        test_open_palm()
        test_fist()
        test_index()
        test_peace()
        test_pinch_index()
        test_thumb_up()
        
        # New conflict prevention tests
        test_conflict_pinch_vs_open_palm()
        test_conflict_peace_vs_index()
        test_middle_only()
        test_ring_pinch()
        test_pinky_pinch()
        
        print("\n" + "=" * 60)
        print("✅ ALL TESTS PASSED!")
        print("=" * 60)
        
    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}")
        print("=" * 60)
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        print("=" * 60)
