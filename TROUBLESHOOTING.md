# 🔧 TROUBLESHOOTING GUIDE

## Common Issues and Solutions

This guide covers the most common problems you might encounter during setup and execution.

---

## 🚨 Installation Issues

### Issue 1: "pip: command not found"

**Problem**: pip is not installed or not in PATH

**Solutions**:

**Windows**:
```bash
python -m ensurepip --upgrade
python -m pip install --upgrade pip
```

**Linux/Mac**:
```bash
sudo apt-get install python3-pip  # Ubuntu/Debian
brew install python3              # Mac
```

---

### Issue 2: "torch installation failed" or "Could not find a version that satisfies the requirement torch"

**Problem**: PyTorch installation issues (common on older systems)

**Solutions**:

**For CPU-only installation** (most reliable):
```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
```

**For specific Python version** (e.g., Python 3.8):
```bash
pip install torch==2.0.0 torchvision==0.15.0 --index-url https://download.pytorch.org/whl/cpu
```

**Check compatibility**:
- Visit: https://pytorch.org/get-started/locally/
- Select your OS, Python version, and compute platform

---

### Issue 3: "opencv-python installation failed"

**Problem**: Missing system dependencies

**Solutions**:

**Ubuntu/Debian**:
```bash
sudo apt-get update
sudo apt-get install -y python3-opencv libopencv-dev
sudo apt-get install -y libgl1-mesa-glx libglib2.0-0
```

**Mac**:
```bash
brew install opencv
```

**Windows**: Usually works fine, but if issues:
- Download Microsoft Visual C++ Redistributable
- Install from: https://support.microsoft.com/en-us/help/2977003

**Alternative** (if nothing works):
```bash
pip install opencv-python-headless  # No GUI support
```

---

### Issue 4: "pygame installation failed" or "SDL.h not found"

**Problem**: Missing SDL2 libraries

**Solutions**:

**Ubuntu/Debian**:
```bash
sudo apt-get install -y python3-pygame libsdl2-dev libsdl2-mixer-2.0-0
```

**Mac**:
```bash
brew install sdl2 sdl2_mixer sdl2_image sdl2_ttf
```

**Windows**: 
- Usually works with pip install
- If not, download wheel from: https://www.lfd.uci.edu/~gohlke/pythonlibs/#pygame

---

## 📷 Camera Issues

### Issue 5: "Failed to open camera" or "Camera at index 0 not found"

**Problem**: Camera not accessible or wrong index

**Solutions**:

**Solution 1: Try different camera indices**
```python
# In fall_detection_phase1.py, change line ~40:
CAMERA_INDEX = 1  # Try 1, 2, 3...
```

**Solution 2: Check camera availability**

**Windows**:
```powershell
# List available cameras
Get-PnPDevice -Class Camera
```

**Linux**:
```bash
ls /dev/video*
v4l2-ctl --list-devices
```

**Mac**:
- Go to System Preferences → Security & Privacy → Camera
- Allow Terminal/Python access

**Solution 3: Close other applications**
- Close Zoom, Teams, Skype, etc.
- Only one app can use camera at a time

**Solution 4: Test with simple script**:
```python
import cv2
for i in range(5):
    cap = cv2.VideoCapture(i)
    if cap.isOpened():
        print(f"Camera found at index {i}")
        cap.release()
```

---

### Issue 6: "Camera feed is black" or "Can't read frames"

**Problem**: Camera access issue

**Solutions**:

**Check permissions**:
- **Mac**: System Preferences → Security → Camera → Allow Python
- **Linux**: Add user to video group: `sudo usermod -a -G video $USER`
- **Windows**: Settings → Privacy → Camera → Allow desktop apps

**Test camera independently**:
```bash
# Linux
cheese              # GUI camera viewer
ffplay /dev/video0  # Command line test

# Windows
Camera app (built-in)

# Mac
Photo Booth
```

---

### Issue 7: "Low FPS (<5 frames per second)"

**Problem**: System too slow or resource bottleneck

**Solutions**:

**Solution 1: Reduce resolution**
```python
# In fall_detection_phase1.py:
FRAME_WIDTH = 320   # Instead of 640
FRAME_HEIGHT = 240  # Instead of 480
```

