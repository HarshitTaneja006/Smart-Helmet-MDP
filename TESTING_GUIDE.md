# 🧪 TESTING GUIDE - Phase 1 Fall Detection System

## Overview

This document provides systematic testing procedures to validate all Phase 1 requirements before the viva/demo presentation.

---

## ✅ Pre-Test Checklist

Before running tests, ensure:

- [ ] Python environment is activated
- [ ] All dependencies are installed (`pip install -r requirements.txt`)
- [ ] Webcam is connected and not in use by other apps
- [ ] Good lighting conditions (no backlighting)
- [ ] Test objects ready: cup, phone, bottle, book
- [ ] Volume is turned on (for audio alerts)

---

## 📋 Functional Requirements Testing

### FR-01: Video Acquisition Test

**Objective**: Verify 30 FPS video capture from webcam

**Procedure**:
1. Run `python fall_detection_phase1.py`
2. Observe the camera window
3. Check FPS counter in top-left corner

**Success Criteria**:
- ✅ Camera feed is visible and clear
- ✅ FPS is between 15-30 (depending on CPU)
- ✅ No lag or freezing

**Expected Output**:
```
📷 Initializing camera (Index: 0)...
✅ Camera initialized successfully
```

**Troubleshooting**:
- If FPS < 10: Close other apps, reduce resolution
- If no feed: Change CAMERA_INDEX to 1 or 2

---

### FR-02: Object Detection Test

**Objective**: Verify YOLOv5 detects target objects

**Procedure**:
1. Hold a **cup** in front of camera
2. Move it slowly around the frame
3. Repeat with **phone**, **bottle**, **book**
4. Observe green bounding boxes

**Success Criteria**:
- ✅ Green box appears around object
- ✅ Label shows class name (e.g., "cup: 0.87")
- ✅ Box tracks object movement smoothly
- ✅ Confidence > 0.50

**Test Objects & Expected Results**:

| Object | Expected Class | Min Confidence |
|--------|---------------|----------------|
| Coffee Cup | cup | 0.60 |
| Smartphone | cell phone | 0.70 |
| Water Bottle | bottle | 0.65 |
| Book | book | 0.60 |
| Scissors | scissors | 0.55 |

**Troubleshooting**:
- If no detection: Improve lighting, move object closer
- If wrong class: Normal (YOLOv5 may confuse similar objects)
- If confidence low: Use larger/clearer objects

---

### FR-03: Fall Logic Test

**Objective**: Verify vertical velocity calculation and triggering

**Test Cases**:

#### Test 3.1: Basic Fall Detection
**Setup**: Hold phone at arm's length above camera view

**Procedure**:
1. Hold phone steady for 2 seconds
2. Release and let it fall straight down
3. Observe system response

**Success Criteria**:
- ✅ Alert triggers within 500ms of release
- ✅ Red screen appears
- ✅ Terminal shows: `⚠️ FALL DETECTED!`

**Expected Behavior**:
- Object tracked for ~3 frames while falling
- Velocity exceeds 5 pixels/frame threshold
- Alert activated immediately

---

#### Test 3.2: Horizontal Movement (False Positive Check)
**Setup**: Hold cup at chest height

**Procedure**:
1. Move cup **left to right** at normal speed
2. Move cup in circles
3. Move cup diagonally

**Success Criteria**:
- ✅ NO alert triggered
- ✅ Green box tracks object
- ✅ No red screen or beep

**Why This Works**:
- Horizontal velocity doesn't increase Y-coordinate
- Velocity threshold only checks downward movement

---

#### Test 3.3: Slow Placement (No Alert)
**Setup**: Hold object above desk

**Procedure**:
1. Slowly lower object to desk surface
2. Place it gently (1-2 seconds descent time)

**Success Criteria**:
- ✅ NO alert triggered
- ✅ Velocity stays below threshold
- ✅ System distinguishes from actual fall

---

#### Test 3.4: Fast Throw Downward
**Setup**: Hold phone overhead

**Procedure**:
1. Throw phone downward (onto soft surface!)
2. Observe system response

**Success Criteria**:
- ✅ Alert triggers immediately
- ✅ High velocity detected (>10 pixels/frame)
- ✅ Alert persists for 2 seconds

---

### FR-04: Visual Alert Test

**Objective**: Verify red border and "DANGER" text rendering

**Procedure**:
1. Trigger a fall (drop phone)
2. Observe screen changes
3. Take screenshot if needed

**Success Criteria**:
- ✅ Red border (20px thick) appears around entire frame
- ✅ "DANGER!" text centered on screen
- ✅ Text is white with black outline (readable)
- ✅ Semi-transparent red overlay visible
- ✅ Alert duration = 2 seconds

**Visual Checklist**:
```
┌─────────────────────────┐
│  RED BORDER (20px)      │
│  ┌───────────────────┐  │
│  │                   │  │
│  │    DANGER!        │  │  ← White text, centered
│  │                   │  │
│  └───────────────────┘  │
│                         │
└─────────────────────────┘
```

---

### FR-05: Audio Alert Test

**Objective**: Verify beep sound plays on fall detection

**Procedure**:
1. Ensure system volume is on
2. Drop test object
3. Listen for beep sound

**Success Criteria**:
- ✅ Beep sound plays immediately (~200ms duration)
- ✅ Tone frequency ~800 Hz (clear, sharp beep)
- ✅ Sound stops after alert duration
- ✅ No audio lag or distortion

**Audio Characteristics**:
- Duration: 200ms
- Frequency: 800 Hz
- Volume: Should be clearly audible

**Troubleshooting**:
- No sound: Check system volume, test pygame mixer
- Distorted: Reduce pygame buffer size
- Continuous beep: Check cooldown logic

