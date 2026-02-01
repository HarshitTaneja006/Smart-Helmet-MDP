"""
SIMPLIFIED TEST VERSION - Quick Validation
Use this to quickly test if your environment is working

This minimal version:
- Tests camera access
- Tests YOLOv5 loading
- Tests basic object detection
- No fall detection (just validates components)
"""

import cv2
import torch
import numpy as np

print("=" * 60)
print("🧪 SIMPLIFIED TEST - Component Validation")
print("=" * 60)

# Test 1: Camera Access
print("\n[TEST 1] Camera Access...")
try:
    cap = cv2.VideoCapture(0)
    if cap.isOpened():
        ret, frame = cap.read()
        if ret:
            print(f"✅ Camera working - Resolution: {frame.shape[1]}x{frame.shape[0]}")
        else:
            print("❌ Camera opened but can't read frames")
        cap.release()
    else:
        print("❌ Can't open camera at index 0")
        print("   Try changing index to 1 or 2")
except Exception as e:
    print(f"❌ Camera test failed: {e}")

# Test 2: YOLOv5 Loading
print("\n[TEST 2] YOLOv5 Model Loading...")
try:
    model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)
    model.conf = 0.5
    print("✅ YOLOv5 model loaded successfully")
except Exception as e:
    print(f"❌ Model loading failed: {e}")
    print("   Check internet connection for first-time download")

# Test 3: Basic Detection
print("\n[TEST 3] Running Detection Test...")
try:
    cap = cv2.VideoCapture(0)
    print("📷 Press SPACE to capture and detect, Q to quit")
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        # Display frame
        cv2.putText(frame, "Press SPACE to detect, Q to quit", 
                   (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.imshow('Test Window', frame)
        
        key = cv2.waitKey(1) & 0xFF
        
        if key == ord(' '):  # Space bar
            print("   Running detection...")
            results = model(frame)
            detections = results.xyxy[0]
            
            if len(detections) > 0:
                print(f"   ✅ Detected {len(detections)} objects:")
                for *box, conf, cls in detections:
                    class_name = model.names[int(cls)]
                    print(f"      - {class_name}: {conf:.2f}")
                    x1, y1, x2, y2 = map(int, box)
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.putText(frame, f"{class_name}: {conf:.2f}", 
                              (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 
                              0.5, (0, 255, 0), 2)
                
                cv2.imshow('Detection Result', frame)
                cv2.waitKey(3000)  # Show for 3 seconds
            else:
                print("   ⚠️  No objects detected")
                print("      Try holding a cup/phone closer to camera")
        
        elif key == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()
    print("✅ Detection test complete")
    
except Exception as e:
    print(f"❌ Detection test failed: {e}")

# Test 4: Audio System
print("\n[TEST 4] Audio System...")
try:
    import pygame
    pygame.mixer.init()
    
    # Generate test beep
    sample_rate = 22050
    duration = 0.3
    frequency = 800
    
    n_samples = int(duration * sample_rate)
    buf = np.sin(2 * np.pi * frequency * np.linspace(0, duration, n_samples))
    buf = (buf * 32767).astype(np.int16)
    stereo_buf = np.column_stack((buf, buf))
    
    beep = pygame.sndarray.make_sound(stereo_buf)
    
    print("   Playing test beep...")
    beep.play()
    pygame.time.wait(int(duration * 1000))
    
    pygame.mixer.quit()
    print("✅ Audio system working")
    
except Exception as e:
    print(f"❌ Audio test failed: {e}")

print("\n" + "=" * 60)
print("🎯 COMPONENT VALIDATION COMPLETE")
print("=" * 60)
print("\nIf all tests passed ✅, you can run:")
print("  python fall_detection_phase1.py")
print("\nIf any tests failed ❌, check the troubleshooting guide")
print("=" * 60)