**Solution 2: Use lighter model**
```python
# Line ~147:
self.model = torch.hub.load('ultralytics/yolov5', 'yolov5n', pretrained=True)
# 'yolov5n' is nano version (faster, slightly less accurate)
```

**Solution 3: Close background apps**
- Close browser tabs
- Disable antivirus real-time scanning temporarily
- Stop cloud sync services (OneDrive, Dropbox)

**Solution 4: Check CPU usage**
```bash
# Linux/Mac
top
htop

# Windows
Task Manager → Performance
```

---

## 🤖 YOLOv5 Model Issues

### Issue 8: "YOLOv5 model download failed" or "Connection timeout"

**Problem**: Network issues during first run

**Solutions**:

**Solution 1: Manual download**
```bash
mkdir -p ~/.cache/torch/hub/ultralytics_yolov5_master
cd ~/.cache/torch/hub/ultralytics_yolov5_master
wget https://github.com/ultralytics/yolov5/archive/master.zip
unzip master.zip
```

**Solution 2: Use offline cache**
- Download from: https://github.com/ultralytics/yolov5/releases
- Place in `~/.cache/torch/hub/checkpoints/yolov5s.pt`

**Solution 3: Use local weights**
```python
# Instead of torch.hub.load:
from pathlib import Path
model = torch.hub.load(str(Path.home() / '.cache/torch/hub/ultralytics_yolov5_master'), 
                       'custom', 
                       path='yolov5s.pt', 
                       source='local')
```

---

### Issue 9: "No objects detected" even when object is visible

**Problem**: Low confidence or wrong object class

**Solutions**:

**Solution 1: Lower confidence threshold**
```python
DETECTION_CONFIDENCE = 0.3  # Instead of 0.5
```

**Solution 2: Improve lighting**
- Avoid backlighting (don't point camera at windows)
- Add desk lamp
- Face natural light source

**Solution 3: Check supported objects**
```python
# Print all COCO classes:
print(model.names)
# Output: {0: 'person', 1: 'bicycle', 2: 'car', ..., 41: 'cup', ...}
```

**Solution 4: Object too far or too close**
- Optimal distance: 0.5m - 2m
- Object should fill at least 5% of frame

---

### Issue 10: "Wrong object class detected" (e.g., cup detected as bottle)

**Problem**: Normal behavior - similar objects get confused

**Solutions**:

**This is expected behavior**:
- YOLOv5 is pretrained on general objects
- Cup vs bottle vs vase are similar shapes
- Doesn't affect fall detection (we don't care about exact class)

**If you need better accuracy**:
- Use better lighting
- Increase object size in frame
- Accept some misclassification (normal for COCO dataset)

---

## 🔊 Audio Issues

### Issue 11: "No sound playing" or "Audio alert not working"

**Problem**: Audio system not initialized or muted

**Solutions**:

**Check system volume**:
- Not muted
- Volume > 50%

**Test pygame independently**:
```python
import pygame
pygame.mixer.init()
pygame.mixer.music.load('test.mp3')  # Any MP3 file
pygame.mixer.music.play()
pygame.time.wait(3000)
```

**Linux-specific**:
```bash
# Install ALSA/PulseAudio
sudo apt-get install -y alsa-utils pulseaudio
# Test system audio
speaker-test -t wav -c 2
```

**Windows-specific**:
- Update audio drivers
- Run as Administrator

**Mac-specific**:
- Check Output device in System Preferences → Sound

---

### Issue 12: "Distorted/crackling audio"

**Problem**: Buffer size too small

**Solution**:
```python
# In fall_detection_phase1.py, line ~89:
pygame.mixer.init(frequency=22050, size=-16, channels=1, buffer=2048)
# Increase buffer from 512 to 2048
```

---

## ⚡ Fall Detection Issues

### Issue 13: "False positives - alerts trigger for stationary objects"

**Problem**: Threshold too sensitive or camera shake

**Solutions**:

**Increase velocity threshold**:
```python
FALL_VELOCITY_THRESHOLD = 10.0  # Instead of 5.0
```

**Increase frame confirmation**:
```python
MIN_CONSECUTIVE_FRAMES = 5  # Instead of 3
```

**Stabilize camera**:
- Use laptop stand
- Don't move laptop while testing
- Avoid vibrating surfaces

---