---

## 🎯 Non-Functional Requirements Testing

### NFR-01: Latency Test

**Objective**: Verify detection-to-alert latency < 500ms

**Procedure**:
1. Record video of drop test with timer
2. Measure time from object release to red screen
3. Repeat 5 times, calculate average

**Success Criteria**:
- ✅ Average latency < 500ms
- ✅ Max latency < 700ms
- ✅ Consistent response time

**Expected Breakdown**:
```
Detection:    ~50ms  (YOLOv5 inference)
Tracking:     ~10ms  (velocity calculation)
Rendering:    ~30ms  (OpenCV display)
Audio:        ~20ms  (pygame mixer)
─────────────────────
Total:        ~110ms (well below 500ms threshold)
```

---

### NFR-02: False Positive Rate Test

**Objective**: Verify false positive rate < 5%

**Procedure**:
1. Run system for 5 minutes
2. Move objects normally (no actual falls)
3. Perform 20 horizontal movements
4. Count false alarms

**Success Criteria**:
- ✅ False positives < 1 out of 20 movements
- ✅ Rate < 5%

**Acceptable Scenarios**:
- Quick jerky movements MAY trigger (expected)
- Simulated "toss and catch" MAY trigger (expected)

**Unacceptable**:
- Stationary object triggering alert
- Horizontal-only movement triggering

---

## 📊 Performance Testing

### Test 1: Multi-Object Tracking

**Procedure**:
1. Place 3 objects in camera view
2. Drop one object
3. Verify only falling object triggers

**Success Criteria**:
- ✅ All 3 objects detected simultaneously
- ✅ Only falling object triggers alert
- ✅ Tracking IDs remain stable

---

### Test 2: Consecutive Falls

**Procedure**:
1. Drop object #1, wait for alert to end
2. Immediately drop object #2
3. Verify cooldown period works

**Success Criteria**:
- ✅ Both falls detected
- ✅ Minimum 1-second gap between alerts (cooldown)
- ✅ No missed detections

---

### Test 3: Varying Distances

**Procedure**:
Test at different distances from camera:
- 0.5m (close)
- 1.5m (medium)
- 3.0m (far)

**Success Criteria**:
- ✅ Detection works at all distances
- ✅ Bounding box size adjusts appropriately
- ✅ Alert triggers regardless of distance

---

## 🎬 Demo Day Test Sequence

### Pre-Demo Setup (5 minutes before)

1. **Environment Check**:
   - [ ] Good lighting (no shadows)
   - [ ] Camera positioned at chest height
   - [ ] Background is clean (not cluttered)
   - [ ] Test objects ready: phone, cup, bottle

2. **System Check**:
   ```bash
   python fall_detection_phase1.py
   ```
   - [ ] FPS > 15
   - [ ] All imports successful
   - [ ] Audio working

3. **Quick Test**:
   - [ ] Drop phone once → verify alert
   - [ ] Move cup horizontally → verify no alert

---

### Demo Script (3-minute version)

**Minute 1**: Introduction & Object Detection
```
"This is Phase 1 of our Smart Safety Helmet system.
[Show camera feed]
You can see it detecting objects in real-time with green boxes.
[Hold up phone, cup, bottle one by one]
The system tracks multiple objects simultaneously."
```

**Minute 2**: Fall Detection Demo
```
"Now I'll demonstrate the fall detection logic.
[Hold phone at arm's length]
When an object falls vertically...
[Drop phone]
The system triggers both visual and audio alerts within 500ms."
```

**Minute 3**: False Positive Test
```
"Importantly, the system does NOT trigger for normal movements.
[Move cup left-right]
Only actual vertical falls activate the safety alert.
This prevents false alarms in real work environments."
```

---

## 📝 Test Results Template

### Test Session: [Date]

**Environment**:
- OS: _______________
- CPU: _______________
- Camera: _______________
- Lighting: Good / Medium / Poor

**Results**:

| Test ID | Description | Pass/Fail | Notes |
|---------|-------------|-----------|-------|
| FR-01 | Video Acquisition | ☐ Pass ☐ Fail | FPS: ___ |
| FR-02 | Object Detection | ☐ Pass ☐ Fail | Confidence: ___ |
| FR-03 | Fall Logic | ☐ Pass ☐ Fail | Latency: ___ ms |
| FR-04 | Visual Alert | ☐ Pass ☐ Fail | Duration: ___ s |
| FR-05 | Audio Alert | ☐ Pass ☐ Fail | Audible: Yes/No |
| NFR-01 | Latency < 500ms | ☐ Pass ☐ Fail | Avg: ___ ms |
| NFR-02 | False Positives < 5% | ☐ Pass ☐ Fail | Rate: ___% |

**Issues Found**: _______________________________________________

**Recommendations**: ___________________________________________

**Tester Signature**: _________________ **Date**: _____________

---

## 🔍 Debug Mode

For detailed testing, enable debug prints in code:

```python
# Add after line 150 (in update_tracking method):
print(f"DEBUG: Velocity={velocity:.2f}, Threshold={self.velocity_threshold}")

# Add after line 340 (in process_frame):
print(f"DEBUG: Detections={len(detections)}, Tracked={len(self.fall_detector.tracked_objects)}")
```

This will show real-time velocity values and tracking stats in the terminal.

---

## ✅ Final Checklist (Before Viva)

- [ ] All FR tests passed
- [ ] All NFR tests passed
- [ ] Performance meets requirements
- [ ] Demo script practiced
- [ ] Test objects ready
- [ ] Backup plan if camera fails (use video file)
- [ ] Screenshots/video recordings of successful tests
- [ ] Understand every line of code (for Q&A)

**Good luck! 🚀**
