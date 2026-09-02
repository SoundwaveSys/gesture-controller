# gesture-controller
Gesture Controller is a Python-based desktop application that enables hands-free computer control using hand gestures. It uses a webcam and MediaPipe hand tracking to detect real-time hand movements and translate them into computer actions.

## Features

### 10 Gesture Types Supported
Gesture Controller recognizes 10 distinct hand gestures using advanced hand pose detection:

1. **OPEN_PALM** - All fingers extended and spread
   - Use for: Opening/closing applications, showing state
   
2. **FIST** - All fingers folded
   - Use for: Closing/hiding, reset state
   
3. **INDEX** - Index finger extended, others folded
   - Use for: Pointing, selecting, navigation
   
4. **MIDDLE** - Middle finger extended, others folded
   - Use for: Secondary selection or action
   
5. **PEACE** - Index and middle fingers extended
   - Use for: Peace sign, alternating actions
   
6. **THUMB_UP** - Thumb extended upward, others folded
   - Use for: Approval, thumbs up action
   
7. **PINCH_INDEX** - Index and thumb pinched together
   - Use for: Precision control, fine adjustments
   
8. **PINCH_MIDDLE** - Middle and thumb pinched together
   - Use for: Alternative pinch action
   
9. **PINCH_RING** - Ring and thumb pinched together
   - Use for: Additional pinch variation
   
10. **PINCH_PINKY** - Pinky and thumb pinched together
    - Use for: Fine pinch control variant

### Action Controllers
- **Keyboard** - Text input, navigation, shortcuts (Ctrl+C, Ctrl+V, arrows, etc.)
- **Media** - Play/pause, next/previous track, stop
- **Volume** - Volume up/down, mute/unmute, max/min
- **Mouse** - Cursor movement, clicking, dragging
- **System** - Window management, desktop, screen refresh

## Requirements

- Python 3.8+
- Webcam
- MediaPipe hand_landmarker.task model
- opencv-python
- pyautogui

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Download MediaPipe hand landmark model:
   - Model should be placed in `models/hand_landmarker.task`

## Usage

```bash
python main.py
```

The application will:
1. Open your webcam
2. Display real-time hand tracking visualization
3. Recognize hand gestures
4. Execute corresponding system actions

Press `q` or close the window to exit.

## Configuration

Edit `config.py` to customize:
- Detection confidence thresholds
- Action cooldowns
- Gesture recognition parameters
- Camera resolution

## Testing

Run the comprehensive gesture classification test suite:
```bash
python gestures/test_classifier.py
```

This validates all 10 gesture types and conflict prevention logic.

## Project Structure

```
gesture-controller/
├── main.py                 # Application entry point
├── config.py              # Configuration settings
├── requirements.txt       # Python dependencies
│
├── actions/               # Action controllers
│   ├── keyboard.py       # Keyboard input simulation
│   ├── media.py          # Media control (play, pause, etc.)
│   ├── volume.py         # Volume control
│   ├── mouse.py          # Mouse control
│   └── system.py         # System-level actions
│
├── gestures/             # Gesture recognition
│   ├── classifier.py     # Core gesture classification engine
│   ├── stabilizer.py     # Hand pose smoothing
│   ├── swipe.py          # Swipe gesture detection
│   └── test_classifier.py # Test suite (15+ tests)
│
├── vision/               # Computer vision
│   └── hand_tracker.py   # MediaPipe integration
│
└── models/              # ML models
    └── hand_landmarker.task # MediaPipe hand detection model
```

## How It Works

1. **Hand Tracking**: MediaPipe detects 21 hand landmarks in real-time from webcam feed
2. **Gesture Classification**: Analyzes hand pose using distance/angle calculations
3. **Conflict Prevention**: Priority-based ordering ensures accurate gesture recognition
4. **Action Execution**: Triggers corresponding keyboard/mouse actions with cooldown

## Technical Details

### Hand Landmarks
- 21 3D coordinates per hand (wrist + 5 fingers × 4 joints)
- Normalized to 0.0-1.0 coordinate space
- 60+ FPS detection with MediaPipe's optimized model

### Gesture Classification Algorithm
- Distance-based finger extension detection
- Pinch detection using Euclidean distance threshold (35% of palm width)
- Mathematical angle calculation for complex poses
- Priority-based conflict resolution

### Action Scheduling
- Per-controller cooldown system (0.3-0.7 seconds)
- Prevents repeated rapid firing
- Cross-platform keyboard shortcuts (pyautogui)

## Future Enhancements

- [ ] Swipe gesture support (up/down/left/right)
- [ ] Rotation gesture detection
- [ ] Hand presence tracking optimization
- [ ] Real-time gesture visualization
- [ ] Custom gesture training
- [ ] Voice feedback integration
- [ ] Left/right hand specific actions

## License

See LICENSE file for details.