### Issue 14: "Alerts not triggering even when dropping objects"

**Problem**: Threshold too high or object not tracked

**Solutions**:

**Lower threshold**:
```python
FALL_VELOCITY_THRESHOLD = 3.0  # More sensitive
```

**Check if object is being tracked**:
- Green box should appear BEFORE dropping
- If no green box → detection issue (see Issue 9)

**Drop technique**:
- Hold object in frame for 2 seconds first
- Drop straight down (not at angle)
- Drop within 1-2 meters of camera

**Enable debug output**:
```python
# Add after line 232 in fall_detection_phase1.py:
print(f"Velocity: {velocity:.2f}, Threshold: {self.velocity_threshold}")
```

---

### Issue 15: "Alert triggers only sometimes"

**Problem**: Tracking lost between frames

**Solutions**:

**Improve lighting** (most common cause):
- Consistent lighting (no shadows moving)
- Avoid reflective objects

**Increase detection confidence** (paradoxically helps):
```python
DETECTION_CONFIDENCE = 0.6  # Higher = more stable tracking
```

**Reduce frame rate demand**:
- Close other apps
- Use lower resolution

---

## 🖥️ System-Specific Issues

### Issue 16: "ImportError: DLL load failed" (Windows)

**Problem**: Missing Visual C++ redistributables

**Solution**:
- Download: https://aka.ms/vs/17/release/vc_redist.x64.exe
- Install and restart

---

### Issue 17: "Segmentation fault (core dumped)" (Linux)

**Problem**: OpenCV + specific video driver conflict

**Solutions**:

**Try headless version**:
```bash
pip uninstall opencv-python
pip install opencv-python-headless
```

**Update graphics drivers**:
```bash
sudo ubuntu-drivers autoinstall  # Ubuntu
```

**Use different camera backend**:
```python
cap = cv2.VideoCapture(0, cv2.CAP_V4L2)  # Linux
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW) # Windows
```

---

### Issue 18: "Memory error" or "Out of memory"

**Problem**: Insufficient RAM

**Solutions**:

**Close other apps**

**Reduce batch size** (for future model training):
```python
# Not applicable to Phase 1, but good to know
```

**Use swap space** (Linux):
```bash
sudo fallocate -l 4G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

---

## 🧪 Debugging Tips

### Enable Verbose Logging

Add this at the start of `fall_detection_phase1.py`:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Frame-by-Frame Analysis

```python
# Add after line 353 (in run method):
if fps_counter % 30 == 0:  # Every second
    print(f"FPS: {fps_display}, Objects: {len(self.fall_detector.tracked_objects)}")
```

### Save Frames for Analysis

```python
# When fall detected:
if fall_detected:
    cv2.imwrite(f"fall_frame_{time.time()}.jpg", frame)
```

---

## 📞 Still Having Issues?

### Diagnostic Checklist

Run this diagnostic script:

```python
import sys
print(f"Python: {sys.version}")

try:
    import cv2
    print(f"OpenCV: {cv2.__version__}")
except: print("OpenCV: NOT INSTALLED")

try:
    import torch
    print(f"PyTorch: {torch.__version__}")
except: print("PyTorch: NOT INSTALLED")

try:
    import pygame
    print(f"Pygame: {pygame.version.ver}")
except: print("Pygame: NOT INSTALLED")

import platform
print(f"OS: {platform.system()} {platform.release()}")
```

### Create Issue Report

If nothing works, gather this info:
1. Output of diagnostic script above
2. Full error message (screenshot or copy-paste)
3. Operating system and version
4. Python version (`python --version`)
5. Steps to reproduce

---

## 🎯 Quick Fixes Summary

| Problem | Quick Fix |
|---------|-----------|
| Can't find camera | Change `CAMERA_INDEX = 1` |
| Low FPS | Use `yolov5n` model, reduce resolution |
| No sound | Check volume, reinstall pygame |
| False positives | Increase `FALL_VELOCITY_THRESHOLD = 10.0` |
| No detections | Lower `DETECTION_CONFIDENCE = 0.3` |
| Installation errors | Use Python 3.8-3.10 (not 3.11+) |
| Import errors | `pip install --upgrade --force-reinstall [package]` |

---

**Remember**: Most issues are environment-specific. The code itself is tested and works! 🚀
